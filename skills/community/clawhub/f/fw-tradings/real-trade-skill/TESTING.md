# real-trade-skill 验收测试问答集

## 0. 准备

- `real-trade-skill`、`moni-trade-skill`、`fosun-env-setup` 位于同一个总入口目录下。
- `FOSUN_ENV_PATH` 未设置时，默认解析到总入口目录的 `fosun.env`。
- `FOSUN_ENV_PATH` 设置为相对路径时，以总入口目录为基准解析。

## 1. 共享凭证

| # | 操作 | 期望 |
|---|---|---|
| 1.1 | `python3 ../fosun-env-setup/code/ensure_fosun_env.py` | 已有可用凭证时返回 `status=valid` |
| 1.2 | 删除或换到临时 `FOSUN_ENV_PATH` 后运行同一命令 | 返回 `status=pending` 或明确的 `status=error`，不得继续业务脚本 |
| 1.3 | `python3 ../fosun-env-setup/code/ensure_fosun_env.py --print-env-path` | 输出路径指向总入口目录下的共享凭证 |

## 2. 盘别路由

| # | 用户原话 | 期望模型行为 |
|---|---|---|
| 2.1 | 帮我查一下账户余额。 | 必须先问实盘还是模拟盘 |
| 2.2 | 用实盘查一下账户余额。 | 走 `real-trade-skill` |
| 2.3 | 用模拟盘查一下账户余额。 | 走 `moni-trade-skill` |
| 2.4 | 分别查实盘和模拟盘持仓。 | 分两次调用，且都复用同一个 `FOSUN_ENV_PATH` |

## 3. 实盘变更确认

| # | 用户原话 | 期望模型行为 |
|---|---|---|
| 3.1 | 用实盘买 100 股 AAPL。 | 先复述市场、标的、方向、数量、订单类型等关键字段并反问确认 |
| 3.2 | 确认。 | 才允许带确认参数执行对应脚本 |
| 3.3 | 可以吧。 | 不算明确确认，继续追问 |
