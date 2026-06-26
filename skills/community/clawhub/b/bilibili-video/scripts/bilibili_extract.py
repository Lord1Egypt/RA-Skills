#!/usr/bin/env python3
"""
B站视频字幕与音频提取工具
三级降级：CC字幕 → AI字幕 → 音频下载+ASR转写
基于 bilibili-api-python，自带 WBI 签名反爬
"""

import asyncio
import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

# bilibili-api-python
from bilibili_api import video, Credential, HEADERS
from bilibili_api import cheese as cheese_module

# 常量
OUTPUT_DIR = Path("/tmp/openclaw/bilibili")
COOKIE_PATH = Path.home() / ".openclaw/workspace/.bilibili_cookies.json"
ASR_SCRIPT = Path.home() / ".openclaw/workspace/scripts/speech-to-text.sh"
MAX_RETRIES = 2
RETRY_DELAY = 3

# AI 字幕语言代码（优先级排序）
AI_SUBTITLE_LANGS = ["ai-zh", "ai-en", "ai-ja", "ai-ko", "ai-es", "ai-fr", "ai-de", "ai-pt", "ai-ar"]


def parse_input(raw: str) -> dict:
    """解析用户输入，返回 {type: 'bv'|'ep'|'ss', id: str}"""
    raw = raw.strip()

    # BV号
    m = re.search(r'(BV[\w]+)', raw, re.IGNORECASE)
    if m:
        return {"type": "bv", "id": m.group(1)}

    # EP号
    m = re.search(r'ep(\d+)', raw, re.IGNORECASE)
    if m:
        return {"type": "ep", "id": int(m.group(1))}

    # SS号
    m = re.search(r'ss(\d+)', raw, re.IGNORECASE)
    if m:
        return {"type": "ss", "id": int(m.group(1))}

    # AV号
    m = re.search(r'av(\d+)', raw, re.IGNORECASE)
    if m:
        return {"type": "av", "id": int(m.group(1))}

    raise ValueError(f"无法解析输入: {raw}\n支持格式: BV号、AV号、EP号、SS号、完整URL")


def load_credential() -> Credential:
    """从文件加载 cookie"""
    if not COOKIE_PATH.exists():
        print("[INFO] 未找到 cookie 文件，以游客身份运行（部分功能受限）")
        return Credential()

    try:
        data = json.loads(COOKIE_PATH.read_text())
        cred = Credential(
            sessdata=data.get("sessdata", ""),
            bili_jct=data.get("bili_jct", ""),
            buvid3=data.get("buvid3", ""),
            dedeuserid=data.get("dedeuserid", ""),
            ac_time_value=data.get("ac_time_value", ""),
        )
        print("[INFO] 已加载 cookie")
        return cred
    except Exception as e:
        print(f"[WARN] cookie 加载失败: {e}，以游客身份运行")
        return Credential()


async def auto_refresh_credential(cred: Credential) -> Credential:
    """检查并自动刷新 cookie，刷新后回写文件"""
    if not cred.has_sessdata():
        return cred

    try:
        # check_refresh 可能是同步或异步，兼容处理
        result = cred.check_refresh()
        if asyncio.iscoroutine(result):
            need_refresh = await result
        else:
            need_refresh = result
        if need_refresh:
            print("[INFO] Cookie 即将过期，自动刷新中...")
            await cred.refresh()
            # 回写文件
            data = {
                "sessdata": cred.sessdata or "",
                "bili_jct": cred.bili_jct or "",
                "buvid3": cred.buvid3 or "",
                "dedeuserid": cred.dedeuserid or "",
                "ac_time_value": cred.ac_time_value or "",
            }
            COOKIE_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False))
            COOKIE_PATH.chmod(0o600)
            print("[OK] Cookie 已自动刷新并保存")
    except Exception as e:
        print(f"[WARN] Cookie 自动刷新失败: {e}（继续使用现有 cookie）")

    return cred


