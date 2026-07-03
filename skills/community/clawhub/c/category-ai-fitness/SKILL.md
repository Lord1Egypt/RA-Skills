---
name: category-ai-fitness
description: "输入三级类目表 → 自动抓取 Amazon/Walmart TOP 商品主图 → Claude 多模态分析 → 输出类目级决策表（AI改图适配度、侵权风险、经济性、竞争度）。触发词：类目分析、场景化适配、改图评估、类目筛选、搬运决策。"
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["python3"],"env":["LINKFOXAGENT_API_KEY","ANTHROPIC_API_KEY"]}}}
---

# 类目 AI 改图适配度分析器

输入三级类目表格，自动抓取双平台 TOP 商品数据 + 主图，用 Claude 多模态视觉分析，输出类目级综合决策报告。

## 用法

### 🚀 Streamlit Web UI（推荐）

```bash
cd ~/.openclaw/workspace/skills/category-ai-fitness
streamlit run app.py
```

启动后浏览器访问 `http://localhost:8501`，上传类目 Excel 文件，点击开始分析即可。

### CLI 命令行

```bash
cd ~/.openclaw/workspace/skills/category-ai-fitness/scripts

# 基本用法：输入类目 Excel
python3 main.py --input categories.xlsx

# 指定输出路径
python3 main.py --input categories.xlsx --output ../output/report_20260529.xlsx

# 只跑 Amazon（跳过 Walmart）
python3 main.py --input categories.xlsx --amazon-only

# 只跑 Walmart
python3 main.py --input categories.xlsx --walmart-only

# 指定每类目抓取数量（默认 10）
python3 main.py --input categories.xlsx --top-n 15
```

## 输入格式

Excel 或 CSV，至少包含一列「类目」，支持以下格式混合：
- Amazon BSR URon.com/Best-Sellers-Home-Kitchen/zgbs/home-garden`
- Amazon 类目路径：`Home & Kitchen > Bedding > Sheets`
- Walmart URL：`https://www.walmart.com/cp/home/4044`
- Walmart 类目路径：`Home > Bedroom > Sheets`
- 纯关键词：`yoga mat`（自动双平台搜索）

脚本自动识别平台和格式，无需手动标注。

## 输出 Excel 字段

| 分组 | 字段 | 说明 |
|------|------|------|
| 基础 | 类目路径、平台、样本数、抓取时间 | 标识 |
| 改图核心 | 场景化适配度 (0-100) | TOP 主图场景图占比 + 商品形态 |
| | AI 改图难度（低/中/高） | 透明/反光/人物/复杂细节 |
| | 推荐改图策略 | 全场景化 / 主图白底+副图场景 / 不改 |
| 侵权风险 | 图片侵权风险（🔴🟡🟢） | 品牌物/水印/通用图占比 |
| | 必须改图标记 | 通用图/品牌素材命中即 ✅ |
| 经济性 | 价格中位数、月销中位数 | 抓取数据聚合 |
| | 估算毛利率 | WFS 费率公式 |
| 竞争 | 卖家密度 | 红海/蓝海标签 |
| 决策 | 决策档位 | ✅AI改图搬 / ✅白底直搬 / ⚠️谨慎 / ❌弃 |
| | 决策理由 | 一句话说明 |
| 参考图 | 代表主图×3 | 缩略图嵌入 Excel |

## 环境变量

| 变量 | 用途 | 是否必须 |
|------|------|----------|
| `LINKFOXAGENT_API_KEY` | Amazon/Walmart 数据抓取（LinkFox API） | ✅ 必须 |
| `ANTHROPIC_API_KEY` | Claude 多模态视觉分析 | ✅ 必须 |
| `ANTHROPIC_AUTH_TOKEN` | 同上（二选一） | 可选 |
| `ANTHROPIC_BASE_URL` | 自定义 Claude API 地址 | 可选 |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | 自定义 Haiku 模型名称 | 可选 |

## 依赖

```bash
pip install -r requirements.txt
# 或手动安装
pip install anthropic openpyxl pillow requests pandas streamlit
```
