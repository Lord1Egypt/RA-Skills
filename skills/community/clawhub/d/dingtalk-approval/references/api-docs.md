# 钉钉 OA 审批 API 参考文档

## 📚 API 接口说明

### 1. 获取访问令牌

**接口**：`POST https://api.dingtalk.com/v1.0/oauth2/accessToken`

**请求体**：
```json
{
  "appKey": "your-app-key",
  "appSecret": "your-app-secret"
}
```

**响应**：
```json
{
  "accessToken": "access_token_string",
  "expireIn": 7200
}
```

**注意**：
- accessToken 有效期为 2 小时（7200 秒）
- 建议缓存 token，避免频繁请求
- token 过期后需要重新获取

---

### 2. 查询用户待办任务

**接口**：`POST https://oapi.dingtalk.com/topapi/process/workrecord/task/query`

**请求参数**：
```json
{
  "userid": "user_id",
  "offset": 0,
  "count": 50,
  "status": 0
}
```

**参数说明**：
- `userid`：钉钉用户 ID
- `offset`：分页偏移量，默认 0
- `count`：每页数量，最大 100
- `status`：任务状态（0=待处理，1=已处理）

**响应示例**：
```json
{
  "errcode": 0,
  "result": {
    "list": [
      {
        "task_id": "task_12345",
        "title": "请假申请 - 张三",
        "create_time": 1678886400000,
        "form_component_values": [...]
      }
    ],
    "has_more": false
  }
}
```

**错误码**：
- `0`：成功
- `40014`：token 无效或过期
- `60011`：权限不足
- `40035`：参数错误

---

### 3. 执行审批操作

**接口**：`POST https://oapi.dingtalk.com/topapi/process/workrecord/task/execute`

**请求参数**：
```json
{
  "task_id": "task_12345",
  "action": "agree",
  "remark": "同意"
}
```

**参数说明**：
- `task_id`：待办任务 ID（从查询接口获取）
- `action`：操作类型（`agree`=同意，`refuse`=拒绝）
- `remark`：审批意见（可选，建议填写）

**响应示例**：
```json
{
  "errcode": 0,
  "result": {
    "success": true
  }
}
```

**错误码**：
- `0`：成功
- `40014`：token 无效或过期
- `60011`：权限不足
- `40035`：参数错误
- `125001`：task_id 无效或任务已处理

---

## 🔍 错误码详解

### 常见错误码

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 0 | 成功 | - |
| 40014 | 访问令牌无效或过期 | 重新获取 accessToken |
| 40035 | 请求参数错误 | 检查参数格式和必填项 |
| 60011 | 应用无权限调用接口 | 在钉钉开放平台添加对应权限 |
| 125001 | 任务 ID 无效或任务已处理 | 重新查询待办任务列表 |
| 125002 | 用户 ID 无效 | 检查 dingtalkUserId 配置 |
| 40005 | 应用 appKey 或 appSecret 错误 | 检查配置是否正确 |

---

## 📝 最佳实践

### 1. Token 管理

```javascript
// 缓存 token，避免每次请求都获取
let cachedToken = null;
let tokenExpireTime = 0;

async function getDingtalkToken() {
    const now = Date.now();
    if (cachedToken && now < tokenExpireTime) {
        return cachedToken;
    }
    
    const res = await fetch("https://api.dingtalk.com/v1.0/oauth2/accessToken", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
            appKey: config.appKey, 
            appSecret: config.appSecret 
        })
    });
    const data = await res.json();
    
    // 缓存 token，提前 5 分钟过期
    cachedToken = data.accessToken;
    tokenExpireTime = now + (data.expireIn - 300) * 1000;
    
    return cachedToken;
}
```

### 2. 错误处理

```javascript
try {
    const token = await getDingtalkToken();
    const res = await fetch(apiUrl, {
        method: "POST",
        headers: { 
            "Content-Type": "application/json",
            "x-acs-dingtalk-access-token": token
        },
        body: JSON.stringify(params)
    });
    const data = await res.json();
    
    if (data.errcode !== 0) {
        throw new Error(`钉钉 API 错误：${data.errcode} - ${data.errmsg}`);
    }
    
    return data.result;
} catch (error) {
    console.error("审批操作失败:", error);
    throw error;
}
```

### 3. 分页处理

```javascript
async function getAllTasks(userId) {
    const allTasks = [];
    let offset = 0;
    const count = 50;
    
    while (true) {
        const result = await queryTasks(userId, offset, count);
        allTasks.push(...result.list);
        
        if (!result.has_more) {
            break;
        }
        
        offset += count;
    }
    
    return allTasks;
}
```

---

## 🔗 相关链接

- [钉钉开放平台](https://open.dingtalk.com/)
- [OA 审批 API 文档](https://open.dingtalk.com/document/orgapp-server/query-the-tasks-to-be-processed-by-the-user)
- [错误码查询](https://open.dingtalk.com/document/orgapp-server/error-code)
