# Breakthrough Thinking Skill

<p align="center">
  <a href="#中文">🇨🇳 中文</a> · <a href="#english">🇺🇸 English</a>
</p>

---

## 中文

### 这是什么？
`breakthrough-thinking` 是一个给 AI 用的“卡住即换框架”技能：
- 当用户说“换个思路 / 再想想 / 继续”时自动触发
- 当 AI 连续失败、反复微调却无进展时自动触发
- 每次只选一个思维框架，直接应用解决当前问题；不行就换下一个框架

### 使用方式
在对话中直接说：
- 换个思路
- 再想想
- 继续
- try another way

或当 AI 检测到卡住时，会自动调用。

### 核心流程
1. 用一句话总结当前死结
2. 从框架库中选 1 个最相关框架
3. 直接用该框架解决当前问题
4. 若未解决，立即切换到下一个框架

### 思维框架来自哪里？（名人原文示例）
下面是 6 个框架及经典原文（含中译）：

1. **Inversion（查理·芒格推广）**
   - Original: **"All I want to know is where I'm going to die, so I'll never go there."** — Charlie Munger
   - 中译：**“我只想知道我会死在哪里，这样我就永远不去那里。”**

2. **Occam’s Razor（威廉·奥卡姆）**
   - Original (Latin): **"Entities should not be multiplied beyond necessity."**
   - 中译：**“如无必要，勿增实体。”**（即：优先选择更简单解释）

3. **5 Whys（丰田体系）**
   - Original (Toyota principle): **"By repeating why five times, the nature of the problem as well as its solution becomes clear."**
   - 中译：**“把‘为什么’连续问五次，问题本质和解法会变清晰。”**

4. **First Principles（亚里士多德，现代由马斯克广泛传播）**
   - Original (Aristotle): **"A first principle is the first basis from which a thing is known."**
   - 中译：**“第一原理是事物得以被认识的最初基础。”**

5. **Bayesian Updating（托马斯·贝叶斯）**
   - Original (popular formulation): **"When the facts change, I change my mind."** *(Often cited in Bayesian contexts)*
   - 中译：**“当事实变化时，我就改变看法。”**（贝叶斯精神：根据新证据更新判断）

6. **PDCA（戴明推广）**
   - Original idea: **"Plan, Do, Check, Act."** — W. Edwards Deming (popularized cycle)
   - 中译：**“计划、执行、检查、处理（改进）。”**

### 仓库结构
```text
.
├── SKILL.md
├── README.md
└── references/
    └── mental-models.md
```

---

## English

### What is this?
`breakthrough-thinking` is a “switch-frame-when-stuck” skill for AI:
- Auto-triggers when users say things like “try another way / rethink / continue”
- Auto-triggers when AI is clearly stuck (repeated failures, no new evidence)
- Applies one mental model at a time; if it fails, switch to another model

### How to use
In chat, say:
- try another way
- rethink
- continue
- 换个思路

Or let it auto-trigger when stall signals are detected.

### Core loop
1. Summarize the dead-end in one sentence
2. Pick one relevant mental model
3. Apply that model directly to solve the current problem
4. If unsolved, switch to a different model immediately

### Where these frameworks come from (original quotes)
1. **Inversion (popularized by Charlie Munger)**
   - **"All I want to know is where I'm going to die, so I'll never go there."** — Charlie Munger

2. **Occam’s Razor (William of Ockham)**
   - **"Entities should not be multiplied beyond necessity."**

3. **5 Whys (Toyota Production System)**
   - **"By repeating why five times, the nature of the problem as well as its solution becomes clear."**

4. **First Principles (Aristotle, popularized in modern engineering circles)**
   - **"A first principle is the first basis from which a thing is known."**

5. **Bayesian Updating (Bayes spirit)**
   - **"When the facts change, I change my mind."** *(commonly cited in Bayesian discussions)*

6. **PDCA (Deming cycle)**
   - **"Plan, Do, Check, Act."**

### Repo structure
```text
.
├── SKILL.md
├── README.md
└── references/
    └── mental-models.md
```
