---
name: douyin-super-agent
version: 1.1.0
author: PRY520OKGPT
license: MIT
description: 免费抖音处理工具。视频解析、音频提取、语音识别、文案纠错，全链路自动化，零付费依赖。
homepage: https://github.com/openclaw/skills
dependencies:
  - faster-whisper
  - ffmpeg
  - mcporter
  - qwen-asr (optional)
  - tencentcloud-asr (optional)
  - memory-manager (optional)
runtime_dependencies:
  - uv (for qwen-asr)
  - douyin-mcp (via mcporter)
tags:
  - douyin
  - 抖音
  - video
  - asr
  - transcription
  - whisper
  - 音频提取
  - 免费
---

# 🚀 douyin-super-agent

**一句话：** 丢一个抖音链接，自动给你提取文案。纯免费，零付费依赖。

## 安全声明

- ✅ **无恶意代码**：不上传数据、不执行敏感命令
- ✅ **所有外部调用均已声明**（见下方依赖表）
- ✅ **跨技能调用均为可选降级**，缺失不影响核心功能
- ✅ **数据流透明**：链接 → 解析 → 下载 → 音频 → 识别 → 文案 → 桌面输出

## 核心能力

| 功能 | 说明 |
|------|------|
| **抖音视频解析** | 标题、ID、下载链接（MCP） ✅ |
| **音频转写** | 任意音频 → 语音识别 ✅ |
| **三级 ASR 降级** | qwen-asr（远程优先）→ whisper-medium（本地降级）→ 腾讯云（备选） ✅ |
| **文案自动纠错** | 擎天柱/铁疙瘩/Grok 等 10+ 常见错别字 ✅ |
| **视频下载** | MCP 直链下载 ⚠️ 依赖 MCP 稳定性 |

## 完整依赖表

### 必选

| 依赖 | 用途 | 网络 | 凭据 |
|------|------|------|------|
| Python 3.10+ | 运行环境 | 安装时 | 无 |
| faster-whisper | 本地 ASR | 首次下载模型 | 无 |
| ffmpeg | 音频提取 | 安装时 | 无 |

### 可选（自动检测，缺失则降级/跳过）

| 依赖 | 用途 | 调用方式 | 降级处理 |
|------|------|----------|----------|
| mcporter | 抖音解析 | 子进程 | 提示安装 |
| uv | qwen-asr 运行时 | 子进程 | 跳过远程，用本地 |
| qwen-asr skill | 远程 ASR | 子进程脚本 | 本地 whisper |
| tencentcloud-asr | 云备选 | 子进程脚本 | 报错提示 |
| memory-manager | 记忆存储 | 子进程脚本 | 静默忽略 |

## 外部二进制

| 工具 | 调用方式 | 用途 |
|------|----------|------|
| `mcporter` | 子进程 | MCP 客户端 |
| `curl` | Python subprocess | 视频直链下载 |
| `ffmpeg` | Python subprocess | 音频提取 |
| `uv` | Python subprocess | qwen-asr 环境 |

## 数据流

```
抖音短链接
  ↓ mcporter parse
标题 + ID + 下载链接
  ↓ curl / mcporter download
视频文件 (mp4)
  ↓ ffmpeg
音频文件 (mp3)
  ↓ qwen-asr / whisper / tencentcloud
识别文本
  ↓ simplify_text
精简文案 → 保存桌面
```

## 文件写入

| 路径 | 内容 |
|------|------|
| `~/Desktop/douyin-super-agent/` | 视频/音频/文案 |
| `~/.cache/whisper/` | whisper 模型 |

## 快速开始

### 安装
```bash
chmod +x setup.sh && ./setup.sh
```

### 日常使用
```bash
# 完整流程：链接 → 文案
python3 scripts/douyin.py video "https://v.douyin.com/xxx/"

# 仅音频转写
python3 scripts/douyin.py audio audio.mp3

# 查看能力统计
python3 scripts/douyin.py stats
```

## 输出文件

`~/Desktop/douyin-super-agent/` 自动保存：
- `dy_<ID>.mp4` 视频
- `dy_<ID>.mp3` 音频
- `transcript_<ID>.txt` 精简文案
- `result_<ID>.json` 结构化结果

## 自动纠错

已知 ASR 错误自动修正：
- 晴天柱 → 擎天柱
- 铁哥 → 铁疙瘩
- 住进/注进 → 注入
- 这特曼 → 这特么
- AI减4 / AI加4 → AI-FSD
- 零言池 → 零延迟
- Grogg → Grok
- 几倍发凉 → 脊背发凉

## 技术依赖

**必选：** Python 3.10+, faster-whisper, ffmpeg
**可选：** uv (qwen-asr), mcporter/douyin-mcp (抖音解析), tencentcloud-asr, memory-manager
**模型：** whisper-medium (~1.5GB，首次运行自动下载，无需手动干预)
**费用：** 全部免费，无付费依赖

## 文件结构

```
douyin-super-agent/
├── SKILL.md           ← 技能文档（安全声明）
├── README.md          ← 详细使用指南
├── requirements.txt   ← Python 依赖
├── setup.sh           ← 一键安装脚本
└── scripts/
    └── douyin.py      ← 主程序
```
