# 大道至简 Skill · Principled Simplicity

<p align="center">
  <img src="./assets/hero.webp" alt="大道至简 Principled Simplicity 头图：面向 AI Agent 系统的架构修复方法，修问题，更要修层级（Fix the layer, not the case.）；Pattern、Owner Layer、Mechanism、Eval" width="100%">
</p>

**Fix the layer, not the case.**

来自真实 AI / Agent 工程实践的机制层修复 Skill，适用于AI Agent runtime/harness的开发修复。

这是一个 Agent Skill（[`SKILL.md`](SKILL.md)）：把反复出现的失败追溯到根因，并定位真正应该承接修复的那一层。可用于 Claude Code、Codex 或其他支持 Skill / 系统指令注入的 Agent 工作流；安装命令：`npx skills add Longfellow1/Principled-Simplicity-skill --skill deep-fix`。

核心回答的问题是：**这个问题为什么反复出现，真正应该在哪一层解决？**

[English](README.en.md) · [SKILL.md](SKILL.md) · [Examples](examples/) · [References](references/)

---

## 一键安装

遇到重复 badcase、Prompt 膨胀或 Agent 路由问题？用机制层修复代替不断叠加补丁。

```bash
npx skills add Longfellow1/Principled-Simplicity-skill --skill deep-fix
```

> Skill ID：`deep-fix`（与 GitHub 仓库名不同）。需要 Node.js/npm；CLI 直接从 GitHub 安装，无需发布 npm 包。

