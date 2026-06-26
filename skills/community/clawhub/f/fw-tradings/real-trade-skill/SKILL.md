---
name: real-trade
description: 复星财富港美股实盘 OpenAPI skill。通过 `FOSUN_ENV_PATH` 复用总入口共享 `fosun.env`；未设置时由运行时解析到与本 skill 并列的 `fosun.env`。用于明确选择实盘后的账户、资产、行情、订单和交易操作。
version: 1.8.0
requires:
  bins:
    - bash
    - curl
install: install.sh
---

# real-trade — 复星实盘 OpenAPI Skill

这是实盘子 skill。它只负责在用户明确选择`实盘`后执行实盘相关接口；共享凭证的生成与修复由同级 `fosun-env-setup` 负责。

## 最高优先级规则

1. 用户没有明确选择`实盘`时，禁止调用本 skill。
2. 实盘下单、改单、撤单等变更动作必须先复述完整意图，并等待用户明确确认。
3. 全局只使用一个共享凭证：`FOSUN_ENV_PATH` 指向的 `fosun.env`。
4. 禁止为实盘或模拟盘复制第二份凭证文件。
5. 禁止在命令或文档里写死某台机器的绝对路径；需要绝对路径时，只能由环境变量和相对路径在运行时解析得到。

## 共享凭证路径

推荐起手式：

```bash
export SKILL="<real-trade-skill 绝对路径>"
export FOSUN_PY="<python 绝对路径>"   # 总入口 install.sh 共享 venv，默认 fw-trade-skill/.venv/bin/python
export REAL_PY="${FOSUN_PY}"
export FOSUN_ENV_PATH="${FOSUN_ENV_PATH:-$SKILL/../fosun.env}"
```

路径解析规则：

- `FOSUN_ENV_PATH` 未设置：脚本默认使用总入口目录下的 `fosun.env`
- `FOSUN_ENV_PATH` 是相对路径：以总入口目录为基准解析
- `FOSUN_ENV_PATH` 是绝对路径：直接使用

同一个 `fosun.env` 同时供 `real-trade-skill` 和 `moni-trade-skill` 使用。

## 使用前检查

任何业务脚本前，先确保共享凭证存在：

```bash
python3 ../fosun-env-setup/code/ensure_fosun_env.py
```

结果处理：

- `status=valid`：继续执行实盘凭证体检或业务脚本
- `status=pending`：把脚本 JSON 输出里的 `exact_open_url` / `open_url` 逐字符原样给用户完成 OpenAPI 开通，禁止手写或改写 URL；用户在页面完成开通后重试，脚本通过 finalize（APIKeyCheck + 签名请求）验证
- `status=error`：停止实盘业务，先按 `message` 修复凭证生成问题

已有凭证但需要修复时：

```bash
python3 ../fosun-env-setup/code/ensure_fosun_env.py --repair
```

## 合法脚本清单

只允许调用 `code/` 目录中真实存在的脚本。跑命令前先逐字符核对文件名，禁止按英文习惯脑补。

| 类型 | 脚本 | 作用 |
|---|---|---|
| 凭证/账户 | `check_shared_env.py` | 检查共享凭证并刷新账户索引 |
| 凭证/账户 | `account_list.py` | 查询账户列表 |
| 凭证/账户 | `sync_accounts.py` | 强制刷新账户索引 |
| 资产 | `cash_summary.py` | 查询现金与购买力 |
| 资产 | `holdings.py` | 查询持仓 |
| 资产 | `cash_flows.py` | 查询资金流水 |
| 订单 | `order_list.py` | 查询订单列表 |
| 交易变更 | `order_create.py` | 下单，必须二次确认 |
| 交易变更 | `order_modify.py` | 改单，必须二次确认 |
| 交易变更 | `order_cancel.py` | 撤单，必须二次确认 |
| 行情 | `market_quote.py` | 实时报价 |
| 行情 | `market_orderbook.py` | 盘口 |
| 行情 | `market_kline.py` | K 线 |
| 行情 | `market_min.py` | 分时 |
| 行情 | `market_tick.py` | 逐笔成交 |
| 行情 | `market_broker_list.py` | 经纪商队列 |

## 调用顺序

1. 确认用户选择的是`实盘`
2. 运行 `../fosun-env-setup/code/ensure_fosun_env.py`
3. 凭证 `status=valid` 或完成开通后，按用户意图选择本 skill 的脚本
4. 查询类脚本执行后只汇报结果并停手
5. 变更类脚本必须先复述意图并等待明确确认，再带确认参数执行

## 变更操作二次确认

所有实盘变更操作都必须分三步：

1. 用自然语言复述完整意图，包括市场、标的、方向、数量、价格、订单类型或订单号。
2. 明确反问用户是否确认执行。
3. 只有用户明确肯定后，才运行对应脚本并带上确认参数。

模糊回答不算确认，例如“嗯”“可以吧”“你看着办”。必须继续追问。

## 错误处理

脚本失败时先读 stderr/stdout 中的结构化字段，尤其是 `error_code`、`message`、`next_action`。不要凭直觉重复提交命令。

常见处理：

- 共享凭证不存在：回到 `fosun-env-setup` 生成
- 共享凭证无效：运行 `fosun-env-setup --repair` 或按错误信息重新开通
- 用户未明确选择实盘：停手追问盘别
- 变更参数不完整：停手向用户确认缺失字段

## 目录结构

```text
real-trade-skill/
├── SKILL.md
├── README.md
├── _meta.json
├── install.sh              # 兼容入口 → 转调 ../install.sh
└── code/
```
