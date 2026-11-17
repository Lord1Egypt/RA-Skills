# ADB Bot Automation | Android 自动化

> AI-driven Android automation via MCP — OpenClaw ClawHub Skill

[English](#english) | [中文](#中文)

***

<a id="english"></a>

## Overview

[ADB Bot](https://adb-bot.hilbp.com/?utm_source=clawhub&utm_medium=readme) is an AI-powered Android automation platform built on BPMN workflow engine and ADB protocol. It supports natural language control, workflow recording & replay, and multi-device management.

This Skill enables [OpenClaw](https://github.com/openclaw/openclaw) to control Android devices directly via MCP protocol.

## Features

- **Screenshot & Recognition** — Capture screen, identify content with multimodal AI
- **UI Tree Analysis** — Extract interface elements with precise coordinates
- **Screen Actions** — Tap, swipe, type text, press keys
- **App Control** — Launch apps, list installed packages
- **Multi-Device** — Execute the same action across multiple devices concurrently
- **Workflow Recording** — AI actions are automatically recorded as reusable flows

## Installation

### 1. Install ADB Bot

- Download: [adb-bot.hilbp.com](https://adb-bot.hilbp.com/?utm_source=clawhub&utm_medium=readme) (Windows / macOS / Linux)
- GitHub: <https://github.com/hilbp/adb-bot/releases>

Run the installer (`.exe` on Windows), then launch ADB Bot.

### 2. Connect Device

1. Enable **Developer Options**: Settings → About Phone → tap "Build Number" 7 times
2. Enable **USB Debugging** in Developer Options
3. Connect your phone via USB, allow USB debugging when prompted
4. Launch ADB Bot and confirm your device appears in the device list

> Full guide: [adb-bot.hilbp.com](https://adb-bot.hilbp.com/?utm_source=clawhub&utm_medium=readme)

### 3. Install Skill

```bash
npx clawhub@latest install adb-bot
```

### 4. Connect MCP

```bash
openclaw mcp set adb-bot '{"url":"http://localhost:8080/mcp","transport":"streamable-http"}'
```

### 5. Start Using

Talk to OpenClaw in natural language:

```
Take a screenshot and tell me what's on screen
Open WhatsApp
Tap the top right corner
Type "hello" in the search box
```

## Requirements

- ADB Bot v1.0.0+
- Android device with USB debugging enabled
- USB cable or WiFi ADB connection

***

<a id="chinese"></a>

## 介绍

[ADB Bot](https://adb-bot.hilbp.com/?utm_source=clawhub&utm_medium=readme) 是一款 AI 驱动的 Android 自动化平台，基于 BPMN 流程引擎和 ADB 协议，支持自然语言操作、流程录制回放、多设备群控。

这个 Skill 让 [OpenClaw](https://github.com/openclaw/openclaw) 能够通过 MCP 协议直接操控 Android 设备。

## 功能

- **截屏与识别** — 截取屏幕，多模态 AI 识别内容
- **UI 元素分析** — 获取界面元素树，精确定位按钮和输入框
- **屏幕操作** — 点击、滑动、输入文本、按键
- **应用控制** — 启动应用、查询已安装应用
- **多设备群控** — 对多台设备并发执行同一操作
- **流程录制** — AI 操作自动录制为可复用的自动化流程

## 安装

### 1. 安装 ADB Bot

- 官网下载：[adb-bot.hilbp.com](https://adb-bot.hilbp.com/?utm_source=clawhub&utm_medium=readme)（支持 Windows / macOS / Linux）
- GitHub 下载：<https://github.com/hilbp/adb-bot/releases>

Windows 用户下载 `.exe` 安装包，双击运行，然后启动 ADB Bot。

### 2. 连接设备

1. 手机进入「设置 → 关于手机」，连续点击「版本号」7 次，开启「开发者选项」
2. 进入「开发者选项」，开启「USB 调试」
3. 用 USB 数据线连接手机和电脑，手机弹窗点击「允许 USB 调试」
4. 启动 ADB Bot，在设备列表中确认手机已识别

> 详细教程见官网「快速上手」：[adb-bot.hilbp.com](https://adb-bot.hilbp.com/?utm_source=clawhub&utm_medium=readme)

### 3. 安装 Skill

```bash
npx clawhub@latest install adb-bot
```

### 4. 连接 MCP

```bash
openclaw mcp set adb-bot '{"url":"http://localhost:8080","transport":"streamable-http"}'
```

### 5. 开始使用

在 OpenClaw 中直接用自然语言操作手机：

```
帮我截个屏看看手机现在什么界面
打开相册
点击右上角的扫一扫
在搜索框输入张三
```

## 系统要求

- ADB Bot v1.0.0+
- Android 设备（已开启 USB 调试）
- USB 数据线 或 WiFi ADB 连接

***

## Links

- Website: [adb-bot.hilbp.com](https://adb-bot.hilbp.com/?utm_source=clawhub&utm_medium=readme)
- GitHub：<https://github.com/hilbp/adb-bot>

