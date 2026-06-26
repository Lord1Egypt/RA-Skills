# real-trade-skill

复星财富港美股实盘 OpenAPI skill。它与 `moni-trade-skill` 共用总入口目录下的同一个 `fosun.env`，凭证生成与修复由同级 `fosun-env-setup` 负责。

## 起手式

```bash
export SKILL="<real-trade-skill 绝对路径>"
export REAL_PY="<python 绝对路径>"
export FOSUN_ENV_PATH="${FOSUN_ENV_PATH:-$SKILL/../fosun.env}"
```

不要写死某台机器的绝对路径。安装到 skill 目录后，只要 `real-trade-skill`、`moni-trade-skill`、`fosun-env-setup` 与 `fosun.env` 保持同级关系，就能用相同相对路径解析到共享凭证。

## 共享凭证

```bash
python3 ../fosun-env-setup/code/ensure_fosun_env.py
```

- `status=valid`：凭证已可用，可以继续实盘体检或业务脚本。
- `status=pending`：把脚本 JSON 输出里的 `exact_open_url` / `open_url` 逐字符原样给用户完成 OpenAPI 开通，禁止手写或改写 URL；用户在页面完成开通后重试，脚本通过 finalize（APIKeyCheck + 签名请求）验证。
- `status=error`：先修复凭证生成问题，不要继续跑实盘业务脚本。

修复已有凭证：

```bash
python3 ../fosun-env-setup/code/ensure_fosun_env.py --repair
```

## 使用前提

- 用户已明确选择`实盘`
- `FOSUN_ENV_PATH` 指向的共享 `fosun.env` 已存在
- 实盘变更操作已经过用户二次确认

## 安装 SDK

```bash
# macOS / Linux
bash ../install.sh

# Windows (PowerShell)
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

安装脚本会自动下载并安装官方 `fsopenapi` SDK，默认版本为 `v1.2.0`。
下载主源默认是 GitHub；主源失败时会自动读取 `../fosun-env-setup/code/ensure_fosun_env.py` 中的
`DEFAULT_SDK_ZIP_FALLBACK_URL` 作为备用源（实现一处改动全局生效）。
可用 `REAL_SDK_VERSION` / `REAL_SDK_URL` / `REAL_SDK_FALLBACK_URL` 覆盖。

## 常用命令

```bash
$REAL_PY $SKILL/code/check_shared_env.py
$REAL_PY $SKILL/code/sync_accounts.py
$REAL_PY $SKILL/code/account_list.py
$REAL_PY $SKILL/code/cash_summary.py
$REAL_PY $SKILL/code/holdings.py
$REAL_PY $SKILL/code/order_list.py
$REAL_PY $SKILL/code/market_quote.py --code hk00700 --field price
```

下单、改单、撤单前必须先复述完整意图并等待用户明确确认。

## 路由关系

- 实盘：`real-trade-skill`
- 模拟盘：`moni-trade-skill`
- 共享凭证：`fosun-env-setup` 生成和修复，两个交易 skill 共同读取同一个 `fosun.env`
