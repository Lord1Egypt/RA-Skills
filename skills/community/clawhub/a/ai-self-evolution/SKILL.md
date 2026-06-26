---
name: ai-self-evolution
description: "记录经验、错误与修正，持续改进。触发场景：命令失败 | 操作出错 | 用户纠正（不对、实际上、你错了） | 功能请求（能不能、我希望、有没有办法） | API或工具失败 | 知识过时 | 发现更优做法 | 重复模式 | 非显而易见的问题。执行重大任务前先回顾历史经验。会话开始时回顾，会话结束时总结。"
metadata:
---

# 自我改进技能

将经验与错误记录到 `.learnings/` 目录，形成持续改进闭环。高价值经验沉淀到项目记忆。

> 安装/配置/Hook/多代理适配 → 见 `references/` 目录

## 快速参考

| 场景 | 操作 |
|------|------|
| 命令/操作失败 | 记录到 `ERRORS.md` |
| 用户纠正你 | 记录到 `LEARNINGS.md`，分类 `correction` |
| 用户提出新需求 | 记录到 `FEATURE_REQUESTS.md` |
| API/外部工具失败 | 记录到 `ERRORS.md`，补充集成细节 |
| 知识已过时 | 记录到 `LEARNINGS.md`，分类 `knowledge_gap` |
| 发现更好做法 | 记录到 `LEARNINGS.md`，分类 `best_practice` |
| 重复模式（simplify-and-harden） | 记录或更新 `LEARNINGS.md`，设 `Pattern-Key` |
| 与已有条目相似 | 用 `See Also` 关联，必要时提高优先级 |
| 可广泛复用的经验 | 提升到 `CLAUDE.md` / `AGENTS.md` |
| 工作流/工具/行为类 | 提升到 `AGENTS.md` / `TOOLS.md` / `SOUL.md`（OpenClaw 工作区） |

所有日志文件位于 `.learnings/` 目录（项目级或 `~/.openclaw/workspace/.learnings/`）。

---

## 会话开始：自动回顾

每次会话开始或执行重大任务前，执行以下回顾流程：

1. **检查待处理条目**：
   ```bash
   grep -c "Status\*\*: pending" .learnings/*.md 2>/dev/null
   ```
2. **扫描高优先级问题**：
   ```bash
   grep -B3 "Priority\*\*: high\|Priority\*\*: critical" .learnings/*.md | grep "^## \["
   ```
3. **检查与当前任务相关的历史经验**：根据任务涉及的 Area 和关键词搜索
4. **加载最近条目**（最近 7 天内创建的）：快速浏览最新 3-5 条记录
5. **输出回顾摘要**（内部执行，不打扰用户）：待处理数 / 高优数 / 相关经验

> 如果 `.learnings/` 不存在或为空，跳过回顾，正常工作。

---

## 会话结束：经验总结

在会话即将结束时（用户明确结束、任务完成、长时间无新指令），执行：

1. **回顾本次会话**：检查是否有未记录的错误、纠正或新发现
2. **补录遗漏条目**：将本次会话中遗漏的经验补充记录
3. **更新已解决条目**：本次修复的问题，将状态改为 `resolved`
4. **输出会话经验摘要**（简短告知用户）：
   - 本次新增条目数 / 关闭条目数
   - 建议提升的高价值经验（如有）
5. **触发归档检查**：如果条目总数超过阈值，执行归档流程

---

## 自动合并与归档

### 触发条件（满足任一即执行）

- 单个文件超过 50 条 pending 条目
- 存在超过 90 天未更新的 pending 条目
- 会话结束总结时检测到条目膨胀

### 归档流程

1. **合并重复条目**：相同 `Pattern-Key` 或高度相似 Summary → 合并为一条，累加 `Recurrence-Count`，保留最新 `Last-Seen`，用 `See Also` 记录被合并的原始 ID
2. **归档已关闭条目**：`resolved` / `wont_fix` / `promoted` 超过 30 天 → 移动到 `.learnings/archive/YYYY-MM.md`
3. **清理低价值条目**：`low` 优先级 + `pending` 超过 60 天 → 标记 `stale`；`stale` 超过 30 天 → 归档

---

## 检测触发器

观察到以下信号时**立即记录**：

| 类型 | 信号 | 记录到 |
|------|------|--------|
| **纠正** | "不对" "实际上应该" "你这里错了" "已经过时了" | `LEARNINGS.md` 分类 `correction` |
| **功能请求** | "你还能不能" "我希望你可以" "有没有办法" "为什么你不能" | `FEATURE_REQUESTS.md` |
| **知识缺口** | 用户提供你不知道的信息、文档过时、API 行为不一致 | `LEARNINGS.md` 分类 `knowledge_gap` |
| **错误** | 非零退出码、异常堆栈、输出异常、超时、连接失败 | `ERRORS.md` |
| **更优做法** | 发现比当前方案更好的实现 | `LEARNINGS.md` 分类 `best_practice` |

---

## 记录格式

