#!/usr/bin/env python3
"""
豆包播客 TTS API — 完整参考实现

支持两种模式：
  - URL 文章模式：传入网页链接，生成双人播客
  - 短文本模式：传入文本内容（< 200 字），生成短播客

使用前：
  1. pip install websockets
  2. 设置环境变量：DOUBAO_APP_ID, DOUBAO_ACCESS_KEY, DOUBAO_RESOURCE_ID, DOUBAO_APP_KEY
     或者直接修改下方 CONFIG 字典

用法：
  # 单个 URL 生成
  python generate_podcast.py --url "https://mp.weixin.qq.com/s/xxx" --output podcast.mp3

  # 短文本生成
  python generate_podcast.py --text "你好世界，这是一段测试文本" --output test.mp3

  # 批量 URL 生成（从 JSON 文件读取）
  python generate_podcast.py --batch urls.json --output-dir ./podcasts/
"""

import asyncio
import json
import struct
import time
import os
import sys
import argparse

try:
    import websockets
except ImportError:
    print("请先安装 websockets: pip install websockets")
    sys.exit(1)

# ============================================================
#  配置（优先从环境变量读取）
# ============================================================
CONFIG = {
    "app_id": os.environ.get("DOUBAO_APP_ID", ""),
    "access_key": os.environ.get("DOUBAO_ACCESS_KEY", ""),
    "resource_id": os.environ.get("DOUBAO_RESOURCE_ID", "volc.service_type.10050"),
    "app_key": os.environ.get("DOUBAO_APP_KEY", ""),
}

WS_URL = "wss://openspeech.bytedance.com/api/v3/sami/podcasttts"

# 默认发音人（男女双主持）
DEFAULT_SPEAKERS = [
    "zh_male_dayixiansheng_v2_saturn_bigtts",
    "zh_female_mizaitongxue_v2_saturn_bigtts",
]

# 默认音频配置（固定 mp3 96kbps 24kHz mono）
DEFAULT_AUDIO_CFG = {"format": "mp3", "sample_rate": 24000, "speech_rate": 0}

# 超时设置
DEFAULT_TIMEOUT = 900  # 15 分钟，足够覆盖超长文章


# ============================================================
#  二进制协议：帧构造与解析
# ============================================================
HEADER = bytes([0x11, 0x14, 0x10, 0x00])


def pre_frame(event: int, payload: dict) -> bytes:
    """构造 Pre-connection 帧（建连前，无 session_id）"""
    p = json.dumps(payload, ensure_ascii=False).encode()
    return HEADER + struct.pack(">I", event) + struct.pack(">I", len(p)) + p


def post_frame(event: int, sid: str, payload: dict) -> bytes:
    """构造 Post-connection 帧（建连后，含 session_id）"""
    sb = sid.encode()
    p = json.dumps(payload, ensure_ascii=False).encode()
    return (
        HEADER
        + struct.pack(">I", event)
        + struct.pack(">I", len(sb))
        + sb
        + struct.pack(">I", len(p))
        + p
    )


def parse_event(data: bytes) -> tuple:
    """解析服务端返回帧

    Returns:
        (event_type, payload_dict)
        event_type = -1 表示错误帧
        payload 中如有音频: {"audio_data": bytes, "audio_bytes": int}
    """
    if len(data) < 8:
        return None, {}

    mt = (data[1] >> 4) & 0xF  # message_type
    fl = data[1] & 0xF  # flags
    ser = (data[2] >> 4) & 0xF  # serialization

    # 错误帧
    if mt == 0xF:
        js = data.find(b"{")
        return -1, json.loads(data[js:]) if js >= 0 else {"error": "unknown"}

    evt = struct.unpack(">I", data[4:8])[0]
    off = 8
    payload = {}
    audio_data = None

    if fl & 0x04:  # 含 session_id
        if len(data) >= off + 4:
            sid_len = struct.unpack(">I", data[off : off + 4])[0]
            off += 4 + sid_len
        if len(data) >= off + 4:
            p_len = struct.unpack(">I", data[off : off + 4])[0]
            off += 4
            if p_len > 0 and len(data) >= off + p_len:
                pd = data[off : off + p_len]
                if ser == 1:  # JSON
                    try:
                        payload = json.loads(pd)
                    except Exception:
                        pass
                elif ser == 0:  # raw binary = 音频
                    audio_data = pd

    if audio_data is not None:
        return evt, {"audio_data": audio_data, "audio_bytes": len(audio_data)}
    return evt, payload


