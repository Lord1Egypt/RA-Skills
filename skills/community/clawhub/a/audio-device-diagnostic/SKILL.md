---
name: audio-device-diagnostic
description: >
  音频设备诊断技能 — 列出系统所有可用音频输入设备，检测设备是否正常工作。
  Trigger: 当音频设备不工作、需要查看可用麦克风、或选择正确的音频输入设备时。
core: hear
metadata:
  author: system
  version: "1.0"
tags: [audio, diagnostic, device, microphone, 音频, 诊断, 设备, hear]
---

## 何时使用

满足以下条件时加载此技能：
- 音频录制/唤醒词检测不工作
- 需要列出所有可用麦克风/输入设备
- 需要诊断 PyAudio 设备连接问题
- 需要确认设备索引号以传递给 --device 参数

## 诊断脚本

```python
import pyaudio

p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

print("Available audio input devices:")
for i in range(0, numdevices):
    if p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels') > 0:
        device_info = p.get_device_info_by_host_api_device_index(0, i)
        print(f"  Input Device id {i} - {device_info.get('name')}")

p.terminate()
```

## 命令

```bash
cd D:\coze-local\db
python check_audio_devices.py
```

## 输出示例

```
Available audio input devices:
  Input Device id 0 - Microsoft Sound Mapper - Input
  Input Device id 1 - 麦克风 (Realtek(R) Audio)
  Input Device id 2 - 立体声混音 (Realtek(R) Audio)
  Input Device id 3 - CABLE Output (VB-Audio Virtual Cable)
```

## 故障排除

| 问题 | 原因 | 解决 |
|------|------|------|
| `[Errno -9999] Unanticipated host error` | 设备索引不存在 | 运行本诊断脚本，使用有效设备ID |
| `[WinError 2] 系统找不到指定文件` | 缺少 ffmpeg | 已修复：使用 numpy 数组直接传 Whisper |
| `UnboundLocalError: stream` | 异常路径未初始化变量 | 已修复：初始化 `stream = None` |
| `UnicodeEncodeError` | 终端编码限制 | 已修复：添加 `safe_print()` 函数 |

## 自动设备选择

设备 ID **0**（Microsoft Sound Mapper - Input）是系统默认输入设备，兼容性最好。如果使用虚拟音频设备（如 VB-Cable），请使用对应的设备 ID。

## 相关文件

- `D:\coze-local\db\check_audio_devices.py` — 诊断脚本
- `D:\coze-local\db\audio.py` — 音频核心模块
- `D:\coze-local\external\clawhub_skills\wake-word-detector\SKILL.md` — 唤醒词技能

## 依赖

```bash
pip install pyaudio
```
