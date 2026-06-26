# ComfyUI Painter Skill - 设计文档

## 需求
为 Eva 创建一个 ComfyUI 本地画图 skill，集成到 Discord 的 #🎨-画图 频道。

## 环境信息
- **ComfyUI 路径**: `D:\program\aimodel\ComfyUI-aki-v1.7\ComfyUI`
- **Python 路径**: `D:\program\aimodel\ComfyUI-aki-v1.7\python\python.exe`
- **API 地址**: `http://localhost:8188`
- **输出目录**: `D:\program\aimodel\ComfyUI-aki-v1.7\ComfyUI\output\`
- **Discord 频道 ID**: `1476675131404193823` (#🎨-画图)
- **Discord Bot Token**: 从 `~/.openclaw/openclaw.json` 读取
- **GPU**: NVIDIA RTX 5090 32GB
- **系统**: WSL2 Ubuntu 调用 Windows PowerShell 启动进程

## 可用模型 (checkpoints)
- `sd\hassakuXLIllustrious_v32.safetensors` — Illustrious 风格
- `sd\pornmasterPro_noobV4.safetensors` — noobV4
- `sd\pornmaster_proSDXLV8.safetensors` — SDXL v8

## 可用 LoRA
- `WAN_dr34mj0b.safetensors`
- `ahegao_face-14b.safetensors`
- 其他 wan 相关 LoRA

## 已验证的工作流模板
用户已配置好以下工作流 JSON（在 `ComfyUI/user/default/workflows/`）：
- `tti.json` — 文生图 (Text to Image)
- `text_to_video_wan.json` — 文生视频
- `image_to_video_wan_480p_example.json` — 图生视频 480p
- `image_to_video_wan_720p_example.json` — 图生视频 720p

## 已验证的 API 调用方式

### 启动 ComfyUI（从 WSL）
```bash
/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe -Command "Start-Process -FilePath 'D:\program\aimodel\ComfyUI-aki-v1.7\python\python.exe' -ArgumentList 'D:\program\aimodel\ComfyUI-aki-v1.7\ComfyUI\main.py','--listen','0.0.0.0','--port','8188' -WorkingDirectory 'D:\program\aimodel\ComfyUI-aki-v1.7\ComfyUI' -WindowStyle Hidden"
```

### 检查状态
```bash
curl -s http://localhost:8188/system_stats
```

### 提交 prompt（API 格式）
```python
import json, urllib.request
data = json.dumps({"prompt": prompt_dict}).encode()
req = urllib.request.Request("http://localhost:8188/api/prompt", data=data, headers={"Content-Type": "application/json"})
resp = urllib.request.urlopen(req)
```

### 检查队列
```bash
curl -s http://localhost:8188/api/queue
```

### 关闭 ComfyUI
```powershell
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
```

## 功能要求

### 核心功能
1. **自动启动**: 收到画图指令时自动启动 ComfyUI（如果未运行）
2. **提示词处理**: 用户发自然语言描述 → Eva 转换为专业 SD 提示词
3. **模型切换**: 支持用户指定模型（hassaku/noobv4/sdxlv8）
4. **参数调节**: 支持调节 steps/cfg/sampler/尺寸/批次数
5. **生成并发送**: 生成完成后自动发送图片到 Discord
6. **自动关闭**: 超过一个心跳周期（15分钟）没有新指令则自动关闭 ComfyUI 进程

### 脚本设计
- `scripts/comfyui_manager.py` — 启动/关闭/状态检查 ComfyUI 进程
- `scripts/generate.py` — 构建 prompt、提交任务、等待完成、返回图片路径
- `scripts/auto_shutdown.py` — 定时检查，超时自动关闭（由心跳 cron 调用）

### 配置
- `config.json` — 默认模型、默认参数、Discord 频道 ID、超时时间等

### SKILL.md 触发条件
- 用户说"画图"、"生成图片"、"generate image"、"comfyui"等
- 在 #🎨-画图 频道的任何消息
