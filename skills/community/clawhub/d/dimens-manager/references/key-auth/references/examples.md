# dimens-manager Key 鉴权章节 接口案例

本文档只写维表智联当前已经可用的真实接口、CLI 命令和返回结构，重点覆盖：

1. `apiKey + apiSecret` 换 token
2. 换到 token 后如何继续访问 `/app/*`
3. 当前 Skill 在说明问题时必须引用的真实入参、出参与边界

更细的规则说明请分别查看：

- `login-flow.md`
- `integration-boundaries.md`
- `capability-status.md`

---

## 1. API Key 登录换 token

### 1.1 服务端接口

| 项 | 内容 |
| --- | --- |
| 方法 | `POST` |
| 路径 | `/open/user/login/apiKey` |
| 入口角色 | 开放登录接口 |
| 鉴权 | 不需要 Bearer token |
| 请求体 | `apiKey`、`apiSecret` |

请求体定义：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `apiKey` | `string` | 是 | 平台生成的 Key，通常形如 `ak_xxx` |
| `apiSecret` | `string` | 是 | 平台生成的 Secret，通常形如 `sk_xxx` |

请求示例：

```http
POST /open/user/login/apiKey
Content-Type: application/json
```

```json
{
  "apiKey": "ak_xxx",
  "apiSecret": "sk_xxx"
}
```

成功返回字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `code` | `number` | 成功通常为 `1000` |
| `message` | `string` | 成功通常为 `success` |
| `data.expire` | `number` | access token 过期秒数 |
| `data.token` | `string` | 维表智联用户 JWT |
| `data.refreshExpire` | `number` | refresh token 过期秒数 |
| `data.refreshToken` | `string` | 刷新 token |
| `data.teamIds` | `string[]` | 当前用户所属团队 ID 列表 |

基于本次实测的成功返回示例：

```json
{
  "code": 1000,
  "message": "success",
  "data": {
    "expire": 604800,
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "refreshExpire": 2592000,
    "refreshToken": "eyJhbGciOiJIUzI1NiIs...",
    "teamIds": ["TTFFEN", "TABBL5B", "TCKB43C"]
  }
}
```

### 1.2 CLI 命令

当前 CLI 真实入口：

```bash
dimens-cli auth api-key-login \
  --api-key ak_xxx \
  --api-secret sk_xxx
```

或：

```bash
dimens-cli auth api-key-login \
  --api-key=ak_xxx \
  --api-secret=sk_xxx
```

CLI 入参：

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `--api-key` | 是 | API Key |
| `--api-secret` | 是 | API Secret |
| `--base-url` | 否 | API 根地址；不传时当前默认 `https://dimens.bintelai.com/api` |

CLI 成功输出：

| 字段 | 说明 |
| --- | --- |
| `message` | `API Key 登录成功` |
| `data.token` | 写入本地 profile，供后续 `project/sheet/row/ai` 命令复用 |
| `data.refreshToken` | 若返回则一并写入本地 profile |
| `data.teamIds` | 当前用户团队列表 |

### 1.3 登录后继续访问 `/app/*`

这条链路的关键点不是“换 token 结束”，而是“换 token 后继续访问原有业务接口”。

标准请求头格式：

```http
Authorization: Bearer {token}
```

示例：

```http
POST /app/org/TTFFEN/project/page
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json
```

```json
{
  "page": 1,
  "size": 20
}
```

### 1.4 排查顺序

当用户说“Key 登录不通”或“登录成功后接口没权限”时，Skill 必须按下面顺序解释：

1. 先判断 `apiKey/apiSecret` 能否成功换 token。
2. 再判断 token 是否被正确带到了 `/app/*` 请求头里。
3. 最后判断用户是否对目标团队、项目、表格本来就有权限。

---

## 2. API Key 管理相关接口

这些接口当前主要由维表智联平台提供，CLI 还没有完全封装成独立命令，但 Skill 里不能遗漏。

### 2.1 创建 API Key

| 项 | 内容 |
| --- | --- |
| 方法 | `POST` |
| 路径 | `/app/base/apiKey` |
| 鉴权 | `Authorization: Bearer {token}` |
| 入口角色 | API Key 管理入口 |

请求体：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `name` | `string` | 是 | Key 名称 |
| `expireTime` | `string` | 否 | 过期时间，常见格式 `YYYY-MM-DD HH:mm:ss` |
| `remark` | `string` | 否 | 备注 |
| `ipWhitelist` | `string[]` | 否 | IP 白名单 |

请求示例：

```json
{
  "name": "报表同步 Key",
  "expireTime": "2026-12-31 23:59:59",
  "remark": "第三方同步使用"
}
```

成功返回重点：

| 字段 | 说明 |
| --- | --- |
| `data.id` | Key 记录 ID |
| `data.apiKey` | 明文 apiKey |
| `data.apiSecret` | 明文 apiSecret，只返回一次 |
| `data.status` | 状态，通常 `1` 表示启用 |

### 2.2 查询 API Key 列表

| 项 | 内容 |
| --- | --- |
| 方法 | `GET` |
| 路径 | `/app/base/apiKey/list` |
| 鉴权 | `Authorization: Bearer {token}` |

列表返回重点：

| 字段 | 说明 |
| --- | --- |
| `data.list[].apiKey` | Key 值 |
| `data.list[].status` | 启停状态 |
| `data.list[].expireTime` | 过期时间 |
| `data.list[].remark` | 备注 |
| `data.list[].apiSecret` | 不返回 |

### 2.3 启用 / 禁用 API Key

| 项 | 内容 |
| --- | --- |
| 方法 | `PUT` |
| 路径 | `/app/base/apiKey/status` |
| 鉴权 | `Authorization: Bearer {token}` |

请求体：

```json
{
  "id": "key_xxx",
  "status": 0
}
```

字段说明：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `id` | `string` | 是 | Key 记录 ID |
| `status` | `number` | 是 | `1` 启用，`0` 禁用 |

### 2.4 删除 API Key

| 项 | 内容 |
| --- | --- |
| 方法 | `DELETE` |
| 路径 | `/app/base/apiKey/{id}` |
| 鉴权 | `Authorization: Bearer {token}` |

### 2.5 重置 Secret

| 项 | 内容 |
| --- | --- |
| 方法 | `POST` |
| 路径 | `/app/base/apiKey/{id}/reset-secret` |
| 鉴权 | `Authorization: Bearer {token}` |

成功返回重点：

| 字段 | 说明 |
| --- | --- |
| `data.id` | Key 记录 ID |
| `data.apiKey` | 原 apiKey |
| `data.apiSecret` | 新 secret，只返回一次 |

### 2.6 查询登录日志

| 项 | 内容 |
| --- | --- |
| 方法 | `GET` |
| 路径 | `/app/base/apiKey/logs?page=1&size=10` |
| 鉴权 | `Authorization: Bearer {token}` |

扩展说明：

- 也支持按单个 Key 查询日志
- 用于排查“某个 Key 在某个时间点为什么登录失败”

---

## 3. Skill 输出要求

当用户提到 Key 登录、Key 创建、第三方接入时，Skill 输出里至少要明确这些信息：

1. 当前访问的是哪个真实接口路径。
2. 请求体里每个字段的含义、是否必填。
3. 返回里真正关键的字段是什么。
4. `apiSecret` 只会返回一次，不能从列表反查。
5. 登录成功只代表换 token 成功，不代表目标资源一定有权限。
