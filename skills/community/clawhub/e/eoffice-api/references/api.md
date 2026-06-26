# e-office OpenAPI 完整接口文档

## 目录

- [认证](#认证)
- [用户管理 (Hrm)](#用户管理-hrm)
- [部门管理 (Department)](#部门管理-department)
- [建模管理 (Modeling)](#建模管理-modeling)
- [附件管理 (Attachment)](#附件管理-attachment)

---

## 认证

### 获取访问令牌

在调用其他 API 之前，必须先获取访问 token。

```
POST /api/auth/openapi-token
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user | string | 是 | 用户标识（工号/账号/手机号，根据应用配置） |
| agent_id | string/int | 是 | 应用 Agent ID |
| secret | string | 是 | 应用密钥 |

**响应：**

```json
{
  "status": 1,
  "data": {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "expired_in": 7200,
    "refresh_token_expired_in": 604800,
    "user_id": "admin",
    "agent_id": "100001"
  }
}
```

### 刷新 Token

当 token 即将过期时，使用 refresh_token 获取新 token。

```
POST /api/auth/openapi-refresh-token
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| token | string | 是 | 当前过期的 token |
| refresh_token | string | 是 | 刷新令牌 |

---

## 用户管理 (Hrm)

### 获取用户列表

```
POST /api/hrm/lists
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| fields | string | 否 | 需要查询的字段，不传默认为全部 |
| page | int | 否 | 页码（默认 1） |
| limit | int | 否 | 每页显示数量（默认 20） |
| order_by | json | 否 | 排序，如 `{"list_number":"desc"}` |
| search | json | 否 | 查询条件 |

**查询条件示例：**

```json
{
  "search": {
    "user_name": ["张", "like"],
    "phone_number": ["138", "like"],
    "dept_id": [1]
  }
}
```

**响应：**

```json
{
  "status": 1,
  "data": {
    "total": 669,
    "list": [
      {
        "data_id": 1,
        "user_id": "admin",
        "user_accounts": "admin",
        "user_name": "系统管理员",
        "user_name_py": "xitongguanliyuan",
        "user_job_number": "2058",
        "dept_id": 18,
        "dept_id_TEXT": "技术部",
        "role_id": ["1"],
        "role_id_TEXT": "OA管理员",
        "user_status": 1,
        "user_status_TEXT": "在职",
        "phone_number": "18612345678",
        "email": "admin@example.com",
        "sex": 1,
        "sex_TEXT": "男",
        "join_date": "2024-04-12",
        "work_date": "2024-04-23",
        "superior_user_id": ["WV00000008"],
        "superior_user_id_TEXT": "龙利锋",
        "..."
      }
    ]
  }
}
```

---

### 获取用户详情

```
GET /api/hrm/detail/{user_id}
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | string | 是 | 用户 ID |

**响应：**

```json
{
  "status": 1,
  "data": {
    "data_id": 39,
    "user_id": "WV00000001",
    "user_accounts": "zhangsan",
    "user_name": "张三",
    "dept_id": 20,
    "dept_id_TEXT": "研发部",
    "role_id": ["20"],
    "role_id_TEXT": "研发经理",
    "user_status": 1,
    "user_status_TEXT": "在职",
    "phone_number": "13800138000",
    "email": "zhangsan@example.com",
    "sex": 1,
    "sex_TEXT": "男",
    "join_date": "2024-01-15",
    "work_date": "2024-01-20",
    "superior_user_id": ["WV00000002"],
    "superior_user_id_TEXT": "李经理",
    "subordinate_user_id": ["WV00000003", "WV00000004"],
    "subordinate_user_id_TEXT": "王工程师,赵工程师",
    "last_login_time": "2024-12-01 09:30:00",
    "..."
  }
}
```

**说明：**
- 所有 ID 类型的字段都有对应的 `_TEXT` 字段显示文本值
- 如 `dept_id: 1` 对应 `dept_id_TEXT: "研发部"`

---

### 新建用户

```
POST /api/hrm/add
```

**必填参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| user_accounts | string | 用户名/账号 |
| user_name | string | 真实姓名 |
| user_status | int | 用户状态 ID（1=在职） |
| dept_id | int | 部门 ID |
| allow_login | int | 是否开通账号（0=不开通, 1=开通） |
| role_id | array | 角色 ID 数组 |
| wap_allow | int | 是否允许手机访问（0=不允许, 1=允许） |
| sex | int | 性别（0=女, 1=男） |

**可选参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| phone_number | string | 手机号码 |
| login_password | string | 登录密码 |
| user_job_number | string | 工号 |
| scheduling_id | int | 考勤排班类型 ID |
| list_number | string | 序号（用于排序） |
| birthday | date | 生日，格式：`YYYY-MM-DD` |
| email | string | 邮箱 |
| weixin | string | 微信 |
| subordinate_user_id | array | 下级用户 ID 数组 |
| superior_user_id | array | 上级用户 ID 数组 |

**请求示例：**

```json
{
  "user_accounts": "zhangsan",
  "user_name": "张三",
  "phone_number": "13800138000",
  "login_password": "123456",
  "user_job_number": "EMP001",
  "sex": 1,
  "user_status": 1,
  "dept_id": 20,
  "role_id": [1, 5],
  "wap_allow": 1,
  "allow_login": 1,
  "email": "zhangsan@example.com",
  "join_date": "2024-01-15",
  "superior_user_id": ["WV00000002"]
}
```

**响应：**

```json
{
  "status": 1,
  "data": {
    "user_id": "WV00000693",
    "user_accounts": "zhangsan",
    "user_name": "张三",
    "user_job_number": "EMP001"
  }
}
```

---

### 编辑用户

```
POST /api/hrm/edit
```

**必填参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| user_id | string | 被编辑的用户 ID |
| user_accounts | string | 用户名 |
| user_name | string | 真实姓名 |
| user_status | int | 用户状态 ID |
| dept_id | int | 部门 ID |
| role_id | array | 角色 ID 数组 |
| wap_allow | int | 是否允许手机访问 |
| allow_login | int | 是否开通账号 |
| sex | int | 性别 |

**可选参数：**

| 参数 | 类型 | 说明 |
|------|------|------|
| expire_time | date | 账号有效截止日期，格式：`YYYY-MM-DD` |
| phone_number | string | 手机号码 |
| email | string | 邮箱 |
| ... | ... | 其他可选字段同新建用户 |

**请求示例：**

```json
{
  "user_id": "WV00000693",
  "user_accounts": "zhangsan",
  "user_name": "张三（已修改）",
  "dept_id": 21,
  "role_id": [1, 6],
  "user_status": 1,
  "wap_allow": 1,
  "allow_login": 1,
  "sex": 1,
  "expire_time": "2025-12-31"
}
```

**响应：**

```json
{
  "status": 1
}
```

---

### 删除用户

```
POST /api/hrm/delete/{user_id}
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_id | string | 是 | 用户 ID |

**响应：**

```json
{
  "status": 1
}
```

**说明：** 支持批量删除，user_id 用逗号分隔，如 `WV00000001,WV00000002`

---

### 获取用户上级列表

```
GET /api/hrm/superior/{user_id}
```

---

### 获取用户下级列表

```
GET /api/hrm/subordinate/{user_id}
```

---

### 获取当前用户详情

```
GET /api/hrm/current
```

返回当前登录用户的详细信息。

---

## 部门管理 (Department)

### 获取部门列表（树形）

```
GET /api/department/allTree
```

**响应：**

```json
{
  "status": 1,
  "data": [
    {
      "id": 1,
      "name": "总公司",
      "parent_id": 0,
      "children": [
        {
          "id": 2,
          "name": "技术部",
          "parent_id": 1,
          "children": []
        },
        {
          "id": 3,
          "name": "市场部",
          "parent_id": 1,
          "children": []
        }
      ]
    }
  ]
}
```

---

### 获取部门详情

```
GET /api/department/detail/{dept_id}
```

---

### 新建部门

```
POST /api/department/add
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| dept_name | string | 是 | 部门名称 |
| parent_id | int | 否 | 上级部门 ID（默认为 0） |
| dept_code | string | 否 | 部门编码 |
| manager_user_id | string | 否 | 部门负责人用户 ID |

---

### 编辑部门

```
POST /api/department/edit
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| dept_id | int | 是 | 部门 ID |
| dept_name | string | 否 | 部门名称 |
| dept_code | string | 否 | 部门编码 |
| manager_user_id | string | 否 | 部门负责人 |

---

### 删除部门

```
POST /api/department/delete/{dept_id}
```

---

### 获取部门下用户列表

```
GET /api/department/users/{dept_id}
```

---

## 建模管理 (Modeling)

用于操作自定义建模的数据。

### 新建建模数据

```
POST /api/modeling/add
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| model_id | int | 是 | 建模 ID |
| data | object | 是 | 要保存的数据对象 |

**请求示例：**

```json
{
  "model_id": 123,
  "data": {
    "DATA_1": "字段1的值",
    "DATA_2": "字段2的值"
  }
}
```

---

### 获取建模数据列表

```
POST /api/modeling/lists
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| model_id | int | 是 | 建模 ID |
| page | int | 否 | 页码 |
| limit | int | 否 | 每页数量 |
| search | json | 否 | 查询条件 |

---

### 编辑建模数据

```
POST /api/modeling/edit
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| model_id | int | 是 | 建模 ID |
| data_id | int | 是 | 数据 ID |
| data | object | 是 | 要更新的数据 |

---

### 删除建模数据

```
POST /api/modeling/delete
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| model_id | int | 是 | 建模 ID |
| data_id | int | 是 | 数据 ID |

---

### 获取建模数据详情

```
GET /api/modeling/detail/{model_id}/{data_id}
```

---

## 附件管理 (Attachment)

### 上传附件

```
POST /api/attachment/upload
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | file | 是 | 上传的文件 |
| chunk | int | 否 | 分片序号（用于大文件分片上传） |
| chunks | int | 否 | 总分片数 |

---

### 获取附件列表

```
GET /api/attachment/list
```

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| source_id | string | 否 | 关联业务 ID |
| source_type | string | 否 | 关联业务类型 |

---

### 下载附件

```
GET /api/attachment/download/{attachment_id}
```

---

## 附录：字段类型说明

### 用户状态 (user_status)

| 值 | 说明 |
|----|------|
| 1 | 在职 |
| 2 | 离职 |
| 3 | 退休 |
| ... | 其他自定义状态 |

### 性别 (sex)

| 值 | 说明 |
|----|------|
| 0 | 女 |
| 1 | 男 |

### 是否允许 (wap_allow, allow_login)

| 值 | 说明 |
|----|------|
| 0 | 否 |
| 1 | 是 |

---

## 附录：查询操作符

在 `search` 参数中，支持以下操作符：

| 操作符 | 说明 | 示例 |
|--------|------|------|
| `=` 或无操作符 | 精确匹配 | `"dept_id": [1]` |
| `like` | 模糊匹配 | `"user_name": ["张", "like"]` |
| `>` | 大于 | `"work_date": ["2024-01-01", ">"]` |
| `<` | 小于 | `"work_date": ["2024-12-31", "<"]` |
| `>=` | 大于等于 | `"work_date": ["2024-01-01", ">="]` |
| `<=` | 小于等于 | `"work_date": ["2024-12-31", "<="]` |
| `in` | IN 查询 | `"user_status": [[1,2], "in"]` |
| `not_in` | NOT IN 查询 | `"user_status": [[3], "not_in"]` |
