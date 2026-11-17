# AGENTS.md — AI 技能说明书

本文件面向使用或扩展本技能的 AI 编码代理（以及接手的人类维护者）。人类读者请优先读 `README.md`。

技能：`ai-brain-learning-memory-pro`
一句话定位：ai-brain-learning-memory 的进阶工程版，面向 AI 开发者 / 认知科学爱好者 / agent 架构师。在基础版（概念+例子+速查）之上往工程化推一步：三层记忆的参考实现（Python）、与 agent-memory 工具集成、评测电池 memory_eval_battery.py 的跑法与 6 维解读、OWASP ASI06 记忆投毒防御的代码落地、复习四节点的自动化 rrule 配置、认知科学证据→工程决策映射。建议先读基础版再读本版。触发词：大脑学习记忆进阶、记忆系统实现、memory system design、记忆架构代码、agent-memory 集成、记忆评测电池、记忆投毒防御、ASI06、间隔重复实现、遗忘曲线代码、记忆溯源、reference implementation、学习记忆工程版、brain memory pro。

---

## 一、用途（Purpose）

本技能是 LGD/UIBC 治理理论技能体系的一员。调用入口为 `SKILL.md`：AI 代理应先读 `SKILL.md`，按其 frontmatter 的 `name`/`description` 判断是否适用，再按正文步骤执行。

## 二、文件约定（Directory conventions）

| 路径 | 用途 |
|---|---|
| `SKILL.md` | 主说明书：frontmatter + 触发条件 + 执行步骤（AI 调用入口） |
| `AGENTS.md` | 本文件：面向 AI 代理的说明书 |
| `README.md` | 面向人类的总览（如存在） |
| `llms.txt` | 面向 AI 的轻量索引（如存在） |
| `scripts/`、`assets/` 等 | 技能执行所需资源（按需） |

## 三、可改 / 不可改边界（Editable / non-editable boundary）

### 可以改
- 本技能自身的文档、脚本与配置；按主题新增资产并同步更新 `SKILL.md` 说明。

### 不可改（改动即视为合规偏差）
- **许可与署名声明**：LICENSE / 许可口径（保留所有权利）不得删除或弱化。
- **任何"文件即证据"类声明**：版本号、日期、权属、DOI、徽章来源。

> 代理若判断某项改动触及上述边界，默认停下来并在变更记录里显式提问。

## 四、给代理的行为准则（Agent rules of engagement）

- **先读后写**：改任何文件前先读原文件，理解既有约定。
- **最小改动**：只做被要求的改动，不顺手重构。
- **不做远端写操作**：不执行 `git push`、不调用远端发布接口；远端写入是人工步骤。
- **如实报告**：无法确认的事项标为 TODO，不要编造。

