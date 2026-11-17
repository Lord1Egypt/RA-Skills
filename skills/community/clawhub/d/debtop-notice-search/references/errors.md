# 错误码与处置

> 判定"要不要创建游客"看 SKILL.md §二；本文是**失败之后**怎么处置。
> 关键区分：**工具级错误以 `200` 返回**（`result.isError=true`，看文案），只有鉴权、限流、网关类错误才是 4xx/5xx。

## 工具与接口错误

| 返回 | 含义 | 处置 |
|------|------|------|
| 401 / `AUTH_REQUIRED`、`AUTH_INVALID` | 游客令牌缺失/失效 | try `refresh`；失败则重新创建游客 |
| `INSUFFICIENT_SCOPE`（**工具级错误，HTTP 仍为 200**） | 缺 `notice:read` 或 `enterprise:read` | 游客令牌本已包含，出现即说明用了错误令牌（如用户/PAT 令牌），换回游客令牌 |
| 429 / `RATE_LIMITED` | 限流。**创建**类 429 需看响应体区分来源：nginx `limit_req` 返回 **HTML**（突发拦截），BFF 返回 JSON（如 `RATE_LIMITED: guest_public:ip 超过限制 3/hour`） | 指数退避重试，降低并发，不要短时间内重复画像同一主体；创建类避免突发 |
| `GUEST_LIMITED`（**工具级错误，HTTP 仍为 200**） | 游客限流，如 `GUEST_LIMITED: RATE_LIMITED: guest:qps 超过限制 1/sec` | **退避 1 秒后重试**；串联工具时保持串行（相邻调用间隔 ≥1 秒） |
| `POW_REQUIRED`（400） | 免凭据创建未携带 PoW 解答 | 先 `GET {guest_api_path}/challenge`，解法见 `@references/guest-access.md` 速查 |
| `POW_INVALID`（400） | PoW 解答错误 / 挑战过期 / 挑战已被用过 | 重新取挑战再提交（挑战**一次性**） |
| `FEATURE_DISABLED`（404） | 服务端未开启公开游客创建 | 引导用户走 OAuth，或联系平台开启；自建 / 内网部署见 `@references/guest-access.md`「若服务端未开启公开通道」 |
| `PARAM_INVALID` | 参数错误 | 空 `keyword`、`page_size>100`（工具校验上限）、关键词过宽（`搜索内容过于宽泛`）都会命中，改用完整企业名 |
| `RESOURCE_NOT_FOUND` | 企业/公告不存在 | 换 ID 或全称重查，不臆造 ID |
| `UPSTREAM_TIMEOUT` / `INTERNAL_ERROR` | 上游异常 | 稍后重试，必要时降级为「仅公告搜索」，并提示用户稍后再试 |

## 两个端点的错误不要混淆

| 端点 | 典型返回与含义 |
|------|----------------|
| MCP 端点 `/mcp/debt/stream` | `401` = 无凭据或凭据过期（两者响应相同，无法区分）；`200 + isError` = 工具级错误；`429` = 限流；连不上 / `404` / `405` = 服务未接入或路径不对 |
| 创建游客 / 挑战端点 | `404 FEATURE_DISABLED` = 服务端未开放免凭据创建；`401 AUTH_REQUIRED` = 缺/坏 PoW（凭据方式下为 Skill Token 失效）；`POW_REQUIRED` / `POW_INVALID` 见上表；`429` 多为创建限流 |

> `403 INSUFFICIENT_SCOPE` 只可能出现在**创建游客**（Skill 客户端未授 `guest:create`）；**工具调用**的 scope 不足是 `200 + isError`。
