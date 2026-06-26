# cjl-autoresearch-cc

通过迭代变异测试自动改进任何 skill、prompt、文章、工作流或系统。

灵感来自 [Karpathy/autoresearch](https://github.com/karpathy/autoresearch) 和 [openclaw-autoresearch-pro](https://github.com/0xcjl/openclaw-autoresearch-pro)。

---

**语言:** [English](README.md) | [中文](README_zh.md)

---

## 目录

1. [设计原理](#设计原理)
2. [工作原理](#工作原理)
3. [快速开始](#快速开始)
4. [详细工作流程](#详细工作流程)
5. [优化模式](#优化模式)
6. [变异类型](#变异类型)
7. [使用示例](#使用示例)
8. [注意事项](#注意事项)
9. [参与贡献](#参与贡献)

---

## 设计原理

### 问题

AI 生成的内容往往存在人类容易发现但 AI 难以自我纠正的问题：
- 模糊的指令应该更精确
- 缺少边缘情况处理
- 术语不一致
- 内容冗余或啰嗦

### 解决方案：变异测试

不是让 AI 重写一切（通常会让情况更糟），而是：

1. **每次做一个小改动**
2. **用实际场景测试每个改动**
3. **用检查清单客观评分**
4. **只保留改进，回滚退步**

这模仿了进化的方式 — 小变异，适者生存。

### 为什么要小改动？

大规模重写是**不可验证的** — 你无法证明它有帮助还是有害。单个句子更改是可验证的：前后可比较。

**核心原则：** 每轮一个小而可验证的更改。

---

## 工作原理

### 循环流程

```
┌─────────────────────────────────────────────────────────────┐
│                      AUTORESEARCH 循环                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐           │
│   │   变异   │───▶│   测试   │───▶│   评分   │           │
│   │ (1个改动)│    │ (用例)  │    │(检查清单)│           │
│   └──────────┘    └──────────┘    └──────────┘           │
│                                          │                  │
│                                          ▼                  │
│                                    ┌──────────┐             │
│                                    │   决策   │             │
│                                    │ 保留/回滚│            │
│                                    └──────────┘             │
│                                          │                  │
└──────────────────────────────────────────┼──────────────────┘
                                           │
                           ┌───────────────┴───────────────┐
                           │      重复直到完成              │
                           │    （最多100轮）               │
                           └───────────────────────────────┘
```

### 评分标准

每轮根据检查清单产生一个分数：
- **10/10 = 100%**（完美）
- **7/10 = 70%**（良好）
- **5/10 = 50%**（最低可行）

分数提升？→ **保留变异**
分数下降？→ **回滚变异**

---

## 快速开始

### 安装

```bash
# 通过 ClawHub
clawhub install cjl-autoresearch-cc

# 或手动克隆
git clone https://github.com/0xcjl/cjl-autoresearch-cc.git ~/.claude/skills/cjl-autoresearch-cc
```

### 基本用法

```
# 优化一个 skill
autoresearch coding-standards

# 带路径优化
autoresearch ~/.claude/skills/my-skill

# 内联优化 prompt
autoresearch optimize this prompt: [粘贴你的prompt]

# 中文关键词
自动优化 coding-standards
```

---

## 详细工作流程

### 第一步 — 识别模式和目标

skill 会自动检测你要优化的内容：

| 模式 | 触发条件 |
|------|----------|
| **Skill** | skill 目录路径或 "optimize [skill名称]" |
| **Plugin** | 插件目录路径 |
| **Prompt** | 内联 prompt 文本 |
| **Article** | 长文档文本 |
| **Workflow** | 流程描述 |
| **System** | 系统/机制描述 |

### 第二步 — 生成检查清单

skill 会根据内容类型生成 10 个是/否问题：

**Skill 模式（示例问题）：**
1. 描述是否精确且可操作？
2. 是否覆盖主要用例？
3. 工作流程步骤是否清晰无歧义？
4. 是否处理错误状态？
5. 工具使用是否正确？
6. 示例是否反映真实用法？
7. 内容是否简洁（无冗余）？
8. 指令特异性是否合适？
9. 引用是否准确？
10. 所有部分是否完整？

### 第三步 — 准备测试用例

生成 3-5 个内容会处理的真实输入：

- 对于 skill："用户会说什么来触发这个 skill？"
- 对于 prompt："这个 prompt 会处理什么输入？"
- 对于文章："别人会怎么阅读这篇文章？"

### 第四步 — 运行循环

```
第 N/100 轮 | 最佳: 85% | 上次: +2%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
变异: Type D (收紧语言)
     "try to" → "must"
分数: 85% → 87% ✅ 保留
```

**循环配置：**
- 每 30 轮一批次，然后暂停供人工审核
- 最多 100 轮
- 停止条件：用户说停、100轮完成、100%分数、连续10轮无改进

### 第五步 — 报告结果

```
优化目标: coding-standards
分数: 65% → 92% (+27%)
轮数: 45 (保留: 38, 回滚: 7)
最有效变异: Type D (收紧语言), Type A (添加约束)

---
最终内容保存至: ~/.claude/skills/coding-standards/SKILL.md
```

---

## 优化模式

### Skill 模式
优化 Claude Code 或 OpenClaw 的 SKILL.md 文件。

```
autoresearch coding-standards
autoresearch ~/.claude/skills/tdd-workflow
```

### Plugin 模式
优化插件配置和代码。

```
autoresearch everything-claude-code
```

### Prompt 模式
改进任何 prompt 文本。

```
autoresearch optimize this prompt: You are a helpful assistant that...
```

### Article 模式
润色文档或文章。

```
autoresearch polish this article: [粘贴文章]
```

### Workflow 模式
优化流程和步骤。

```
autoresearch optimize the deployment workflow
```

### System 模式
改进系统架构或机制。

```
autoresearch improve the error handling system
```

---

## 变异类型

每轮选择**一种**变异类型：

| 类型 | 名称 | 使用场景 |
|------|------|---------|
| **A** | 添加约束 | 内容太模糊时 |
| **B** | 加强覆盖 | 触发条件缺失时 |
| **C** | 添加示例 | 步骤太抽象时 |
| **D** | 收紧语言 | 词语太软时 ("try to" → "must") |
| **E** | 错误处理 | 失败模式缺失时 |
| **F** | 删除冗余 | 内容冗长时 |
| **G** | 改进过渡 | 流程不流畅时 |
| **H** | 扩展薄弱部分 | 内容稀疏时 |
| **I** | 添加交叉引用 | 各部分孤立时 |
| **J** | 调整自由度 | 平衡失调时 |

### 高影响力变异

这些通常能持续提升分数：
- 在模糊内容处添加明确约束
- 扩展到边缘情况
- 为抽象步骤添加具体示例
- 收紧软语言 ("try to" → "must")

### 应避免的操作

- 大段重写整个部分
- 一次做多个不相关的更改
- 改变基本范围或目的
- 仅更改格式（无可验证价值）
- 删除超过 10% 的内容

---

## 使用示例

### 示例一：优化 Skill

```bash
# 触发
autoresearch coding-standards

# AI 响应:
# "以 Skill 模式优化 coding-standards？ (yes/no)"
# > yes

# AI 生成检查清单、准备测试用例、运行循环
# 30轮后: 分数 68% → 89%
```

### 示例二：优化 Prompt

```bash
# 触发
autoresearch optimize this prompt: Write a function that...

# AI 响应:
# "以内联 Prompt 模式优化？ (yes/no)"
# > yes

# AI 生成检查清单、运行循环
```

### 示例三：中文用法

```bash
# 触发
自动优化 coding-standards

# 中文关键词同样有效
自动研究 错误处理系统
```

### 示例四：语义触发

```bash
# 无需关键词 - 自动识别意图
帮我优化一下这个skill
这个prompt不太行
让文章更通顺
```

---

## 注意事项

### 1. 每轮一个变异

**关键规则。** 多个更改 = 不可验证 = 会被回滚。

### 2. 相信分数

不要为糟糕的变异找借口。如果分数下降了，就回滚。不要想"但实际上它更好因为..."

### 3. 最少 5 个检查问题

使用太少会使评分不可靠。默认是 10 个。

### 4. 上下文长度

Autoresearch 最适合能放进上下文的内容。对于很长的文档，逐部分优化。

### 5. 有意义的测试用例

测试用例必须真实。不匹配真实用法的"测试输入"会产生虚假分数。

### 6. 人工审核点

每 30 轮，循环会暂停供人工审核。用这个时机来：
- 评估优化是否在正确方向上
- 识别检查清单可能遗漏的问题
- 决定停止或继续

### 7. 不是万能的

Autoresearch 适用于**基于文本的内容**，即可以用检查清单评分的内容。不适合：
- 有实际运行时行为的代码（用测试）
- 二进制内容
- 没有明确标准的主观创意作品

---

## 参与贡献

欢迎提交 Issue 和 Pull Request！查看 [SKILL.md](SKILL.md) 获取完整的技术规范。

---

## 致谢

- [Karpathy/autoresearch](https://github.com/karpathy/autoresearch) — 原创概念
- [openclaw-autoresearch-pro](https://github.com/0xcjl/openclaw-autoresearch-pro) — Prompt/文章优化扩展

---

详细技术文档请查看 [SKILL.md](SKILL.md)。
