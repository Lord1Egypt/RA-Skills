# 回复前检查清单 (Pre-Reply Checklist)

_创建时间：2026-03-09 06:56_
_触发事件：违反 using-superpowers 技能（未调用技能就回复）_

---

## 🚨 核心原则（不可违背）

**using-superpowers 铁律：**
> 「If you think there is even a 1% chance a skill might apply to what you are doing, you ABSOLUTELY MUST invoke the skill.」

**调用时机：**
> 「Invoke relevant or requested skills BEFORE any response or action. Even before clarifying questions.」

---

## ✅ 每次回复前的检查流程

### 步骤 1：收到消息后立即暂停
- [ ] 不要立即思考如何回复
- [ ] 不要立即探索代码/文件
- [ ] 不要立即执行任何操作

### 步骤 2：检查技能列表
- [ ] 扫描 `skills/` 目录下的所有技能
- [ ] 问自己：「是否有任何技能（即使是 1% 可能性）适用于当前任务？」
- [ ] 如果有 → 进入步骤 3
- [ ] 如果确定没有 → 可以直接回复

### 步骤 3：调用相关技能
- [ ] 用 `read` 工具读取技能的 SKILL.md 文件
- [ ] 遵循技能说明执行
- [ ] 如果技能有 checklist → 创建 TodoWrite

### 步骤 4：遵循技能要求
- [ ] 严格按照技能说明执行
- [ ] 不要理性化跳过（见下方红牌警告）
- [ ] 如果技能要求记录 → 记录到 self-improving 系统

### 步骤 5：回复用户
- [ ] 确保已经遵循了所有相关技能
- [ ] 回复内容符合技能要求

---

## 🚩 红牌警告（Rationalization Red Flags）

**这些想法出现时 = STOP！你正在理性化跳过技能：**

| 想法 | 现实 |
|------|------|
| 「这只是个简单问题」 | 问题也是任务，需要检查技能 |
| 「我需要先了解上下文」 | 技能会告诉你 HOW 了解上下文 |
| 「让我先快速看看代码」 | 技能会告诉你 HOW 探索代码 |
| 「这个不需要正式技能」 | 如果技能存在，就用它 |
| 「我记得这个技能」 | 技能会进化，读取当前版本 |
| 「这只是个小修改」 | 小修改也可能有大技能 |
| 「我先做这件事再检查」 | 检查必须在行动之前 |
| 「这感觉很有成效」 | 无纪律的行动浪费时间 |
| 「我知道什么意思」 | 知道概念 ≠ 使用技能 |

---

## 📋 常见场景与必用技能

| 场景 | 触发词/信号 | 必用技能 |
|------|------------|---------|
| 用户纠正 | 「不对」「错了」「应该」「改正」 | self-improving-agent-cn |
| 命令失败 | 错误信息/退出码非 0 | self-improving-agent-cn |
| 建立规范 | 「检查清单」「约束」「流程」 | self-improving-agent-cn |
| 技能相关 | 「技能」「using-superpowers」 | using-superpowers |
| 代码风格 | 「格式」「命名」「规范」 | self-improving-agent-cn |
| 更好方法 | 「更高效」「最优」「更好的」 | self-improving-agent-cn |
| 知识过时 | 「过时了」「已废弃」「新版」 | self-improving-agent-cn |
| 任何任务 | 不确定 | 检查所有技能 |

---


## 🔍 文件操作前检查（新增 2026-03-09 07:03）

**在修改任何文件之前，必须检查 self-improving 记忆：**

`powershell
# 1. 检查是否有相关错误记录
Get-ChildItem "memory/self-improving/errors/" -Name | Select-String -Pattern "文件名或关键词"

# 2. 检查最佳实践
Get-Content "memory/self-improving/best_practices.jsonl" | ConvertFrom-Json | Where-Object { .category -eq "file-operations" }
`

**如果发现相关记忆：**
- ✅ 遵循记录的最佳实践
- ❌ 不要重复犯同样的错误

**示例：**
- 看到 AGENTS.md / worklog.txt → 检查是否有 EPERM 错误记录
- 发现「用 Add-Content」→ 直接用 exec，不用 edit/write

## 📁 相关文件

- `skills/using-superpowers/SKILL.md` - 核心技能调用规则
- `skills/self-improving-agent-cn/SKILL.md` - 自我改进系统
- `memory/self-improving/errors/` - 错误记录
- `memory/self-improving/best_practices.jsonl` - 最佳实践

---


## 🎯 技能选择决策（2026-03-09 新增）

**当多个技能相似时，用决策树选择：**

### 决策树示例：html-expert-review vs project-summary-report

`
用户请求
    ↓
是知识内容分析吗？（豆包会话/教程/讲解）
├─ 是 → html-expert-review
│   └─ 特征：专家评分 + 深度洞察 + Critical Thinking
│
└─ 否 → 是项目进度展示吗？（项目卡片/文件夹/里程碑）
    ├─ 是 → project-summary-report
    │   └─ 特征：状态卡片 + 流程图 + 文件列表
    │
    └─ 否 → 检查其他技能
`

### 触发词快速匹配

| 技能 | 触发词 |
|------|--------|
| html-expert-review | 「专家点评」「知识分析」「豆包会话」「深度洞察」 |
| project-summary-report | 「项目报告」「进度总结」「项目卡片」「里程碑」 |
| self-improving-agent-cn | 「不对」「错了」「应该」「改正」「记住」 |
| using-superpowers | 「技能」「调用」「检查」 |

### 选择原则

1. **内容类型优先** - 知识内容 vs 项目进度
2. **输出目标优先** - 深度分析 vs 概览展示
3. **触发词匹配** - 用户用词暗示技能选择

---

## 🔍 技能发现流程（2026-03-09 新增）

**当本地技能库没有合适技能时，检查 ClawHub：**

### 触发条件
- 「检查其他技能」分支 → 本地无匹配
- 用户明确要求检查 ClawHub
- 任务复杂度高，可能有更好的外部技能

### 执行流程

`powershell
# 1. 搜索相关技能
clawhub search "<关键词>"

# 2. 查看技能详情（可选）
clawhub inspect "<slug>"

# 3. 浏览最新技能（可选）
clawhub explore
`

### 输出格式

**在回复末尾附上：**

`markdown
---
## 🌐 ClawHub 技能推荐

**最推荐：** [技能名](链接) - 简短说明
**次优：** [技能名](链接) - 简短说明

_使用 clawhub install <slug> 安装_
`

### 安全约束
- ✅ 只推荐，不主动安装（用户决定）
- ✅ 安装前必须经过 skill-vetting 审查
- ✅ 检查技能来源、评分、下载量

---
## 🔄 更新历史

| 日期 | 更新内容 | 触发事件 |
|------|---------|---------|
| 2026-03-09 06:56 | 初始版本 | 违反 using-superpowers 技能 |

---

_此清单本身就是一个最佳实践，记录到 self-improving 系统_