def try_t2s(text: str) -> str:
    """尝试繁体转简体，opencc 没装就原样返回"""
    try:
        from opencc import OpenCC
        cc = OpenCC('t2s')
        return cc.convert(text)
    except ImportError:
        return text


def format_duration(seconds: int) -> str:
    """秒数转 HH:MM:SS 或 MM:SS"""
    h, remainder = divmod(seconds, 3600)
    m, s = divmod(remainder, 60)
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m}:{s:02d}"


async def retry_async(func, *args, retries=MAX_RETRIES, **kwargs):
    """带重试的异步调用"""
    last_err = None
    for i in range(retries + 1):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            last_err = e
            err_str = str(e)
            if "412" in err_str:
                print(f"[ERROR] 412 风控拦截！请运行 bilibili_login.py 登录获取 cookie")
                raise
            if i < retries:
                print(f"[WARN] 第 {i+1} 次失败: {e}，{RETRY_DELAY}秒后重试...")
                await asyncio.sleep(RETRY_DELAY)
    raise last_err


async def get_video_info(v: video.Video) -> dict:
    """获取视频基本信息"""
    info = await retry_async(v.get_info)
    return {
        "title": info.get("title", "未知"),
        "owner": info.get("owner", {}).get("name", "未知"),
        "duration": info.get("duration", 0),
        "pubdate": datetime.fromtimestamp(info.get("pubdate", 0)).strftime("%Y-%m-%d"),
        "desc": info.get("desc", ""),
        "bvid": info.get("bvid", ""),
        "aid": info.get("aid", 0),
        "pages": info.get("pages", []),
    }


async def try_cc_subtitles(v: video.Video) -> tuple:
    """尝试获取 CC 字幕，返回 (text, source) 或 (None, None)"""
    print("[INFO] 尝试获取 CC 字幕...")
    try:
        cid = await retry_async(v.get_cid, 0)
        subtitle_info = await retry_async(v.get_subtitle, cid)
        subtitles = subtitle_info.get("subtitles", [])
        if not subtitles:
            print("[INFO] 无 CC 字幕")
            return None, None

        # 优先中文
        target = None
        for sub in subtitles:
            lan = sub.get("lan", "")
            if lan.startswith("zh") and "ai-" not in lan:
                target = sub
                break
        if not target:
            # 取第一个非AI字幕
            for sub in subtitles:
                if "ai-" not in sub.get("lan", ""):
                    target = sub
                    break
        if not target:
            print("[INFO] 无 CC 字幕（仅有 AI 字幕）")
            return None, None

        # 下载字幕内容
        url = target.get("subtitle_url", "")
        if url.startswith("//"):
            url = "https:" + url

        import aiohttp
        async with aiohttp.ClientSession(headers=HEADERS) as session:
            async with session.get(url) as resp:
                data = await resp.json()

        lines = []
        for item in data.get("body", []):
            content = item.get("content", "").strip()
            if content:
                lines.append(content)

        text = "\n".join(lines)
        text = try_t2s(text)
        source = f"CC字幕({target.get('lan', 'unknown')})"
        print(f"[OK] 获取到 {source}，共 {len(lines)} 行")
        return text, source

    except Exception as e:
        print(f"[WARN] CC 字幕获取失败: {e}")
        return None, None


