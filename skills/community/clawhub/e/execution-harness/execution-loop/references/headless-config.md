# Headless Execution Control

## Problem

`claude -p` (headless) 模式没有 Stop 事件循环，Ralph 的 Stop hook 不生效。Headless agent 行为由 `--max-turns`、prompt 结构、budget 注入共同控制，但配置不当会导致：任务做一半就到 turn 上限停了，或者 token 预算耗尽但任务还差最后一步。

## Solution

为 headless 模式提供三维控制：`--max-turns` 限制执行轮数，prompt 结构确保关键指令在 prefix cache 范围内，budget 注入让 agent 感知资源约束并做优先级决策。三者协同替代 interactive 模式下的 Ralph + Stop hook。

## Implementation

1. **--max-turns 估算**：根据任务复杂度设置。简单任务 10-20，中等 30-50，复杂 80-120。设置过低会截断任务，过高浪费资源
2. **Prompt 结构**：系统指令放在 prompt 开头（前 ~2000 token），利用 Anthropic 的 prefix cache。任务细节紧随其后。动态 context（文件内容）放末尾
3. **Budget 注入**：在 prompt 中显式告知 agent 资源约束

```bash
# Headless 执行模板
claude -p \
  --max-turns 50 \
  --allowedTools "Read,Write,Edit,Bash,Glob,Grep" \
  "$(cat <<'PROMPT'
[SYSTEM] 你的执行预算：50 轮 / ~200K token。
在第 40 轮时如果任务未完成，开始做收尾工作（保存进度、写 handoff 文档）。
不要把预算浪费在探索性操作上——先规划再执行。

[TASK]
修改 src/parser.ts 支持新的 AST 节点类型...
PROMPT
)"
```

4. **阶段性 budget 告知**：若有多轮 headless 调用（pipeline），每次调用时告知当前阶段和剩余预算

```bash
# Pipeline 中的第 2 阶段
claude -p --max-turns 30 \
  "$(cat <<PROMPT
[阶段 2/4] 实现阶段。前序阶段（Research）已完成，结果见 .working-state/research-output.md。
本阶段预算：30 轮。完成后将结果写入 .working-state/implementation-output.md。
PROMPT
)"
```

## Tradeoffs

- **Pro**: 可预测的资源消耗，适合 CI/CD 和 automation
- **Pro**: Prompt 结构化利用 prefix cache 降低成本
- **Con**: 没有 Stop hook 的灵活性——不能动态决定是否继续
- **Con**: max-turns 估算依赖经验，没有自动调优

## Source

Claude Code `-p` 模式文档。OMC 的 pipeline 执行系统（多阶段 headless 调用 + handoff 文件传递）。Claude Anthropic prefix caching 文档。
