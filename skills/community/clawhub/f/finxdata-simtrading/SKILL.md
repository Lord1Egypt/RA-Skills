---
name: finxdata-simtrading
description: 通过专用 X-FINXDATA-TRADING-KEY 使用 FinXData 已开放的 A 股与港股模拟交易能力。适用于用户要求管理 A 股或港股自选股、创建或查询对应市场的模拟账户、提交或查询模拟订单、查看持仓、成交、资金流水、资产与收益、撤单或重置账户的场景。港股模拟交易已完整开放：A 股账户使用人民币和 T+1，港股账户使用港币和 T+0。
---

# FinXData 模拟交易（已支持 A 股与港股）

使用内置 Python 客户端管理 FinXData 自选股和模拟交易。专用 Trading Key 拥有全部模拟交易权限，与普通数据 API Key 及套餐额度相互独立。

当前市场范围：

- A 股：人民币账户，支持自选股、模拟账户、下单、订单、T+1 持仓、成交、资金、资产和收益查询。
- 港股：港币账户，支持相同能力；买入至少为该证券一手，超过一手门槛后可按 1 股递增，持仓按 T+0 可卖。

港股模拟账户、费用、持仓和下单链路均已开放。

## 配置

将用户后台创建的专用 Key 写入 `FINXDATA_TRADING_KEY`。如需切换服务地址，可设置 `FINXDATA_BASE_URL`；默认地址为 `https://api.finxdata.ai`。

不要打印、记录或复述完整 Key。鉴权失败时，请用户在系统外创建或轮换 Trading Key，不要要求用户再次把 Key 粘贴到对话中。

## 执行

在本 Skill 目录运行 `python3 scripts/finxdata_simtrading.py`。脚本输出 JSON；接口或配置出错时以非零状态退出。客户端使用稳定的 FinXData Agent `User-Agent`，避免 Python urllib 默认签名触发生产环境 Cloudflare 拦截。

管理 A 股或港股自选股：

```bash
python3 scripts/finxdata_simtrading.py watchlist list
python3 scripts/finxdata_simtrading.py watchlist add --code 600519 --note "A股长期观察"
python3 scripts/finxdata_simtrading.py watchlist add --code 00700 --note "港股长期观察"
python3 scripts/finxdata_simtrading.py watchlist remove --code 600519
```

创建并查询对应市场的模拟账户和组合：

```bash
python3 scripts/finxdata_simtrading.py accounts create --name "A股模拟账户" --market CN --initial-cash 100000
python3 scripts/finxdata_simtrading.py accounts create --name "港股模拟账户" --market HK --initial-cash 100000
python3 scripts/finxdata_simtrading.py accounts list
python3 scripts/finxdata_simtrading.py accounts list --market HK
python3 scripts/finxdata_simtrading.py accounts list --status archived --limit 20
python3 scripts/finxdata_simtrading.py positions list --account-id 1
python3 scripts/finxdata_simtrading.py assets get --account-id 1
python3 scripts/finxdata_simtrading.py performance get --account-id 1 --period 3m
```

创建账户时不要显式指定结算模式，服务会为 `CN` 选择 `t_plus_1`、为 `HK` 选择 `t_plus_0`。提交模拟订单前生成稳定的 `client_order_id`；相同请求超时或断线重试时必须复用原值，不要重新生成：

```bash
python3 scripts/finxdata_simtrading.py orders place --account-id 1 --client-order-id skill-20260721-0001 --code 600519 --side buy --order-type market --quantity 100
python3 scripts/finxdata_simtrading.py orders place --account-id 2 --client-order-id skill-20260721-hk-0001 --code 00700 --side buy --order-type market --quantity 100
```

港股代码可使用 `00700`、`HK00700` 或 `00700.HK`。下单前读取证券或错误详情确认实际每手数量，不要假设所有港股都是 100 股一手。

## 操作流程

1. 写操作前先读取当前自选股、账户、持仓或订单状态。
2. 仅在用户明确要求时添加或删除自选股。
3. 下单前确认账户市场与证券市场一致：A 股订单使用 `CN` 账户，港股订单使用 `HK` 账户；不要跨市场下单。
4. 下单前复述账户、市场、证券代码、方向、订单类型、数量和限价，仅在用户明确要求模拟买卖后执行。首次请求前生成一个稳定的 `client_order_id`，超时或连接失败时复用同一值。
5. 明确说明成交为模拟结果，数量和费用规则经过简化，可能与真实交易所或券商不同；不要将模拟持仓描述为真实持仓或投资建议。
6. 重置账户会归档历史账户并创建替代账户。必须确认用户的明确意图，并传入 `--confirm RESET`。
7. 收到 `401` 时请用户创建或轮换 `FINXDATA_TRADING_KEY`；收到 `429` 时等待模拟交易独立写限流恢复。不要改用 `X-API-Key` 或登录 JWT。

需要精确参数、响应字段、市场范围、额度行为或业务错误码时，读取 [references/api.md](references/api.md)。脚本也可作为 `FinXDataSimTradingClient` 导入并直接调用方法。
