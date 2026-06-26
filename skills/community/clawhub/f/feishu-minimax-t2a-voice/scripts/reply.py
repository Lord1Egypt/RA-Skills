#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书语音回复脚本（供 OpenClaw TTS 回调使用）
用法: python reply.py "文字内容" [voice_id]

优先级: MiniMax opus → MiniMax mp3+ffmpeg → Edge TTS
全部超时/失败 → 输出纯文字说明，不发送语音
"""
from __future__ import print_function
import os, sys, time, shutil

if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach(), errors="replace")

# 复用 send_voice.py 的逻辑
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from send_voice import send_voice

MEDIA_OUT = r"e:\Profile\Mac\.openclaw\media\out"
os.makedirs(MEDIA_OUT, exist_ok=True)

if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else "听到了，我在。"
    voice = sys.argv[2] if len(sys.argv) > 2 else None

    start = time.time()
    path, reason = send_voice(text, voice)
    elapsed = time.time() - start

    if path:
        dest = os.path.join(MEDIA_OUT, "reply.opus")
        shutil.copy(path, dest)
        print(dest)          # 输出文件路径，供 OpenClaw message 工具引用
    else:
        # 语音合成彻底失败，输出降级说明
        print(f"[语音合成失败:{reason}，耗时{elapsed:.1f}秒] {text}")
