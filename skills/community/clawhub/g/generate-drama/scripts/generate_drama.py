#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
短剧生成 Skill 脚本
输入剧本 JSON → SenseAudio TTS 逐段合成 → 拼接完整音频

剧本由 Claude 生成，本脚本只负责 TTS 合成和音频拼接。
"""

import os
import re
import io
import json
import struct
import argparse
import requests
import time as time_module


# ============== API 配置 ==============
SENSEAUDIO_API_KEY = os.environ.get("SENSEAUDIO_API_KEY", "")
SENSEAUDIO_API_URL = "https://api.senseaudio.cn/v1/t2a_v2"

# 可用音色列表（voice_id → 描述）
VOICE_CATALOG = {
    "child_0001_a": "可爱萌娃(开心)，适合小孩、活泼少女、可爱类角色",
    "child_0001_b": "可爱萌娃(平稳)，适合小孩、安静少女、乖巧类角色",
    "male_0004_a": "儒雅道长(平稳)，适合学者、道长、智者、长辈、沉稳男性角色",
    "male_0018_a": "沙哑青年(深情)，适合江湖浪子、叛逆少年、男主类角色",
}


def tts_synthesize(text: str, voice_id: str, api_key: str) -> bytes:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "senseaudio-tts-1.5-260319",
        "text": text,
        "stream": False,
        "voice_setting": {
            "voice_id": voice_id,
            "speed": 1.0,
            "vol": 1.0,
            "pitch": 0,
        },
        "audio_setting": {
            "format": "wav",
            "sample_rate": 24000,
            "channel": 1,
        },
    }
    for retry in range(3):
        try:
            resp = requests.post(SENSEAUDIO_API_URL, json=payload, headers=headers, timeout=60)
            result = resp.json()
            if result.get("data") and result["data"].get("audio"):
                return bytes.fromhex(result["data"]["audio"])
            else:
                raise Exception(f"API Error: {result.get('base_resp', result)}")
        except Exception as e:
            print(f"  TTS 重试 {retry+1}/3: {e}")
            time_module.sleep(3 * (retry + 1))
    raise RuntimeError(f"TTS 合成失败: {text[:30]}...")


def read_wav_pcm(wav_bytes: bytes):
    if wav_bytes[:4] != b'RIFF':
        raise ValueError("不是有效的 WAV 文件")
    pos = 12
    sample_rate, channels, bits_per_sample = 24000, 1, 16
    pcm_data = b''
    while pos < len(wav_bytes) - 8:
        chunk_id = wav_bytes[pos:pos+4]
        chunk_size = struct.unpack('<I', wav_bytes[pos+4:pos+8])[0]
        if chunk_id == b'fmt ':
            fmt = struct.unpack('<HHIIHH', wav_bytes[pos+8:pos+24])
            channels = fmt[1]
            sample_rate = fmt[2]
            bits_per_sample = fmt[5]
        elif chunk_id == b'data':
            pcm_data = wav_bytes[pos+8:pos+8+chunk_size]
            break
        pos += 8 + chunk_size
        if chunk_size % 2 == 1:
            pos += 1
    return pcm_data, sample_rate, channels, bits_per_sample


def make_silence(duration_sec, sample_rate=24000, channels=1, bits_per_sample=16):
    num_samples = int(duration_sec * sample_rate)
    return b'\x00' * (num_samples * channels * (bits_per_sample // 8))


def concat_wavs(wav_bytes_list, gap_sec=0.3):
    all_pcm = b''
    sample_rate = channels = bits_per_sample = None
    for i, wav_bytes in enumerate(wav_bytes_list):
        pcm, sr, ch, bps = read_wav_pcm(wav_bytes)
        if sample_rate is None:
            sample_rate, channels, bits_per_sample = sr, ch, bps
        if i > 0:
            all_pcm += make_silence(gap_sec, sample_rate, channels, bits_per_sample)
        all_pcm += pcm

    buf = io.BytesIO()
    byte_rate = sample_rate * channels * bits_per_sample // 8
    block_align = channels * bits_per_sample // 8
    data_size = len(all_pcm)
    buf.write(b'RIFF')
    buf.write(struct.pack('<I', 36 + data_size))
    buf.write(b'WAVE')
    buf.write(b'fmt ')
    buf.write(struct.pack('<I', 16))
    buf.write(struct.pack('<HHIIHH', 1, channels, sample_rate,
                          byte_rate, block_align, bits_per_sample))
    buf.write(b'data')
    buf.write(struct.pack('<I', data_size))
    buf.write(all_pcm)
    return buf.getvalue()


def synthesize_drama(script_json: str, output_path: str, api_key: str, gap_sec: float = 0.3):
    """
    根据剧本 JSON 合成有声短剧。

    script_json 格式：
    {
      "topic": "主题",
      "roles": {"角色名": "voice_id", ...},
      "segments": [{"sid": "角色名", "text": "台词"}, ...]
    }
    """
    script = json.loads(script_json)
    topic = script.get("topic", "未命名短剧")
    voice_map = script.get("roles", {})
    segments = script.get("segments", [])

    if not segments:
        print("错误: 剧本中没有对白")
        return

    # 校验 voice_id
    all_ids = list(VOICE_CATALOG.keys())
    for role, vid in voice_map.items():
        if vid not in VOICE_CATALOG:
            print(f"  警告: 音色 {vid} 不在可用列表中，回退到 {all_ids[0]}")
            voice_map[role] = all_ids[0]

    # 未分配音色的角色兜底
    used = set(voice_map.values())
    remaining = [v for v in all_ids if v not in used]
    for seg in segments:
        if seg["sid"] not in voice_map:
            voice_map[seg["sid"]] = remaining.pop(0) if remaining else all_ids[0]

    print(f"短剧主题: {topic}")
    print(f"角色音色分配:")
    for role, vid in voice_map.items():
        desc = VOICE_CATALOG.get(vid, "")
        print(f"  {role} -> {vid} ({desc})")

    # TTS 合成
    print(f"\n[1/2] TTS 合成 ({len(segments)}句)...")
    wav_list = []
    for i, seg in enumerate(segments):
        print(f"  ({i+1}/{len(segments)}) [{seg['sid']}] {seg['text'][:40]}...")
        wav_bytes = tts_synthesize(seg["text"], voice_map[seg["sid"]], api_key)
        wav_list.append(wav_bytes)

    # 拼接
    print(f"\n[2/2] 拼接音频...")
    final_wav = concat_wavs(wav_list, gap_sec=gap_sec)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)) or ".", exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(final_wav)

    # 保存剧本 JSON
    script_path = output_path.rsplit('.', 1)[0] + "_script.json"
    with open(script_path, 'w', encoding='utf-8') as f:
        json.dump(script, f, ensure_ascii=False, indent=2)

    print(f"\n完成!")
    print(f"音频: {output_path}")
    print(f"剧本: {script_path}")


def main():
    parser = argparse.ArgumentParser(description="短剧 TTS 合成（接收 Claude 生成的剧本 JSON）")
    parser.add_argument("script_json", type=str,
                        help="剧本 JSON 字符串，或 JSON 文件路径（以 @ 开头）")
    parser.add_argument("--output", type=str, default=None, help="输出 wav 路径")
    parser.add_argument("--gap", type=float, default=0.3, help="对白间隔秒数")
    parser.add_argument("--senseaudio-api-key", type=str, default=None,
                        help="SenseAudio API 密钥")
    args = parser.parse_args()

    api_key = args.senseaudio_api_key or SENSEAUDIO_API_KEY
    if not api_key:
        api_key = input("未检测到 SENSEAUDIO_API_KEY，请输入 SenseAudio API 密钥（https://senseaudio.cn 注册获取）: ").strip()
        if not api_key:
            print("错误: 未提供 API 密钥，无法继续。")
            return

    # 支持传 JSON 字符串或 @文件路径
    script_input = args.script_json
    if script_input.startswith("@"):
        file_path = script_input[1:]
        with open(file_path, "r", encoding="utf-8") as f:
            script_input = f.read()

    # 确定输出路径
    output_path = args.output
    if output_path is None:
        try:
            topic = json.loads(script_input).get("topic", "drama")
            safe_name = re.sub(r'[^\w\u4e00-\u9fff]', '_', topic)[:30]
        except Exception:
            safe_name = "drama"
        default_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs")
        user_dir = input(f"请输入输出目录（直接回车使用默认 {default_dir}）: ").strip()
        out_dir = user_dir if user_dir else default_dir
        os.makedirs(out_dir, exist_ok=True)
        output_path = os.path.join(out_dir, f"{safe_name}.wav")

    synthesize_drama(script_input, output_path, api_key, gap_sec=args.gap)


if __name__ == "__main__":
    main()
