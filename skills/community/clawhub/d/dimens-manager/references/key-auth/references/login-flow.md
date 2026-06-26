# dimens-manager Key 鉴权章节 登录链路说明

适用产品：

- 产品名称：`维表智联`
- 开发方：`方块智联工作室`
- 官网：[https://dimens.bintelai.com/](https://dimens.bintelai.com/)

本文档把 API Key 登录链路拆成“接口请求”、“CLI 行为”、“后续业务访问”三段，便于 Skill 在解释问题时不混淆。

它主要聚焦登录链路本身，不再展开：

- 哪些能力已经 CLI 化、哪些仍是 `server-only`
- 第三方接入为什么不是新开放平台

这些已经拆到独立 references 中。

---

## 1. 换 token 链路

### 1.1 接口入口

| 项 | 内容 |
| --- | --- |
| 方法 | `POST` |
| 路径 | `/open/user/login/apiKey` |
| 入口角色 | API Key 登录入口 |
| 能力归类 | 认证与令牌签发 |

### 1.2 请求体

```json
{
  "apiKey": "ak_xxx",
  "apiSecret": "sk_xxx"
}
```

字段定义：

| 字段 | 类型 | 必填 | 说明 |
| --- | --- | --- | --- |
| `apiKey` | `string` | 是 | 平台发放的 Key |
| `apiSecret` | `string` | 是 | 与 Key 对应的 Secret |

### 1.3 服务端校验顺序

Skill 在解释登录失败时，必须按这个顺序描述：

1. Key 是否存在
2. Key 是否启用
3. 是否过期
4. 绑定用户是否存在且启用
5. Secret 是否匹配
6. 如果配置了 IP 白名单，当前来源 IP 是否允许

### 1.4 成功返回

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

返回字段说明：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `data.expire` | `number` | access token 生命周期，单位秒 |
| `data.token` | `string` | 业务接口使用的用户 token |
| `data.refreshExpire` | `number` | refresh token 生命周期，单位秒 |
| `data.refreshToken` | `string` | 刷新 token |
| `data.teamIds` | `string[]` | 用户当前所属团队 |

---

## 2. CLI 行为

### 2.1 命令入口

```bash
dimens-cli auth api-key-login \
  --api-key ak_xxx \
  --api-secret sk_xxx
```

也支持等号写法：

```bash
dimens-cli auth api-key-login \
  --api-key=ak_xxx \
  --api-secret=sk_xxx
```

### 2.2 入参

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `--api-key` | 是 | API Key |
| `--api-secret` | 是 | API Secret |
| `--base-url` | 否 | API 根地址，当前默认 `https://dimens.bintelai.com/api` |

### 2.3 成功后的副作用

CLI 登录成功后会：

1. 把 `token` 写入本地 profile
2. 如果返回了 `refreshToken`，也会一并写入本地 profile
3. 后续 `project/sheet/column/row/ai` 命令默认复用该登录态

---

## 3. 换 token 之后的业务访问

### 3.1 标准请求头

后续访问 `/app/*` 时，标准请求头是：

```http
Authorization: Bearer {token}
```

### 3.2 示例：查询项目列表

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

### 3.3 成功不等于有权限

Skill 在解释“已经换到 token，但接口仍报无权限”时，必须把结论写完整：

- Key 登录成功，只代表认证成功
- 不代表该用户自动拥有目标团队、项目、表格、工作流权限
- 需要继续检查团队成员关系、项目成员关系、角色和资源授权

---

## 4. 当前可复用的真实闭环案例

本次已实测成功的真实链路：

1. `auth api-key-login`
2. `project list --team-id TTFFEN`
3. `project info --team-id TTFFEN --id PUQUNFE`
4. `sheet list --project-id PUQUNFE`
5. `column list --team-id TTFFEN --project-id PUQUNFE --sheet-id sh_ja2IwgaBhV1jUWB4`
6. `row page --team-id TTFFEN --project-id PUQUNFE --sheet-id sh_ja2IwgaBhV1jUWB4`

这说明当前 API Key 登录能力的实际用途就是：

- 先换出现有用户 token
- 再直接访问现有 `/app/*` 业务接口

而不是单独提供一套开放平台权限模型。
