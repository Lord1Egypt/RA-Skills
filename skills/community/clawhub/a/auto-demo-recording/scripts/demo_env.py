"""See what this machine has for recording a demo video, and make the skill's own Python.

    python3 demo_env.py                  # what is there, what is missing, and how to get each missing thing
    python3 demo_env.py setup            # makes the skill's Python (packages only, a few hundred MB)
    python3 demo_env.py setup --models   # also fetches the two checking models (about 3 GB; public, from Hugging Face and GitHub)
    python3 demo_env.py setup --kokoro   # also fetches Kokoro, the CPU voice for Chinese and English (about 400 MB)
    python3 demo_env.py set chromium=/snap/bin/chromium tts_python=/path/to/python   # where things are on this machine
    python3 demo_env.py key openai=sk-…  # remember the key of a remote speech service (secrets.json, owner only)
    python3 demo_env.py key --list       # which services have a key

Any Python 3.10 or later runs this script; everything else of the skill is run with the Python it makes. Nothing is
downloaded by the plain check; `setup` fetches only what its flags name. On Windows, `py -3` or `python` stands where
`python3` is written here.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path

import demo_common
import demo_tts
from demo_common import BIN, BROWSERS, HOME, KEYS, SPEECH, THINGS, WINDOWS, browsers, key, remember, remember_key, secrets, settings, where

SCRIPTS = Path(__file__).resolve().parent
PACKAGES = ['playwright', 'httpx', 'numpy', 'opencv-python-headless', 'pillow', 'soundfile', 'soxr', 'scipy', 'faster-whisper', 'pypinyin', 'sherpa-onnx']
RECORDING = ['playwright', 'httpx', 'numpy', 'cv2', 'PIL']                  # modules: record and render
MIXING = ['soundfile', 'soxr', 'scipy']                                     # narration: fit, level, mix
CHECKING = ['faster_whisper', 'pypinyin', 'sherpa_onnx']                    # narration: what was said, in whose voice, and Kokoro's runtime
SPEAKING = ['torch', 'faster_qwen3_tts', 'soundfile', 'librosa', 'numpy']   # the speech model's own Python
KOKORO_URL = 'https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/kokoro-multi-lang-v1_1.tar.bz2'
FETCH = '''
import sys, urllib.request
from pathlib import Path
from huggingface_hub import snapshot_download
models = Path(sys.argv[1])
models.mkdir(parents=True, exist_ok=True)
if not (models / 'whisper-large-v3/model.bin').is_file():
    snapshot_download('Systran/faster-whisper-large-v3', local_dir=str(models / 'whisper-large-v3'),
                      allow_patterns=['config.json', 'model.bin', 'tokenizer.json', 'vocabulary.json', 'preprocessor_config.json'])
if not (models / 'campplus_zh.onnx').is_file():
    part = models / 'campplus_zh.onnx.part'
    urllib.request.urlretrieve('https://github.com/k2-fsa/sherpa-onnx/releases/download/speaker-recongition-models/3dspeaker_speech_campplus_sv_zh-cn_16k-common.onnx', part)
    part.rename(models / 'campplus_zh.onnx')
'''
PY = 'python' if WINDOWS else 'python3'


def answer(command, **more):
    try:
        done = subprocess.run([str(part) for part in command], capture_output=True, text=True, timeout=120, **more)
    except (OSError, subprocess.TimeoutExpired) as error:
        return 1, str(error)
    return done.returncode, (done.stdout + done.stderr).strip()


def lacking(python, modules):
    """Which of these modules this Python cannot import."""
    code, out = answer([python, '-c', f'import importlib.util, json; print(json.dumps([m for m in {modules!r} if importlib.util.find_spec(m) is None]))'])
    try:
        return json.loads(out.splitlines()[-1]) if not code else modules
    except (ValueError, IndexError):
        return modules


def browsers_of(python):
    """Browsers the recorder can use, the one it would take first: the one named in the settings, the one Playwright brought, those of the system."""
    found = [str(path) for path in [where('chromium')] if path]
    if python:
        code, out = answer([python, '-c', 'from playwright.sync_api import sync_playwright\nwith sync_playwright() as p: print(p.chromium.executable_path)'])
        if not code and out and Path(out.splitlines()[-1]).is_file():
            found.append(out.splitlines()[-1])
    return found + [path for path in browsers() if path not in found]


def temporary(path):
    try:
        return Path(path).resolve().is_relative_to(Path(tempfile.gettempdir()).resolve())
    except OSError:
        return False


def look():
    """Everything the three stages need, one row each: (stage, what, 'ok' | 'missing' | 'warn', where or what is wrong, how to get it)."""
    rows = []
    add = lambda *row: rows.append(row)
    python = where('python')
    setup = f'{PY} {SCRIPTS / "demo_env.py"} setup'
    if python:
        gone = lacking(python, RECORDING)
        add('录制与渲染', '本技能的 Python', 'missing' if gone else 'ok', f'{python}' + (f'（缺 {"、".join(gone)}）' if gone else ''), setup)
    else:
        add('录制与渲染', '本技能的 Python', 'missing', f'{HOME / "venv"} 还没有', setup)
    for tool in ('ffmpeg', 'ffprobe'):
        add('录制与渲染', tool, 'ok' if shutil.which(tool) else 'missing', shutil.which(tool) or '不在 PATH 里',
            '装系统的 ffmpeg（要带 libx264）：Windows 用 winget install Gyan.FFmpeg，macOS 用 brew install ffmpeg，Debian/Ubuntu 用 sudo apt install ffmpeg')
    if shutil.which('ffmpeg'):
        encoders, filters = answer(['ffmpeg', '-hide_banner', '-encoders'])[1], answer(['ffmpeg', '-hide_banner', '-filters'])[1]
        gone = [name for name in ('libx264', 'aac') if f' {name} ' not in encoders] + [name for name in ('atempo', 'ebur128') if f' {name} ' not in filters]
        add('录制与渲染', 'ffmpeg 的编码器和滤镜', 'missing' if gone else 'ok', '缺 ' + '、'.join(gone) if gone else 'libx264、aac、atempo、ebur128 都有', '换一个完整的 ffmpeg')
    found = browsers_of(python)
    add('录制与渲染', 'Chromium', 'ok' if found else 'missing', found[0] if found else '没有找到',
        f'{python or "<本技能的 Python>"} -m playwright install chromium；或装系统的 Chrome/Edge/Chromium，再用 demo_env.py set chromium=路径 记下')
    if python and not lacking(python, RECORDING):
        code, out = answer([python, '-c', 'import demo_render\nfor weight in ("Bold", "Medium", "Regular"): print(weight, *demo_render.font_file(weight))'], cwd=SCRIPTS)
        add('录制与渲染', '字幕和标注的字体', 'missing' if code else 'ok', out.splitlines()[-1] if code else '；'.join(out.splitlines()),
            'Windows 与 macOS 自带中文黑体（微软雅黑 / 苹方）；Linux 装 Noto Sans CJK（fonts-noto-cjk），或用 DEMO_FONT_BOLD / DEMO_FONT_MEDIUM / DEMO_FONT_REGULAR 指到字体文件')

    # ---- narration: the three kinds of engine
    code, out = answer(['nvidia-smi', '--query-gpu=name,memory.total,memory.used', '--format=csv,noheader'])
    add('配音 · 本机 GPU（Qwen）', '显卡', 'warn' if code else 'ok', '没有 nvidia-smi：Qwen 语音模型要在 NVIDIA 显卡上跑' if code else out.replace('\n', '；'), 'Qwen 约占 6 GB 显存；没有显卡用 Kokoro 或远程服务')
    speaker = where('tts_python')
    if speaker:
        gone = lacking(speaker, SPEAKING)
        code, out = (1, '') if gone else answer([speaker, '-c', 'import torch; print(torch.__version__, torch.cuda.is_available())'])
        fine = not gone and not code and out.endswith('True')
        add('配音 · 本机 GPU（Qwen）', '语音模型的 Python', 'ok' if fine else 'missing', f'{speaker}' + (f'（缺 {"、".join(gone)}）' if gone else f'（torch {out.splitlines()[-1] if out else "?"}）'),
            'torch（带 CUDA）、faster-qwen3-tts、soundfile、librosa；见 references/environment.md')
        if fine and temporary(speaker):
            add('配音 · 本机 GPU（Qwen）', '语音模型的 Python 的位置', 'warn', f'{speaker} 在临时目录里，重启后会消失', '见 references/environment.md 的“放到不会丢的地方”')
    else:
        add('配音 · 本机 GPU（Qwen）', '语音模型的 Python', 'missing', '没有找到', '建一个带 torch 和 faster-qwen3-tts 的 Python，用 demo_env.py set tts_python=路径 记下；见 references/environment.md')
    for name, variant in (('tts_custom', 'CustomVoice'), ('tts_base', 'Base')):
        path = where(name)
        add('配音 · 本机 GPU（Qwen）', f'语音模型 {SPEECH}-{variant}', 'ok' if path else 'missing', str(path) if path else '没有找到',
            f'下载 Qwen/{SPEECH}-{variant}（约 4.5 GB）到 {HOME / "models" / f"{SPEECH}-{variant}"}，或 demo_env.py set {name}=已有的路径')
        if path and temporary(path):
            add('配音 · 本机 GPU（Qwen）', f'{SPEECH}-{variant} 的位置', 'warn', f'{path} 在临时目录里，重启后会消失', '见 references/environment.md 的“放到不会丢的地方”')

    kokoro = where('kokoro')
    add('配音 · 本机 CPU（Kokoro）', 'Kokoro 模型', 'ok' if kokoro else 'missing', str(kokoro) if kokoro else '没有找到（中文、英文；不需要显卡，任何机器都能用）',
        f'{setup} --kokoro（约 400 MB，公开模型）')
    if python:
        add('配音 · 本机 CPU（Kokoro）', 'sherpa-onnx', 'ok' if not lacking(python, ['sherpa_onnx']) else 'missing',
            '在' if not lacking(python, ['sherpa_onnx']) else '缺', setup)
    for provider, variable in KEYS.items():
        has = key(provider)
        add('配音 · 远程服务', provider, 'ok' if has else 'warn', '有密钥' if has else '没有密钥（要用时再设）',
            f'demo_env.py key {provider}=…，或环境变量 {variable[-1]}')
    add('配音 · 远程服务', 'OpenAI 兼容接口', 'warn', '用 base_url 指向自己的服务（本地或第三方）', '在 VOICE 里写 engine: compatible 与 base_url、model、speaker')

    if python:
        gone = lacking(python, MIXING + CHECKING)
        add('配音的核验', '混音和听写的包', 'missing' if gone else 'ok', '缺 ' + '、'.join(gone) if gone else '、'.join(MIXING + CHECKING), setup)
    for name, what in (('whisper', '听写模型 Whisper large-v3'), ('voiceprint', '声纹模型 CAM++')):
        path = where(name)
        add('配音的核验', what, 'ok' if path else 'missing', str(path) if path else '没有找到', f'{setup} --models（共约 3 GB，公开模型）')
    return rows


def download(url, target):
    """Fetch a file, saying how it goes; a partial file left behind by an earlier run is started over."""
    part = target.with_name(target.name + '.part')
    with urllib.request.urlopen(url, timeout=60) as answer, open(part, 'wb') as sink:
        whole = int(answer.headers.get('content-length') or 0)
        done = 0
        while True:
            chunk = answer.read(1 << 20)
            if not chunk:
                break
            sink.write(chunk)
            done += len(chunk)
            if whole and done % (64 << 20) < (1 << 20):
                print(f'  {target.name}: {done * 100 // whole}%', flush=True)
    part.rename(target)
    print(f'  {target.name}: 完成（{target.stat().st_size / 1e6:.0f} MB）', flush=True)


def kokoro_models():
    """Kokoro, the CPU voice: unpacked into the skill's models folder."""
    folder = HOME / 'models/kokoro-multi-lang-v1_1'
    if (folder / 'model.onnx').is_file():
        print(f'Kokoro 已经有了：{folder}')
        return folder
    archive = HOME / 'models/kokoro-multi-lang-v1_1.tar.bz2'
    archive.parent.mkdir(parents=True, exist_ok=True)
    print(f'下载 Kokoro（约 350 MB）：{KOKORO_URL}')
    download(KOKORO_URL, archive)
    with tarfile.open(archive, 'r:bz2') as tar:
        try:
            tar.extractall(HOME / 'models', filter='data')   # Python 3.12+: no path out of the folder
        except TypeError:
            tar.extractall(HOME / 'models')
    archive.unlink(missing_ok=True)
    print(f'Kokoro 放在 {folder}')
    return folder


