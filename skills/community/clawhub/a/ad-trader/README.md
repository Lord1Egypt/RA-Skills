# 🎯 AI广告投手 (Ad Trader)

> AI驱动的广告投放全流程管理助手，帮你从"手动盯盘"进化到"AI指挥作战"。

一个 WorkBuddy Skill，专为广告优化师/投放人员设计，覆盖 **数据导入 → 投放分析 → 预算优化 → 素材诊断 → 智能报表 → 异常告警** 六大阶段。

## ✨ 核心能力

| 模块 | 功能 | 说明 |
|------|------|------|
| 📥 数据管理 | CSV/Excel/JSON导入 | 多平台数据格式自动识别和标准化 |
| 📊 投放分析 | KPI计算、异常检测、趋势分析 | CTR/CVR/CPA/ROAS/ROI多维度诊断 |
| 💰 预算优化 | 出价建议、预算分配 | 532法则智能预算优化建议 |
| 🎨 素材诊断 | 素材疲劳度、A/B分析 | 识别素材衰减、推荐优胜素材 |
| 📈 智能报表 | HTML可视化报告 | 日报/周报/月报一键生成 |
| 🚨 异常告警 | 消耗异常、效果暴跌 | 自动检测预算泄漏和效果异常 |

## 🚀 快速开始

### 1. 准备数据

支持 CSV / Excel / JSON 三种格式，列名自动识别（中英文、各平台命名均可）。

标准字段：
- `日期` / `date`
- `计划名称` / `campaign`
- `素材名称` / `creative`
- `展现量` / `impressions`
- `点击量` / `clicks`
- `消耗` / `cost` / `spend`
- `转化量` / `conversions`
- `成交额` / `revenue` / `gmv`

### 2. 使用

在 WorkBuddy 对话中直接说：
- "帮我导入广告数据 [文件路径]"
- "分析一下我的投放数据"
- "生成日报"
- "预算怎么优化？"
- "看看哪些素材疲劳了"

### 3. CLI 命令

```bash
# 导入数据并查看概览
python scripts/cli.py import 广告数据.csv

# 快速分析（摘要+异常+趋势）
python scripts/cli.py analyze 广告数据.csv

# 综合诊断（健康评分+问题清单）
python scripts/cli.py diagnose 广告数据.csv

# 预算分配建议
python scripts/cli.py budget 广告数据.csv

# 素材分析
python scripts/cli.py creative 广告数据.csv

# 全方位优化建议
python scripts/cli.py optimize 广告数据.csv

# 生成可视化HTML报告
python scripts/cli.py report 广告数据.csv --type diagnose

# A/B测试对比
python scripts/cli.py compare 广告数据.csv 素材A 素材B
```

## 📊 核心指标

| 指标 | 含义 | 计算公式 |
|------|------|----------|
| CTR | 点击率 | 点击 / 曝光 |
| CVR | 转化率 | 转化 / 点击 |
| CPC | 点击成本 | 消耗 / 点击 |
| CPM | 千次曝光成本 | 消耗 / 曝光 × 1000 |
| CPA | 获客成本 | 消耗 / 转化 |
| ROAS | 广告支出回报 | 收入 / 消耗 |
| ROI | 投资回报 | (收入-成本) / 成本 |

## 🏗️ 技能结构

```
ad-trader/
├── SKILL.md                    # 技能定义（触发词、能力说明）
├── README.md                   # 本文件
├── scripts/
│   ├── data_manager.py         # 数据导入、清洗、标准化
│   ├── performance.py          # 诊断引擎（健康评分/异常/趋势/排行榜）
│   ├── optimizer.py            # 优化引擎（预算/出价/素材/AB测试）
│   ├── report.py               # HTML报表生成（Chart.js可视化）
│   └── cli.py                  # 统一CLI入口
├── references/
│   ├── metrics.md              # 广告指标体系详解+行业基准
│   ├── platforms.md            # 5大广告平台特性对比
│   └── strategies.md           # 投放优化最佳实践
└── templates/                  # 报告模板目录
```

## 🎯 支持平台

自动识别以下平台导出数据：

- **腾讯广告** (Tencent Ads)
- **巨量引擎** (Ocean Engine)
- **百度推广** (Baidu Ads)
- **Meta Ads** (Facebook/Instagram)
- **Google Ads**

> 无法识别时按通用格式解析，列名自动映射。

## 📈 报告类型

| 类型 | 命令参数 | 适用场景 |
|------|----------|----------|
| 日报 | `--type daily` | 每日快速复盘 |
| 周报 | `--type weekly` | 每周趋势分析 |
| 月报 | `--type monthly` | 月度深度复盘 |
| 综合诊断 | `--type diagnose` | 全面健康检查 |

报告为交互式 HTML，内置 Chart.js 图表，包含：健康评分仪表盘、KPI卡片、趋势图、异常告警、预算分配建议、计划排行榜、素材诊断、优化建议卡片。

## 🧠 优化策略内置

- **532预算分配法**：50%优质计划 + 30%潜力计划 + 20%测试计划
- **出价决策矩阵**：基于ROAS+转化量自动给出加量/维持/观望/关停建议
- **素材疲劳度模型**：综合CTR衰减、在线天数、ROAS表现评分
- **5类异常检测**：CPA突增、CTR骤降、ROAS下滑、消耗异常、无转化

## 📝 配置

可通过 `ad_trader_config.json` 自定义告警阈值：

```json
{
  "platform": "auto",
  "currency": "CNY",
  "alert_thresholds": {
    "cpa_spike_pct": 50,
    "ctr_drop_pct": 30,
    "budget_burn_rate": 0.8
  },
  "report_type": "daily"
}
```

## 🔧 依赖

- Python 3.8+
- 读取 Excel 需要 `openpyxl`（`pip install openpyxl`）
- 报告图表使用 CDN 加载的 Chart.js，无需本地安装

## 📜 License

MIT

## 🤖 关于

这是一个 [WorkBuddy](https://codebuddy.cn) Skill。

- 作者：bettermen
- 版本：1.0.0
- 触发词：广告投手、投放分析、广告优化、ROI分析、素材分析、广告报表、投放诊断、预算优化
