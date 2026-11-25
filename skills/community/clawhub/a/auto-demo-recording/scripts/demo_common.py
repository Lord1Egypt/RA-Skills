"""What the scripts of this skill share: where the skill keeps its own things on this machine, where the tools it needs are, and the keys of remote services.

The skill's own things live in one folder, ~/.cache/auto-demo-recording unless AUTO_DEMO_HOME names another (the same
path on Linux, macOS and Windows: C:\\Users\\<you>\\.cache\\auto-demo-recording):

    venv/            the Python that records, draws and checks (demo_env.py setup makes it)
    models/          whisper-large-v3 and campplus_zh.onnx for checking; the speech models and Kokoro, if put here
    tts-venv/        a Python with the speech model's packages, if one was made here
    settings.json    where things are on this machine when they are somewhere else
    secrets.json     the keys of remote speech services (written by demo_env.py key, mode 600)

Each thing is looked for in this order: its environment variable, settings.json, the folder above, the usual
download places. The first that exists is taken.
"""
from __future__ import annotations

import json
import os
import shutil
import stat
import sys
from pathlib import Path

HOME = Path(os.environ.get('AUTO_DEMO_HOME') or Path(os.environ.get('XDG_CACHE_HOME') or Path.home() / '.cache') / 'auto-demo-recording').expanduser()
WINDOWS = os.name == 'nt'
BIN = 'Scripts' if WINDOWS else 'bin'
EXE = '.exe' if WINDOWS else ''
HUB = Path(os.environ.get('HF_HUB_CACHE') or Path(os.environ.get('HF_HOME') or Path.home() / '.cache/huggingface') / 'hub').expanduser()
SPEECH = 'Qwen3-TTS-12Hz-1.7B'   # the local speech model this skill reads the captions with: its CustomVoice and its Base variant
KOKORO = 'kokoro-multi-lang-v1_1'   # the CPU speech model: 103 voices, Chinese and English

# name: (environment variable, what the path must contain to count, where it is by default)
THINGS = {
    'python': ('DEMO_PYTHON', None, lambda: [HOME / 'venv' / BIN / f'python{EXE}']),
    'chromium': ('DEMO_CHROMIUM', None, lambda: []),
    'tts_python': ('QWEN_TTS_PYTHON', None, lambda: [HOME / 'tts-venv' / BIN / f'python{EXE}']),
    'tts_custom': ('QWEN_TTS_CUSTOM', 'model.safetensors', lambda: [HOME / 'models' / f'{SPEECH}-CustomVoice', *sorted(HUB.glob(f'models--Qwen--{SPEECH}-CustomVoice/snapshots/*'))]),
    'tts_base': ('QWEN_TTS_BASE', 'model.safetensors', lambda: [HOME / 'models' / f'{SPEECH}-Base', *sorted(HUB.glob(f'models--Qwen--{SPEECH}-Base/snapshots/*'))]),
    'kokoro': ('DEMO_KOKORO_MODEL', 'model.onnx', lambda: [HOME / 'models/kokoro-multi-lang-v1_1', HOME / 'models/kokoro-multi-lang-v1_0']),
    'whisper': ('DEMO_WHISPER', 'model.bin', lambda: [HOME / 'models/whisper-large-v3', *sorted(HUB.glob('models--Systran--faster-whisper-large-v3/snapshots/*'))]),
    'voiceprint': ('DEMO_VOICEPRINT', None, lambda: [HOME / 'models/campplus_zh.onnx']),
}

# the keys of the remote speech services: the environment variable, and the one some tools already use
KEYS = {'openai': ('DEMO_TTS_API_KEY', 'OPENAI_API_KEY'), 'elevenlabs': ('DEMO_TTS_API_KEY', 'ELEVENLABS_API_KEY'),
        'dashscope': ('DEMO_TTS_API_KEY', 'DASHSCOPE_API_KEY')}

# browsers the recorder can use, in the order it tries them: the one named in settings.json comes before these
if WINDOWS:
    BROWSERS = [r'C:\Program Files\Google\Chrome\Application\chrome.exe', r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
                r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe', r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
                'chrome', 'msedge', 'chromium']
elif sys.platform == 'darwin':
    BROWSERS = ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
                '/Applications/Chromium.app/Contents/MacOS/Chromium', '/snap/bin/chromium', 'google-chrome', 'chromium', 'chromium-browser', 'microsoft-edge']
else:
    BROWSERS = ['/snap/bin/chromium', 'chromium', 'chromium-browser', 'google-chrome', 'google-chrome-stable', 'microsoft-edge']


def browser(name):
    """A browser as a path that exists, or the name if it is on PATH, or None."""
    if not name:
        return None
    path = Path(name).expanduser()
    if path.is_file():
        return str(path)
    return shutil.which(name) or (str(path) if name.startswith('/') and path.exists() else None)


def browsers():
    """Every browser the recorder could use, the ones it would take first."""
    found = []
    for name in BROWSERS:
        path = browser(name)
        if path and path not in found:
            found.append(path)
    return found


def settings():
    try:
        return json.loads((HOME / 'settings.json').read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return {}


def remember(**values):
    """Write down where things are on this machine; an empty value forgets one."""
    kept = {**settings(), **values}
    kept = {key: value for key, value in kept.items() if value}
    HOME.mkdir(parents=True, exist_ok=True)
    (HOME / 'settings.json').write_text(json.dumps(kept, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    return kept


def where(name):
    """Where one of THINGS is on this machine, or None."""
    variable, inside, usual = THINGS[name]
    named = [os.environ.get(variable), settings().get(name)]
    for path in [Path(value).expanduser() for value in named if value] + usual():
        if (path / inside).is_file() if inside else path.exists():
            return path
    return None


def need(name, how):
    """Where it is, or stop and say how to get it."""
    path = where(name)
    if not path:
        raise SystemExit(f'缺 {name}：{how}')
    return path


# ---------- the keys of remote services ----------
def secrets():
    try:
        return json.loads((HOME / 'secrets.json').read_text(encoding='utf-8'))
    except (OSError, ValueError):
        return {}


def key(provider):
    """The key of a remote speech service: the environment variable first, then secrets.json. None when there is none."""
    for variable in KEYS.get(provider, ('DEMO_TTS_API_KEY',)):
        if os.environ.get(variable):
            return os.environ[variable]
    return secrets().get(provider) or None


def remember_key(provider, value):
    """Write down a key, readable by the owner only."""
    kept = {**secrets(), provider: value}
    kept = {name: secret for name, secret in kept.items() if secret}
    HOME.mkdir(parents=True, exist_ok=True)
    path = HOME / 'secrets.json'
    path.write_text(json.dumps(kept, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    try:
        path.chmod(stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass   # Windows keeps its own access control; the file stays under the user's profile
    return kept
