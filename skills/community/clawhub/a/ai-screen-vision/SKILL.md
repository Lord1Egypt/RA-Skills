---
name: screen-vision
description: >
  AI screen vision and desktop computer control skill for OpenClaw.
  Let your AI agent see the screen, understand UI elements, and autonomously perform
  mouse and keyboard operations (click, type, scroll, drag) via a screenshot-analyze-action loop.
  Cross-platform: Linux (headless server with XFCE4+noVNC, or desktop), macOS (cliclick),
  Windows (pyautogui). Supports any OpenAI-compatible vision API (SiliconFlow, OpenAI,
  DashScope, Zhipu, Ollama, etc.). Smart diff detection saves tokens.
  Safety mechanisms block dangerous operations.
  Trigger: when user asks to operate/control computer, view/interact with screen,
  open applications, browse websites, fill forms, perform desktop GUI tasks, take screenshots,
  or any task requiring visual screen understanding and desktop automation.
  Keywords: computer use, screen control, desktop automation, GUI agent, visual agent,
  屏幕操控, 桌面控制, 视觉代理, 截屏, 自动化操作, 远程桌面, AI操控电脑,
  screen vision, desktop agent, mouse keyboard automation, UI automation,
  computer use agent, CUA, computer control, screen interaction.
  Examples: "打开Chrome搜索天气", "看看屏幕上有什么", "帮我操作电脑", "截个屏",
  "open browser and search weather", "click the submit button", "take a screenshot",
  "fill this form", "帮我打开微信", "操作电脑下载文件", "远程操作桌面".
---

# Screen Vision

Control the desktop visually: screenshot → AI vision analysis → execute actions → loop until done.

## Quick Start

### 1. Setup (one-time)

Detect platform and install dependencies:

```bash
bash scripts/setup/setup-linux.sh --headless   # Linux server (no desktop)
bash scripts/setup/setup-linux.sh --desktop     # Linux with desktop
bash scripts/setup/setup-mac.sh                 # macOS
python scripts/setup/setup-win.py          # Windows
```

### 2. Configure API

Copy `config.example.json` to `config.json` and fill in your vision API credentials.
You must set `baseUrl`, `apiKey`, and `model` — supports any OpenAI-compatible API.

```json
{
  "vision": {
    "baseUrl": "https://api.siliconflow.cn/v1",
    "apiKey": "sk-your-key",
    "model": "Qwen/Qwen3-VL-32B"
  }
}
```

Environment variables also work: `SV_VISION_API_KEY`, `SV_VISION_BASE_URL`, `SV_VISION_MODEL`.
See [references/API_CONFIG.md](references/API_CONFIG.md) for all supported providers and detailed setup.

### 3. Usage

The skill operates through a screenshot-analyze-action loop:

1. **Take screenshot** → `bash scripts/platform/screenshot.sh [output_path] [display]`
2. **Analyze with AI** → `python3 scripts/vision/analyze.py --image <path> --task "<task>"`
3. **Execute action** → `python3 scripts/platform/execute.py --action <type> [options]`
4. **Full task loop** → `python3 scripts/core/run_task.py --task "<task>"`

## Architecture

```
User task → run_task.py (orchestrator)
  ├── screenshot.sh (capture screen)
  ├── diff_check.py (detect changes, skip if unchanged → saves tokens)
  ├── analyze.py (send screenshot + task to vision API)
  ├── safety_check.py (block dangerous operations)
  ├── execute.py (xdotool/cliclick/pyautogui)
  └── loop until done or timeout
```

## Platform Tools

| Platform | Screenshot | Mouse/Keyboard | Notes |
|----------|-----------|----------------|-------|
| Linux | scrot | xdotool | Headless: XFCE4 + VNC |
| macOS | screencapture | cliclick | Needs Accessibility permission |
| Windows | pyautogui | pyautogui | No extra setup needed |

See [references/PLATFORM_GUIDE.md](references/PLATFORM_GUIDE.md) for platform-specific commands.

## Vision Providers

Supports **any OpenAI-compatible vision API**. You choose the provider and model.

### Recommended Models

| Model | Provider | Cost/Task | Quality |
|-------|----------|-----------|---------|
| Qwen3-VL-32B | SiliconFlow | Low | ★★★★ |
| GLM-4V-Plus | Zhipu BigModel | Low | ★★★★ |
| GPT-5.4-Mini | OpenAI / relays | Medium | ★★★★★ |
| GPT-5.4 CUA | OpenAI | High | ★★★★★ |
| Llama 3.2 Vision | Ollama (local) | Free | ★★ |

See [references/API_CONFIG.md](references/API_CONFIG.md) for per-provider configuration examples.

**No defaults are hardcoded** — you must configure your own API credentials before use.

## Action Types

- `click` — Click at (x, y). Supports left/right/double-click.
- `type` — Type text string.
- `key` — Press a key (Return, Tab, Escape, etc.).
- `scroll` — Scroll up or down.
- `drag` — Drag from (x1,y1) to (x2,y2).
- `wait` — Wait for screen to update.
- `done` — Task complete.
- `failed` — Cannot complete task.

## Safety

- **Blocked**: rm -rf, format disk, shutdown, drop database, etc.
- **Confirmation required**: delete, sudo, payment-related operations
- **Limits**: max 5 minutes, max 100 actions per task
- **Logging**: all screenshots saved to `/tmp/screen-vision/logs/`
- **Auto-stop** on error or API failure

## Examples

See [references/EXAMPLES.md](references/EXAMPLES.md) for usage examples.

## Config

| Variable | Default | Description |
|----------|---------|-------------|
| `SV_VISION_API_KEY` | — | Vision API key |
| `SV_VISION_BASE_URL` | — | API endpoint (required) |
| `SV_VISION_MODEL` | — | Vision model name (required) |
| `SV_DISPLAY` | `:1` | X11 display (Linux) |
| `SV_MAX_DURATION` | `5` | Max task duration (min) |
| `SV_MAX_ACTIONS` | `100` | Max actions per task |
| `SV_SCREENSHOT_INTERVAL` | `1.0` | Seconds between screenshots |
