# Environment

The skill needs three things at different levels:

| Layer | Used for | Needs |
| --- | --- | --- |
| system | everything | Python 3.10+, `ffmpeg`/`ffprobe`, a Chromium (Chrome, Edge or Chromium), a Chinese font |
| skill Python | record, render, check, mix | `playwright`, `opencv-python-headless`, `pillow`, `numpy`, `soundfile`, `soxr`, `scipy`, `faster-whisper`, `pypinyin`, `sherpa-onnx` |
| an engine | narration only | one of: Qwen on an NVIDIA GPU (CUDA torch, `faster-qwen3-tts`, two models) · Kokoro on the CPU (model + `sherpa-onnx`) · a remote key |

Recording and rendering work on a CPU-only machine, on **Linux, Windows and macOS**. Narration works wherever one of
the engines does: Qwen only with an NVIDIA GPU (so not on macOS), Kokoro on any CPU, remote services anywhere with a
network and a key.

## Check first

```bash
cd ~/.claude/skills/autoDemoRecordingSkill
python3 scripts/demo_env.py        # Windows: py -3 scripts/demo_env.py
```

It is read-only and prints one row per requirement with `有` / `缺` / `注意` and a `→` line saying how to get what is
missing; the last line lists which narration engines can speak. `--json` gives the same as JSON.

## The skill's own Python

```bash
python3 scripts/demo_env.py setup            # packages only
python3 scripts/demo_env.py setup --models   # also Whisper large-v3 + CAM++ checks
python3 scripts/demo_env.py setup --kokoro   # also Kokoro, the CPU voice (Chinese + English)
```

This creates `~/.cache/auto-demo-recording/venv` (`%USERPROFILE%\.cache\auto-demo-recording\venv` on Windows) and
installs the packages above. If `uv` is installed it is used, otherwise `venv` + `pip`. `--models` downloads:

- `Systran/faster-whisper-large-v3` from Hugging Face (about 3 GB);
- `3dspeaker_speech_campplus_sv_zh-cn_16k-common.onnx` from the sherpa-onnx GitHub releases (about 28 MB).

`--kokoro` downloads `kokoro-multi-lang-v1_1` (about 400 MB) from the sherpa-onnx releases and unpacks it under
`models/kokoro-multi-lang-v1_1`. All public. The check models are optional: whatever is missing only removes the
corresponding numeric check, and the scripts say so.

## System packages

### ffmpeg

Needs `libx264`, `aac`, `atempo` and `ebur128`:

```bash
ffmpeg -hide_banner -encoders | grep -E 'libx264|aac'
ffmpeg -hide_banner -filters  | grep -E 'atempo|ebur128'
```

- **Windows**: `winget install Gyan.FFmpeg` (or `choco install ffmpeg`), then open a new terminal so `PATH` has it.
- **macOS**: `brew install ffmpeg`.
- **Debian/Ubuntu**: `sudo apt install ffmpeg`. Some minimal or snap builds omit `libx264`; use a full build.

### Chromium

Windows and macOS usually have Chrome or Edge already — the recorder finds them in their usual places
(`C:\Program Files\Google\Chrome\Application\chrome.exe`, `/Applications/Google Chrome.app/…`, Edge likewise). On
Linux it looks for `/snap/bin/chromium` and the `PATH` names. To pin one:

```bash
# a system browser
python3 scripts/demo_env.py set chromium=/snap/bin/chromium
# or Playwright's own (any OS)
~/.cache/auto-demo-recording/venv/bin/python -m playwright install chromium
```

The recorder tries the configured browser first, then Playwright's, then the system's. It runs headless with
`--no-sandbox` and `--disable-dev-shm-usage`, which is what makes snap/container Chromium work.

### Fonts

Captions and labels use Noto Sans CJK SC or Source Han Sans where installed; otherwise the system's own Chinese face:

