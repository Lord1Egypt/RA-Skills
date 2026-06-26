# Agent Team Builder — 数据契约

本文档定义 agent-team-builder 核心文件的 JSON 字段规范。每个契约标明生产者（写入方）和消费者（读取方），确保跨 Agent 通信格式统一。

---

## 1. Team Charter（团队宪章）

**文件**: `.claude/teams/<team_name>/team_charter.md`

### 字段定义

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `team_name` | string | ✅ | 团队唯一标识名 |
| `mission` | string | ✅ | 团队总体任务场景与长远目标 |
| `roles` | array | ✅ | 角色列表，每项含 `{name, responsibilities, agent_type}` |
| `workflow` | array | ✅ | 工作流拓扑，每项含 `{from, to, trigger}` |
| `created_at` | ISO 8601 | ❌ | 创建时间 |
| `updated_at` | ISO 8601 | ❌ | 最后更新时间 |

### JSON Schema

```json
{
  "team_name": "ldd_research",
  "mission": "构建基于 LLM 的文献发现与总结系统",
  "roles": [
    {
      "name": "team-leader",
      "responsibilities": "任务分发、进度跟踪、冲突解决",
      "agent_type": "team-leader"
    },
    {
      "name": "innovator",
      "responsibilities": "方案探索、假设生成",
      "agent_type": "innovator"
    }
  ],
  "workflow": [
    {
      "from": "team-leader",
      "to": "innovator",
      "trigger": "任务分发"
    },
    {
      "from": "innovator",
      "to": "team-leader",
      "trigger": "成果提交"
    }
  ]
}
```

**生产者**: Team Builder orchestrator（场景 A 步骤 1）、team-leader agent
**消费者**: 所有 role agents、Team Builder 场景 B 加载流程

---

## 2. Role Profile（角色配置）

**文件**: `.claude/agents/<role_name>.md`

### 字段定义

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` (frontmatter) | string | ✅ | 角色名，与文件名一致 |
| `description` (frontmatter) | string | ✅ | 角色简短描述 |
| `type` (frontmatter) | string | ✅ | 角色类型，必须与 name 一致 |
| `职责` | string | ✅ | 核心职责描述 |
| `系统级 Prompt 要求` | string | ✅ | 专业领域、行为风格、输出格式 |
| `工作机制` | section | ✅ | 4 项强制机制（沙盒/渐进式披露/记忆/技能） |

### JSON 表示

```json
{
  "name": "innovator",
  "description": "方案探索与假设生成专家",
  "type": "innovator",
  "职责": "负责探索新技术方案，生成创新假设",
  "系统级 Prompt 要求": [
    "你是前沿技术探索专家",
    "优先使用最新开源方案",
    "输出需包含可行性评估"
  ],
  "工作机制": {
    "沙盒纪律": "仅在 workspace/ 下创建临时文件",
    "渐进式披露": "progress.md 存摘要，workspace/ 存细节",
    "个性化记忆": "经验教训记录到 memory.md",
    "独立技能系统": "专属技能存放在 skills/ 下"
  }
}
```

**生产者**: Team Builder orchestrator（场景 A 步骤 4）
**消费者**: generate_prompts.py、Agent 实例化工具

---

## 3. Memory（角色记忆）

**文件**: `.claude/teams/<team_name>/<role_name>/memory.md`

### 字段定义

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `lessons` | array | ✅ | 经验教训，每项含 `{date, context, insight, application}` |
| `pitfalls` | array | ✅ | 踩坑记录，每项含 `{date, symptom, root_cause, fix}` |
| `user_notes` | array | ✅ | 用户强调的"记住"内容，每项含 `{date, note}` |

### JSON 表示

```json
{
  "lessons": [
    {
      "date": "2026-04-15",
      "context": "实现 RAG 索引构建",
      "insight": "增量构建比全量重建快 10x",
      "application": "下次遇到索引重建优先检查变更范围"
    }
  ],
  "pitfalls": [
    {
      "date": "2026-04-15",
      "symptom": "Agent 无法识别新的 subagent_type",
      "root_cause": "创建 .claude/agents/ 后未重启 Claude Code",
      "fix": "创建角色配置后必须提示用户重启"
    }
  ],
  "user_notes": [
    {
      "date": "2026-04-15",
      "note": "team_charter.md 是二次加载团队的唯一入口"
    }
  ]
}
```

**生产者**: role agents（执行过程中主动记录）、team-leader（"记住这个坑"时）
**消费者**: generate_prompts.py（组装 prompt 时注入）、同角色 agent 恢复时

---

## 4. Progress（角色进度）

**文件**: `.claude/teams/<team_name>/<role_name>/progress.md`

### 字段定义

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `completed_tasks` | array | ✅ | 已完成任务，每项含 `{date, summary, detail_ref}` |
| `current_status` | string | ✅ | 当前工作状态（一句话摘要） |
| `pending_tasks` | array | ✅ | 待办任务，每项含 `{summary, blocker?, detail_ref?}` |

### JSON 表示

```json
{
  "completed_tasks": [
    {
      "date": "2026-04-15",
      "summary": "完成 RAG 索引构建脚本",
      "detail_ref": "workspace/rag-index-build.md"
    }
  ],
  "current_status": "正在优化查询性能",
  "pending_tasks": [
    {
      "summary": "集成 Jina embedding",
      "blocker": "等待 API key 配置"
    }
  ]
}
```

**生产者**: role agents（任务完成后更新）
**消费者**: team-leader（状态收集）、SendMessage 指令（状态对齐时）
