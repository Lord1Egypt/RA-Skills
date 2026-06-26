---
name: fun-voice-type
description: 一个语音输入法插件。它基于阿里云FunASR实时语音识别技术，允许用户通过长按快捷键（Right Option键）直接将语音转换为文字并“打”在当前光标所在的任何输入框中。此外，还能将语音翻译为多种语言（例：中英日韩）。
---

## 激活条件

| 触发场景 | 说明 |
|----------|------|
| 请求语音转译 | "实时录音转写"、"语音转文字"、"实时语音翻译" |
| 功能咨询 | "怎么用语音打字？" |
| 效率需求 | "我不方便打字"、"帮我记录这段话" |

## 核心功能
- **长按即说**：将鼠标光标点击到任何你想输入文字的地方，长按 **Right Option** <kbd>⌥</kbd> 开始录音，松开自动完成。
- **全场景兼容**：无缝支持浏览器、文档编辑器、IM 聊天软件等任何 macOS 标准输入控件。
- **多语种兼容**：支持多语种输入，以及翻译功能（点击fun-voice-type图标选择目标语种）。

## 环境依赖

### 1. 系统库依赖
由于使用了 `pyaudio`，你需要先在系统中安装portaudio以及python依赖：
```bash
brew install portaudio
pip install dashscope pynput pyaudio pystray
```

### 2. 设置 DashScope API Key
为了安全起见，建议将API Key设置为环境变量：
```bash
export DASHSCOPE_API_KEY='你的API_KEY'
```

如果还没有API Key，建议访问 [阿里云 DashScope 控制台](https://dashscope.console.aliyun.com/)，申请并获取API Key。

## 安装与运行
运行脚本，fun-voice-type将显示为Mac菜单栏右上角的小图标：
```bash
nohup python fun-voice-type.py > /dev/null 2>&1
```
此时长按**右Option**即可实现语音输入功能。

## 权限授予

由于该 Skill 需要监听全局键盘按键并模拟键盘输入，在不同系统下需要额外权限：

### macOS
- **辅助功能 (Accessibility)**：前往 `系统设置 -> 隐私与安全性 -> 辅助功能`，将你运行脚本的终端（如 Terminal, iTerm2 或 VSCode）勾选开启。
- **麦克风 (Microphone)**：首次运行时，系统会弹出麦克风权限请求，请点击允许。
- **输入监听 (Input Monitoring)**：同样在隐私设置中确保终端有权监听键盘。

--- 

*版本*: 2.0.0
*日期*: 2026-03-21