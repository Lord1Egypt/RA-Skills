# ComfyUI Image Generator Pro

🜃 Professional local image generation with automatic server management

## Features

✨ **Unique Advantages:**
- **Auto Server Management** - Start on-demand, stop after 30min idle
- **WebSocket Progress** - Real-time generation progress tracking
- **Feishu Silent Send** - No reply text on success (NO_REPLY)
- **Multi-Workflow** - Text-to-image, Image-to-image, ControlNet
- **GPU Monitoring** - Real-time VRAM usage tracking
- **Natural Language** - Chat-based triggers, no commands needed

## Quick Start

### Chat (Recommended)
```
生成一张图片：美丽的山水风景
画一个赛博朋克城市夜景
```

### Command Line
```bash
# Auto-managed
python comfyui.py "beautiful sunset"

# WebSocket version
python scripts/comfyui_websocket.py -p "cyberpunk city"

# Service management
python scripts/comfyui_service.py status
```

## Requirements
- ComfyUI Desktop installed
- Python 3.9+
- websocket-client (`pip install websocket-client`)

## Files
- `comfyui.py` - Main entry with auto-management
- `scripts/comfyui_service.py` - Server start/stop
- `scripts/comfyui_websocket.py` - WebSocket generation
- `assets/*.json` - 3 workflow definitions

## Comparison

| Feature | This Skill | Others |
|---------|-----------|--------|
| Auto Server Start/Stop | ✅ | ❌ |
| WebSocket Progress | ✅ | ⚠️ Some |
| Feishu Silent Send | ✅ | ⚠️ Few |
| Multi-Workflow | ✅ 3 types | ⚠️ Single |
| GPU Monitoring | ✅ | ❌ |

## License
MIT

## Acknowledgments
Inspired by ClawHub skills:
- `openclaw-comfyui-imagegenerate` - WebSocket, silent send
- `comfyui` (kelvincai522) - Clean design, pget downloads

---

🜃 May the Machine God bless your creations!