- **Windows**: Microsoft YaHei (`msyh.ttc`, `msyhbd.ttc`) — built in.
- **macOS**: PingFang SC (`PingFang.ttc`), Hiragino — built in.
- **Debian/Ubuntu**: `sudo apt install fonts-noto-cjk`.

The renderer searches the usual folders and falls back to `fc-match` where fontconfig exists. If it still cannot find
a face, point at a file (use `file#index` for a face inside a `.ttc`):

```bash
export DEMO_FONT_BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc#2'
export DEMO_FONT_MEDIUM='/usr/share/fonts/opentype/noto/NotoSansCJK-Medium.ttc#2'
export DEMO_FONT_REGULAR='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc#2'
```

Missing glyphs are detected by `demo_render.py --check` and reported as `字体里没有这些字符`.

## The narration engines

See [`engines.md`](../references/engines.md) for voices, keys and costs. This is the installation only.

### Qwen on the GPU (Linux, Windows)

A separate Python environment (the speech stack is heavy and conflicts with some recording packages). Python
3.10–3.12 is the safe range; tested with 3.11.

```bash
C=~/.cache/auto-demo-recording
uv venv --python 3.11 $C/tts-venv
# or: python3.11 -m venv $C/tts-venv

# the CUDA wheel matching the installed driver (cu121 / cu124 / cu128)
uv pip install --python $C/tts-venv/bin/python torch torchaudio --index-url https://download.pytorch.org/whl/cu128
uv pip install --python $C/tts-venv/bin/python faster-qwen3-tts==0.2.1 soundfile librosa
```

On Windows the interpreter is `%USERPROFILE%\.cache\auto-demo-recording\tts-venv\Scripts\python.exe`. Check it:

```bash
$C/tts-venv/bin/python -c 'import torch, faster_qwen3_tts; print(torch.__version__, torch.cuda.is_available())'
```

`True` is required. Download the two models (about 4.5 GB each; `hf` is the current Hugging Face CLI):

```bash
hf download Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice --local-dir $C/models/Qwen3-TTS-12Hz-1.7B-CustomVoice
hf download Qwen/Qwen3-TTS-12Hz-1.7B-Base        --local-dir $C/models/Qwen3-TTS-12Hz-1.7B-Base
```

Then tell the skill where things are:

```bash
python3 scripts/demo_env.py set tts_python=$C/tts-venv/bin/python \
    tts_custom=$C/models/Qwen3-TTS-12Hz-1.7B-CustomVoice tts_base=$C/models/Qwen3-TTS-12Hz-1.7B-Base
```

Weights stay in bfloat16 on the GPU; `demo_voice.py` refuses to start when free VRAM is below 6.5 GB and tells you to
close other GPU programs. Steps are resumable, so this is not lost work. macOS has no CUDA: use Kokoro or a remote
service there.

### Kokoro on the CPU (Linux, Windows, macOS)

```bash
python3 scripts/demo_env.py setup --kokoro
```

That installs `sherpa-onnx` into the skill's Python (if it was not there) and puts the model under
`models/kokoro-multi-lang-v1_1`. Nothing else. `demo_env.py set kokoro=/path/to/kokoro-multi-lang-v1_1` moves it; an
older `kokoro-multi-lang-v1_0` is found too, with fewer voices.

### A remote service

Nothing to install: set a key once, or use the environment variable.

```bash
python3 scripts/demo_env.py key openai=sk-…          # or ELEVENLABS_API_KEY / DASHSCOPE_API_KEY / DEMO_TTS_API_KEY
python3 scripts/demo_env.py key --list               # which are set, masked
```

