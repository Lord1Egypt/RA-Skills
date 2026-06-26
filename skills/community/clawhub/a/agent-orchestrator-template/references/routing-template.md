# Routing Configuration Template

This template upgrades routing from a simple keyword table to a full orchestration model:

1. Check no-spawn rules first
2. Classify task type
3. Classify domain
4. Select an execution strategy
5. Dispatch only with a task contract

## Minimal Orchestration Template

```yaml
# agent-routing.yaml

task_types:
  - id: explore
    preferred_agent: explorer
  - id: implement
    preferred_agent: worker
  - id: verify
    preferred_agent: main
  - id: operate
    preferred_agent: worker

domains:
  - id: code
    triggers: [代码, debug, 报错, 修复, git]
  - id: knowledge
    triggers: [知识库, Obsidian, 入库, 归档]
  - id: content
    triggers: [文案, 写作, 文章, 内容]

no_spawn_rules:
  - trigger: "What is"
    action: main
  - trigger: "你自己来"
    action: main

parallel_rules:
  allow_parallel_if_disjoint_write_sets: true
  prefer_parallel_for_read_only_exploration: true
  avoid_parallel_on_blocking_tasks: true
```

## Agent Registry Extension

Add an optional `agents` list so you can describe the registry of available agent kinds and map task types to those ids. Each agent entry should include at least `id` and `description`, and may also offer capability metadata such as supported domains or cost tiers. When `agents` exists, `preferred_agent` and `fallback_agent` must reference ids defined in the registry, but the runtime keeps working without the registry by falling back to the simple strings shown above.

With the registry in place you can define `ops-specialist`, `researcher`, or other names that are specific to your workspace, freeze the local OpenClaw five-agent profile as a sample entry point, and still enjoy validation via `scripts/validate-routing-config.py`.

## OpenClaw Local Example

For the current local OpenClaw profile, use agent ids that already exist in config:

```yaml
task_types:
  - id: explore
    preferred_agent: codex
  - id: implement
    preferred_agent: codex
  - id: verify
    preferred_agent: main
  - id: operate
    preferred_agent: knowledge

domains:
  - id: code
    triggers: [代码, debug, 报错, 修复, git]
  - id: knowledge
    triggers: [知识库, Obsidian, 入库, 归档]
  - id: content
    triggers: [文案, 写作, 文章, 内容]
  - id: community
    triggers: [社区, 评论, 互动, 发帖, 运营]
  - id: invest
    triggers: [股票, 财报, 估值, 基本面, ETF, 投资]

parallel_rules:
  allow_parallel_if_disjoint_write_sets: true
  prefer_parallel_for_read_only_exploration: true
  avoid_parallel_on_blocking_tasks: true
  max_concurrent_subagents: 2
```

Recommended domain map in this profile:

- `code` -> `codex`
- `knowledge` -> `knowledge`
- `content` -> `content`
- `community` -> `community`
- `invest` -> `invest`

## Recommended Full Template

```yaml
# agent-routing.yaml

task_types:
  - id: explore
    description: Read-only investigation, search, inspection, bounded analysis
    preferred_agent: explorer
    fallback_agent: main

  - id: implement
    description: File changes, content drafting, configuration changes
    preferred_agent: worker
    fallback_agent: main

  - id: verify
    description: Review, testing, validation, comparison
    preferred_agent: main
    fallback_agent: explorer

  - id: operate
    description: External side effects such as archive, publish, update, sync
    preferred_agent: worker
    fallback_agent: main

domains:
  - id: code
    triggers:
      - 代码
      - 写代码
      - 改代码
      - bug
      - debug
      - 报错
      - 修复
      - 功能
      - 开发
      - 实现
      - 重构
      - 接口
      - API
      - 数据库
      - SQL
      - 测试
      - PR
      - git

  - id: knowledge
    triggers:
      - 知识库
      - Obsidian
      - 入库
      - 归档
      - 整理资料
      - 标签
      - 摘要
      - 去重

  - id: content
    triggers:
      - 文案
      - 写作
      - 文章
      - 内容
      - 标题
      - 选题
      - 封面

  - id: community
    triggers:
      - 社区
      - 评论
      - 互动
      - 发帖
      - 运营

  - id: invest
    triggers:
      - 股票
      - 财报
      - 估值
      - 基本面
      - ETF
      - 投资

no_spawn_rules:
  - trigger: "What is"
    action: main
    reason: simple factual question

  - trigger: "你自己来"
    action: main
    reason: user explicitly wants local handling

  - trigger: "配置"
    action: main
    reason: often coupled to current context

  - trigger: "排障"
    action: main
    reason: may require immediate iterative reasoning

parallel_rules:
  allow_parallel_if_disjoint_write_sets: true
  prefer_parallel_for_read_only_exploration: true
  avoid_parallel_on_blocking_tasks: true
  require_main_agent_verification: true

status_model:
  - pending
  - in_progress
  - blocked

## Resume and Recovery

Because routing decisions can spawn long-lived bundles, we treat resume support as part of the runtime configuration. Use `scripts/resume-orchestration.py` to replay an interrupted `examples/orchestration-state.json`, reuse existing `dispatch_id`/`bundle_dir` data, and finish tasks that were already `dispatched` or `running`. Inspect and edit persisted resume metadata beforehand with `scripts/state-store.py update-resume`.
  - needs_review
  - completed
  - abandoned
```

## How To Route A Task

Use this decision order:

```text
1. Check no-spawn rules
2. Infer task type
3. Infer domain
4. Decide whether local handling is cheaper or safer
5. If delegating, create a task contract
6. Dispatch to the preferred agent for that task type
7. Keep verification with the main agent
```

## Classification Examples

| Request | Task Type | Domain | Recommended Handling |
|---------|-----------|--------|----------------------|
| "这个报错是怎么来的" | explore | code | send bounded analysis to explorer |
| "修这个 bug" | implement | code | let main agent scope it, then dispatch worker |
| "帮我检查这个修复有没有回归" | verify | code | keep local or use reviewer, then main verifies |
| "把这篇文章入库" | operate | knowledge | dispatch archive workflow |
| "给我 3 个标题" | implement | content | local or content worker depending on scope |

## No-Spawn Heuristics

Do not dispatch when:

- The answer is short and direct
- The next immediate step depends on the result
- File boundaries are unclear
- The user asked for the current agent specifically
- Dispatch overhead exceeds execution cost

## Integration With MEMORY.md

You can embed the same concepts into `MEMORY.md`:

```markdown
## Orchestration Rules

### Task Types

- explore -> explorer
- implement -> worker
- verify -> main
- operate -> worker

### Domains

- code: 代码, debug, 报错, git
- knowledge: 知识库, Obsidian, 入库
- content: 文案, 写作, 内容

### No-Spawn Rules

- "What is X" -> main
- "你自己来" -> main
- 配置/排障 -> main

### Parallel Rules

- 只在写集不重叠时并行
- 只对读型探索优先并行
- 阻塞任务不要并行外包
```

## Best Practices

1. Task type is more important than domain
2. Treat `implement` tasks as bounded change requests, not general requests
3. Require a task contract before every dispatch
4. Prefer explorer-style agents for read-only analysis
5. Keep final verification and synthesis with the main agent
