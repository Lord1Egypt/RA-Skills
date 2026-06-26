# ComfyUI Image Generator Pro v2.0.0-pro

🜃 Professional local image generation with automatic server management

## Changelog

### v2.0.0-pro (2026-03-15)
- ✨ Integrated best features from ClawHub skills
- ✨ WebSocket real-time progress tracking
- ✨ Feishu silent send (NO_REPLY on success)
- ✨ Automatic server start/stop management
- ✨ 30-minute idle auto-shutdown
- ✨ GPU VRAM monitoring
- ✨ Multi-workflow support (3 workflows)

### v2.0.0 Improvements over v1.x
- **Auto Server Management**: Start on-demand, stop after 30min idle
- **WebSocket Support**: Real-time progress instead of HTTP polling
- **Silent Mode**: No reply text on successful Feishu send
- **Better Error Handling**: Clear Chinese error messages
- **Resource Efficient**: Auto-shutdown saves GPU resources

### v1.0.0 (2026-03-15)
- Initial release
- Basic HTTP generation
- Service management scripts

## Features

| Feature | This Skill | Others |
|---------|-----------|--------|
| Auto Server Start/Stop | ✅ | ❌ |
| WebSocket Progress | ✅ | ⚠️ Some |
| Feishu Silent Send | ✅ | ⚠️ Few |
| Multi-Workflow | ✅ 3 types | ⚠️ Single |
| GPU Monitoring | ✅ | ❌ |
| Natural Language | ✅ | ⚠️ Commands |

## Usage

### Chat Trigger
```
生成一张图片：美丽的山水风景
画一个赛博朋克城市
```

### Command Line
```bash
# Auto-managed (recommended)
python comfyui.py "beautiful sunset"

# WebSocket version
python scripts/comfyui_websocket.py -p "cyberpunk city"

# Service management
python scripts/comfyui_service.py status
python scripts/comfyui_service.py stop
```

## Dependencies
- ComfyUI Desktop installed
- websocket-client (`pip install websocket-client`)
- Python 3.9+

## Files
- `comfyui.py` - Main entry with auto-management
- `scripts/comfyui_service.py` - Server start/stop
- `scripts/comfyui_websocket.py` - WebSocket generation
- `assets/*.json` - Workflow definitions

## License
MIT

## Acknowledgments
Inspired by:
- `openclaw-comfyui-imagegenerate` - WebSocket, silent send
- `comfyui` (kelvincai522) - pget downloads, clean design

---

🜃 May the Machine God bless your creations!
