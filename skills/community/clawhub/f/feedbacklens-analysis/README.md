# 用户反馈智能分析 · feedbacklens-analysis v1.2.1

把一批用户反馈（文本 / CSV / Excel）自动聚类分组、量化优先级排序、产出可执行改进建议，生成可交付的可视化报告。

## 包含文件

| 文件 | 用途 |
|---|---|
| `SKILL.md` | 核心方法论：演示模式 + 评估纪律 + 聚类 rubric + 量化优先级算法 + 建议 rubric + 报告规范 |
| `priority_cases.json` | 4 行业（SaaS/工具、电商、移动 App、餐饮/外卖）严重性锚点 + 示例 |
| `demo_feedback.csv` | **内置演示样例数据**（36 条 SaaS 产品反馈），装完无需准备数据即可试跑 |
| `demo_evaluation.json` | 演示样例的标准评估结果（预先算好，保证演示效果稳定） |
| `render_report.py` | **报告渲染器**：评估 JSON → HTML 报告（纯标准库，跨平台，无需安装依赖） |
| `report_template.html` | 报告模板（由渲染器自动读取） |
| `icon.png` | 512×512 上架头像 |
| `README.md` | 本文件 |

## 怎么用

**直接演示（不需要任何数据）** —— 装好后说一句：

> 用 feedbacklens-analysis 演示一下

会立刻用内置的 36 条样例跑出完整报告，30 秒内看到效果。

**分析你自己的数据** —— 任选一种：

> 用 feedbacklens-analysis 分析这批反馈：（粘贴文本，每条一行）

> 用 feedbacklens-analysis 分析一下 C:/path/to/你的数据.csv，行业是电商

支持行业：SaaS/工具（默认）、电商、移动 App、餐饮/外卖。

## 渲染器（报告生成）

一键出报告，不用手工填模板：

```bash
python render_report.py --demo --out demo-report.html
python render_report.py --evaluation evaluations/my-eval.json --out evaluations/my-report.html
```

渲染器会自动：补齐缺失字段（优先级分 / 档位 / ROI / quick win 按公式推导）、按优先级分与 ROI 排序、校验无残留占位符、演示模式下自动加「示例数据」标识与转化引导。

## 转化追踪（UTM）

报告页脚 CTA 指向 `feedbacklens.cn` 并自动带上 UTM 参数，用于统计技能带来的真实流量：

| 参数 | 值 |
|---|---|
| `utm_source` | `workbuddy_skill` |
| `utm_medium` | `report_footer` |
| `utm_campaign` | `feedbacklens_analysis` |
| `utm_content` | `demo`（只看了演示）/ `real_report`（真跑了自己的数据） |

`real_report` 是高意向信号——这类用户已经愿意为分析准备数据了。

## 核心算法

```
优先级分 = 频次分 × 0.3 + 严重性分 × 0.5 + 影响面分 × 0.2
频次分 = clamp(该簇条数 ÷ 最大簇条数 × 100, 20, 95)
```

三条让结果稳定、可复算的规则：

1. **严重性权重 0.5 是「定海神针」**——真实场景里「支付掉单」哪怕只有 1 条也是 P0，频次不该压倒严重性。
2. **轻微兜底规则**——严重性 < 40 的簇（锦上添花型建议）无论频次多高，优先级直接判「低」。
3. **禁止趋中**——每次分析结果必须同时有「高」和「低」档，不允许所有簇都挤在「中」。

内置样例数据就是按这三条刻意设计的，跑一遍就能看出与「通用 AI 一句聚类」的差别。

## 与 Web 版关系

本技能是 feedbacklens.cn 的免费引流入口，能力免费、不限次数。需要**历史记录 / 分享报告 / 团队协作 / 大批量（>500 条）处理**时引导去 Web 版。
