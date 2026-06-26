---
name: ebfx-cli
description: 当用户需要通过 ebfx CLI 在终端查询 EBFX 金融业务平台的数据、报价或运营信息时使用此技能。适用于跨境支付、外汇交易、留学支付场景；当用户提到登录系统、查询 dashboard、pending、deal profit、留学支付报价、学费试算、利润试算、佣金试算、出款方式、支持币种，或要求直接用命令行访问这些业务能力时，应触发此技能。
---

# ebfx

使用 `ebfx` 从终端访问当前项目的业务能力。这个技能重点在“如何触发”和“该落到哪个命令”，而不是系统介绍。

## 何时触发

当用户表达以下意图时，优先使用本技能：

- 要求“用 CLI 查”
- 要求“在终端登录系统”
- 要求“查 dashboard pending”
- 要求“查 deal profit / 利润数据 / finance dashboard”
- 要求“查留学支付报价”
- 要求“按学费金额和币种做试算”
- 要求“查留学支付利润 / 佣金 / 收益”
- 要求“查 price calculator 的结果”
- 要求“查支持币种”
- 要求“查 payout method / 出款方式”

如果用户明确提到 `ebfx`，也直接触发本技能。

## 使用规则

- 默认输出 JSON，适合 agent 和自动化消费
- OpenClaw 通过 `exec` 调用 `ebfx` 时，优先信任运行时注入的 `OPENCLAW_SENDER_ID`
- 如果已经有 `OPENCLAW_SENDER_ID`，不要重复手写 `--sender-id`，除非你明确要覆盖它
- 访问受保护接口前，优先先确认 sender 绑定和 token 状态
- 如果 sender 尚未绑定，先执行 `ebfx auth status`
- 如果 token 不存在或已失效，先执行 `ebfx auth login`
- 受保护命令会按 sender 维度读取 token；不同 Lark 用户会命中不同 token 文件

## 认证命令

适用于：

- “登录系统”
- “退出登录”
- “查看 token 状态”
- “确认 CLI token 存在哪个目录”


```bash
ebfx auth login
ebfx auth logout
ebfx auth token-status
ebfx auth status
```

如果需要显式指定 sender，也可以手动传：

```bash
ebfx auth status --sender-id ou_xxx
ebfx auth login --sender-id ou_xxx
ebfx dashboard pending --sender-id ou_xxx
```

推荐的 OpenClaw 执行顺序：

```bash
ebfx auth status
ebfx auth token-status
ebfx dashboard pending
```

如果 `auth status` 返回未绑定，应停止继续查询并返回授权链接，而不是直接执行业务命令。

## Dashboard 命令

适用于：

- “查 dashboard”
- “查 pending”
- “查 overdue deals”
- “查 auto reversal”

```bash
ebfx dashboard pending
ebfx dashboard pending --type overdue
ebfx dashboard pending --type auto-reversal
```

如果是 OpenClaw 场景，默认直接执行上面的命令即可；sender 会从环境自动解析。

适用于：

- “查 deal profit”
- “查利润数据”
- “查 finance dashboard”
- “按日期查利润”

```bash
ebfx dashboard deal-profit
ebfx dashboard deal-profit --start-date 2026-05-01 --end-date 2026-05-31
ebfx dashboard deal-profit --branch-id 1001 --dealer-id 2002
```

## 留学支付试算命令

适用于：

- “查留学支付报价”
- “查学费报价”
- “做留学利润试算”
- “做佣金试算”
- “查 price calculator”
- “给定学费 38862.20 NZD 算一下”

先查支持币种：

```bash
ebfx edu-calc currencies
```

再查某个币种可用的出款方式：

```bash
ebfx edu-calc payout-methods --currency NZD
```

最后做正式试算：

```bash
ebfx edu-calc price --payout 38862.20 --currency NZD
ebfx edu-calc price --payout 38862.20 --currency NZD --margin 2.5 --percentage 0.4
ebfx edu-calc price --payout 38862.20 --currency NZD --receivable 168000 --commission 1200 --extra-commission 500
ebfx edu-calc price --payout 38862.20 --currency NZD --payout-method 1
```

## 结果理解

- `ebfx auth status` 会返回当前 sender 是否已绑定，以及可能的授权链接
- `ebfx auth token-status` 会返回当前 token 是否存在、token 作用域，以及当前 token 文件路径
- `ebfx edu-calc price` 会返回价格试算结果、利润相关字段，以及 CLI 侧补充计算的 `trial`
- 用户只说“查一下利润”但没有说明是 dashboard 还是留学报价时，优先结合上下文判断：
  - dashboard 运营利润，使用 `ebfx dashboard deal-profit`
  - 留学学费报价利润，使用 `ebfx edu-calc price`
