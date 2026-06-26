---
name: colab
description: Execute code on Google Colab GPU runtimes (T4/L4/A100/H100) and manage persistent storage via Google Drive. Use when tasks need GPU compute (ML training, inference, TTS), when running experiments that exceed local hardware, or when the user mentions Colab, GPU training, or remote compute. Also use for voice synthesis via F5-TTS on Colab. NOT for local-only code, simple scripts that don't need GPU, or tasks better suited for the host machine.
---

# Colab Skill

Execute Python on Google Colab GPU runtimes via headless API. No browser needed.

## Setup

1. **Authenticate with Colab** (one-time): Run the `colab-mcp` OAuth flow to create `~/.colab-mcp-auth-token.json`. See https://github.com/googlecolab/colab-mcp
2. **Add Drive scope** (optional, for persistence): `scripts/reauth_with_drive.py`
3. **Enable Drive API** (if using Drive): https://console.developers.google.com/apis/api/drive.googleapis.com — enable for your GCP project
4. **Python deps**: On first run, `colab_run.py` auto-creates a `.colab-venv/` venv via `uv` and installs deps. Requires `uv` (install: `pip install uv`). Deps: `google-auth-oauthlib`, `google-auth`, `jupyter-kernel-client`, `requests`, `google-api-python-client`

## Scripts

All scripts live in `scripts/` and use a `.colab-venv/` sibling directory for dependencies.

### `colab_run.py` — Execute code on Colab

```bash
# Inline code on CPU
python3 scripts/colab_run.py exec "print('hello')"

# Script on T4 GPU
python3 scripts/colab_run.py exec --gpu T4 --file script.py

# Keep runtime alive between calls
python3 scripts/colab_run.py exec --gpu T4 --keep "x = 42"

# GPU options: T4 (default), L4, A100, H100
python3 scripts/colab_run.py exec --gpu A100 --file heavy_training.py

# Runtime management
python3 scripts/colab_run.py list          # Active runtimes
python3 scripts/colab_run.py stop <ep>     # Stop runtime
python3 scripts/colab_run.py info          # CU balance + eligible GPUs
```

### `colab_drive.py` — Google Drive file transfer

```bash
python3 scripts/colab_drive.py upload file.pt --folder colab-workspace
python3 scripts/colab_drive.py download checkpoint.pt --output ./checkpoint.pt
python3 scripts/colab_drive.py list --folder colab-workspace
```

Requires `drive.file` OAuth scope (run `scripts/reauth_with_drive.py` once).

### `inject_and_run.sh` — Run scripts with Drive access inside Colab

Injects the local OAuth token into a script before sending it to Colab. Place `__COLAB_TOKEN_PLACEHOLDER__` where the base64 token should go:

```bash
bash scripts/inject_and_run.sh my_script.py --gpu T4
```

Inside the script:
```python
import json, base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

token_data = json.loads(base64.b64decode("__COLAB_TOKEN_PLACEHOLDER__"))
with open('/tmp/token.json', 'w') as f:
    json.dump(token_data, f)
creds = Credentials.from_authorized_user_file('/tmp/token.json')
service = build('drive', 'v3', credentials=creds)
```

### `colab_tts.py` — Voice synthesis via F5-TTS

```bash
# One-time: fetch voice samples from ElevenLabs
python3 scripts/colab_tts.py fetch-voice --voice-id <id> --api-key <key>

# Generate speech with cloned voice
python3 scripts/colab_tts.py speak "Hello world" --output hello.wav --gpu T4
```

### `reauth_with_drive.py` — Add Drive scope to OAuth token

```bash
python3 scripts/reauth_with_drive.py
```

Opens browser for Google sign-in. One-time setup.

## GPU Selection Guide

| GPU | CU/hr | $/hr | VRAM | Use for |
|-----|-------|------|------|---------|
| **T4** | ~2 | $0.20 | 15GB | Default. Inference, small training, TTS |
| **L4** | ~3.5 | $0.35 | 24GB | Medium models, need bf16 or >15GB |
| **A100** | ~5-15 | $0.50-1.50 | 40/80GB | Large models, serious training |
| **H100** | ~20+ | $2.00+ | 80GB | Maximum throughput, time-critical |

Start with T4. Escalate only when VRAM or speed demands it.

## Patterns

### Short task (inference, TTS, quick experiment)
Assign → execute → get output → unassign. Don't use `--keep`.

### Multi-step session
Use `--keep`. State persists in kernel between `exec` calls. Unassign when done.

### Long training with Drive checkpoints
Use `inject_and_run.sh`. Script checkpoints to Drive every N epochs. If runtime dies, re-run — script loads latest checkpoint from Drive. See `references/examples.md` for template.

### Structured output
Embed parseable markers in script stdout:
```python
print(f"__RESULT__{json.dumps(metrics)}")    # Structured data
print(f"__AUDIO__{base64_audio}")             # Binary as base64
```

## Timeouts

- **Idle timeout (Pro):** ~90 min without active execution
- **Max session (Pro):** ~24 hours continuous
- **Active code execution prevents idle disconnect**
- **Runtime death loses `/tmp/`** — use Drive for anything you need to keep

## API Quirk

GPU assignment requires split GET/POST: GET fetches XSRF token (no GPU params), POST creates assignment with `variant=GPU&accelerator=T4`. Already handled by `colab_run.py`.
