# 飞书开放平台权限申请 API 模式

## 问题

飞书自建应用需要开通 API 权限才能调用接口。传统的控制台手动搜索勾选效率低、易遗漏。

## 两个 API 工具

### 1. 一键授权链接（推荐用于 Setup 阶段）

飞书支持把权限 scope 打包在 URL 里，用户点一次确认即可批量开通。

**格式：**
```
https://open.feishu.cn/app/{appId}/auth?q=scope1,scope2,...&op_from=openapi&token_type=tenant
```

**示例（记账系统）：**
```
https://open.feishu.cn/app/cli_xxx/auth?q=base:app:read,base:app:update,base:app:create,base:table:read,base:table:create,base:table:update,base:table:delete,base:field:read,base:field:create,base:field:update,base:field:delete,base:record:read,base:record:create,base:record:update,base:record:delete,base:view:read,base:view:write_only&op_from=openapi&token_type=tenant
```

**用户操作：** 点击链接 → 确认开通 → 完成。

### 2. scopes/apply API（用于触发审批）

```http
POST https://open.feishu.cn/open-apis/application/v6/scopes/apply
Authorization: Bearer {tenant_access_token}
Content-Type: application/json; charset=utf-8
```

Body 为空 JSON `{}`。不需要额外权限即可调用（Required Scopes: None）。

**返回码：**
| code | 含义 |
|------|------|
| 0 | 成功，已提交审批 |
| 212002 | 所有权限已授权，无需审批 |
| 212003 | 同版本申请超过 10 次限制 |
| 212004 | 重复申请 |

### 完整流程

1. 用户创建飞书自建应用，提供 App ID + App Secret
2. Agent 生成**一键授权链接**给用户
3. 用户点击链接 → 确认开通所有权限 → **即时生效** ✅

> ⚠️ 常见误区：**不需要创建版本和发布**。对于自建应用，管理员（也是应用创建者）点击确认后权限立即生效。发版流程是商店应用或需要管理员审核的企业应用场景，不适用于个人自建应用。

### 注意事项

- `scopes/apply` 同版本上限 10 次。确认权限后调用返回 212002（均已授权）是正常现象，无需重复调用
- Tenant Token 需通过 `POST /open-apis/auth/v3/tenant_access_token/internal` 获取
- 权限生效后仍需重试 API 调用（之前的 400/403 错误已经过去，需要重新请求）
- 自建应用场景下，应用开发者和管理员同一人时，无额外审批节点
