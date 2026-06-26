# 🎵 Accompaniment Generator

一个 OpenClaw 技能，从 YouTube 或本地音频文件中分离人声和伴奏，生成纯伴奏音乐。

## 功能特性

- ✅ **YouTube 搜索下载** — 输入歌名+歌手，自动搜索下载并分离
- ✅ **直接视频 URL** — 提供 YouTube 链接直接处理
- ✅ **本地文件处理** — 上传本地音频文件进行分离
- ✅ **人声/伴奏双轨输出** — 同时保留人声轨道

## 使用方法

### 通过 OpenClaw 调用

对话中直接告诉 AI 你想提取某首歌的伴奏即可，支持三种模式：

**模式 1：歌名+歌手**
> "帮我提取《光年之外》邓紫棋的伴奏"
> "生成周杰伦《七里香》的卡拉OK版"

**模式 2：YouTube 链接**
> "帮我提取这个视频的伴奏 https://youtube.com/xxx"

**模式 3：本地文件**
> 直接发送音频文件，AI 会自动分离伴奏

### 输出说明

- 伴奏音频文件（.wav 格式）
- 人声音频文件（.wav 格式）
- 文件可通过 OpenClaw 下载链接获取

## 技术原理

基于 [spleeter](https://github.com/deezer/spleeter) 深度学习模型进行音源分离，支持：

- `spleeter:2stems` — 人声 + 伴奏（默认，推荐）
- 模型自动下载缓存，首次使用需联网

## 依赖

- Python 3.7+
- spleeter
- ffmpeg
- yt-dlp（YouTube 下载）

## 安装

```bash
pip install spleeter
pip install yt-dlp
apt install ffmpeg
```

## 项目结构

```
accompaniment-generator/
├── SKILL.md                  # OpenClaw 技能描述
├── README.md                 # 本文件
├── .gitignore
├── references/               # 参考文档（预留）
└── scripts/
    └── get_accompaniment.py  # 核心伴奏提取脚本
```
