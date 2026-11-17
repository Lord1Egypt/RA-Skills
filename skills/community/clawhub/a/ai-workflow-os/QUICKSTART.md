# Quickstart / 快速开始

Router. Install this so your agent knows **which** specialist skill to hand a
request to when it spans more than one area.

## Install / 安装

```bash
openclaw skills install ai-workflow-os
```

## When to use / 什么时候用

A single request crosses several surfaces — intake plus coding plus memory plus
research — and it is not obvious which skill should own it.

## Try it in 30 seconds / 30 秒验证

Say to your agent / 对 agent 说：

```text
我想把这个调研变成一个新项目，还要能每天接着做
```

You should get / 你应该得到：

- an explicit routing order — who runs first, who runs next;
- one writer per state file, so no two skills write competing state.

## Safety / 安全

- Routes only. Routing is not authorization — it never approves work for you.
- Delegates to specialist skills when they are installed.
- Runs locally and stores no credentials.
