---
name: asmrone-downloader
description: "从 ASMR.one 下载音频作品，自动压缩，并生成发送列表。使用场景：下载 RJ 编号的 ASMR 音频。"
license: MIT-0
---

# ASMR.one 下载器

从 [ASMR.one](https://asmr.one) 下载音频作品，自动压缩，支持收藏管理。

## 完整工作流

```
配置环境 → 验证环境 → 搜索/推荐 → 下载压缩 → 收藏记录
无网络时 → 导入本地音频 → 压缩 → 收藏
```

---

## 快速安装

```bash
# 1. 安装依赖
pip3 install requests

# 2. 安装 ffmpeg（用于压缩）
# Ubuntu/Debian:
sudo apt install ffmpeg
# macOS:
brew install ffmpeg

# 3. 配置初始化
python3 asmr_tool.py config init
```

---


---

## 环境验证

```bash
python3 asmr_tool.py check
```

输出示例：
```
  [Python]    ✅ 3.12.3
  [requests]  ✅ 2.31.0
  [ffmpeg]    ✅ ffmpeg version 6.1.1
  [ffprobe]   ✅ ffprobe version 6.1.1
  [网络]
   外网: ✅
   ASMR.one: ✅
  [配置]      ✅ 配置文件已存在
```

网络检查会同时检测外网连通性和 ASMR.one 服务状态。外网不通时，搜索下载功能不可用，但可以通过 `import` 命令使用本地文件。

---

## 常用命令

| 命令 | 用途 |
|------|------|
| `config init` | 交互式配置代理、输出目录 |
| `config show` | 查看当前配置 |
| `config set key value` | 设置单个配置项 |
| `check` | 检查运行环境（含外网检测） |
| `search 关键词` | 搜索作品（多关键词 AND） |
| `hot` | 热门推荐 |
| `info RJ编号` | 作品详情 |
| `download RJ编号` | 下载，默认 voice 模式压缩至 QQ 兼容格式 |
| `import RJ编号 目录` | 从本地目录导入已有音频文件 |
| `sendlist RJ编号` | 列出已下载文件 |
| `collection` | 查看收藏列表 |

### 配置项说明

| 配置项 | 含义 | 环境变量 |
|--------|------|----------|
| `proxy` | 代理地址 | `ASMR_PROXY` |
| `output_dir` | 下载目录 | `ASMR_OUTPUT_DIR` |
| `default_vbr` | 默认 VBR 质量 (q0~q9) | `ASMR_VBR` |
| `default_bitrate` | 默认比特率 | `ASMR_BITRATE` |
| `qq_target` | QQ Bot 发送目标 | `QQ_TARGET` |

**配置优先级：** CLI 参数 > 环境变量 > 配置文件 > 默认值

---

## 示例

```bash
# 初始化配置
python3 asmr_tool.py config init

# 验证环境
python3 asmr_tool.py check

# 搜索作品
python3 asmr_tool.py search "陽向葵ゅか"

# 查看作品详情
python3 asmr_tool.py info RJ01377478

# 下载，语音模式（默认，压缩至 QQ 兼容格式）
python3 asmr_tool.py download RJ01377478

# 下载，文件模式（不压缩，保持原始质量）
python3 asmr_tool.py download RJ01377478 --mode file

# 指定代理（覆盖配置文件）
python3 asmr_tool.py search "关键词" --proxy http://127.0.0.1:7890

# 从本地目录导入音频（无需网络）
python3 asmr_tool.py import RJ01230165 /path/to/audio/files --title "作品标题" --cv "CV名"
```

---

## 下载选项

| 参数 | 说明 |
|------|------|
| `--vbr q3` | VBR 压缩（推荐，q3~q5 音质好体积均衡） |
| `--opus` | OPUS 格式（体积最小，兼容性有限） |
| `--no-compress` | 保留原始文件 |
| `--all-formats` | 下载非 MP3 格式 |
| `--mode voice` | 语音模式：压缩至 QQ 兼容格式，超过 20MB 自动降码率到 64k（默认） |
| `--mode file` | 文件模式：不压缩，保持原始质量，适合通过 QQ 文件发送 |

**自动降码率（voice 模式）：** 超过 20MB 的文件会自动降码率到 64k。
**file 模式：** 跳过所有压缩和降码率，直接保存原始文件。

---

## 本地导入（无网络场景）

当无法访问外网或 ASMR.one 时，可以将本地已有的音频文件导入管理：

```bash
python3 asmr_tool.py import RJ01230165 ./my_audio_folder --title "作品名" --cv "CV名"
```

导入功能：
- 自动复制音频文件到输出目录
- 超过 20MB 的非 MP3 文件自动压缩
- 生成封面文件并记录到收藏
- 不需要网络连接

---

## 搜索限制

- API 搜索仅覆盖最新作品（约 600 个以内）
- 老作品或小众作品请用已知 RJ 编号直接查 `info RJxxxx`
- 也可以通过浏览器在 ASMR.one 网站上搜索

---

## 安全说明

配置文件权限默认设为 600（仅本用户可读），不要分享配置文件。

---

## 收藏功能

下载或导入完成后自动记录。配置文件存储在 `~/.config/asmr-tool/collection.json`。

```bash
python3 asmr_tool.py collection          # 列表
python3 asmr_tool.py collection --detail # 详细信息
```

---

## 目录结构

```
~/.config/asmr-tool/          # 配置文件目录
├── config.json               # 代理、输出目录等配置（权限 600）
└── collection.json           # 收藏记录

~/asmr_downloads/             # 默认下载目录
└── RJxxxxxx/
    ├── RJxxxxxx_001_音轨.mp3
    ├── RJxxxxxx_002_音轨.mp3
    ├── raw/                   # 原始文件（压缩后保留）
    └── manifest.json         # 下载清单
```

---

## 文件说明

| 文件 | 说明 |
|------|------|
| `scripts/asmr_tool.py` | 主工具 |
| `requirements.txt` | Python 依赖 |
| `example_config.json` | 配置示例 |
| `.gitignore` | Git 忽略规则 |
| `SKILL.md` | 本文件 |
