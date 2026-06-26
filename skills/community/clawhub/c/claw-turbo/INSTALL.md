# Installation

## Requirements
- Python 3.10+
- pip

## Install

```bash
git clone https://github.com/jacobye2017-afk/claw-turbo.git
cd claw-turbo
pip install -e .
```

## Configure

1. Edit `routes.yaml` to define your command patterns
2. Start the proxy: `claw-turbo serve --port 11435`
3. Update OpenClaw's `~/.openclaw/openclaw.json`:

```json
{
  "models": {
    "providers": {
      "ollama": {
        "baseUrl": "http://127.0.0.1:11435"
      }
    }
  }
}
```

4. Restart OpenClaw: `openclaw gateway stop && openclaw gateway start`

## Verify

```bash
claw-turbo test "deploy auth to staging"
```
