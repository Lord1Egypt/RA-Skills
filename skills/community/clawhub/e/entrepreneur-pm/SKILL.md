---
name: entrepreneur-pm
description: 企业家 PM 思维框架 Skill — 面向 Leevar 团队管理层。激活场景：(1) 分配 Agent 处理复杂多步骤任务，(2) 确保 Agent 精准理解并达成用户目标，(3) 让 Agent 100% 按任务需求调用已掌握的 Skill，(4) 促进管理层持续学习和经验积累，(5) 任何涉及"如何更好地管理AI团队""如何拆解任务"" "如何提升 Agent 执行质量"的讨论。触发词：任务分配、Agent 管理、团队协作、经验积累、管理能力、任务拆解、PM 视角、跨 Agent 协作、Skill 调用、团队优化。
---

# Entrepreneur PM 框架

Lee 的 AI 团队管理操作系统。面对任何团队管理、任务分配、Agent 协作问题，强制执行以下框架。

---

## 核心三原则

### 1. 精准路由 — 把对的任务给对的 Agent
### 2. 目标对齐 — 确保 Agent 真正理解用户需求
### 3. Skill 强制调用 — Agent 必须使用已掌握的 Skill，不得重复造轮子

---

## 原则 1：精准路由

**每次任务分配前，强制执行 3 秒决策：**

```
任务是什么？
  ↓
哪个 Agent 拥有最相关的 Skill？
  ↓
这个 Agent 现在有能力执行吗？（工具权限 / Skill 已加载）
  ↓
任务包需要什么输入？我是否都提供了？
```

**团队路由矩阵（快速参考）：**

| 任务类型 | 首选 Agent | 备选 |
|---------|-----------|------|
| Shopify 产品/订单/主题 | Shopify Writer subagent | cloud browser |
| 市场数据/期权分析 | MarketWatcher | sessions_spawn |
| 供应商研究/选品 | SupplierAgent | batch_web_search |
| 社媒内容创作 | SocialAgent / ContentAgent | Mia subagent |
| 外链开发/潜在客户 | OutreachAgent | Kai subagent |
| 代码/自动化/API | sessions_spawn(acp) | exec |
| 视觉验证/截图 | cloud browser | LocalAgent |
| 本地登录/2FA | LocalAgent/Hex | 仅此路径 |

**路由质量标准：**
- ✅ 任务包含：目标、背景、输出格式、截止时间
- ✅ 已明确说明 Agent 应调用哪些 Skill
- ✅ 已说明成功的验收标准
- ❌ 不可以：任务描述模糊、输出路径不明、没有验证要求

---

## 原则 2：目标对齐 — 确保 Agent 理解用户真实需求

**任务包标准模板（每次分配都要用）：**

```
## 任务目标
[Lee 真正想要的结果，不只是表面任务]

## 背景
[为什么要做这件事，有哪些约束]

## 具体要求
1. [步骤1]
2. [步骤2]
...

## 输出要求
- 格式：[JSON / Markdown / 直接操作]
- 存放位置：[具体文件路径]
- 验证方法：[如何确认成功]

## 禁止事项
- [不得做的事，避免 Agent 走弯路]

## 时间要求
[紧急/正常/下次巡逻时完成]
```

**对齐检查（任务发出前）：**
- [ ] Agent 有没有可能误解任务？
- [ ] 我有没有说清楚"完成"的标准？
- [ ] Agent 知道遇到阻塞时怎么办吗？

---

## 原则 3：Skill 强制调用

**为什么重要：** Agent 有时会"重新发明轮子"——写全新代码而不是调用已有 Skill。这浪费时间，产生不一致的结果。

**任务包中必须包含 Skill 指引：**

```markdown
## 要求使用的 Skill
- 使用 [skill-name] Skill 处理 [具体环节]
- 参考 /root/.openclaw/skills/[skill-folder]/SKILL.md
- 不得绕过 Skill 自行实现相同功能
```

**可用 Skill 速查（常用）：**

| Skill | 用途 |
|-------|------|
| minimax-xlsx | 表格/数据/Excel 生成 |
| minimax-pdf | PDF 报告输出 |
| minimax-docx | Word 文档输出 |
| superdesign | 前端 UI 设计 |
| cron-mastery | 定时任务/提醒设置 |
| self-improving-agent | 错误记录/经验沉淀 |
| automation-workflows | 自动化流程设计 |
| leevar-entrepreneur | 商业决策框架 |
| agent-team-orchestration | 多 Agent 协作设计 |
| weather | 天气查询 |
| options-trader | 期权交易分析 |

完整列表：`/root/.openclaw/skills/`

---

## 管理层持续学习系统

### 每次任务完成后：30 秒经验沉淀

```markdown
## 任务复盘模板

任务：[一句话]
结果：✅成功 / ⚠️部分完成 / ❌失败

学到了什么：
- [新发现的规律或方法]

下次更好：
- [改进点]

沉淀到 Skill：是/否
→ 若是，更新：[Skill 路径]
```

**写入位置：** `/workspace/memory/learnings-[YYYY-MM].md`

### 经验积累层级

```
单次任务经验
    ↓ 复盘沉淀
Agent LEARNING.md（每个 Agent 专属）
    ↓ 提炼共性
Skill 更新（rules/references 更新）
    ↓ 内化
下次自动调用正确方法
```

### 管理层 KPI（每周一次 Lee 评审）

| 指标 | 目标 | 来源 |
|------|------|------|
| 任务首次成功率 | >80% | 任务报告 |
| Agent 路由准确率 | >90% | 任务日志 |
| Skill 调用率 | >70% | 代码审查 |
| 平均任务周期 | <15分钟/任务 | 时间戳 |
| 经验沉淀频率 | 每周≥3条 | LEARNING.md |

---

## 常见失败模式 & 修复

| 失败模式 | 症状 | 修复 |
|---------|------|------|
| 任务包模糊 | Agent 返回无用输出 | 用模板重写任务包 |
| 路由错误 | 错的 Agent 接了任务 | 参考路由矩阵重新分配 |
| 没用 Skill | Agent 自写代码完成已有 Skill 的功能 | 在任务包中明确指定 Skill |
| 无验证标准 | Agent 自称完成但结果无法核实 | 所有任务必须有验收标准 |
| 经验未沉淀 | 同样错误反复出现 | 强制执行 30 秒复盘模板 |

---

## 参考文档

- 任务包完整案例：见 `references/task-examples.md`
- Agent 能力矩阵详细版：见 `references/agent-capabilities.md`
- 经验积累历史：见 `/workspace/memory/`