### Learning 条目（追加到 `LEARNINGS.md`）

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
一行描述学到了什么

### Details
完整上下文：发生了什么、哪里错了、正确做法是什么

### Suggested Action
可执行的修复或改进建议

### Metadata
- Source: conversation | error | user_feedback | simplify-and-harden
- Related Files: path/to/file.ext
- Tags: tag1, tag2
- See Also: LRN-20250110-001
- Pattern-Key: simplify.dead_code（可选）
- Recurrence-Count: 1（可选）
- First-Seen / Last-Seen: 2025-01-15（可选）

---
```

### Error 条目（追加到 `ERRORS.md`）

```markdown
## [ERR-YYYYMMDD-XXX] skill_or_command_name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
失败情况简述

### Error
实际错误信息或输出

### Context
- 尝试执行的命令/操作
- 使用的输入或参数

### Suggested Fix
潜在修复方式

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file.ext
- See Also: ERR-20250110-001

---
```

### Feature Request 条目（追加到 `FEATURE_REQUESTS.md`）

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Requested Capability
用户希望实现的能力

### User Context
用户为什么需要它

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
可行实现思路

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_feature_name

---
```

---

## ID 与状态

**ID 格式**：`TYPE-YYYYMMDD-XXX`（TYPE: LRN/ERR/FEAT，XXX: 顺序号或随机 3 位）

**状态流转**：
- `pending` → `in_progress` → `resolved`（附 Resolution 块）
- `pending` → `wont_fix`（附原因）
- `pending` / `resolved` → `promoted`（已提升到项目记忆）
- `pending` → `promoted_to_skill`（已抽取为独立 skill）
- `pending` → `stale` → 归档

**关闭条目时**，在 Metadata 后添加：

```markdown
### Resolution
- **Resolved**: ISO-8601 timestamp
- **Commit/PR**: abc123 or #42
- **Notes**: 简述
```

---

## 重复模式检测

记录前先搜索已有条目：

1. `grep -r "关键词" .learnings/`
2. 若已有相似条目：添加 `See Also` 关联，增加 `Recurrence-Count`
3. 重复 3 次以上 → 提高优先级，考虑系统性修复
4. 系统性修复方向：文档缺失 → 提升到 CLAUDE.md；自动化缺失 → 写入 AGENTS.md；架构问题 → 创建技术债任务

### Simplify & Harden 吸收

1. 从任务摘要读取 `simplify_and_harden.learning_loop.candidates`
2. 以 `pattern_key` 去重，搜索 `LEARNINGS.md`
3. 已存在 → 增加 `Recurrence-Count`，更新 `Last-Seen`
4. 不存在 → 新建条目，设 `Source: simplify-and-harden`

---

## 提升到项目记忆

### 何时提升

- 经验适用于多个文件/功能
- 任何贡献者都应知晓
- 能避免重复犯错
- 重复模式满足：`Recurrence-Count >= 3` + 涉及 2+ 任务 + 30 天窗口内

### 提升目标

| 经验类型 | 提升到 |
|----------|--------|
| 项目事实、通用约定 | `CLAUDE.md` |
| 工作流、自动化规则 | `AGENTS.md` |
| 行为准则、沟通风格 | `SOUL.md`（OpenClaw） |
| 工具能力、集成坑点 | `TOOLS.md`（OpenClaw） |

### 如何提升

1. **提炼**为简洁预防规则（编码前/编码中该做什么），而非事故复盘
2. **写入**目标文件对应章节
3. **更新**原条目状态为 `promoted`，添加 `Promoted: <目标文件>`

### Skill 抽取

当经验满足以下任一条件时，可抽取为独立 skill：
- 通过 `See Also` 关联到 2+ 相似问题
- 状态为 `resolved` 且修复已验证
- 非项目特定，可跨代码库复用
- 用户明确要求"保存成 skill"

抽取流程与模板 → 见 `references/skill-extraction.md`

---

## 优先级与 Area

| 优先级 | 适用场景 |
|--------|----------|
| `critical` | 阻塞核心功能、数据丢失风险、安全问题 |
| `high` | 影响显著、常用流程、重复出现 |
| `medium` | 影响中等、有可行绕过方案 |
| `low` | 轻微不便、边缘场景 |

| Area | 范围 |
|------|------|
| `frontend` | UI、组件、客户端 |
| `backend` | API、服务端 |
| `infra` | CI/CD、部署、Docker |
| `tests` | 测试文件、覆盖率 |
| `docs` | 文档、README |
| `config` | 配置、环境、参数 |

---

## 最佳实践

1. **立即记录** — 问题刚发生时上下文最完整
2. **具体明确** — 便于后续代理快速理解
3. **包含复现步骤** — 尤其是错误类条目
4. **关联相关文件** — 提高修复效率
5. **给出可执行建议** — 避免仅写"需要调查"
6. **记录前先搜索** — 避免重复，优先关联已有条目
7. **积极提升** — 有疑问时优先沉淀到项目记忆
8. **定期归档** — 保持日志文件精简高效
