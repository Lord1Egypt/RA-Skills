#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import random
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUTBOUND = Path.home() / '.openclaw' / 'media' / 'outbound' / 'continuance'

ZH_VOICES = [
    'zh-TW-HsiaoChenNeural',
    'zh-TW-HsiaoYuNeural',
    'zh-CN-XiaoxiaoNeural',
    'zh-CN-XiaochenNeural',
]
EN_VOICES = [
    'en-GB-SoniaNeural',
    'en-US-JennyNeural',
    'en-US-AriaNeural',
]


def detect_language(text: str) -> str:
    if any('\u4e00' <= ch <= '\u9fff' for ch in text):
        return 'zh'
    return 'en'


def build_bg_prompt(theme: str, seed: int) -> str:
    prompts = {
        'rest': 'soft ambient meditation music, warm pads, slow breathing tempo, gentle bells, calming atmosphere, no vocals',
        'alignment': 'serene ambient meditation soundscape, soft drones, subtle chimes, spacious calming mood, no vocals',
        'release': 'gentle flowing ambient meditation music, soft water-like textures, airy pads, peaceful release, no vocals',
        'passage': 'quiet contemplative ambient music, slow evolving pads, soft piano droplets, meditative journey, no vocals',
        'default': 'soft meditation ambient music, gentle warm pads, subtle bells, deeply calming, no vocals',
    }
    base = prompts.get(theme, prompts['default'])
    return f"{base}; variation seed {seed}"


def run(cmd: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True)


def edge_tts_to_file(text: str, voice: str, rate: str, out_path: Path) -> None:
    cmd = [
        str(Path.home() / '.local' / 'bin' / 'edge-tts'),
        '--text', text,
        '--voice', voice,
        '--rate', rate,
        '--write-media', str(out_path),
    ]
    proc = run(cmd)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or 'edge-tts failed')


def generate_bg_music(theme: str, out_path: Path) -> dict:
    seed = random.randint(1000, 999999)
    prompt = build_bg_prompt(theme, seed)
    cmd = [
        'ffmpeg', '-y',
        '-f', 'lavfi', '-i', f'sine=frequency={220 + seed % 120}:duration=45:sample_rate=44100',
        '-f', 'lavfi', '-i', f'sine=frequency={440 + seed % 80}:duration=45:sample_rate=44100',
        '-filter_complex',
        '[0:a]volume=0.03[a0];[1:a]volume=0.015[a1];[a0][a1]amix=inputs=2:normalize=0,afade=t=in:st=0:d=2,afade=t=out:st=40:d=5',
        '-c:a', 'libmp3lame', '-q:a', '4', str(out_path)
    ]
    proc = run(cmd)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or 'bg generation failed')
    return {'prompt': prompt, 'seed': seed, 'path': str(out_path)}


def mix_voice_and_bg(voice_path: Path, bg_path: Path, out_path: Path) -> None:
    cmd = [
        'ffmpeg', '-y',
        '-i', str(voice_path),
        '-stream_loop', '-1', '-i', str(bg_path),
        '-filter_complex',
        '[1:a]volume=0.10,aloop=loop=-1:size=2e+09[bg];[0:a][bg]amix=inputs=2:weights=1 0.22:normalize=0:duration=first[a]',
        '-map', '[a]',
        '-c:a', 'libmp3lame', '-q:a', '2',
        str(out_path)
    ]
    proc = run(cmd)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or 'mix failed')


def main() -> None:
    ap = argparse.ArgumentParser(description='Generate Continuance meditation audio with soft TTS + random background')
    ap.add_argument('--text', required=True)
    ap.add_argument('--theme', default='default')
    ap.add_argument('--date')
    args = ap.parse_args()

    text = args.text.strip()
    lang = detect_language(text)
    voice = random.choice(ZH_VOICES if lang == 'zh' else EN_VOICES)
    rate = '-18%'
    date_str = args.date or __import__('datetime').datetime.now().strftime('%Y%m%d')

    OUTBOUND.mkdir(parents=True, exist_ok=True)
    final_path = OUTBOUND / f'continuance-meditation-{date_str}.mp3'

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        voice_path = td / 'voice.mp3'
        bg_path = td / 'bg.mp3'

        edge_tts_to_file(text, voice, rate, voice_path)
        bg_meta = generate_bg_music(args.theme, bg_path)
        mix_voice_and_bg(voice_path, bg_path, final_path)

    print(json.dumps({
        'success': True,
        'path': str(final_path),
        'language': lang,
        'voice': voice,
        'rate': rate,
        'theme': args.theme,
        'background': bg_meta,
        'delivery': 'voice-bubble-or-audio'
    }, ensure_ascii=False))


if __name__ == '__main__':
    main()
