---
name: asale-buy-opencode
version: 0.2.7
description: "Switch opencode between buying from the asale market and using its own subscription, and see which running sessions are still on the old config. 在「从 asale 市场买」和「用它自己的订阅」之间切换 opencode，并查看哪些正在运行的会话还用着旧配置。"
metadata: {"clawdbot":{"emoji":"📥","requires":{"bins":["curl"]},"install":"curl -fsSL https://asale.ai/dl/install.sh | sh","installAlternative":"irm https://asale.ai/dl/install.ps1 | iex","homepage":"https://asale.ai","source":"https://github.com/asale-ai/asale","author":"asale","license":"see-repo","configLocation":"~/.asale/daemon.token","apiEndpoints":["127.0.0.1:9700"]},"openclaw":{"systemPrompt":"Drive the asale daemon at 127.0.0.1:9700 with the token from ~/.asale/daemon.token. Always run buy_tools before set_buy_tool for tool opencode. tool_processes is listing only — never signal those pids."}}
---

# asale-buy-opencode

[English](./SKILL.md) · [中文](./SKILL-cn.md)

在「从 asale 市场买」和「用它自己的订阅」之间切换 opencode，并查看哪些正在运行的会话还用着旧配置。

## 触发关键词

- 让 opencode 从市场买
- 把 opencode 指向 asale
- 给 opencode 加 asale provider
- asale 买入 opencode

## 身份验证 (Authentication)

有两件事必须同时成立。

**1. 本机守护进程要在跑，并且你需要它的 token。** `asaled` 首次启动会写
`~/.asale/daemon.token`（0600），之后每个 `/rpc` 调用都必须带上它——走回环也一样。

```bash
asale status            # 守护进程在不在，监听哪个端口
asale start             # 没在跑就启动
```

```bash
# 每个 /rpc 调用都要带上守护进程 token——走回环也一样。
TOKEN=$(cat ~/.asale/daemon.token)
call() {
  body=$2; [ -n "$body" ] || body='{}'
  # --noproxy is not optional: a machine with HTTP_PROXY set sends even
  # 127.0.0.1 through it, and the proxy answers 502 with an empty body,
  # which reads exactly like a broken daemon.
  curl -sS --noproxy 127.0.0.1 -X POST "http://127.0.0.1:9700/rpc/$1" \
    -H 'content-type: application/json' -H "x-asale-token: $TOKEN" -d "$body"
}
```

连接被拒绝就是守护进程没起来——直接说明并停下，起不起是用户的决定。

`~/.asale/asaled.bind` 存着上次 `asale start` 用的端口，读不到就回落
`127.0.0.1:9700`。监听在 `0.0.0.0` 不是一个可以拨的地址——保留端口、换回环。

**2. 买入和卖出都需要已登录的 asale 账号。** 消费密钥由守护进程签发，卖家身份也是
挂在这个会话上的。命令行没有登录入口：打开应用（`asale open`）在里面登录。没登录会拿到
`errors.session.signInToSell` / `errors.session.signInToBuy`——这不是可以绕开的东西。

## 关于与来源 (Provenance)

