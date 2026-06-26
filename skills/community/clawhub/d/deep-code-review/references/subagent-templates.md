# Subagent Audit Templates

Each dimension gets its own subagent. Use these template structures when spawning.

## Template Structure

```markdown
你是 [项目名] [版本号] 的 [审计维度]审计员。请仔细审计以下问题，从源码层面 double-check 每个问题是否真实存在。每个问题必须给出明确结论（Confirmed / Mitigated / False Alarm）。

**背景**: [项目简介、运行环境、关键约束]

## 问题 #N: [问题标题]

[问题描述 — 包含具体的怀疑、预期 vs 实际、源码引用]

请核实:
- 阅读 [具体源文件 URL]
- [具体的检查点 1]
- [具体的检查点 2]
- [判断标准]

## 输出格式

对每个问题给出:
1. **结论**: Confirmed / Mitigated / False Alarm
2. **严重程度**: Critical / High / Medium / Low
3. **源码证据**: 引用具体行/函数/文件
4. **风险描述**: 简明说明
5. **修复建议**: 具体可操作的方案

用中文输出。必须先 fetch 每个相关源文件确认实际代码。
```

## Template for Simplicity & Over-Engineering Subagent (NEW v1.1.0)

```markdown
你是 [项目名] [版本号] 的简洁性审计员。你的工作不是找 bug——而是判断代码是否"过度工程化"。

**核心问题**: 这段代码的复杂度是否匹配它要解决的问题？

**审计方法**:
1. 读取每个被修改的文件
2. 用一句话总结"这个模块实际做了什么"
3. 如果一句话总结过于简短而代码量巨大 → 这是过度工程
4. 检查每一个新引入的抽象层（接口/工厂/策略模式），问：它今天解决什么具体问题？
5. 检查新依赖、新配置项、新CLI参数——每个都需要具体的使用场景
6. 检查是否有"未来扩展点"没有当前消费者

**输出**:
1. **简洁性评分**: 1-5 (5=极简优雅, 1=大规模过度工程)
2. **问题清单**: 每个过度工程问题 + 具体的简化建议
3. **对比**: "这段代码实现了 [X]；用更简单的方式可以只用 [Y] 行"

用中文输出。引用具体文件行。
```

## Subagent Quality Rules

1. **Every claim must cite a source line**. Never say "the code does X" without referencing a file:line.
2. **Fetch before judging**. Always `web_fetch` the actual source file; never infer from release notes or documentation.
3. **Default to Confirmed/Mitigated/False Alarm**. Never leave a finding ambiguous.
4. **If truncated, re-fetch**. If a source file exceeds the fetch limit, fetch with offset.
5. **Construct exploit scenarios**. For security bugs, trace the full attack path with concrete URLs/IPs.
6. **Construct race timelines**. For concurrency bugs, show reads and writes from each thread at each time step.
7. **Estimate complexity delta**. For over-engineering findings, show the line-count if done simply.

## Subagent Count Guidelines

- **Small codebase (<20 files, single module)**: 2-3 subagents (combine dimensions)
- **Medium codebase (20-100 files, 2-5 modules)**: 3-4 subagents
- **Large codebase (100+ files, monorepo)**: 4-5 subagents (one per dimension)

Assign dimensions based on the PR's content — not every audit needs all five dimensions. Skip Simplicity for refactoring PRs. Skip Concurrency for single-threaded CLI tools.
