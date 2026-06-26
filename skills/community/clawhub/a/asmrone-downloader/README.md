# asmrone-downloader

从 [ASMR.one](https://asmr.one) 下载音频作品，自动压缩至 QQ 兼容格式，支持收藏管理。

适用于 RJ 编号的 ASMR 音频下载，支持代理、多格式压缩、去重下载。

---

## 功能

- 搜索作品（关键词 AND，覆盖最新 ~600 个作品）
- 查看作品详情
- 下载并自动压缩（VBR / CBR 64k / OPUS）
- 超出 20MB 自动降码率
- 收藏管理，去重下载
- 环境检查

---

## 依赖

- Python 3.8+
- `requests`
- `ffmpeg` + `ffprobe`（压缩用）

```bash
pip3 install requests
# Ubuntu: sudo apt install ffmpeg
# macOS:  brew install ffmpeg
```

---

## 快速开始

```bash
# 交互式配置（代理 / 输出目录）
python3 scripts/asmr_tool.py config init

# 验证环境
python3 scripts/asmr_tool.py check

# 搜索
python3 scripts/asmr_tool.py search "陽向葵ゅか"

# 下载
python3 scripts/asmr_tool.py download RJ01230165
```

---

## 配置

优先级：CLI 参数 > 环境变量 > 配置文件 > 默认值。

配置文件：`~/.config/asmr-tool/config.json`（权限 600）。

| 配置项 | 说明 | 环境变量 |
|--------|------|----------|
| `proxy` | HTTP 代理地址 | `ASMR_PROXY` |
| `output_dir` | 下载目录 | `ASMR_OUTPUT_DIR` |
| `default_vbr` | VBR 质量 q0~q9 | `ASMR_VBR` |
| `default_bitrate` | 默认比特率 | `ASMR_BITRATE` |

---

## 命令

| 命令 | 用途 |
|------|------|
| `config` | 配置管理（init / show / set / get） |
| `check` | 环境检查 |
| `search` | 搜索作品 |
| `hot` | 热门推荐 |
| `info` | 作品详情 |
| `download` | 下载并压缩 |
| `sendlist` | 列出已下载文件 |
| `collection` | 收藏列表 |

---

## 安全

- 配置文件保存在 `~/.config/asmr-tool/config.json`，权限自动设为 600
- 配置文件不提交到 Git（已加入 `.gitignore`）

---

## 目录结构

```
asmrone-downloader/
├── scripts/
│   └── asmr_tool.py          # 主工具
├── SKILL.md                   # OpenClaw 技能文档
├── README.md
├── requirements.txt
├── example_config.json
├── asmrone-downloader.skill
└── .gitignore
```
