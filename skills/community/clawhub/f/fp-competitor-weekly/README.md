# fp_competitor_weekly — 竞品周报生成 Skill（炼化版 v1.0）

一个可直接导入 GetClawHub 的 Skill，把两个来源的竞品数据（**Socialinsider 付费** + **Agent-Reach 免费的 YouTube**）合并成一份有洞察的运营周报。

**核心特点：不念数据，从数据里读出结论 + 给可落地建议。**

---

## 📦 文件库结构

```
fp-competitor-skill/
├── README.md                          ← 本文件
├── skill/
│   └── SKILL.md                       ← Skill 本体（导入这个）
├── examples/
│   └── example_competitor_weekly.md   ← 真实样例（两份数据→完整周报）
├── reference/
│   └── 输出质量checklist.md            ← 输出抽查清单
└── docs/
    └── 如何导入GetClawHub.md            ← 5分钟导入教程
```

---

## 🚀 怎么用（3 步）

1. **导入**：照 `docs/如何导入GetClawHub.md`，把 `skill/SKILL.md` 导入 GetClawHub。
2. **测试**：用 `examples/` 的两份数据跑一遍，对照看周报质量。
3. **验证**：用 `reference/输出质量checklist.md` 抽查，重点看有没有读出结论。

---

## 🔗 在工作流里的位置（竞品追踪线的终点）

```
Socialinsider（IG/TT/FB 9竞品）──┐
                                 ├→ 本 Skill → 竞品周报 → 周二选题会
Agent-Reach（竞品 YouTube）  ────┘
```

组合方案：IG/TikTok/Facebook 用 Socialinsider 付费买稳定，YouTube 用 Agent-Reach 免费抓，本 Skill 把两边合并成一份报告。

---

## ✨ 关键设计：读结论，不念数据

普通"数据汇总"会把每个数字念一遍。这个 Skill 不一样：

| 普通汇总 | 本 Skill |
|---------|---------|
| "brokentractorllc TikTok 12.4K粉，+3100" | "增长几乎全集中在 TikTok，FB 普遍停滞" |
| 列出每条 Top 内容 | "修复改造连载是本周最强形式" |
| "互动率 11.2%、7.8%、5.2%…" | "FB 全员低于 1.2%，TikTok 是高互动主战场" |
| —— | 给出 3 条可落地建议（做修复连载/改before-after/FB别投入） |

见 `examples/` 里的实际输出。

---

## 📥 输入：两份数据

| 来源 | 内容 | 怎么拿 |
|------|------|--------|
| A. Socialinsider | IG/TT/FB 9竞品（粉丝/互动率/Top posts） | 每周一导出 CSV |
| B. Agent-Reach | 竞品 YouTube（播放/点赞） | 跑爬虫脚本 |

两份都粘进 Skill，它会合并分析（不割裂）。

---

## 📝 关于运营 SOP

SKILL.md 预留三个占位区：
- `[FridayParts 自己的数据]` —— 想把 FP 自己数据放进来对比就填
- `[重点关注的竞品]` —— 最想盯的1-2家
- `[关注的指标偏好]` —— 最在意哪些指标

---

## ⚙️ 配置参数

| 参数 | 值 |
|------|-----|
| Model | claude-sonnet-4-6 |
| Temperature | 0.5（数据分析要稳定准确） |
| Max Tokens | 2000 |

---

## 这条线之外

内容生产闭环（社区分析→YouTube脚本→四平台）是另一条线，在 `fp-content-pipeline` 总库里。本 Skill 属于竞品追踪线，输出的爆款形式和平台结论可以反哺内容线的选题。
