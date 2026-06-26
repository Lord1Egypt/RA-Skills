#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书语音合成脚本（MiniMax T2A + Edge TTS 双引擎，自动降级）

链路：
  MiniMax TTS (mp3) + ffmpeg 转 opus  【ffmpeg 不可用则跳过】
    └─ 失败 → Edge TTS (ogg 直出)
              └─ 失败 → (None, error)

超时：每步 10 秒
环境变量:
  MINIMAX_API_KEY  - MiniMax API Key（无则跳到 Edge TTS）
  EDGE_TTS_VOICE   - Edge TTS 音色，默认 zh-CN-XiaoxiaoNeural
"""
from __future__ import print_function
import os, sys, time, tempfile, subprocess, shutil, re

# ── Windows stdout fix ──────────────────────────────────────────────────────
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach(), errors="replace")

import requests
import asyncio
import edge_tts

AUDIO_OUT = os.path.join(tempfile.gettempdir(), "feishu-voice-out")
os.makedirs(AUDIO_OUT, exist_ok=True)

FFMPEG_AVAILABLE = None

def ffmpeg_available():
    global FFMPEG_AVAILABLE
    if FFMPEG_AVAILABLE is None:
        try:
            r = subprocess.run(["ffmpeg", "-version"],
                               capture_output=True, timeout=5)
            FFMPEG_AVAILABLE = (r.returncode == 0)
        except Exception:
            FFMPEG_AVAILABLE = False
    return FFMPEG_AVAILABLE


# ── MiniMax 拟人化文本预处理 ───────────────────────────────────────────────
BREATH = "(breath)"
SIGHS  = "(sighs)"
EMM    = "(emm)"
CLEAR  = "(clear-throat)"
CHUCKLE = "(chuckle)"
SNIFFS = "(sniffs)"
HUMMING = "(humming)"
LAUGHS  = "(laughs)"

def humanize(text: str) -> str:
    """
    在 MiniMax 可发音文本中插入语气词和停顿，让语音更拟人。
    
    规则：
    - 逗号后加短暂停顿 <#0.3#>
    - 句号前/后插入自然呼吸 (breath)
    - 问句结尾插 (emm) 表示思考
    - 感叹句插 (laughs) 或 (sighs)
    - 连续叙述每 30 字符插一次 (breath)
    - 语气词 "啊" 后插 (breath)
    - 省略号 "..." 后插 (emm)
    - 不破坏已有标签结构（不重复插入）
    """
    MAX_CHUNK = 28  # 插入 (breath) 的最大字符间距

    # 已有语气词标签则跳过，防止重复注入
    if any(tag in text for tag in [BREATH, SIGHS, EMM, CLEAR, CHUCKLE, SNIFFS, HUMMING, LAUGHS]):
        return _humanize_plain(text)

    return _humanize_plain(text)

def _humanize_plain(text: str) -> str:
    """
    在纯文本中插入停顿和语气词（中英文标点均支持）。
    规则：
      - 省略号 ... → ...(emm)
      - 感叹号 ！/! → (laughs)
      - 问号 ？/? → (emm)
      - "啊"后 → (breath)
      - 句末标点后 → <#0.4#> 停顿
      - 长段落每隔28字符均分 (breath)
    """
    MAX_CHUNK = 28

    # 省略号 → (emm)
    text = re.sub(r'\.{3}(?=[^<(]|$)', '...(emm)', text)
    text = re.sub(r'\u2026(?=[^<(])', '\u2026(emm)', text)

    # 感叹号（中英文）→ (laughs)
    text = re.sub(r'([!\uff01])+(?=[^<(]|$)', r'\1(laughs)', text)

    # 问号（中英文）→ (emm)
    text = re.sub(r'([?\uff1f])+(?=[^<(]|$)', r'\1(emm)', text)

    # "啊"后 → (breath)
    text = re.sub(r'\u554a(?=[^<(]|$)', '\u554a(breath)', text)

    # 句末标点后 → 0.4秒停顿
    text = re.sub(r'([\u3002\uff01\uff1f.!?])(?=[^<(\s])', r'\1<#0.4#>', text)

    # 长段落均分 (breath)
    safe_punct = re.compile(r'[\u3002\uff01\uff1f\uff0c\u3001,._!?;；:\s]')
    result = []
    chars = list(text)
    last_safe = -1
    last_insert = -1
    for i, ch in enumerate(chars):
        result.append(ch)
        if safe_punct.match(ch):
            last_safe = i
        if i - last_safe > MAX_CHUNK and last_safe > last_insert:
            result.insert(last_safe + 1, '(breath)')
            last_insert = last_safe + 1
            last_safe = -1

    return "".join(result)

def minimax_synth(text, voice_id="badao_shaoye"):
    """
    MiniMax T2A → mp3 → ffmpeg 转 opus
    text 会经过 humanize() 预处理，插入语气词和停顿。
    返回: (file_path, method)
    """
    key = os.environ.get("MINIMAX_API_KEY", "").strip()
    if not key:
        return None, None

    # 拟人化预处理（仅 MiniMax 用）
    processed = humanize(text)

    headers = {"Authorization": "Bearer " + key, "Content-Type": "application/json"}
    payload = {
        "model": "speech-2.8-hd",
        "text": processed,
        "stream": False,
        "voice_setting": {"voice_id": voice_id, "speed": 1, "vol": 1, "pitch": 0, "emotion": "happy"},
        "audio_setting": {"sample_rate": 32000, "bitrate": 128000, "format": "mp3", "channel": 1}
    }

    try:
        r = requests.post(
            "https://api.minimaxi.com/v1/t2a_v2",
            headers=headers, json=payload, timeout=10
        )
    except requests.exceptions.Timeout:
        return None, "timeout"
    except Exception as e:
        return None, f"request_error:{e}"

    if r.status_code >= 400:
        return None, f"http_{r.status_code}"

    data = r.json()
    if data.get("base_resp", {}).get("status_code", 0) != 0:
        return None, "api_error"

    audio_hex = data["data"]["audio"]
    mp3_path = os.path.join(AUDIO_OUT, "minimax.mp3")
    with open(mp3_path, "wb") as f:
        f.write(bytes.fromhex(audio_hex))

    if ffmpeg_available():
        opus_path = os.path.join(AUDIO_OUT, "minimax.opus")
        try:
            r2 = subprocess.run(
                ["ffmpeg", "-y", "-i", mp3_path,
                 "-c:a", "libopus", "-ac", "1", "-ar", "16000", opus_path],
                capture_output=True, timeout=10
            )
            os.remove(mp3_path)
            if r2.returncode == 0:
                return opus_path, "minimax_opus"
        except Exception:
            pass

    return mp3_path, "minimax_mp3"


# ── Edge TTS ────────────────────────────────────────────────────────────────
async def _edge_synth(text, output_path, voice):
    await edge_tts.Communicate(text, voice).save(output_path)

def edge_synth(text, voice=None):
    """Edge TTS 合成 ogg/opus，直接输出，无需 ffmpeg。"""
    voice = voice or os.environ.get("EDGE_TTS_VOICE", "zh-CN-XiaoxiaoNeural")
    out_path = os.path.join(AUDIO_OUT, "edge.ogg")

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(asyncio.wait_for(
            _edge_synth(text, out_path, voice), timeout=10
        ))
    except asyncio.TimeoutError:
        return None, "timeout"
    except Exception as e:
        return None, f"error:{e}"

    return out_path, "edge_tts"


# ── 主入口 ─────────────────────────────────────────────────────────────────
def send_voice(text, voice_id=None):
    """
    完整合成流程：
    1. MiniMax (humanize 预处理) + ffmpeg opus（10 秒）
    2. Edge TTS（10 秒）
    3. 全失败 → (None, "all_failed")

    返回: (opus_or_ogg_path, method_string)
    """
    voice_id = voice_id or "badao_shaoye"
    start = time.time()

    path, reason = minimax_synth(text, voice_id)
    if path and time.time() - start < 10:
        return path, reason

    path, reason = edge_synth(text)
    if path and time.time() - start < 10:
        return path, reason

    return None, "all_failed"


if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else "你好，今天天气真不错，我们出去走走吧！"
    voice = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"[raw  ] {text}")
    print(f"[proc ] {humanize(text)}")

    start = time.time()
    path, reason = send_voice(text, voice)
    elapsed = time.time() - start

    if path:
        print(f"[OK:{reason}] {path} ({elapsed:.1f}s)")
        media_dir = r"e:\Profile\Mac\.openclaw\media\out"
        os.makedirs(media_dir, exist_ok=True)
        dest = os.path.join(media_dir, "send_voice.opus")
        shutil.copy(path, dest)
        print(f"[copy] {dest}")
    else:
        print(f"[FAIL:{reason}] ({elapsed:.1f}s)")
        sys.exit(1)
