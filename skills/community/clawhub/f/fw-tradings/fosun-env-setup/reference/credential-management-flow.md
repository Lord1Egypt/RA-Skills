# 复星 OpenAPI 凭据管理流程

> 适用范围：本 skill（`fosun-env-setup`）及同级 `real-trade-skill` / `moni-trade-skill` 共用的 `fosun.env`。
> 命令入口见本目录上一级的 `SKILL.md`。

## 1. 凭据构成

一份完整凭据由四部分组成：

| 字段 | env 键 | 来源 | 说明 |
|------|--------|------|------|
| apikey | `FSOPENAPI_API_KEY` | 用户在授权页复制 / TicketCreate 临时返回 | 账号身份凭证 |
| 客户端私钥 | `FSOPENAPI_CLIENT_PRIVATE_KEY` | **本地生成**，每次 TicketCreate 配套 | 不出本机；公钥随 TicketCreate 上送 |
| 服务端公钥 | `FSOPENAPI_SERVER_PUBLIC_KEY` | **授权页展示**（回填时）/ TicketCreate 临时返回（首次开通） | 用于握手验签 |
| （服务端私钥） | 不落本地 | 服务端持有 | — |

业务调用走「ECDH + 签名」握手：用**本地客户端私钥**与**服务端公钥**协商，对请求签名；apikey 标识身份。

## 2. 关键不变量

1. **一个账号只有一个 apikey，开通后固定不变**。续期不换 apikey。
2. **`serverPubKey` 按 ticket 生成，每次 TicketCreate 可能不同**；授权页展示的服务端公钥与 ticket 临时返回的公钥**可能不一致**。
3. **「客户端私钥 + 授权 url」必须来自同一次 TicketCreate**；已开通/重置场景下，**服务端公钥必须用用户在页面上复制的那份**，禁止跨 ticket 混用或仅用 ticket 临时公钥代替页面公钥。
   - 用户在某张 ticket 的 url 上完成授权/重置后，服务端按**该 ticket** 的客户端公钥绑定。
   - 若此时轮换客户端密钥或重签新 ticket，会与用户刚完成的页面绑定错位 → 握手失败 → 再判 invalid → 再轮换，形成「重置→不匹配→再重置」死循环。

## 3. TicketCreate

- 路径：`POST {BASE_URL}/api/v1/auth/TicketCreate`
- 请求体：`{"macId": <设备号>, "clientPubKey": <本地客户端公钥, 必传>}`
- 响应字段：`{ "apiKey", "serverPubKey", "ticket", "url", "expireTime" }`
  - `apiKey`：**临时**（尚未知用户身份）；每次可能不同
  - `serverPubKey`：本 ticket 返回的服务端公钥（**不等于**重置后页面展示的公钥）
  - `url`：授权页（用户登录并授权 / 重置 / 续期）
  - 续期：须在 url 的 **hashtag query** 中追加 `isExpired=1`

开通 / 重置 / 续期均从 TicketCreate 起步。

## 4. APIKeyCheck

- 路径：`POST {BASE_URL}/api/v1/auth/APIKeyCheck`，请求体 `{"apiKey": <apikey>}`
- **只校验 apikey 值的服务端状态，不比对密钥对。**
- 响应 `data.status`：`0=invalid`、`1=valid`、`2=disabled`、`3=expired`
- 临时（未授权）apikey 与无效 apikey 都可能返回 `status=0`（invalid），**无法区分「待授权」与「真无效」**。
- 因此：APIKeyCheck 为 invalid/unknown 时仍会尝试一次签名业务请求；仅 expired/disabled 直接路由续期/客服。
- **不要把 invalid 解释成「apikey 与服务端公钥不匹配」。**

## 5. 三类写入流程

### 5.1 首次开通
1. TicketCreate → ticket、serverPubKey、url、临时 apiKey。
2. 用户在 url 完成开通后回复「开通好了」。
3. 写入 env：**TicketCreate 返回的 apiKey + serverPubKey + 本次生成的客户端私钥**。

### 5.2 已开通过（重置 / 换设备 / 凭据丢失）
1. TicketCreate（同上）。
2. 用户在 url 点 **「忘记 API 参数」** 重置（**只重置客户端密钥绑定，apikey 不变**）。
3. 用户必须把页面上 **apikey + 服务端公钥（PEM 全文）** 一并发给 Agent。**缺一不可**。
4. 写入 env：**回填的 apikey + 页面服务端公钥 + 本次 ticket 的客户端私钥**（私钥来自 pending，公钥必须用页面提供的值）。

### 5.3 续期
- env 中 apikey、客户端私钥、服务端公钥 **均不更新**。
- 仅签发带 `isExpired=1` 的续期 url，用户扫码后续期，完成后重试原操作。
- 须本地已有 apikey 与服务端公钥；换设备无凭据时须先走 §5.2 回填，再由系统识别过期转续期。

## 6. 四个场景

| 场景 | 触发 | 处置 |
|------|------|------|
| 1 首次开通 | 全新用户 | §5.1 |
| 2 开通过 + 换设备（无 env） | 本地无凭据 | §5.2 |
| 3 凭据损坏 | env 无效或不完整 | §5.2（不完整自动转重置） |
| 4 apikey 过期 | 40010 / APIKeyCheck=expired | §5.3 |

- **场景 1 与 2 无法区分**：均先 TicketCreate；曾开通过 →「忘记 API 参数」+ 回填 apikey 与公钥；首次 → 回复「开通好了」。
- **场景 4 × 2**：换设备且过期 → 先 §5.2 回填，系统识别过期后自动转续期，**不能直接 `--renew`**。

## 7. 防死循环（回填被判 invalid）

- **禁止**在回填 invalid 后轮换客户端密钥或重签新 ticket（除非用户明确要求重来或无可复用二维码）。
- **应**：复用当前二维码（`created_new_ticket=false`），让用户在**同一页面**再点「忘记 API 参数」，把页面上 **apikey + 服务端公钥** 一并发来，再执行回填命令。
- 返回 `api_key_rejected=true` 时表示已写入但校验未过，按上述引导处理。

## 8. 命令对应

| 动作 | 命令 |
|------|------|
| 开通 / 换设备 / 凭据丢失 | `code/ensure_fosun_env.py` |
| 回填（**须** apikey + 页面服务端公钥） | `code/ensure_fosun_env.py --api-key <apikey> --server-public-key '<PEM>'` |
| 续期 | `code/ensure_fosun_env.py --renew` |
| 重置（签码后须回填） | `code/ensure_fosun_env.py --reset-credentials` |
| 立即签新 ticket | `code/ensure_fosun_env.py --force-new-ticket` |

模拟盘命中 apikey 错误码（40001/40005/40008/40010/40015）时，引导用户回 `real-trade-skill` / 本 skill 处理，**禁止**在模拟盘内自行签 ticket 或改 env。