# ============================================================
#  核心：生成单个播客
# ============================================================
async def generate_podcast(
    url: str = None,
    text: str = None,
    output_path: str = "podcast.mp3",
    speakers: list = None,
    audio_config: dict = None,
    timeout: int = DEFAULT_TIMEOUT,
    use_head_music: bool = True,
    use_tail_music: bool = False,
    on_progress=None,
) -> dict:
    """生成单个播客

    Args:
        url: 文章 URL（与 text 二选一）
        text: 短文本内容（与 url 二选一）
        output_path: 输出 mp3 路径
        speakers: 发音人列表，默认男女双主持
        audio_config: 音频配置，默认 mp3/24kHz/正常语速
        timeout: 超时秒数，默认 900
        use_head_music: 是否加片头音乐
        use_tail_music: 是否加片尾音乐
        on_progress: 回调函数 (event, info) -> None

    Returns:
        {
            "success": bool,
            "output_path": str,
            "audio_url": str,       # CDN URL，24h 有效
            "duration_sec": float,
            "rounds": int,
            "total_tokens": int,
            "elapsed_sec": float,
            "size_bytes": int,
            "error": str or None,
        }
    """
    if not url and not text:
        raise ValueError("必须提供 url 或 text 参数")

    speakers = speakers or DEFAULT_SPEAKERS
    audio_config = audio_config or DEFAULT_AUDIO_CFG

    headers = {
        "X-Api-App-Id": CONFIG["app_id"],
        "X-Api-Access-Key": CONFIG["access_key"],
        "X-Api-Resource-Id": CONFIG["resource_id"],
        "X-Api-App-Key": CONFIG["app_key"],
    }

    t_start = time.time()
    audio_chunks = []
    rounds = 0
    total_tokens = 0
    audio_url = ""
    duration_sec = 0
    error_msg = None

    def progress(event, info):
        if on_progress:
            on_progress(event, info)

    try:
        async with websockets.connect(
            WS_URL,
            additional_headers=headers,
            max_size=50 * 1024 * 1024,
            ping_interval=20,
            ping_timeout=120,  # 长文生成时可能长时间无消息
            close_timeout=30,
        ) as ws:
            # ── Step 1: StartConnection ──
            await ws.send(pre_frame(1, {}))
            data = await asyncio.wait_for(ws.recv(), timeout=15)
            evt, info = parse_event(data)
            if evt == -1:
                return _result(False, error=f"建连失败: {info}", t_start=t_start)

            # 提取 session_id
            off = 8
            sid_len = struct.unpack(">I", data[off : off + 4])[0]
            off += 4
            sid = data[off : off + sid_len].decode()
            progress("connected", {"session_id": sid, "elapsed": time.time() - t_start})

            # ── Step 2: StartSession ──
            if url:
                # ⚠️ URL 放在 input_info 内部
                session_payload = {
                    "input_info": {"input_url": url, "return_audio_url": True},
                    "use_head_music": use_head_music,
                    "use_tail_music": use_tail_music,
                    "audio_config": audio_config,
                    "speaker_info": {"random_order": True, "speakers": speakers},
                }
            else:
                # ⚠️ text 放在顶层
                session_payload = {
                    "input_text": text,
                    "audio_config": audio_config,
                    "speaker_info": {"random_order": True, "speakers": speakers},
                }

            await ws.send(post_frame(100, sid, session_payload))
            data = await asyncio.wait_for(ws.recv(), timeout=30)
            evt, info = parse_event(data)
            if evt == -1:
                return _result(False, error=f"会话启动失败: {info}", t_start=t_start)
            progress("session_started", {"elapsed": time.time() - t_start})

            # ── Step 3: 接收流式数据 ──
            while True:
                remaining = timeout - (time.time() - t_start)
                if remaining <= 0:
                    error_msg = f"超时 {timeout}s"
                    break

                try:
                    data = await asyncio.wait_for(
                        ws.recv(), timeout=min(remaining, 60)
                    )
                    evt, info = parse_event(data)

                    if evt == -1:
                        error_msg = f"API 错误: {info}"
                        break
                    elif evt == 360:  # RoundStart
                        rounds += 1
                        txt = str(info.get("text", ""))[:80]
                        progress("round_start", {"round": rounds, "text": txt})
                    elif evt == 361:  # RoundResp — 音频块
                        ad = info.get("audio_data")
                        if ad:
                            audio_chunks.append(ad)
                        total_bytes = sum(len(c) for c in audio_chunks)
                        progress("audio_chunk", {"total_bytes": total_bytes})
                    elif evt == 154:  # Usage
                        usage = info.get("usage", {})
                        t = usage.get("total_tokens", 0)
                        if t > 0:
                            total_tokens += t
                    elif evt == 363:  # PodcastEnd — 核心！
                        meta = info.get("meta_info", {})
                        audio_url = meta.get("audio_url", "")
                        duration_sec = meta.get("duration_sec", 0)
                        progress(
                            "podcast_end",
                            {
                                "audio_url": audio_url,
                                "duration_sec": duration_sec,
                            },
                        )
                        # ⚠️ 立即 break！不要等 SessionFinished(152)
                        # SessionFinished 经常延迟很久甚至不来
                        break
                    elif evt == 152:  # SessionFinished
                        break

                except asyncio.TimeoutError:
                    # 60s 内无消息，继续等（长文生成时正常）
                    continue

            # ── 关闭连接 ──
            try:
                await ws.send(post_frame(2, sid, {}))
            except Exception:
                pass

    except Exception as e:
        error_msg = f"{type(e).__name__}: {e}"
        # 连接断了但已有音频块 → 照样保存
        if audio_chunks:
            progress("connection_lost_with_data", {"chunks": len(audio_chunks)})

    elapsed = time.time() - t_start

    if not audio_chunks:
        return _result(
            False, error=error_msg or "无音频数据", t_start=t_start
        )

    # ── 保存 MP3 ──
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "wb") as f:
        for chunk in audio_chunks:
            f.write(chunk)

    size_bytes = os.path.getsize(output_path)

    return {
        "success": True,
        "output_path": output_path,
        "audio_url": audio_url,
        "duration_sec": round(duration_sec, 1) if duration_sec else None,
        "rounds": rounds,
        "total_tokens": total_tokens,
        "elapsed_sec": round(elapsed, 1),
        "size_bytes": size_bytes,
        "error": error_msg,
    }