[![skills.sh 上的 Principled-Simplicity-skill 页面](https://skills.sh/b/Longfellow1/Principled-Simplicity-skill)](https://skills.sh/Longfellow1/Principled-Simplicity-skill)

**安装后试试：** “Agent 总选错工具，已经加了三次 Prompt 规则。请分析根因，并提出可回归验证的机制级修复方案。”


## 为什么需要它

AI 系统最容易进入一种看似高效、实际原地打转的状态：

- 一个 badcase → 加一句 Prompt
- 再来一个 → 加关键词
- 路由又错 → 加 if/else
- 多轮失败 → 再补一个规则
- 修了 A，B 又坏了

单个修复都“有效”，系统却越来越难理解、难验证、难维护，直到彻底失去可拓展性。

**大道至简关注的不是补丁写得多快，而是能否找到足够稳定的机制，一次解决一类问题。**

> **好的修复让系统忘记这件事，而不是记住更多例外。**

---

## 一个典型例子

### 输入

> Agent 又选错工具了。上次加了关键词规则，这次用户换了个说法又走错了。要不要再补几个 trigger？

### 它不会先给你新的关键词列表

它会先问四件事：

```text
1. 这个问题出现过几次？
2. 处理逻辑散落在几个地方？
3. 有没有客观 eval 可以判断“修好了”？
4. 上次修复是否让别的地方变差？
```

如果同类错误已经反复出现、判断逻辑开始扩散，问题就不再是某句话没覆盖，而更可能是 **Routing / System Boundary** 层缺少正确机制。

更合理的方向会变成：

```text
关键词补丁
    ↓
意图 / 工具选择契约
    ↓
稳定 Router
    ↓
Verifier
    ↓
正例 + 反例 + 边界例回归
```

目标不是让这一句话通过，而是让**同一类表达变化不再击穿系统**。

→ [完整示例：Architecture Whack-a-Mole](examples/architecture-whack-a-mole.md)

---

## 核心工作方式

```text
case → pattern → mechanism → reusable skill/module → evaluation loop
单点    共性      机制           可复用能力                  评测闭环
```

### 1. 先判断是不是值得升维

不是所有 bug 都值得抽象。

| 信号 | 判断 |
|---|---|
| 第一次出现、影响孤立 | 可以先 case fix |
| 同类问题反复出现 | 找 pattern |
| 同一逻辑散落多处 | 检查系统边界 |
| 改了只能“感觉更好” | 先补 eval |
| 连续多次修复失败 | 强制架构审查 |

**过早抽象本身也是反模式。**

### 2. 找真正失败的层

| Failure Type | 典型信号 |
|---|---|
| **Semantic** | 同一意图表达变化，规则枚举不完 |
| **Context** | 单轮正常，多轮 / 跨会话失败 |
| **Routing** | 工具或模式选错，依赖表层词命中 |
| **System Boundary** | 同一逻辑散落多处，Prompt 承担了代码职责 |
| **Evaluation** | 改了很多次，却没有客观判据 |

### 3. 选择最合适的抽象层级

```text
case fix
pattern rule
mechanism
module
skill
harness
migration path
```

不是“抽象越高越好”，而是**把复杂度放到真正应该拥有它的那一层**。

---

## 什么时候用

### Prompt 越修越长

> “每来一个 badcase 都在 System Prompt 里补一句，现在已经没人敢删。”

→ 检查是否应该拆成状态、Router、Verifier、Context Builder 或代码约束。

### Agent 总是选错工具

> “加了十几个关键词 trigger，换个说法还是会错。”

→ 从表层规则回到 Routing 机制与 eval。

### 同一规则散落在多个模块

> “同一个判断，Prompt、后端和 Tool 里各有一份。”

→ 优先检查 System Boundary，而不是继续同步三份补丁。

### 不知道该用规则还是模型

> “这个判断应该 if/else，还是再调一次 LLM？”

→ 根据边界稳定性、错误代价、可枚举性和评测条件决定抽象层级。

---

## 什么时候不要用

- 真正的一次性 edge case
- 明确接受技术债的临时 Demo
- 第一次出现、尚无重复信号的问题
- 单纯审美 / 风格调整

大道至简不是“凡事都重构”。**不必要的抽象，与不必要的补丁一样，都是复杂度。**

---

## 使用

```bash
npx skills add Longfellow1/Principled-Simplicity-skill --skill deep-fix

# Optional: clone the full source repository
git clone https://github.com/Longfellow1/Principled-Simplicity-skill.git
cd Principled-Simplicity-skill
```

核心 Skill 文件是 [`SKILL.md`](SKILL.md)。可用于 Claude Code、Codex 或其他支持 Skill / 系统指令注入的 Agent 工作流。

代码库问题还可以使用扫描脚本补充客观证据：

```bash
python references/deep-fix-scan.py /path/to/project
```

脚本负责观察，Skill 负责判断。

仓库结构：

```text
Principled-Simplicity-skill/
├── SKILL.md
├── README.md
├── README.en.md
├── assets/
│   └── hero.webp            # README 头图
├── references/
│   ├── patterns.md
│   ├── procedure.md
│   ├── heuristics.md
│   ├── abstraction-readiness.md
│   ├── prompt-decompose.md
│   ├── patch-audit.md
│   └── deep-fix-scan.py
└── examples/
    ├── architecture-whack-a-mole.md
    └── eval-blindspot.md
```

---

## 方法来源

**大道至简 / Principled Simplicity 是从真实 AI / Agent 工程实践中总结出来的方法。**

它关注的是一个反复出现的工程事实：当 Prompt、规则、路由、上下文和状态开始彼此补洞时，继续修 case 往往只是在转移复杂度。

这里的“简”不是追求代码少、规则少，也不是为了架构漂亮；而是：

> **找到正确的抽象以后，让不必要的特殊处理失去存在的理由。**

---

## 相关 Skill

如果问题还没进入工程阶段，真正需要先判断的是“这个需求到底该不该做”，可以使用：

**[产品判断 · Product Judgment](https://github.com/Longfellow1/Product-Judgment-skill)**  
*先判断需求，再写 PRD。*

---

## License

[Apache-2.0](LICENSE)

---

作者的其他项目：[KeyPulse](https://github.com/Longfellow1/keypulse)（面向 AI Agent 的本地记忆层，经 MCP 提供）· [CorpusFlow](https://github.com/Longfellow1/CorpusFlow)（面向 LLM 微调 / 评测数据的语料工作台）
