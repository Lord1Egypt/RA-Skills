---
name: book-review
slug: book-review-skill
version: 1.1.1
description: "Generate in-depth book reviews from reading notes — expansion, key takeaways, related concepts. Pure local processing: no external APIs, no filesystem access, no secrets required. Use when you want to turn a snippet of reading insight into a structured book review."
---

# Book Review Skill (Safe Version)

Expand reading insights into in-depth book reviews using **local templates only**. No external calls, no data leaves your machine.

## 🚀 First-Success Path (30秒上手)

直接粘贴你的读书笔记，生成一篇完整书评：

```
/book-review 今天我读了《原子习惯》中关于身份驱动的习惯养成
→ 生成：书籍总结 + 核心原则 + 个人感悟 + 行动建议
```

三步即用：贴笔记 → 选格式（简评/详评/概念关联）→ 获取书评。

## Sample Prompts（输入→输出示例）

### Sample 1: 详细书评

**用户输入：**
```
/book-review 《思考，快与慢》中关于系统1和系统2的论述让我印象深刻，特别是系统1的启发式偏差如何影响日常判断。作者通过大量实验说明人在直觉决策中的系统性错误。
```

**Expected Output：**
> 📖 书评：《思考，快与慢》
> ---------
> **📌 核心观点**
> 人类思维分为两个系统：系统1（快速、直觉、自动）和系统2（缓慢、理性、费力）。虽然我们通常认为自己是理性思考者，但实际上大部分决策由系统1驱动。
>
> **🔑 关键洞见**
> - 系统1的启发式偏差是设计好的认知捷径，但在复杂情境下会导致系统性错误
> - "确认偏误"——我们倾向于寻找支持已有观点的信息
> - "可得性启发"——容易想起的例子被误认为更常见
> - 系统2的懒惰意味着多数人不会主动质疑系统1的判断
>
> **💭 个人感悟**
> 这本书的价值不仅是认知心理学知识，更是对自我决策过程的一次"代码审查"。理解这些偏差后，在高风险决策中主动调用系统2成为一种习惯。
>
> **🎯 行动建议**
> 1. 重大决策前强制停顿30秒，给系统2介入机会
> 2. 记录决策日志，追踪自己是否陷入常见偏差
> 3. 寻找"魔鬼代言人"角色，主动挑战自己的判断

### Sample 2: 简短书评

**用户输入：**
```
/book-review-brief 《刻意练习》的核心在于"有目的的练习"而非单纯重复，这打破了我对一万小时定律的理解
```

**Expected Output：**
> 📝 简评：《刻意练习》
> ---------
> **一句话：** 优秀的不是一万小时，而是每一小时都在有意识地突破舒适区。
>
> **三个要点：**
> 1. 刻意练习 ≠ 简单重复 — 需要明确目标+即时反馈+逐步提升难度
> 2. 心理表征是关键 — 专家与新手最大的区别在于心智模型的质量
> 3. 没有"天赋"只有"练对" — 正确的方法比时间投入更重要
>
> **适合人群：** 想在任何领域精进的实践者

### Sample 3: 概念关联

**用户输入：**
```
/book-review-related 《原子习惯》中的习惯叠加策略与《掌控习惯》中的两分钟法则
```

**Expected Output：**
> 🔗 概念关联
> ---------
> **核心主题：习惯建立的微观机制**
>
> | 概念 | 来源 | 核心观点 | 两者关系 |
> |------|------|---------|---------|
> | 习惯叠加 | 《原子习惯》 | 将新习惯绑定在已有习惯之后 | ⬅️ 行为触发策略 |
> | 两分钟法则 | 《掌控习惯》 | 新习惯前两分钟要极度简单 | ⬅️ 降低启动门槛 |
>
> **整合应用：**
> 1. 找到已有习惯（如"每天早上泡咖啡"）
> 2. 绑定新习惯的"两分钟版本"（如"泡咖啡后立即阅读一页书"）
> 3. 两分钟后可以停也可以继续
>
> **关联推荐：** 《Deep Work》《The Power of Habit》

### Sample 4: 多本书对比

**用户输入：**
```
/book-review 对比《深度工作》和《心流》，两者都谈论专注，但角度有何不同
```

**Expected Output：**
> 📖 双重书评：《深度工作》vs《心流》
> ---------
> **共同目标：** 如何达到最佳的认知状态
>
> **关键差异：**
> - 《深度工作》更偏向"环境设计"——隔绝干扰、建立仪式、管理注意力资源
> - 《心流》更偏向"内在体验"——挑战与技能匹配、即时反馈、自我意识消失
>
> **互补之处：** 深度工作是进入心流的必要条件，心流是深度工作的最佳状态。两者结合 = 最优工作体验。
>
> **行动建议：** 使用深度工作的方法论为心流创造环境条件。

