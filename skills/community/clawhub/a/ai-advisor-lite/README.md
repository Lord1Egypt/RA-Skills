# AI Advisor Lite（AI参谋 · 免费版）

**派活给 AI 之前，先问四句。** A lightweight, fully-offline skill that turns any task you delegate to AI into an expert-grade instruction — based on the "Four Questions" method from Felix Rieseberg (Claude engineering lead), battle-tested on real business tasks.

Most people prompt AI with "act like a 20-year expert" and get polished fluff back. The reason: you asked the model to *mimic* an expert's tone, but never required the expert's *methods*. This skill fixes the delegation step itself.

> 完整版（按 8 类任务定制的专家动作库 + 自动生成派活卡 + 对抗式审查链）在 SkillHub：**AI参谋（ai-advisor）**，单次 ¥1.00。本仓库是免费手动版。

---

## What it does / 它做什么

**输入**：你要派给 AI 的任务（一句话）。
**输出**：改写后的专家级派活指令。

Before you delegate a task to AI, this skill asks four questions and rewrites your task:

## The Four Questions / 四问

1. **Beyond the ask** — What would top experts in this field do that I never explicitly requested?
   这个领域的顶尖专家，会做哪些我没有提出要求的工作？
2. **Raw sources** — What *primary* materials would they start from, instead of pre-processed content?
   他们会从哪些最原始的材料入手，而不是用已经加工过的内容？
3. **Methods & tools** — What methods and tools would they actually use?
   他们具体会用哪些方法和工具？
4. **Independent proof** — Beyond our own judgment, what evidence can prove the result is right?
   除了你我判断，还有什么能独立证明结果是对的？

Then rewrite the task with those answers baked in. / 按答案改写任务后再派活。

## 名词 → 动词公式（The Verb Rewrite）

Turn any task *noun* into an outcome *verb*:

> **In X minutes, make [who] understand [what], and take [what action].**
> **在 X 时间内，让【谁】看懂【什么】，并采取【什么行动】。**

- ❌ "写一篇科普推文" → ✅ "30 分钟内让一个忙碌的矿老板看懂尾矿提金属的生意逻辑，并愿意转发给合伙人"
- ❌ "做个 PPT" → ✅ "15 分钟内让评委记住我们的三个数字并愿意问价"

## Delegation checklist / 派活自查清单

- [ ] **任务写成了动词** — 能用"让谁在什么时间内看懂什么并采取什么行动"一句话说出来
- [ ] **原始材料点名了** — 指令里明确要求用什么一手材料，禁止二手转述
- [ ] **方法写具体了** — 禁止"认真分析、深入研究"式空话
- [ ] **验证独立了** — 有独立于执行 AI 的验证方式（盲评 / 回源核对 / 第三方）
- [ ] **禁止事项写明了** — 不许编造、不许套模板、不许超范围

## Manual usage / 手动用法

把 `SKILL.md` 装进任何支持 Agent Skills 的客户端（WorkBuddy / Claude / Claw 等），或直接把四问贴进对话：

```
派活前先回答四问：
1. 顶尖专家会做哪些我没提出要求的工作？
2. 用什么最原始的材料（不用已加工内容）？
3. 用什么具体方法和工具？
4. 除你我判断外，什么能独立证明结果对？
→ 按答案改写任务 → 执行。
```

---

## Lite vs Full / 免费版 vs 完整版

| | Lite（本仓库，免费） | Full（SkillHub，¥1.00/次） |
|---|---|---|
| 四问框架 + 名词改动词公式 | ✅ | ✅ |
| 手动自查清单 | ✅ | ✅ |
| **8 类任务定制专家动作库**（方案/报告/推文/PPT/代码/合同/分析/通用，120+ 条） | ❌ | ✅ |
| **自动生成完整派活卡**（可直接复制执行，含材料要求/方法要求/验证要求） | ❌ 手动改写 | ✅ 自动 |
| **对抗式审查链**（主稿→挑错→裁判三段指令） | ❌ | ✅ |
| 免费骨架诊断 + 付费定制执行分层 | ❌ | ✅ |

Lite 给你"知道该怎么想"；Full 替你"执行到位"。就像体检表人人能看，诊断书要医生出。

## Attribution / 方法论来源

The Four Questions method is popularized by Felix Rieseberg's *How to be more ambitious: A tutorial for humans with models* (2026). The task-type action library, verb-rewrite cards, and adversarial review chain in the full version are original work battle-tested on mining/engineering/business tasks.

## License / 版权

专有版权 · 保留所有权利。免费版可自由使用与转发，禁止拆分用于商业竞品。Full version © 广西冠宁建材有限公司.
