# Quickstart / 快速开始

Advanced. This is the control plane — use it when **the goal itself is still
unclear**. If the goal and acceptance criteria are already clear, use
`agent-loop-engineering` instead.

## Install / 安装

ClawHub slug / 商店名是 **`coding-management-system`**：

```bash
openclaw skills install coding-management-system
```

## When to use / 什么时候用

- 想做个东西但说不清到底要什么
- 老项目文档互相打架，不知道哪个算数
- 需要 QA 验收、目标重基线，或把模糊需求收敛成可执行范围

## Try it in 30 seconds / 30 秒验证

Say to your agent / 对 agent 说：

```text
我想做个 XX，但说不清要什么，帮我理清楚
```

You should get / 你应该得到：

- one compact delivery state — target, Non-Goals, scope, acceptance;
- conflicts flagged explicitly instead of being silently merged;
- an explicit stop at anything that needs your decision.

## Safety / 安全

- Does not write product code on its own.
- Stops for your decision on target, production, credentials, deployment,
  paid resources or destructive actions.
- Stores no API keys, tokens or credentials.
