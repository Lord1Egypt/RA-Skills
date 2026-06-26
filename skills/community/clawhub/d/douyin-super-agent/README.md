# 🚀 douyin — 全能抖音处理

**一键处理抖音视频/音频转写/语音识别**，整合多种引擎自动降级，零配置开箱即用。

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-green)]()

---

## ✨ 一句话介绍

丢一个抖音链接，自动给你提取文案（视频→音频→文字→精简），全链路零干预。

---

## 🎯 核心能力

| 功能 | 说明 |
|------|------|
| **抖音视频处理** | 发链接 → 自动下载 + 提取文案 + 自动纠错，结果自动保存到桌面 |
| **音频转写** | 任意音频文件 → 语音识别（支持中文/英文） |
| **三级 ASR 降级** | qwen-asr（远程优先）→ whisper-medium（本地降级）→ 腾讯云（最后备选） |
| **文案自动纠错** | 擎天柱/铁疙瘩/注入/Grok/AI-FSD 等 10+ 常见 ASR 错别字自动修正 |
| **内存管理** | 处理记录自动写入本地记忆库 |

---

## 🚀 快速开始

### 方法 1：一键安装（推荐）

```bash
# 克隆/下载 skill 到 ~/.openclaw/skills/
chmod +x setup.sh && ./setup.sh
```

脚本会自动完成：
- ✅ 安装 Python 依赖（faster_whisper、ffmpeg 等）
- ✅ 下载 whisper-medium 模型（1.5GB）
- ✅ 创建输出目录（~/Desktop/douyin-douyin-super-agent/）
- ✅ 验证环境完整性

### 方法 2：手动安装

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 首次运行（自动下载模型）
python3 scripts/douyin.py stats

# 3. 开始使用！
python3 scripts/douyin.py video "https://v.douyin.com/xxx/"
```

### 方法 3：仅音频转写（不下载模型）

如果你只需要音频转写且已有 whisper 模型：

```bash
# --engine whisper 直接跳过下载
python3 scripts/douyin.py audio audio.mp3 --engine whisper
```

---

## 📖 使用方式

### 抖音视频处理

```bash
# 完整流程：下载 + 提取文案
python3 scripts/douyin.py video "https://v.douyin.com/xxx/"

# 仅下载，不转写
python3 scripts/douyin.py video "https://v.douyin.com/xxx/" --no-asr

# 指定 ASR 引擎
python3 scripts/douyin.py video "https://v.douyin.com/xxx/" --engine qwen
```

### 音频转写

```bash
# 自动选择最佳引擎
python3 scripts/douyin.py audio audio.mp3

# 指定引擎
python3 scripts/douyin.py audio audio.mp3 --engine whisper
python3 scripts/douyin.py audio audio.mp3 --engine qwen
python3 scripts/douyin.py audio audio.mp3 --engine tencent
```

### 能力统计

```bash
python3 scripts/douyin.py stats
```

---

## 📂 输出文件

所有输出自动保存到 `~/Desktop/douyin-douyin-super-agent/`：

```
~/Desktop/douyin-douyin-super-agent/
├── dy_7625013269783068529.mp4        ← 视频文件
├── dy_7625013269783068529.mp3        ← 音频文件
├── transcript_7625013269783068529.txt ← 精简文案（自动纠错）
└── result_7625013269783068529.json   ← 结构化结果
```

---

## 🏗️ 技术架构

```
用户输入
    │
    ▼
┌─────────────────────────┐
│    自动路由引擎          │
├─────────────────────────┤
│ 1. qwen-asr    (远程)   │ ← 优先，短音频最优
│ 2. whisper-med (本地)   │ ← 降级，长音频稳
│ 3. tencent-c (云端)     │ ← 备胎
└─────────────────────────┘
    │
    ▼
┌─────────────────────────┐
│    文案后处理            │
│ • 错别字修正 (10+ 规则) │
│ • 口语词过滤            │
│ • 标点规范化            │
└─────────────────────────┘
    │
    ▼
输出文件 (txt/md/json)
```

---

## ⚙️ 依赖

### 必选

| 依赖 | 用途 | 安装方式 |
|------|------|----------|
| Python 3.10+ | 运行环境 | 系统自带/`brew install python3` |
| faster-whisper | 本地 ASR | `pip install -r requirements.txt` |
| ffmpeg | 音频提取 | `brew install ffmpeg` |

### 可选（自动降级，无则跳过）

| 依赖 | 用途 |
|------|------|
| uv | qwen-asr 运行时 |
| mcporter | MCP 客户端 |
| douyin-mcp | 抖音视频解析 |

### 模型

| 模型 | 大小 | 安装方式 |
|------|------|----------|
| whisper-small | ~500MB | 自动下载 |
| whisper-medium | ~1.5GB | 自动下载（默认） |
| whisper-large-v3 | ~3GB | 可选，更高精度 |

---

## 🤖 错别字自动修正

已知 ASR 常见错误，已内置自动修正：

| 错误输出 | 修正为 |
|---------|--------|
| 晴天柱 | 擎天柱 |
| 铁哥 | 铁疙瘩 |
| 住进/注进 | 注入 |
| 这特曼 | 这特么 |
| AI减4 / AI加4 | AI-FSD |
| 零言池 | 零延迟 |
| Grogg | Grok |
| 几倍发凉 | 脊背发凉 |
| 这几倍发粮 | 这脊背发凉 |

---

## 📜 License

MIT License