def _result(success, error=None, t_start=0):
    return {
        "success": success,
        "output_path": None,
        "audio_url": "",
        "duration_sec": None,
        "rounds": 0,
        "total_tokens": 0,
        "elapsed_sec": round(time.time() - t_start, 1),
        "size_bytes": 0,
        "error": error,
    }


# ============================================================
#  批量生成
# ============================================================
async def batch_generate(
    items: list,
    output_dir: str = "./podcasts",
    timeout: int = DEFAULT_TIMEOUT,
    delay_between: int = 3,
) -> list:
    """批量生成播客

    Args:
        items: [{"id": "xxx", "url": "https://...", "category": "..."}, ...]
        output_dir: 输出目录
        timeout: 每个的超时
        delay_between: 两个之间的间隔秒数

    Returns:
        结果列表
    """
    os.makedirs(output_dir, exist_ok=True)
    results = []

    for i, item in enumerate(items):
        file_id = item.get("id", f"podcast_{i:03d}")
        url = item.get("url")
        text = item.get("text")
        category = item.get("category", "")

        print(f"\n[{i+1}/{len(items)}] {file_id} ({category})")
        output_path = os.path.join(output_dir, f"{file_id}.mp3")

        def on_progress(event, info):
            if event == "round_start":
                print(f"  Round #{info['round']}: {info['text']}")
            elif event == "audio_chunk":
                mb = info["total_bytes"] / 1024 / 1024
                if mb > 0 and int(mb * 2) > int((mb - 0.5) * 2):
                    print(f"  Audio: {mb:.1f}MB...")
            elif event == "podcast_end":
                print(f"  PodcastEnd! duration={info.get('duration_sec')}s")

        result = await generate_podcast(
            url=url,
            text=text,
            output_path=output_path,
            timeout=timeout,
            on_progress=on_progress,
        )
        result["file_id"] = file_id
        result["category"] = category
        result["source_url"] = url
        results.append(result)

        status = "OK" if result["success"] else f"FAIL: {result['error']}"
        size_mb = result["size_bytes"] / 1024 / 1024 if result["size_bytes"] else 0
        print(f"  → {status} | {size_mb:.1f}MB | {result['elapsed_sec']}s")

        if i < len(items) - 1:
            await asyncio.sleep(delay_between)

    # 保存 manifest
    manifest_path = os.path.join(output_dir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nManifest: {manifest_path}")

    ok = sum(1 for r in results if r["success"])
    print(f"Results: {ok}/{len(items)} succeeded")

    return results


# ============================================================
#  CLI
# ============================================================
def main():
    parser = argparse.ArgumentParser(description="豆包播客 TTS 生成器")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="文章 URL")
    group.add_argument("--text", help="短文本内容")
    group.add_argument("--batch", help="批量 JSON 文件路径")
    parser.add_argument("--output", "-o", default="podcast.mp3", help="输出文件路径")
    parser.add_argument("--output-dir", default="./podcasts", help="批量输出目录")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="超时秒数")
    args = parser.parse_args()

    # 检查凭证
    if not CONFIG["app_id"] or not CONFIG["access_key"]:
        print("错误：请设置环境变量 DOUBAO_APP_ID, DOUBAO_ACCESS_KEY, DOUBAO_RESOURCE_ID, DOUBAO_APP_KEY")
        print("或者直接修改脚本中的 CONFIG 字典")
        sys.exit(1)

    if args.batch:
        with open(args.batch, "r", encoding="utf-8") as f:
            items = json.load(f)
        asyncio.run(batch_generate(items, args.output_dir, args.timeout))
    else:
        def on_progress(event, info):
            if event == "round_start":
                print(f"  Round #{info['round']}: {info['text']}")
            elif event == "podcast_end":
                print(f"  Done! duration={info.get('duration_sec')}s")

        result = asyncio.run(
            generate_podcast(
                url=args.url,
                text=args.text,
                output_path=args.output,
                timeout=args.timeout,
                on_progress=on_progress,
            )
        )

        if result["success"]:
            size_mb = result["size_bytes"] / 1024 / 1024
            print(f"\nSaved: {result['output_path']} ({size_mb:.1f}MB)")
            if result["audio_url"]:
                print(f"CDN URL (24h): {result['audio_url'][:100]}...")
        else:
            print(f"\nFailed: {result['error']}")
            sys.exit(1)


if __name__ == "__main__":
    main()
