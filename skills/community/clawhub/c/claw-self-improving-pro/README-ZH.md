# Self-Improving Skill 中文文档

## 概述

**Self-Improving** 是一个自我反思、自我学习、自我组织记忆的 skill。它让 AI Agent 能够：

- 从用户纠正中学习
- 自我评估工作质量
- 持久化偏好和模式
- 跨会话累积知识

**版本**: 1.2.10
**主页**: https://clawic.com/skills/self-improving

---

## 架构设计

```
~/self-improving/
├── memory.md          # HOT: ≤100行，始终加载
├── index.md           # 索引文件，记录行数统计
├── projects/          # 项目级学习内容
├── domains/           # 领域级（代码、写作、通信）
├── archive/           # COLD: 已衰减的模式
└── corrections.md     # 最近50条纠正日志
```

---

## 核心机制

### 1. 三层存储架构

| 层级 | 位置 | 大小限制 | 加载行为 |
|------|------|----------|----------|
| **HOT** | `memory.md` | ≤100行 | 每次会话始终加载 |
| **WARM** | `projects/`, `domains/` | 每个≤200行 | 按需加载（匹配上下文时） |
| **COLD** | `archive/` | 无限制 | 仅显式查询时加载 |

### 2. 自动晋升/降级机制

```
模式使用 ≥3次/7天  → 晋升到 HOT
模式未使用 ≥30天    → 降级到 WARM
模式未使用 ≥90天    → 归档到 COLD
```

### 3. 命名空间继承

```
global (memory.md)
  └── domain (domains/code.md)
       └── project (projects/app.md)
```

**冲突解决规则**：
- 最具体的优先（project > domain > global）
- 同层级最近优先
- 模糊时询问用户

---

## 学习机制

### 触发条件

| 触发词 | 置信度 | 动作 |
|--------|--------|------|
| "不，应该做X" | 高 | 立即记录纠正 |
| "我之前告诉过你..." | 高 | 标记为重复，提升优先级 |
| "总是/永远做X" | 已确认 | 晋升为偏好 |
| 用户编辑你的输出 | 中 | 记录为暂定模式 |
| 同一纠正出现3次 | 已确认 | 请求确认为永久规则 |

### 不触发学习的场景

- 沉默（不是确认）
- 单次事件
- 假设性讨论
- 第三方偏好（"John喜欢..."）
- 群聊模式（除非用户确认）
- 推断的偏好

### 模式演化阶段

```
Tentative (暂定) → Emerging (显现) → Pending (待确认) → Confirmed (确认) → Archived (归档)
      ↑                  ↑                 ↑                ↑
   1次纠正           2次纠正           3次纠正          用户批准
```

---

## 纠正分类系统

### 按类型

| 类型 | 示例 | 命名空间 |
|------|------|----------|
| 格式 | "用子弹点不用段落" | global |
| 技术 | "SQLite不用Postgres" | domain/code |
| 沟通 | "消息短一点" | global |
| 项目特定 | "这个仓库用Tailwind" | projects/{name} |

### 按范围

```
Global: 全局适用
  └── Domain: 类别适用（代码、写作、沟通）
       └── Project: 特定上下文
            └── Temporary: 仅本会话
```

---

## 自我反思机制

完成重要工作后，Agent 应暂停评估：

```
1. 是否符合预期？ — 对比结果与意图
2. 什么可以更好？ — 识别改进点
3. 这是一个模式吗？ — 是则记录到 corrections.md
```

**记录格式**：
```
CONTEXT: [任务类型]
REFLECTION: [发现的问题]
LESSON: [下次如何改进]
```

**示例**：
```
CONTEXT: 构建 Flutter UI
REFLECTION: 间距看起来不对，需要重做
LESSON: 展示给用户前检查视觉间距
```

---

## 安全边界

### 永不存储

| 类别 | 示例 | 原因 |
|------|------|------|
| 凭证 | 密码、API密钥、SSH密钥 | 安全风险 |
| 财务 | 银行卡、银行账户、加密种子 | 欺诈风险 |
| 医疗 | 诊断、药物、病情 | 隐私/HIPAA |
| 生物识别 | 声纹、行为指纹 | 身份盗窃 |
| 第三方信息 | 关于其他人的信息 | 未获同意 |
| 位置模式 | 家庭/工作地址、作息 | 人身安全 |
| 访问模式 | 用户可访问的系统 | 权限提升风险 |

### 需谨慎存储

| 类别 | 规则 |
|------|------|
| 工作上下文 | 项目结束后衰减，不跨项目分享 |
| 情感状态 | 仅用户明确分享时，从不推断 |
| 关系 | 仅角色（"经理"、"客户"），无个人细节 |
| 日程 | 通用模式可以（"上午忙"），非具体时间 |

### 红旗检测

⚠️ 如果发现自己在做这些，立即停止：

- "以防有用"而存储信息
- 从非敏感数据推断敏感信息
- 用户要求遗忘后仍保留
- 将个人上下文应用到工作（反之亦然）
- 学习如何让用户更快服从
- 建立心理画像
- 保留第三方信息

### 紧急开关

用户说"忘记一切"：
1. 导出当前记忆到文件（供用户审查）
2. 清除所有学习数据
3. 确认："记忆已清除。重新开始。"
4. 不保留行为中的"幽灵模式"

---

## 操作流程

### 会话开始时