async def try_ai_subtitles(v: video.Video) -> tuple:
    """尝试获取 AI 生成字幕，返回 (text, source) 或 (None, None)"""
    print("[INFO] 尝试获取 AI 字幕...")
    try:
        cid = await retry_async(v.get_cid, 0)
        subtitle_info = await retry_async(v.get_subtitle, cid)
        subtitles = subtitle_info.get("subtitles", [])

        target = None
        for lang in AI_SUBTITLE_LANGS:
            for sub in subtitles:
                if sub.get("lan", "") == lang:
                    target = sub
                    break
            if target:
                break

        if not target:
            print("[INFO] 无 AI 字幕")
            return None, None

        url = target.get("subtitle_url", "")
        if url.startswith("//"):
            url = "https:" + url

        import aiohttp
        async with aiohttp.ClientSession(headers=HEADERS) as session:
            async with session.get(url) as resp:
                data = await resp.json()

        lines = []
        for item in data.get("body", []):
            content = item.get("content", "").strip()
            if content:
                lines.append(content)

        text = "\n".join(lines)
        text = try_t2s(text)
        source = f"AI字幕({target.get('lan', 'unknown')})"
        print(f"[OK] 获取到 {source}，共 {len(lines)} 行")
        return text, source

    except Exception as e:
        print(f"[WARN] AI 字幕获取失败: {e}")
        return None, None


async def try_audio_transcribe(v: video.Video, info: dict) -> tuple:
    """下载音频并用 ASR 转写，返回 (text, source) 或 (None, None)"""
    print("[INFO] 字幕均不可用，尝试下载音频进行转写...")

    if not ASR_SCRIPT.exists():
        print(f"[ERROR] ASR 脚本不存在: {ASR_SCRIPT}")
        return None, None

    bvid = info.get("bvid", "unknown")
    audio_path = OUTPUT_DIR / f"{bvid}_audio.m4a"

    try:
        # 获取下载链接
        download_url = await retry_async(v.get_download_url, 0)
        dash = download_url.get("dash", {})
        audios = dash.get("audio", [])
        if not audios:
            print("[WARN] 无可用音频流")
            return None, None

        # 选最高质量音频
        audios.sort(key=lambda x: x.get("bandwidth", 0), reverse=True)
        audio_url = audios[0]["baseUrl"]

        # 下载音频
        print(f"[INFO] 下载音频... ({audios[0].get('bandwidth', 0) // 1000}kbps)")
        import aiohttp
        headers = {**HEADERS, "Referer": "https://www.bilibili.com"}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(audio_url) as resp:
                if resp.status != 200:
                    print(f"[WARN] 音频下载失败: HTTP {resp.status}")
                    return None, None
                audio_data = await resp.read()

        audio_path.write_bytes(audio_data)
        print(f"[OK] 音频已保存: {audio_path} ({len(audio_data) // 1024}KB)")

        # 转换为 wav（ASR 脚本可能需要）
        wav_path = OUTPUT_DIR / f"{bvid}_audio.wav"
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(audio_path), "-ar", "16000", "-ac", "1", str(wav_path)],
            capture_output=True, timeout=120
        )

        # 调用 ASR
        print("[INFO] 调用 ASR 转写...")
        result = subprocess.run(
            ["bash", str(ASR_SCRIPT), str(wav_path)],
            capture_output=True, text=True, timeout=300
        )

        if result.returncode != 0:
            print(f"[WARN] ASR 转写失败: {result.stderr[:200]}")
            # 保留音频文件，用户可以手动处理
            print(f"[INFO] 音频文件保留在: {audio_path}")
            return None, None

        text = result.stdout.strip()
        if not text:
            print("[WARN] ASR 转写结果为空")
            return None, None

        print(f"[OK] 转写完成，共 {len(text)} 字")

        # 清理临时文件
        wav_path.unlink(missing_ok=True)

        return text, "音频转写(ASR)"

    except Exception as e:
        print(f"[WARN] 音频转写失败: {e}")
        return None, None


async def download_audio_only(v: video.Video, info: dict) -> str:
    """仅下载音频，返回文件路径"""
    bvid = info.get("bvid", "unknown")
    audio_path = OUTPUT_DIR / f"{bvid}_audio.m4a"

    download_url = await retry_async(v.get_download_url, 0)
    dash = download_url.get("dash", {})
    audios = dash.get("audio", [])
    if not audios:
        raise RuntimeError("无可用音频流")

    audios.sort(key=lambda x: x.get("bandwidth", 0), reverse=True)
    audio_url = audios[0]["baseUrl"]

    import aiohttp
    headers = {**HEADERS, "Referer": "https://www.bilibili.com"}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(audio_url) as resp:
            audio_data = await resp.read()

    audio_path.write_bytes(audio_data)
    return str(audio_path)


