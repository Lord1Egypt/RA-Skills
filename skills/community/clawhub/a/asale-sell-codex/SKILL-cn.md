---
name: asale-sell-codex
version: 0.2.7
description: "Put a Codex / ChatGPT subscription on the asale market: import it, set a price floor and a concurrency cap, and see which of its models are actually selling. 把 Codex / ChatGPT 订阅挂到 asale 市场上：导入账号、设定价格底价与并发上限，并查看它的哪些模型真的在卖。"
metadata: {"clawdbot":{"emoji":"📤","requires":{"bins":["curl"]},"install":"curl -fsSL https://asale.ai/dl/install.sh | sh","installAlternative":"irm https://asale.ai/dl/install.ps1 | iex","homepage":"https://asale.ai","source":"https://github.com/asale-ai/asale","author":"asale","license":"see-repo","configLocation":"~/.asale/daemon.token","apiEndpoints":["127.0.0.1:9700"]},"openclaw":{"systemPrompt":"Drive the asale daemon at 127.0.0.1:9700 with the token from ~/.asale/daemon.token. Always run list_accounts before set_account_sell for provider codex, and never lower minRatio without asking."}}
---

# asale-sell-codex

[English](./SKILL.md) · [中文](./SKILL-cn.md)

把 Codex / ChatGPT 订阅挂到 asale 市场上：导入账号、设定价格底价与并发上限，并查看它的哪些模型真的在卖。

## 触发关键词

- 卖 Codex 订阅
- ChatGPT Plus / Pro 上架
- 出租 Codex 额度
- asale 卖出 codex

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

卖出是**按订阅账号**的，不是按机器。守护进程持有该账号凭证的自有副本（卖出侧从不读写
CLI 自己的配置），把账号的模型作为**车道（lane）**申报给市场，然后用它服务别人的请求——
在你设定的限制内：一个价格底价、同时服务几个请求、以及可选的每日 token 上限。

市场价跌破你的底价时，车道会自己下市；价格回来了它自己上架。这中间不需要谁去关一次
再开一次。

凭证来自 macOS 钥匙串条目 `Codex Auth` 或 `~/.codex/auth.json`。Codex 是唯一一个
光有 token 还不够的厂商——ChatGPT 后端要求同时带上 `chatgpt-account-id` 头，所以导入时
会把这个 id 跟 bearer 一起带上。少了它就是一个 401，看起来和「登录被吊销」一模一样。
## 使用方法

### 1. 找到这个订阅

```bash
call discovery_scan          # 这台机器上有什么——只看，不导入
call import_cli_all          # 把找到的都导入
call list_accounts           # 已接入的账号，以及它们各自的条件
```

Codex 订阅在 `Codex Auth` 钥匙串条目或 `~/.codex/auth.json` 里。套餐
（`chatgpt_plan_type`）和账号邮箱是从 token 自己的 claim 里解出来的，所以不用调任何上游
接口就能把订阅认出来。

挑 `provider` 是 `codex` 的那一行，它的 `account_id` 就是后面每个调用用来指代它的名字。

### 2. 上架

```bash
call set_account_sell '{"provider":"codex","accountId":"<id>","enabled":true,"minRatio":10,"concurrency":5,"dailyLimit":0}'
```

`enabled` 之后的字段都是可选的，不传就保持当前值。`dailyLimit` 单位是 token，`0` 表示不限。

### 价格底价

`minRatio` 是**占厂商原价的整数百分比**——`60` 就是「低于原价六成我不卖」，`100` 是原价。

- `5` 是平台地板价。市场永远不会定到它以下，所以底价设成 5 等于什么都不会被撤下。
- `10` 是新账号的默认底价。

没有「不限价格」这个选项：每个账号都按一条底价成交。调低底价是一个关于钱的真实决定——
先提议，别直接改。


### 3. 看实际在卖什么

```bash
call list_lanes '{"provider":"codex","accountId":"<id>"}'
```

每个模型一行：`status`、`paused_reason`、`requires_user`、`ratio`（市场现在出的价）、
`min_ratio`（你的底价）。

| `status` | 含义 |
| --- | --- |
| `selling` | 在市场上。 |
| `withheld` | 低于你的底价（`paused_reason: "price"`），价格回升后自己上架。 |
| `cooldown` | 刚出过错，`resume_at` 时自动回来。 |
| `paused` | 需要人处理。看 `paused_reason`，修好之后再 `resume_lane`。 |
| `exhausted` | 订阅自己的额度窗口用完了。 |
| `expired` | 凭证需要重新认证。 |

```bash
call resume_lane '{"provider":"codex","accountId":"<id>","model":"<model>"}'
```

### 4. 下架

```bash
call set_account_sell '{"provider":"codex","accountId":"<id>","enabled":false}'
```

**AGENT 关键指令**：

1. 每次 `set_account_sell` 之前都先 `list_accounts`。开关、底价、并发是各自独立的，
   拿着过期的读数去写会静默覆盖掉用户自己选的值。
2. 绝不主动调低 `minRatio`。把数字和理由摆出来，让用户回答。
3. `resume_lane` 只在 `paused_reason` 指的问题真的修好之后再调。暂停条件还在就去清它，
   车道只会立刻再暂停一次，而每来一轮都在扣卖家的信誉分。
4. 卖出被 `errors.session.signInToSell` 拒绝时，停下并说明。

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