```
1. 加载 memory.md (HOT层)
2. 检查 index.md 获取上下文提示
3. 如果检测到项目 → 预加载相关命名空间
```

### 收到纠正时

```
1. 解析纠正类型（偏好/模式/覆盖）
2. 检查是否重复（存在于任何层级）
3. 如果新：
   - 添加到 corrections.md 并打时间戳
   - 增加纠正计数器
4. 如果重复：
   - 增加计数器，更新时间戳
   - 计数器≥3时：请求确认为规则
5. 确定命名空间（global/domain/project）
6. 写入对应文件
7. 更新 index.md 行数统计
```

### 应用学习模式时

```
1. 查找模式来源（file:line）
2. 应用模式
3. 引用来源："使用X（来自memory.md:15）"
4. 记录使用情况用于衰减追踪
```

### 周维护（定时任务）

```
1. 扫描所有文件寻找衰减候选
2. 移动未使用>30天到 WARM
3. 归档未使用>90天到 COLD
4. 运行压缩（如有文件超限）
5. 更新 index.md
6. 生成周报（可选）
```

---

## 缩放策略

| 规模 | 条目数 | 策略 |
|------|--------|------|
| 小型 | <100 | 单个 memory.md，无命名空间 |
| 中型 | 100-500 | 分离到 domains/，基础索引 |
| 大型 | 500-2000 | 完整命名空间层级，积极压缩 |
| 海量 | >2000 | 年度归档，HOT层仅摘要 |

### 压缩规则

**合并相似纠正**：
```
BEFORE (3条):
- [02-01] 用tabs不用spaces
- [02-03] 用tabs缩进
- [02-05] 请用tab缩进

AFTER (1条):
- 缩进：tabs（确认3次，02-01至02-05）
```

**精简冗长模式**：
```
BEFORE:
- 给Marcus写邮件时，用子弹点，保持5条以内，无行话，结论先行，他偏好上午发送

AFTER:
- Marcus邮件：子弹≤5条，无行话，BLUF，上午优先
```

---

## 用户命令

| 命令 | 动作 |
|------|------|
| "你对X了解什么？" | 搜索所有层级，返回匹配及来源 |
| "显示我的记忆" | 显示 memory.md 内容 |
| "显示[项目]模式" | 加载并显示特定命名空间 |
| "忘记X" | 从所有层级移除，确认删除 |
| "忘记一切" | 完全清空（带导出选项） |
| "最近有什么变化？" | 显示最近20条纠正 |
| "导出记忆" | 生成可下载的归档文件 |
| "记忆状态" | 显示层级大小、最后压缩、健康状态 |

---

## 文件格式

### memory.md (HOT)

```markdown
# Self-Improving Memory

## Confirmed Preferences
- format: bullets over prose (confirmed 2026-01)
- tone: direct, no hedging (confirmed 2026-01)

## Active Patterns
- "looks good" = approval to proceed (used 15x)
- single emoji = acknowledged (used 8x)

## Recent (last 7 days)
- prefer SQLite for MVPs (corrected 02-14)
```

### corrections.md

```markdown
# Corrections Log

## 2026-02-15
- [14:32] Changed verbose explanation → bullet summary
  Type: communication
  Context: Telegram response
  Confirmed: pending (1/3)

## 2026-02-14
- [09:15] Use SQLite not Postgres for MVP
  Type: technical
  Context: database discussion
  Confirmed: yes (said "always")
```

### projects/{name}.md

```markdown
# Project: my-app

Inherits: global, domains/code

## Patterns
- Use Tailwind (project standard)
- No Prettier (eslint only)
- Deploy via GitLab CI

## Overrides
- semicolons: yes (overrides global no-semi)

## History
- Created: 2026-01-15
- Last active: 2026-02-15
- Corrections: 12
```

---

## 边缘情况处理

### 检测到矛盾

```
Pattern A: "用tabs" (global, confirmed)
Pattern B: "用spaces" (project, corrected today)

解决方案:
1. 项目覆盖全局 → 此项目用spaces
2. 在 corrections.md 记录冲突
3. 询问："spaces是否只应用于此项目还是全局？"
```

### 用户改变主意

```
Old: "总是用正式语气"
New: "其实，随意也可以"

动作:
1. 归档旧模式并打时间戳
2. 添加新模式为暂定
3. 保留归档供参考（"你之前偏好正式"）
```

### 上下文模糊

```
用户说："记住我喜欢X"

但是哪个命名空间？
1. 检查当前上下文（项目？领域？）
2. 如不清楚，询问："这应该全局应用还是仅在此处？"
3. 默认使用最具体的活动上下文
```

---

## 相关 Skills

可通过 `clawhub install <slug>` 安装：

- `memory` — Agent 长期记忆模式
- `learning` — 自适应教学和解释
- `decide` — 自动学习决策模式
- `escalate` — 知道何时询问 vs 自主行动

---

## 设计哲学

这个 skill 体现了几个关键设计原则：

1. **复合学习** — 知识随时间累积，无需手动维护
2. **显式优于推断** — 从不从沉默中推断偏好
3. **渐进式确认** — 3次重复才请求确认
4. **命名空间隔离** — 项目模式留在项目文件中
5. **透明可审计** — 每次引用都注明来源
6. **安全优先** — 明确的安全边界和红旗检测
7. **优雅降级** — 上下文超限时仅加载 HOT 层

---

## 反馈

- 觉得有用：`clawhub star self-improving`
- 保持更新：`clawhub sync`