### Sample 5: 技术类书籍笔记扩展

**用户输入：**
```
/book-review 《系统设计面试》中关于一致性哈希的设计要点很有用，尤其是虚拟节点如何解决分布不均的问题
```

**Expected Output：**
> 📖 书评：《系统设计面试》
> ---------
> **📌 核心概念**
> 一致性哈希 (Consistent Hashing) 解决了传统哈希取模在节点增减时需要大规模数据迁移的问题。
>
> **🔑 技术要点**
> - 哈希环（Hash Ring）的概念：将节点和数据都映射到一个环上
> - 虚拟节点：每个物理节点对应多个虚拟节点，解决哈希分布不均
> - 节点增减时只影响相邻节点数据，最小化重分布
>
> **💡 实践价值**
> 在分布式缓存（如Redis集群）、CDN、负载均衡中广泛应用。理解这一设计对后端架构设计至关重要。
>
> **📚 相关概念**
> 一致性哈希 → 分片(sharding) → 分布式系统 → CAP理论

## Features

- 📖 **Insight Expansion**: Expand short reading notes into in-depth book reviews
- 🔒 **Local Processing**: All templates processed locally with no external dependencies
- 📋 **Multiple Formats**: Brief, detailed, and comprehensive review options
- 💡 **Related Concepts**: Get suggested related learning concepts

## Review Integrity Workflow

This skill expands user-provided reading notes. It must not pretend to have read pages that were not supplied in the prompt.

1. **Source check**
   - Separate `user-provided notes`, `common book knowledge`, and `agent inference`.
   - If the user asks for page-specific claims, quotes, or chapter details not provided, ask for the excerpt or mark the answer as a memory-based summary.
2. **No fabricated evidence**
   - Do not invent page numbers, direct quotes, author anecdotes, or citations.
   - Keep user-provided quotes short and preserve their meaning.
3. **Choose output mode**
   - `brief`: one-sentence thesis, 3 takeaways, 1 action.
   - `detailed`: thesis, argument structure, key ideas, personal reflection, actions.
   - `related`: concept map and nearby books/ideas.
   - `comparison`: shared question, differences, complementarity, use cases.
4. **Upgrade the usefulness**
   - Turn vague praise into a specific claim about the book's value.
   - Add one practical application and one limitation or open question.

Preferred output:

```text
Source basis: <user notes | common knowledge | inference>
Review mode: <brief | detailed | related | comparison>
Main thesis: <one sentence>
Key takeaways: <3-5 bullets>
Application: <one concrete action>
Limits/open question: <one honest caveat>
```

## Commands

- `/book-review [insight]` - Generate a detailed book review
- `/book-review-brief [insight]` - Generate a brief review
- `/book-review-related [insight]` - Get related concepts for the insight

## Usage Examples

```
/book-review Today I read about deliberate practice and found it very inspiring
/book-review-brief The importance of spaced repetition in learning
/book-review-related How to build effective learning habits
```

## Technical Details

- **TypeScript** implementation
- **OpenClaw SDK** integration
- **Pure Local Processing**: No network calls, no file I/O
- **Version**: 1.1.1 (Integrity Upgrade)

## Safety Assurance

This skill has been specifically designed to address ClawHub security concerns:
1. ✅ **No External Dependencies**: Removed all external API calls
2. ✅ **No Filesystem Access**: No reading of local notes or files
3. ✅ **No Secrets**: No environment variables or API keys required
4. ✅ **Transparent Processing**: All logic visible in source code

## Installation

```bash
clawhub install book-review-skill
```

## Requirements

- Node.js >= 18.0.0
- OpenClaw >= 2026.3.0

## 真实任务示例

| 场景 | 用户会说 | Skill 执行 |
|------|---------|-----------|
| 读书笔记扩展 | "刚读完一章关于XX的，帮我整理成书评" | 提取要点 → 结构化输出 → 补充相关概念 |
| 快速回顾 | "之前读的那本书讲了什么来着" | 简要模式 → 核心观点摘要 → 关键行动建议 |
| 跨书对比 | "这两本书的观点有什么不同" | 识别对比维度 → 并列分析 → 给出互补视角 |
| 学习输出 | "把这段话展开，写一篇学习笔记" | 语义扩展 → 添加框架 → 组织成可发布格式 |