def save_output(info: dict, text: str, source: str) -> str:
    """保存输出文件，返回文件路径"""
    bvid = info.get("bvid", "unknown")
    output_path = OUTPUT_DIR / f"{bvid}_transcript.txt"

    content = f"""# 视频信息
标题: {info['title']}
UP主: {info['owner']}
时长: {format_duration(info['duration'])}
发布日期: {info['pubdate']}
来源: {source}

---

{text}
"""
    output_path.write_text(content, encoding="utf-8")
    return str(output_path)


async def main():
    parser = argparse.ArgumentParser(description="B站视频字幕与音频提取工具")
    parser.add_argument("input", help="BV号、AV号、EP号、SS号或完整URL")
    parser.add_argument("--audio-only", action="store_true", help="仅下载音频，不转写")
    parser.add_argument("--info", action="store_true", help="仅显示视频信息")
    parser.add_argument("--no-asr", action="store_true", help="禁用ASR兜底，字幕不可用时仅下载音频")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 解析输入
    parsed = parse_input(args.input)
    cred = load_credential()
    cred = await auto_refresh_credential(cred)

    # 目前主要支持 BV/AV 号
    if parsed["type"] == "ss":
        print(f"[INFO] SS 号暂不直接支持，请提供具体的 EP 号")
        sys.exit(1)

    if parsed["type"] == "ep":
        print(f"[INFO] EP 号支持有限，尝试获取信息...")
        # EP 号需要通过 cheese 或 bangumi 接口，简化处理
        print("[WARN] EP 号建议先在 B 站页面找到对应的 BV 号后使用")
        sys.exit(1)

    # 创建 Video 对象
    if parsed["type"] == "bv":
        v = video.Video(bvid=parsed["id"], credential=cred)
    elif parsed["type"] == "av":
        v = video.Video(aid=parsed["id"], credential=cred)
    else:
        print(f"[ERROR] 不支持的类型: {parsed['type']}")
        sys.exit(1)

    # 获取视频信息
    print(f"[INFO] 获取视频信息...")
    try:
        info = await get_video_info(v)
    except Exception as e:
        print(f"[ERROR] 获取视频信息失败: {e}")
        sys.exit(1)

    print(f"  标题: {info['title']}")
    print(f"  UP主: {info['owner']}")
    print(f"  时长: {format_duration(info['duration'])}")
    print(f"  发布: {info['pubdate']}")

    if args.info:
        print(f"  BV号: {info['bvid']}")
        print(f"  AV号: {info['aid']}")
        print(f"  简介: {info['desc'][:100]}...")
        print(f"  分P数: {len(info['pages'])}")
        return

    if args.audio_only:
        print("[INFO] 仅下载音频模式")
        path = await download_audio_only(v, info)
        print(f"[OK] 音频已保存: {path}")
        return

    # 三级降级提取字幕
    text, source = await try_cc_subtitles(v)

    if text is None:
        text, source = await try_ai_subtitles(v)

    if text is None:
        if args.no_asr:
            print("[INFO] 字幕不可用，--no-asr 模式，下载音频...")
            path = await download_audio_only(v, info)
            print(f"[OK] 音频已保存: {path}")
            print("[INFO] 可手动使用 speech-to-text.sh 转写")
            return
        text, source = await try_audio_transcribe(v, info)

    if text is None:
        print("[ERROR] 三种方式均失败，无法提取内容")
        sys.exit(1)

    # 保存结果
    output_path = save_output(info, text, source)
    print(f"\n[OK] 提取完成！")
    print(f"  来源: {source}")
    print(f"  文件: {output_path}")
    print(f"  字数: {len(text)}")


if __name__ == "__main__":
    asyncio.run(main())
