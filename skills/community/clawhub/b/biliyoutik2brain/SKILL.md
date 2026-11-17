---
name: biliyoutik2brain
description: "视频→结构化知识引擎 v4.0。触发：B站/YouTube/抖音/小红书链接→转录+结构化分析+知识归档。不触发：纯文本内容/非视频链接/无URL的对话。单条命令完成采集→转录→LLM修复→分析→保存。支持一键部署、4+N平台插件、反爬中间件、OCR关键帧、多格式输出(笔记/卡片/富文本/错题)、反馈闭环、图文并茂MD。"
version: "4.0.5"
---

# BiliYouTik2Brain v4.0.5 — 视频→结构化知识引擎

**全链路：采集 → 转录 → LLM修正 → 结构化分析 → 图文并茂输出**

## 支持平台

| 平台 | 状态 | 特点 |
|------|:--:|------|
| B站 | ✅ 完整 | API bypass 直接下载音频 |
| YouTube | ✅ 完整 | yt-dlp 驱动 |
| 抖音 | ✅ 完整 | Web scraping + 音频提取 |
| 小红书 | 🔨 基础 | yt-dlp 通用提取 |
| 更多平台 | 🔌 插件 | 插件架构兼容任意平台 |

## 核心能力

- **ASR**: faster-whisper 本地转录，自动选择最优模型（环境自适应），置信度≥87%
- **LLM修正**: DeepSeek v4-flash 三层提示词 + 纠错词典 + 反馈闭环
- **关键帧**: 混合驱动（音频引导 + 视觉确认 + OCR），图文并茂输出
- **多格式**: 笔记 / 知识卡片 / 富文本(图文) / 错题集
- **双层知识**: UP主画像 + 领域知识体系
- **反爬**: 4平台差异化策略（B站412/抖音Session/小红书yt-dlp/YouTube代理+鉴权）
- **隐私**: `--private` 全本地模式
- **集成**: 记忆系统/Obsidian/Notion（默认关闭，配置开启）
- **一键部署**: `bash install.sh` → 自动检测环境 → 安装依赖

## 基础用法

```bash
# 一键部署
bash install.sh

# 完整管线
python3 run.py <视频链接>

# 隐私模式（全本地）
python3 run.py --private <视频链接>

# 仅评论分析
python3 run.py --comments <链接>

# 查看系统状态
python3 run.py --status

# 查看已注册平台
python3 run.py --list-platforms
```

## 完整管线流程

```
URL → 平台识别 → 反爬中间件 → 采集(元信息/音频/字幕/评论)
    → 转录(faster-whisper) → LLM修正(纠错闭环)
    → 关键帧检测+OCR → 结构化分析
    → 模板渲染(笔记/卡片/富文本/错题) → 反馈闭环 → 集成推送
```

## 场景示例

**处理B站视频：**
```bash
python3 run.py https://b23.tv/xxx
```

**处理抖音视频：**
```bash
python3 run.py https://v.douyin.com/xxx/
```

**处理YouTube视频：**
```bash
python3 run.py https://youtu.be/xxx
```

**批量处理：** 多次调用 `run.py`（每个视频独立进程，智能并发）

## 输出位置

| 类型 | 路径 |
|------|------|
| 笔记 | `~/openclaw/workspace/storage/notes/` |
| 卡片 | `~/openclaw/workspace/storage/cards/` |
| 错题 | `~/openclaw/workspace/storage/errors/` |
| 音频 | `/tmp/douyin_b2b/` (抖音临时) |

## 质量指标

- 转录准确率 ≥ 90% (实测置信度 0.87~0.95)
- 10分钟视频处理 ≤ 5分钟 (实测 33~150s)
- 成本 ≤ ¥0.20/视频
- OCR 覆盖 ≥ 60% 关键帧

## 配置

配置文件: `~/.biliyoutik2brain/`

- `sync_config.json` — 同步目标(GitHub/Obsidian/Notion)
- `integration_config.json` — 外部集成开关
- `env.yaml` — 硬件/引擎/模型选择

## 注意事项

- 首次运行会自动下载 faster-whisper 模型(~150MB)
- 抖音需要可用的 yt-dlp
- 隐私模式下不调用任何外部 LLM API

## 版本历史

### v4.0.5 安全修整
- [安全] eval() 替换为 dict 映射（system_monitor.py）
- [安全] SSL 证书验证禁用统一管理（_create_insecure_ssl_context()）
- [安全] 安装脚本示例 Key 替换为安全占位符
- [安全] 全量扫描零硬编码密钥