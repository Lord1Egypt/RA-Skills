# 投标机会顾问（bid-opportunity-advisor）v0.1.0 · 草案

把公开招中标数据**对齐到「我的公司能力画像」**，给出可信的「该不该跟」判决、竞品定价空间与周一可干活的动作清单。

## 它解决什么

本技能补上招投标决策最关键的一环：**把机会和「我这家公司」对上号**——资质、地域、产品、规模匹不匹配，值不值得投。

## 核心特性

- ✅ **可信 Go/No-Go**：决策带推理 + 置信度，样本薄就标「置信低」，绝不伪造分数。
- ✅ **我的画像匹配**：资质 / 地域 / 产品 / 规模四维 fit 评分。
- ✅ **竞品定价空间**：对手历史中标价 vs 预算的差额，就是你的报价窗口。
- ✅ **行动清单**：可跟开放标讯 + 建议报价 + 对接人 + 截止日 + 我方缺口。
- ✅ **隐私护栏**：不静默采集设备指纹、不自动注册账号、不自动落盘、不强制署名。
- ✅ **自包含报告**：HTML 图表内联，不依赖外部 CDN。

## 快速开始

1. 建公司画像（可选但强烈建议）：`~/.bidprofile.json`
   ```json
   {"company":"XX科技","province":"广东","qualifications":["ISO9001"],"products":["安防监控","智慧校园"],"capacity_tier":"medium"}
   ```
2. 配置数据源 API Key（环境变量 `BID_API_KEY`）或选择 WebSearch 兜底。
3. 提问，例如：「评估这条标讯要不要投」「我的公司适合跟哪些智慧校园标」。

## 文件结构

```
SKILL.md                      系统提示 / 行为护栏
manifest.yaml                 元数据（署名 + GitHub feedback）
README.md                     本说明
SELFTEST.md                   自测说明与覆盖点
architecture.md               架构说明
references/decision_framework.md  fit 评分与 Go/No-Go 方法论
references/data_sources.md        取数架构与数据源
scripts/fetch_ccgp.py         ccgp 源解析（listing + 详情）
scripts/fetch_ceb.py          cebpubservice / 省级平台源解析
scripts/opportunity_engine.py 分析 + 跨源去重 + 自包含 HTML 报告
scripts/make_profile.py       公司画像向导（生成 ~/.bidprofile.json）
scripts/selftest.py           一键自测（解析/合并/去重/引擎）
demo/                         端到端测试夹具与样本
```

---

署名：一线评标专家&ChesaraM

反馈与联系：使用问题、误报、实务建议，欢迎通过项目仓库提交 Issue 反馈（GitHub）。