- **源码**：[github.com/asale-ai/asale](https://github.com/asale-ai/asale)
- **主页**：[asale.ai](https://asale.ai)
- **安装**：`curl -fsSL https://asale.ai/dl/install.sh | sh`（Windows：
  `irm https://asale.ai/dl/install.ps1 | iex`）。`asale update` 会重跑同一个安装器。
- **配置**：`~/.asale/` —— token、SQLite 存储和守护进程日志都在这里，`$ASALE_DATA_DIR`
  可以整体搬走。

这个技能只跟**你自己机器上**的守护进程说话。它不直接访问 asale 服务器——那是守护进程用
它自己的已认证会话去做的。技能读到的唯一凭证就是那个 token 文件，且它不会离开回环接口。

## 工作原理

买入是把某个本机已装的 AI CLI 指向 asale 的本地代理，而不是指向厂商。开关会改写**那个
工具自己的**配置文件——只改它自己的，所以各个开关完全独立——并注入一个 asale key，工具的
配置里不必明文持有它。它碰的每个文件都会先快照，所以关掉开关能逐字节还原。

之后请求会走到代理，代理逐个请求做决定：你自己的订阅窗口还有余量且模式允许，就直接打
上游、不产生费用；否则就从市场买。

关于 opencode 的配置有两件事值得知道，因为两件都是问二进制本体问出来的，不是文档写的：

- 目录在**所有**平台上都是 XDG 风格，Windows 也不例外：`opencode debug paths` 回答的是
  `C:\Users\<u>\.config\opencode`，不是 `%APPDATA%`。
- opencode 同时接受 `opencode.json` 和 `opencode.jsonc`，两个都在时**`.jsonc` 赢**——而且
  opencode 首次运行会自己写一个 `.jsonc` 桩。所以在任何跑过 opencode 的机器上，生效的都是
  它。asale 会改已经存在的那个，一个都没有时才创建 `.jsonc`。

开关会拒绝改写一个它无法原样往返的配置：`.jsonc` 允许注释而写入器输出纯 JSON，所以带注释
的文件会被原样留下并报错，而不是被静默剥掉注释。

opencode 走它自己的 `/opencode/v1` 前缀，原因和 OpenClaw 一样——方言分辨不了它们。

## 使用方法

### 1. 先看再动

```bash
call buy_tools
call market_models          # 目录，用来挑模型 id
```

`opencode` 那一行带着 `installed`、`enabled`（开关）、`in_effect`（它的实时配置真的指向代理）、
`models` 和 `config_paths`。

**这个工具必须选模型。** 它只提供配置里写明的模型，所以 `models` 为空就等于装了
asale provider 却没有任何模型可选。不选就开开关不是一个能用的状态——要说明，而不是报「完成」。

### 2. 打开买入

```bash
call set_buy_tool '{"tool":"opencode","enabled":true,"models":["claude-fable-5"]}'
```

不传 `models` 就保持当前选择，传 `[]` 是清空。会改写的配置：`~/.config/opencode/opencode.jsonc`（或 `opencode.json`，取决于哪个是生效的那个）—— 一个 `provider.asale` 块外加顶层的 `model`。

### 3. 说清楚哪些会话还在用旧配置

```bash
call tool_processes
```

opencode **只在启动时**读一次配置，所以已经在跑的会话拿的还是旧的。`running.opencode` 会按 pid 列出
它们，并带上启动时的命令行。

`scanned: false` 表示读不到本机进程表——那是「不知道」，不是「没有在跑」，不能当成后者报。

### 4. 关掉买入

```bash
call set_buy_tool '{"tool":"opencode","enabled":false}'
```

原配置会逐字节还原。

### 如果 `enabled` 是 true 但 `in_effect` 是 false

说明 asale 写完之后有别的东西又改了配置（另一个切换器、编辑器、安装程序）。重跑第 2 步
即可修复；`open_config_path` 可以把文件打开给用户自己看。

```bash
call open_config_path '{"path":"<config_paths 里的某一个>"}'
```

**AGENT 关键指令**：

1. 每次 `set_buy_tool` 之前都先 `buy_tools`。开关和模型选择是独立的，拿过期读数去写会
   静默覆盖用户自己选的。
2. **绝不要把 `tool_processes` 列出的 pid 当成「可以杀掉的东西」列出来，更不要去杀。**
   CLI 挂在终端上，外部进程没法把一个新进程接回那个终端；杀掉就是丢掉它正在做的事。
   把它们报出来，让用户自己决定重启哪个。
3. 打开开关之后，要告诉用户它对该工具的**下一次**启动才生效。当前会话还在花用户自己的
   订阅，却把开关报成「已完成」，那是一个错误的答案。
4. 买入被 `errors.session.signInToBuy` 拒绝时，停下并说明。

## 错误处理

| 状态码 | 错误类型 | 示例信息 |
| --- | --- | --- |
| — | 守护进程没起来 | `curl: (7) Failed to connect to 127.0.0.1 port 9700` |
| 401 | token 缺失或不对 | `{"key":"errors.daemon.unauthorized","message":"unauthorized (missing or bad X-Asale-Token)"}` |
| 400 | 未登录（卖出） | `{"key":"errors.session.signInToSell","message":"sign in before selling"}` |
| 400 | 未登录（买入） | `{"key":"errors.session.signInToBuy","message":"sign in before buying"}` |
| 400 | 账号不存在 | `{"message":"unknown account"}` |
| 400 | 工具 id 不对 | `{"message":"unknown tool: <id>"}` |

> **AGENT 关键指令**：
> 1. 错误里除了 `message` 还有 `key`。`key` 是稳定的翻译 id——原样引用，不要转述 message。
> 2. 遇到 `errors.session.signInToSell` / `errors.session.signInToBuy`，让用户去应用里
>    登录（`asale open`），然后停下。不要重试，也不要去找别的路子达成同样的效果。
> 3. 连接失败就报「守护进程没在跑」，起不起交给用户。不要自作主张跑 `asale start`。

## Tips

更多信息见 https://asale.ai。同样的开关在桌面应用和浏览器里都有界面——`asale open`
就能打开，这个技能做的每一件事都可以在那里核对。
