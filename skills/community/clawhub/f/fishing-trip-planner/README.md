# 🎣 Fishing Trip Planner

AI 钓鱼行程规划工具 — 输入出发地、目的地、钓鱼时间、出行方式，自动生成完整钓鱼行程规划报告。

[![Version](https://img.shields.io/badge/version-2.0-blue)](https://github.com/bettermen/fishing-trip-planner)
[![Python](https://img.shields.io/badge/python-3.9+-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT--0-orange)](LICENSE)

## ✨ 功能

- 🗺️ **路线规划** — 高德地图 API，支持驾车/步行/公交/骑行
- 🌤️ **天气预报** — 和风天气 API，7天预报 + 逐小时
- 🌊 **潮汐数据** — 满潮/干潮时间、潮高曲线
- 📊 **综合评分** — 风力/温度/降水/潮汐四维打分 (0-100)
- 📝 **HTML 报告** — 深色海洋风格、评分圆盘、条件评估表
- 💾 **历史存档** — 每次规划自动保存，支持回顾对比
- ⚙️ **配置向导** — `--setup` 一键配置 API Key

## 🚀 快速开始

```bash
# 1. 首次配置
python scripts/fishing_planner.py --setup

# 2. 生成规划
python scripts/fishing_planner.py \
  -o "深圳南山" \
  -d "惠州巽寮湾" \
  -t "2026-06-15" \
  -m driving

# 3. 查看历史
python scripts/fishing_planner.py --history
python scripts/fishing_planner.py --view 1
```

## 📦 安装

```bash
git clone https://github.com/bettermen/fishing-trip-planner.git
cd fishing-trip-planner
pip install requests
```

## 🔑 API 申请

| 服务 | 用途 | 申请地址 | 免费额度 |
|------|------|---------|---------|
| 高德地图 | 路线规划 | https://lbs.amap.com/ | 5000次/天 |
| 和风天气 | 天气+潮汐 | https://dev.qweather.com/ | 1000次/天 |

## 📊 报告预览

![Report Preview](https://img.shields.io/badge/preview-dark%20ocean%20theme-blue)

生成的 HTML 报告包含：
- 🎯 综合评分盘 (0-100分 + 四级评级)
- 📍 路线总览 (距离/耗时/过路费/导航步骤)
- 🌤️ 7天天气卡片 + 逐小时天气表
- 🌊 潮汐预报 (满潮/干潮时间)
- 📊 钓鱼条件评估 (风力/温度/降水/潮汐)
- 💡 智能钓鱼建议 + 装备清单

## 🏗️ 技术栈

- **Python 3.9+**
- **requests** — HTTP API 调用
- **高德地图 Web API v3/v4** — 地理编码 + 路线规划
- **和风天气 API v7** — 天气 + 潮汐 + 钓鱼指数
- **纯 HTML/CSS** — 无框架依赖的报告模板

## 📁 项目结构

```
fishing-trip-planner/
├── SKILL.md                    # Skill 元数据
├── scripts/
│   └── fishing_planner.py      # 核心脚本 (~800行)
└── references/
    └── api_guide.md             # API 配置指南
```

## 📄 License

MIT-0
