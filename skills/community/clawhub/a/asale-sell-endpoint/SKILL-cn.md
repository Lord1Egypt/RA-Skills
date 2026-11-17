---
name: asale-sell-endpoint
version: 0.2.7
description: "Sell a custom OpenAI-compatible endpoint on the asale market: probe it, connect it as an account, and price it above what its own tokens cost. 把自定义 OpenAI 兼容端点挂到 asale 市场上卖：先探测、接入成账号，并把价格定在它自己的 token 成本之上。"
metadata: {"clawdbot":{"emoji":"📤","requires":{"bins":["curl"]},"install":"curl -fsSL https://asale.ai/dl/install.sh | sh","installAlternative":"irm https://asale.ai/dl/install.ps1 | iex","homepage":"https://asale.ai","source":"https://github.com/asale-ai/asale","author":"asale","license":"see-repo","configLocation":"~/.asale/daemon.token","apiEndpoints":["127.0.0.1:9700"]},"openclaw":{"systemPrompt":"Drive the asale daemon at 127.0.0.1:9700 with the token from ~/.asale/daemon.token. connect_custom_endpoint spends and stores the user's API key — confirm before calling. Never call remove_custom_endpoint."}}
---

# asale-sell-endpoint

[English](./SKILL.md) · [中文](./SKILL-cn.md)

把自定义 OpenAI 兼容端点挂到 asale 市场上卖：先探测、接入成账号，并把价格定在它自己的 token 成本之上。

## 触发关键词

- 卖自定义端点
- 转卖 OpenAI 兼容 API
- 把自建端点接入 asale
- asale 卖出 端点

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

自定义端点和别的账号一样是作为「账号」来卖的，区别只在于它的凭证是你提供的 API key，
而不是这台机器本来就登录过的订阅。它也是唯一一种「token 有边际成本」的卖家——底价必须
对着这个成本来定。

## 使用方法

### 1. 接入端点

```bash
call connect_custom_endpoint '{"baseUrl":"https://api.example.com/v1","apiKey":"<key>","label":"house","minRatio":10,"concurrency":5}'
```

守护进程会**先**校验 URL、用这个 key 探测 `GET {base}/models`，**然后才存**任何东西——
所以主机写错或 key 失效会在这一步失败，而不是在第一个买家那里。`wire` 可以不传：不传时
探测器会挨个试各种方言、保留第一个能答的，这是个正确的默认值，因为接入的那一刻恰恰是
操作者最不确定的时候（不少同时提供 `/messages` 的主机也写着「OpenAI 兼容」）。

返回值会说明发生了什么：

| 字段 | 含义 |
| --- | --- |
| `account_id` | 后面每个调用用来指代它的账号 id。 |
| `wire` | 端点实际应答的协议。 |
| `endpoint_models` | 它一共提供多少模型。 |
| `sellable_models` | 其中市场会交易的有多少。 |

用同一个 `label` 再跑一次就是原地更新这个账号——端点、key、条件全部重写，缓存的模型列表
也会被替换。

### 2. 复核并调整条件

```bash
call list_custom_endpoints
call custom_endpoints_status
call set_account_sell '{"provider":"custom","accountId":"<id>","enabled":true,"minRatio":30,"concurrency":10}'
```

### 价格底价

`minRatio` 是**占厂商原价的整数百分比**——`60` 就是「低于原价六成我不卖」，`100` 是原价。

- `5` 是平台地板价。市场永远不会定到它以下，所以底价设成 5 等于什么都不会被撤下。
- `10` 是新账号的默认底价。

没有「不限价格」这个选项：每个账号都按一条底价成交。调低底价是一个关于钱的真实决定——
先提议，别直接改。

计量收费的端点是底价唯一不只关乎利润的场景：定得比你自己的 token 成本还低，每卖一笔都在
亏钱。提议数字之前，先按端点自己的价目表把它算出来。

### 3. 刷新或移除

```bash
call refresh_custom_endpoint '{"accountId":"<id>"}'   # 重新探测模型列表
call set_account_sell '{"provider":"custom","accountId":"<id>","enabled":false}'
```

**AGENT 关键指令**：

1. `connect_custom_endpoint` 会花用户的 key 发一次探测请求，并把 key 存下来。调用之前先跟
   用户确认 URL 和 key——绝不能把它当成别的事情的顺带一步。
2. 绝不调用 `remove_custom_endpoint`。关掉卖出是可逆的，删掉账号不是。
3. `minRatio` 要按端点真实的每 token 成本来定，不要用默认值。默认值是为订阅准备的——
   订阅的边际 token 早就付过钱了。
4. 把 `sellable_models` 念回给用户。「接入成功，400 个模型，其中 12 个在卖」才是他们要的
   答案，光说「接入成功」不是。

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
