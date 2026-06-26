---
name: geo-master
description: 品牌AI可见性监控Skill。自动搜索Kimi/讯飞星火/文心一言/智谱等AI平台，检测品牌关键词可见性，生成0-100 GEM评分，AI分析"为什么没被推荐"，支持飞书推送。
triggers:
  - GEO
  - AI可见性
  - 品牌监控
  - AI搜索可见性
  - 竞品监控
allowed-tools: Bash(python3)
---

# GEO Master - 品牌AI可见性监控

检测品牌在AI搜索平台中的可见性，生成评分与优化建议。

## 版本与定价

| 版本 | 价格 | 品牌限制 | 平台数量 | 技术方案 |
|------|------|:--------:|:--------:|----------|
| **免费版** | ¥0/月 | 1个/月 | 3个平台 | 本地Playwright |
| **标准版** | ¥29/月 | 无限 | 全部9个平台 | 本地Playwright |
| **专业版** | ¥99/月 | 无限 | 全部9个平台 | 🌐 Tavily API（实时搜索） |
| **企业版** | ¥399/月 | 无限 | 全部9个+深度分析 | 专属客服 |

### 免费版限制

- 每月最多检测 **1个品牌**
- 每月最多使用 **3个AI平台**（Kimi、讯飞星火、文心一言）
- 每月1日自动重置配额

### 专业版核心优势（🌐 Tavily实时搜索）

专业版用户通过**Tavily搜索API**获取AI平台的实时搜索结果：

- ✅ 全部9个AI平台（DeepSeek/千问/豆包/秘塔/混元等）
- ✅ 覆盖AI的**实时搜索推荐**（非训练数据）
- ✅ 我们服务器中转，无需本地环境
- ✅ 稳定高效，不封IP

> 购买专业版/企业版后，请在 [https://yk-global.com](https://yk-global.com) 获取API密钥，使用 `--api-key YOUR_KEY` 参数运行即可解锁全部功能。验证接口：`POST https://api.yk-global.com/v1/verify`，验证失败自动降级到免费版，不阻断使用。

## 支持的AI平台

| 平台 | 免费版 | 标准版 | 专业版 | 技术方案 |
|------|:------:|:------:|:------:|---------|
| Kimi | ✅ | ✅ | ✅ | Playwright直接抓取 |
| 讯飞星火 | ✅ | ✅ | ✅ | Playwright直接抓取 |
| 文心一言 | ✅ | ✅ | ✅ | Playwright直接抓取 |
| 智谱 | ❌ | ✅ | ✅ | Playwright直接抓取 |
| DeepSeek | ❌ | ✅ | ✅ | 🌐 Tavily API实时搜索 |
| 通义千问 | ❌ | ✅ | ✅ | 🌐 Tavily API实时搜索 |
| 豆包 | ❌ | ✅ | ✅ | 🌐 Tavily API实时搜索 |
| 秘塔 | ❌ | ✅ | ✅ | 🌐 Tavily API实时搜索 |
| 混元 | ❌ | ✅ | ✅ | 🌐 Tavily API实时搜索 |

**专业版检测维度**：训练收录 + 实时搜索结果（两者全覆盖）

## 快速使用

```bash
# 检测单个品牌
python3 scripts/geo_report.py "品牌名"

# 检测多个品牌（含竞品）
python3 scripts/geo_report.py "品牌A" "品牌B"

# 不推送飞书（调试用）
python3 scripts/geo_report.py "品牌名" --no-push

# 查看配额状态
python3 scripts/geo_report.py --status

# 使用 API Key（专业版/企业版用户）
python3 scripts/geo_report.py "品牌名" --api-key YOUR_API_KEY

# 升级到专业版/企业版
python3 scripts/geo_report.py --upgrade-pro
python3 scripts/geo_report.py --upgrade-ent
```

## 评分说明

| 评分 | 等级 | 说明 |
|-----:|:----:|------|
| 80-100 | 🟢 优秀 | AI主动推荐，品牌强曝光 |
| 60-79 | 🟡 良好 | 被部分AI平台提及 |
| 30-59 | 🟠 一般 | 零星提及，需优化 |
| 0-29 | 🔴 薄弱 | 完全不可见 |

## 配置文件

配置文件位于 `config.json`：

```json
{
  "platforms": {
    "kimi": {"enabled": true, "weight": 1.0},
    "xinhuo": {"enabled": true, "weight": 0.9},
    "yiyan": {"enabled": true, "weight": 0.9},
    "zhipu": {"enabled": true, "weight": 0.8},
    "deepseek": {"enabled": false},
    "qianwen": {"enabled": false},
    "doubao": {"enabled": false},
    "mita": {"enabled": false},
    "hunyuan": {"enabled": false},
    "xunfei": {"enabled": false}
  },
  "report": {
    "push_to_feishu": true,
    "feishu_webhook": "填入您的飞书群机器人地址"
  }
}
```

> **飞书Webhook获取方式**：飞书群设置 → 添加机器人 → 自定义机器人 → 复制Webhook地址。

## 环境变量（可选）

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `GEO_QUOTA_FILE` | `.geo_quota.json` | 配额文件路径（建议默认） |
| `GEO_API_KEY` | （空） | 专业版API密钥（购买后在 yk-global.com 获取） |
| `TAVILY_API_KEY` | （必填） | Tavily搜索API密钥（专业版用户需设置） |

如需自定义配额文件位置：
```bash
export GEO_QUOTA_FILE=/your/custom/path/.geo_quota.json
```

## AI分析功能

GEO AI原因分析默认使用本地分析框架。如需接入外部AI（如MiniMax），请编辑 `scripts/geo_analyzer.py`，找到 `AI_ENDPOINT` 字段填入您的AI接口地址。

## 开发进度

- [x] Phase 0: 技术验证（2026-04-15）
- [x] Phase 1: MVP开发
  - [x] geo_searcher.py - 核心爬虫模块
  - [x] geo_analyzer.py - AI原因分析
  - [x] geo_report.py - 报告生成
  - [x] geo_quota.py - 配额管理（免费版限制）
  - [x] SKILL.md - 本文档
- [x] Phase 2: 手工验证测试（2026-04-16 简单刀完成）
  - [x] 讯飞星火CSS选择器修复（textarea）
  - [x] 文心一言CSS选择器修复（div[contenteditable]）
  - [x] DeepSeek/千问登录墙处理（已禁用）
  - [x] 飞书Webhook配置
- [x] Phase 3: 代码完善
  - [x] xinhuo/xunfei合并（避免重复检测）
  - [x] 免费版配额系统（1品牌+3平台/月）
  - [x] SKILL.md状态同步
- [x] Phase 4: ClawHub上架（v1.0.0）
- [x] Phase 4 Update: 安全扫描修复（v1.0.1）
- [x] Phase 5: 专业版Tavily API架构（v1.0.2）

## 官网

[https://yk-global.com](https://yk-global.com)
