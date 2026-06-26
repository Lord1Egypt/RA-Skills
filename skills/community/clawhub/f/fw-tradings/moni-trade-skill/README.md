# moni-trade-skill

> 模拟盘子 skill。通过 `FOSUN_ENV_PATH` 复用共享凭证；未设置时自动解析到总 skill 根目录的 `fosun.env`，只执行模拟盘接口，不负责凭证生成或修复。

## 起手式（每个新会话先跑一次）

```bash
export SKILL="<moni-trade-skill 绝对路径>"
export FOSUN_PY="<python 绝对路径>"   # 总入口 `bash ../install.sh` 创建的共享 venv，默认 `fw-trade-skill/.venv/bin/python`
export MONI_PY="${FOSUN_PY}"
export FOSUN_ENV_PATH="${FOSUN_ENV_PATH:-$SKILL/../fosun.env}"
```

> `$MONI_PY` 就是 `install.sh` 用 [uv](https://docs.astral.sh/uv/) 自动创建的独立 venv 里的 Python 解释器（uv 自动下载并锁定 3.13，**不依赖系统 Python**）。直接调用比再套一层 `uv run` 少 150–300ms 的环境解析开销，所以速抄表统一用 `$MONI_PY`。
>
> `$SKILL`、`$MONI_PY` 随安装位置而变；**唯一固定的相对关系**是共享凭证 `fw-trade-skill/fosun.env` 与 `moni-trade-skill` 并列，故用 `$SKILL/../fosun.env`。不设 `FOSUN_ENV_PATH` 时，脚本也会从 `code/_client.py` 推出同一路径。

## 使用前提

- `FOSUN_ENV_PATH` 指向的共享凭证文件已存在
- 该共享凭证已通过同级 `fosun-env-setup` 生成或修复
- 当前操作已明确选择为`模拟盘`

## 最简使用

```bash
# macOS / Linux
bash ./install.sh

# Windows (PowerShell)
powershell -ExecutionPolicy Bypass -File .\install.ps1

$MONI_PY $SKILL/code/check_shared_env.py
$MONI_PY $SKILL/code/account_list.py
```

安装脚本会自动下载并安装官方 `fsopenapi` SDK，默认版本为 `v1.2.0`。
下载主源默认是 GitHub；主源失败时会自动读取 `../fosun-env-setup/code/ensure_fosun_env.py` 中的
`DEFAULT_SDK_ZIP_FALLBACK_URL` 作为备用源（实现一处改动全局生效）。
可用 `MONI_SDK_VERSION` / `MONI_SDK_URL` / `MONI_SDK_FALLBACK_URL` 覆盖。

## 核心规则

- 只读取 `FOSUN_ENV_PATH` 指向的共享凭证
- 推荐写法：`FOSUN_ENV_PATH=fosun.env`，由脚本自动解析成总 skill 根目录下的绝对路径
- 不生成、不复制、不维护第二份凭证
- 共享凭证无效时，必须先通过同级 `fosun-env-setup` 生成或修复
- 模拟盘只支持港股、美股正股；不支持 A 股和期权
- 模拟盘下单只支持 `3=限价单`、`9=市价单`；**模拟盘不支持预埋单**，非交易时段也只是普通下单，不要把"预埋"当成额外订单类型
- 子账户解析默认走 `FOSUN_ENV_PATH` 指向的共享凭证中的 `FSOPENAPI_ACCOUNT_INDEX` 缓存，零额外网络；缓存失效会自动刷新并重试一次

## 子账户索引缓存

第一次跑任意脚本时，会自动调一次 `/v1/account/Accounts`，按
`mock` / `real_stock` / `real_option` 分桶写入 `FOSUN_ENV_PATH` 指向的共享凭证中的
`FSOPENAPI_ACCOUNT_INDEX`。之后所有业务脚本都从缓存解析 `subAccountId`，
不再额外打接口。

- 账户有变更时主动刷新：`$MONI_PY $SKILL/code/sync_accounts.py`
- 业务接口报"账户类错误"时，本 skill 会自动重刷一次缓存并用新 ID 重试

## 常用命令

```bash
$MONI_PY $SKILL/code/check_shared_env.py
$MONI_PY $SKILL/code/sync_accounts.py
$MONI_PY $SKILL/code/account_list.py
$MONI_PY $SKILL/code/cash_summary.py
$MONI_PY $SKILL/code/holdings.py --product-types 5 --product-types 6
$MONI_PY $SKILL/code/order_list.py --market hk --market us
$MONI_PY $SKILL/code/market_quote.py --code hk00700 --field price
```

完整命令清单与高频任务速抄表见 `SKILL.md`。

## 常见问题

### 共享凭证不存在或无效

```bash
$MONI_PY $SKILL/code/check_shared_env.py
```

如果失败，先回到总入口或同级 `fosun-env-setup`，生成/刷新 `FOSUN_ENV_PATH` 指向的共享凭证。

### `ModuleNotFoundError: No module named 'fsopenapi'`

```bash
bash ../install.sh
```

如果是下载失败，可额外检查：

- 是否能访问 GitHub
- 本机是否存在 `wget` 或 `curl`
- 是否需要通过 `MONI_SDK_URL` / `MONI_SDK_FALLBACK_URL` 指向可访问镜像

### `Invalid signature`

通常说明共享 `fosun.env` 中的公私钥或 API Key 已失效，应先通过同级 `fosun-env-setup` 修复或重新生成。

### `Session expired`

这不是“订单 / 持仓不存在”，而是共享凭证里的券商会话已过期，当前查询通道失效了。

先做体检：

```bash
$MONI_PY $SKILL/code/check_shared_env.py
```

如果仍然报会话过期，回到总入口或同级 `fosun-env-setup`，刷新 `FOSUN_ENV_PATH` 指向的共享凭证后再试。

### `APIError 60006` / `60009`

这是服务端业务校验，不是安装问题。常见原因是购买力不足、订单参数不合法或订单不存在。