def setup(models, kokoro):
    python = HOME / 'venv' / BIN / f'python{".exe" if WINDOWS else ""}'
    HOME.mkdir(parents=True, exist_ok=True)
    uv = shutil.which('uv')
    if not python.exists():
        subprocess.run([uv, 'venv', '--python', sys.executable, str(HOME / 'venv')] if uv else [sys.executable, '-m', 'venv', str(HOME / 'venv')], check=True)
    subprocess.run([uv, 'pip', 'install', '--python', str(python), *PACKAGES] if uv else [str(python), '-m', 'pip', 'install', *PACKAGES], check=True)
    if models:
        subprocess.run([str(python), '-c', FETCH, str(HOME / 'models')], check=True)
    if kokoro:
        kokoro_models()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('step', nargs='?', default='check', choices=['check', 'setup', 'set', 'key'])
    parser.add_argument('pairs', nargs='*', help='for set: name=path (names: ' + ', '.join(THINGS) + '); for key: provider=key')
    parser.add_argument('--models', action='store_true', help='with setup: also fetch the two checking models')
    parser.add_argument('--kokoro', action='store_true', help='with setup: also fetch Kokoro, the CPU voice')
    parser.add_argument('--list', action='store_true', help='with key: show which services have a key, masked')
    parser.add_argument('--json', action='store_true')
    options = parser.parse_args()
    if options.step == 'setup':
        setup(options.models, options.kokoro)
    elif options.step == 'set':
        pairs = dict(pair.split('=', 1) for pair in options.pairs)
        unknown = [name for name in pairs if name not in THINGS]
        if unknown or not pairs:
            raise SystemExit(f'能记的只有：{", ".join(THINGS)}')
        missing = [value for value in pairs.values() if value and not Path(value).expanduser().exists()]
        if missing:
            raise SystemExit(f'没有这个路径：{missing[0]}')
        remember(**{name: str(Path(value).expanduser().absolute()) if value else '' for name, value in pairs.items()})  # as named: a launcher behind a link (snap) must stay the link
    elif options.step == 'key':
        if options.list or not options.pairs:
            for provider in KEYS:
                found = key(provider)
                print(f'{provider:12s} ' + (f'有：{found[:4]}…{found[-4:]}' if found and len(found) > 10 else '有' if found else '没有'))
        else:
            pairs = dict(pair.split('=', 1) for pair in options.pairs)
            unknown = [name for name in pairs if name not in KEYS]
            if unknown:
                raise SystemExit(f'能记密钥的只有：{", ".join(KEYS)}')
            remember_key(**pairs)
            print(f'记下了 {len(pairs)} 个密钥（{HOME / "secrets.json"}，只有你能读）')
    rows = look()
    if options.json:
        print(json.dumps({'home': str(HOME), 'settings': settings(), 'keys': {name: bool(key(name)) for name in KEYS}, 'rows': rows}, ensure_ascii=False, indent=1))
    else:
        stage = None
        for row in rows:
            if row[0] != stage:
                stage = row[0]
                print(f'\n{stage}')
            print(f'  [{ {"ok": "有", "missing": "缺", "warn": "注意"}[row[2]] }] {row[1]}：{row[3]}' + (f'\n        → {row[4]}' if row[2] != 'ok' else ''))
        print(f'\n本技能自己的东西放在 {HOME}')
        print(f'配音引擎：{"、".join(code for code in demo_tts.ENGINES if demo_tts.usable(code)[0]) or "还没有"}；'
              f'问用户要不要配音、用什么语言、哪个引擎（SKILL.md 的第 0 步）')
