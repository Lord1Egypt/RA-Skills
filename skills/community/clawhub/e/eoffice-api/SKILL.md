---
name: eoffice-api
description: 泛微 e-office 协同办公系统 OpenAPI - 用户管理、部门管理、审批流程、考勤等企业级 API
version: 1.0.0
homepage: https://github.com/yourname/eoffice-skill
metadata:
  emoji: "🏢"
  requires:
    env:
      - EOFFICE_BASE_URL
      - EOFFICE_AGENT_ID
      - EOFFICE_SECRET
      - EOFFICE_USER
  primaryEnv: EOFFICE_SECRET
---

# e-office10 OpenAPI Skill

当用户提到以下场景时使用此 skill：
- 查询/搜索企业内部用户信息
- 新建/编辑/删除用户账号
- 查询部门组织架构
- 发起或审批工作流程
- 查询考勤记录
- 发送内部通知消息
- 管理客户或合同信息
- 任何需要操作 OA 系统的任务

## 认证方式

本 skill 使用自定义 token 流程，与 OAuth2 类似但更简单：

### 首次使用步骤

1. **获取 Token**（调用 `scripts/get-token.py`）
   ```bash
   python scripts/get-token.py
   ```
   这会向 OA 系统发送请求，用环境变量中的 `EOFFICE_AGENT_ID`、`EOFFICE_SECRET`、`EOFFICE_USER` 换取访问 token。

2. **Token 自动管理**
   - Agent 会自动缓存 token
   - Token 过期时自动重新获取
   - 无需手动管理

### 环境配置

安装 skill 后，用户需要提供以下环境变量（在 OpenClaw 配置中设置）：

| 环境变量 | 必填 | 说明 | 示例 |
|----------|------|------|------|
| `EOFFICE_BASE_URL` | 是 | OA 系统部署地址 | `https://oa.example.com/server` |
| `EOFFICE_AGENT_ID` | 是 | 应用 Agent ID | `100001` |
| `EOFFICE_SECRET` | 是 | 应用密钥 | `abc123def456...` |
| `EOFFICE_USER` | 是 | 用户标识（工号/账号/手机号） | `admin` 或 `18612345678` |

**如何获取凭证：**
1. 登录 OA 系统管理后台
2. 进入「集成中心」→「OpenAPI」
3. 创建应用，获取 `Agent ID` 和 `Secret`
4. 配置用户识别字段（工号/账号/手机号）
5. 将用户账号填入 `EOFFICE_USER`

## 使用方法

### 用户管理

#### 查询用户列表
```bash
curl -X GET "$EOFFICE_BASE_URL/api/hrm/lists" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"page": 1, "limit": 10}'
```

#### 查询单个用户详情
```bash
curl -X GET "$EOFFICE_BASE_URL/api/hrm/detail/{user_id}" \
  -H "Authorization: Bearer {token}"
```

#### 新建用户
```bash
curl -X POST "$EOFFICE_BASE_URL/api/hrm/add" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "user_accounts": "zhangsan",
    "user_name": "张三",
    "dept_id": 1,
    "role_id": [1, 2],
    "user_status": 1,
    "allow_login": 1,
    "wap_allow": 1,
    "sex": 1
  }'
```

#### 编辑用户
```bash
curl -X POST "$EOFFICE_BASE_URL/api/hrm/edit" \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "WV00000001",
    "user_accounts": "zhangsan",
    "user_name": "张三（已修改）",
    "dept_id": 2,
    "role_id": [1],
    "user_status": 1,
    "allow_login": 1,
    "wap_allow": 1,
    "sex": 1
  }'
```

#### 删除用户
```bash
curl -X POST "$EOFFICE_BASE_URL/api/hrm/delete/{user_id}" \
  -H "Authorization: Bearer {token}"
```

### 部门管理

#### 获取部门列表（树形）
```bash
curl -X GET "$EOFFICE_BASE_URL/api/department/allTree" \
  -H "Authorization: Bearer {token}"
```

#### 获取部门详情
```bash
curl -X GET "$EOFFICE_BASE_URL/api/department/detail/{dept_id}" \
  -H "Authorization: Bearer {token}"
```

## 常用查询示例

### 搜索用户（按姓名模糊搜索）
```
GET /api/hrm/lists
Body: {"search": {"user_name": ["张", "like"]}}
```

### 获取用户在某个部门的用户列表
```
GET /api/department/users/{dept_id}
```

### 获取用户的上级领导
```
GET /api/hrm/superior/{user_id}
```

### 获取用户的下级下属
```
GET /api/hrm/subordinate/{user_id}
```

## 响应格式

所有 API 返回格式统一：

**成功：**
```json
{
  "status": 1,
  "data": { ... }
}
```

**失败：**
```json
{
  "status": 0,
  "errors": [
    {"code": "0x000003", "message": "未知错误"}
  ]
}
```

## 错误码

| 错误码 | 说明 |
|--------|------|
| `0x000003` | 未知错误 |
| `0x500001` | 参数缺失 |
| `0x500002` | 应用不存在 |
| `0x500003` | Token 无效或已过期 |
| `0x500004` | 语言环境无效 |
| `0x500005` | 用户不存在 |
| `0x500006` | 用户不在白名单内 |
| `0x500007` | 无账号人员不支持生成 Token |

## 注意事项

1. **敏感操作**：删除用户等敏感操作需要管理员权限
2. **用户状态**：`user_status` 字段标识用户是否在职，离职用户通常 `user_status` 为特定值
3. **部门 ID**：新建用户需要指定 `dept_id`，可先调用部门列表 API 查询
4. **角色 ID**：`role_id` 是数组，指定用户的权限角色
5. **Token 有效期**：默认 Token 有效期由 OA 系统配置，通常为数小时

## 完整 API 文档

详见 `references/api.md`
