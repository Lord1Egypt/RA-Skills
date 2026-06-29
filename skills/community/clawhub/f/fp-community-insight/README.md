# fp_community_insight — 社区热点痛点分析 Skill（炼化版 v1.0）

一个可直接导入 GetClawHub 的 Skill，把 Agent-Reach 从机械圈社区（Reddit 17个subreddit + 专业论坛）抓回来的热帖数据，聚类成**热门话题、用户痛点、可直接做的内容选题、趋势信号**。

**这是"挖痛点 → 出内容 → 分发"流水线的源头** —— 它产出的选题直接喂给 YouTube 和 Blog 两个 Skill。

---

## 📦 文件库结构

```
fp-community-skill/
├── README.md                          ← 本文件
├── skill/
│   └── SKILL.md                       ← Skill 本体（导入这个）
├── examples/
│   └── example_community_insight.md   ← 真实样例（8条热帖→完整报告）
├── reference/
│   └── 输出质量checklist.md            ← 输出抽查清单
└── docs/
    └── 如何导入GetClawHub.md            ← 5分钟导入教程
```

---

## 🚀 怎么用（3 步）

1. **导入**：照 `docs/如何导入GetClawHub.md`，把 `skill/SKILL.md` 导入 GetClawHub。
2. **测试**：用 `examples/` 的输入跑一遍，对照看输出质量。
3. **接下游**：把输出的选题复制给 `fp_youtube_script` / `fp_blog_to_social`。

---

## 🔗 在工作流里的位置（这是源头）

```
周一：Agent-Reach 抓 Reddit 17个 + 论坛
          ↓
   本 Skill 分析 → 痛点 + 选题
          ├──→ fp_youtube_script   做视频脚本
          ├──→ fp_blog_to_social   做文章 + 四平台
          └──→ fp_facebook_pro_post 做 FB 科普
```

一条完整闭环：**社区挖痛点 → AI 出内容 → 多平台分发**。

---

## ✨ 输出四个模块

| 模块 | 内容 |
|------|------|
| ① 热门话题 Top5 | 把几百条帖聚类成5个话题，按热度排序 |
| ② 高频痛点 | 按"频率+情绪强度"排序，用用户口吻描述 |
| ③ 内容机会 | 3-5个具体选题，标注适合的下游 Skill ★ |
| ④ 趋势信号 | 新出现、讨论量上升的话题 |

最有价值的是 ③ —— 不是泛泛而谈，每个选题都像真标题，且标注了该喂给哪个 Skill。

---

## ⚠️ 内置合规标注（关键）

机械圈有些话题涉及合规风险，Skill 会**主动标注**：

- **DPF delete / EGR delete**：在美国删除排放后处理系统违法（EPA 法规）。
  Skill 产出的选题只会聚焦"清洗/维护/正确诊断"，并标注"（合规：只讲维护，不碰删除）"
- 破解 ECU、绕过安全系统等话题：同样只做诊断/维护方向

见 `examples/` 里 DPF 话题的实际处理方式。这部分漏了可能产出违规选题，所以导入时务必完整粘贴 System Prompt。

---

## 📝 关于运营 SOP

SKILL.md 预留三个占位区：
- `[重点品类]` —— 让选题往 FP 想主推的品类倾斜
- `[已做过的选题]` —— 避免重复
- `[禁区话题]` —— 运营指定不碰的话题

---

## ⚙️ 配置参数

| 参数 | 值 |
|------|-----|
| Model | claude-sonnet-4-6 |
| Temperature | 0.6 |
| Max Tokens | 2000 |

---

## 📥 输入数据从哪来

- **自动**：`fp-skills` 库里的 `fp_weekly_crawl.sh` 抓 Reddit/论坛，输出 jsonl
- **手动**：起步阶段可手动复制热帖标题+评论摘要

建议至少 20-30 条热帖再跑，聚类更准。