The key is written to `~/.cache/auto-demo-recording/secrets.json` readable by the owner only (on Windows it stays
under the user's profile). A key can also be set with `VOICE['api_key']` for a throwaway run, but prefer the
environment or the secrets file: story files are shared.

## Where things are remembered

`demo_env.py set name=path` writes `~/.cache/auto-demo-recording/settings.json`. Environment variables win over that
file. Each path is accepted only if it exists (a launcher behind a symlink may stay the link).

| Name | Environment variable | Default |
| --- | --- | --- |
| skill home | `AUTO_DEMO_HOME` | `~/.cache/auto-demo-recording` |
| skill Python | `DEMO_PYTHON` | `$HOME/venv/bin/python` (`venv\Scripts\python.exe` on Windows) |
| Chromium | `DEMO_CHROMIUM` | Playwright's, then Chrome / Edge / Chromium |
| speech Python | `QWEN_TTS_PYTHON` | `$HOME/tts-venv/bin/python` |
| CustomVoice model | `QWEN_TTS_CUSTOM` | `$HOME/models/Qwen3-TTS-12Hz-1.7B-CustomVoice` |
| Base model | `QWEN_TTS_BASE` | `$HOME/models/Qwen3-TTS-12Hz-1.7B-Base` |
| Kokoro | `DEMO_KOKORO_MODEL` | `$HOME/models/kokoro-multi-lang-v1_1` |
| Whisper | `DEMO_WHISPER` | `$HOME/models/whisper-large-v3` |
| CAM++ | `DEMO_VOICEPRINT` | `$HOME/models/campplus_zh.onnx` |
| Hugging Face cache | `HF_HUB_CACHE` / `HF_HOME` | `~/.cache/huggingface` |
| remote keys | `DEMO_TTS_API_KEY`, `OPENAI_API_KEY`, `ELEVENLABS_API_KEY`, `DASHSCOPE_API_KEY` | `secrets.json` |

`$HOME` above means the skill home, not the user's home. If you set `AUTO_DEMO_HOME`, use the same value for every
command. The script also finds models already downloaded in the Hugging Face cache.

## Windows notes

- `python3` is usually not a command; use `py -3` or `python`. The skill's Python is
  `%USERPROFILE%\.cache\auto-demo-recording\venv\Scripts\python.exe`.
- The throwaway app is started in its own process group without a console window, and stopped with
  `taskkill /F /T /PID` — a server that parents other processes goes with it.
- Paths with spaces are fine (`subprocess` lists, not shell strings). Long recordings write many small JPEGs under
  `work/frames`; keep the work folder on a local disk.
- `nvidia-smi` must be on `PATH` for the Qwen engine (it ships with the driver).

## macOS notes

- `brew install ffmpeg`; Chrome or Edge from `/Applications` is found; fonts are built in.
- There is no CUDA, so the Qwen engine is skipped; Kokoro (CPU) and remote services work.
- On Apple Silicon the skill's Python runs natively; Kokoro's `sherpa-onnx` wheel is a universal build.

## Proxy, mirrors and offline use

- `HF_ENDPOINT=https://hf-mirror.com` makes `hf download` / `snapshot_download` use a mirror.
- `PIP_INDEX_URL` / `UV_INDEX_URL` point pip/uv at a mirror.
- Remote narration and `demo_env.py setup --models/--kokoro` honour `HTTP(S)_PROXY` and `NO_PROXY`.
- The recorder sets `trust_env=False` on its HTTP client, so a proxy in the environment does not intercept requests
  to the local app; `demo_voice.py` runs its model steps with `HF_HUB_OFFLINE=1` and `TRANSFORMERS_OFFLINE=1`, so it
  never reaches the network after the models are present.

## Disk and cleanup

| Thing | Size |
| --- | --- |
| skill venv | a few hundred MB |
| Whisper large-v3 | ~3 GB |
| CAM++ | ~28 MB |
| Kokoro | ~400 MB |
| two Qwen3-TTS 1.7B models | ~9 GB |
| speech venv (CUDA torch et al.) | several GB |
| one recording's work folder | tens of MB (frames) + takes |

Everything lives under `AUTO_DEMO_HOME` unless you moved it. Delete that folder to uninstall; nothing is installed
system-wide except `ffmpeg`, fonts and optionally a browser.
