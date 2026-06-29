# Profile Template

> ⚠️ All sample data below is placeholder. The agent fills in real data from
> memory at runtime. 以下示例数据已脱敏为占位值,Agent 执行时替换为真实记忆数据。

## Full output format — example (English)

````markdown
## Instructions

[2026-01-01] - Reporting format: ① conclusion → ② process / things to watch → ③ todo list
[2026-01-01] - For long-running tasks: report progress every 4 hours; notify immediately on completion
[unknown] - When unsure, don't guess — self-check first, then ask the user with a concrete example
[unknown] - Do NOT run `git stash` or publish releases without explicit authorization

## Identity

[unknown] - Name: Jane Doe (nickname: J)
[unknown] - Birthplace: San Francisco, CA
[YYYY-MM-DD] - Birth year: 1990
[unknown] - Education: B.S. Computer Science, Stanford University
[unknown] - Languages: English (native), Spanish (conversational)
[unknown] - Interests: rock climbing, indie game dev, sourdough baking

## Profession

[YYYY-MM-DD] - Company: Acme Corp
[YYYY-MM-DD] - Role: Senior Product Engineer
[unknown] - Skill domains: Python, TypeScript, system design, LLM integrations

## Projects

[YYYY-MM-DD] - my-cli-tool: zero-dependency dev productivity CLI; in active development; key decision: keep it Bash-only for portability
[YYYY-MM-DD] - team-dashboard: internal metrics dashboard; shipped v1.0; key decision: SQLite over Postgres for simpler ops

## Preferences

[unknown] - Likes terse, direct technical writing — no marketing fluff
[unknown] - Prefers function-level commits over feature-level commits
[unknown] - Always wants test cases co-located with source code
````

## Full output format — example (中文示例)

````markdown
## 指令

[2026-01-01] - 汇报格式:①结论 → ②过程/需关注事项 → ③待办清单
[2026-01-01] - 长时任务完成后立即告知;超时每 4 小时汇报进度
[unknown] - 遇到不确定时不要猜,先自查,查不到再问用户要样例
[unknown] - 禁止未授权执行 git stash 或发布版本,遇到需要发布时停下来等确认

## 身份

[unknown] - 姓名:张三(花名:小三)
[unknown] - 出生地:北京
[YYYY-MM-DD] - 出生年:1990
[unknown] - 教育:清华大学计算机本科
[unknown] - 语言:中文(母语)、英文
[unknown] - 兴趣:摇滚乐、独立游戏开发、烘焙

## 职业

[YYYY-MM-DD] - 公司:某科技公司
[YYYY-MM-DD] - 职位:资深产品工程师
[unknown] - 技能领域:Python / TypeScript / 系统设计 / LLM 集成

## 项目

[YYYY-MM-DD] - my-cli-tool:零依赖开发效率 CLI;进行中;关键决策:坚持纯 Bash 实现保证可移植性
[YYYY-MM-DD] - team-dashboard:团队内部指标看板;v1.0 已上线;关键决策:用 SQLite 而非 Postgres 简化运维

## 偏好

[unknown] - 喜欢简洁直接的技术写作,不要营销腔
[unknown] - 偏好函数级 commit,而非特性级 commit
[unknown] - 测试代码必须与源代码放在一起
````

## Category criteria

### Instructions — what to include

- ✅ User explicitly said "always do X" / "never do Y" / "remember from now on"
- ✅ User corrected the assistant's behavior and asked for a change
- ✅ Rules marked with ⚠️ in MEMORY.md / AGENTS.md / CLAUDE.md
- ❌ Implied preferences inferred by the agent (put those under Preferences)
- ❌ One-time requirements from the current session only

### Privacy filter

When scanning memory, **skip** these fields:

- Government IDs, phone numbers, home addresses
- Account IDs, passwords, tokens, API keys, secrets
- Specific financial data or salary information
- Detailed family member information (unless the user has actively, explicitly
  shared it)

## File output

- Default path: `./my-profile.md` (current working directory)
- The user can rename / move freely after generation
- If overwriting existing `my-profile.md`, ask for confirmation first
