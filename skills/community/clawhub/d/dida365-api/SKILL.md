---
name: dida365
description: |
  滴答清单 (Dida365) API 集成，支持自建 OAuth 认证。管理任务和项目。
  当用户想要在滴答清单中创建、更新、完成或组织任务和项目时使用此 Skill。
  需要用户在 developer.dida365.com 创建应用并配置 DIDA365_CLIENT_ID、DIDA365_CLIENT_SECRET 环境变量。
metadata:
  author: community
  version: "1.0"
  clawdbot:
    emoji: ✅
    requires:
      env:
        - DIDA365_CLIENT_ID
        - DIDA365_CLIENT_SECRET
---

# Dida365 滴答清单

通过 Dida365 官方 OAuth 认证访问滴答清单 API，支持任务和项目的完整 CRUD 操作。

## 前置准备

### 1. 创建 Dida365 开发者应用

1. 登录 [developer.dida365.com](https://developer.dida365.com)
2. 点击「创建应用」
3. 填写应用名称（任意）
4. 在「回调地址 (Redirect URI)」中添加：`http://127.0.0.1:36500/callback`
5. 创建完成后，记录下 **Client ID** 和 **Client Secret**

### 2. 配置环境变量

```bash
export DIDA365_CLIENT_ID="YOUR_CLIENT_ID"
export DIDA365_CLIENT_SECRET="YOUR_CLIENT_SECRET"
```

建议将上述配置写入 `~/.bashrc`、`~/.zshrc` 或 `.env` 文件。

## 获取 Access Token

首次使用需要通过 OAuth 授权获取 Access Token。以下流程会启动一个临时本地服务来接收回调。

### 一键获取 Token（Python）

```bash
python3 << 'PYEOF'
import os, json, http.server, urllib.parse, urllib.request, threading, webbrowser

CLIENT_ID = os.environ["DIDA365_CLIENT_ID"]
CLIENT_SECRET = os.environ["DIDA365_CLIENT_SECRET"]
REDIRECT_URI = "http://127.0.0.1:36500/callback"
TOKEN_FILE = os.path.expanduser("~/.config/dida365/token")
code_holder = {}

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        if "code" in params:
            code_holder["code"] = params["code"][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Authorization successful! You can close this tab.")
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing code parameter.")
    def log_message(self, *args): pass

server = http.server.HTTPServer(("127.0.0.1", 36500), Handler)
thread = threading.Thread(target=server.handle_request)
thread.start()

auth_url = (
    f"https://dida365.com/oauth/authorize"
    f"?client_id={CLIENT_ID}"
    f"&scope=tasks%3Aread+tasks%3Awrite"
    f"&state=random_state_string"
    f"&redirect_uri={urllib.parse.quote(REDIRECT_URI, safe='')}"
    f"&response_type=code"
)
print(f"请在浏览器中打开以下链接并点击授权：\n\n{auth_url}\n")
webbrowser.open(auth_url)

thread.join(timeout=120)
server.server_close()

if "code" not in code_holder:
    print("❌ 超时：未收到授权码，请重试。")
    exit(1)

code = code_holder["code"]
print(f"✅ 已获取授权码，正在交换 Token...")

data = urllib.parse.urlencode({
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "code": code,
    "grant_type": "authorization_code",
    "redirect_uri": REDIRECT_URI,
}).encode()

req = urllib.request.Request(
    "https://dida365.com/oauth/token",
    data=data,
    method="POST"
)
req.add_header("Content-Type", "application/x-www-form-urlencoded")
resp = json.load(urllib.request.urlopen(req))
token = resp["access_token"]

os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)
with open(TOKEN_FILE, "w") as f:
    json.dump({"access_token": token}, f)
os.chmod(TOKEN_FILE, 0o600)

print(f"✅ Token 已保存到 {TOKEN_FILE}")
print(f"   有效期约 180 天，请注意及时重新授权。")
PYEOF
```

### Token 存储

Token 保存在 `~/.config/dida365/token`，格式：

```json
{
  "access_token": "your_access_token_here"
}
```

**⚠️ 重要提示：**
- Token 有效期约 **180 天**
- 滴答清单当前 API **没有 refresh_token** 机制
- Token 过期后需重新执行上述授权流程
- 请妥善保管 Token 文件，不要提交到版本控制系统

## Base URL

```
https://api.dida365.com/open/v1/
```

## 认证

所有请求需要在 Authorization 头中携带 Access Token：

```
Authorization: Bearer {ACCESS_TOKEN}
```

### 快速测试

```bash
# 读取 Token 并列出项目
python3 << 'PYEOF'
import os, json, urllib.request

token_file = os.path.expanduser("~/.config/dida365/token")
with open(token_file) as f:
    token = json.load(f)["access_token"]

req = urllib.request.Request("https://api.dida365.com/open/v1/project")
req.add_header("Authorization", f"Bearer {token}")
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2, ensure_ascii=False))
PYEOF
```

## API 参考

### 项目操作

#### 列出所有项目

```
GET /open/v1/project
```

**响应示例：**
```json
[
  {
    "id": "6984773291819e6d58b746a8",
    "name": "📝 收集箱",
    "sortOrder": 0,
    "viewMode": "list",
    "kind": "TASK"
  },
  {
    "id": "6984773291819e6d58b746a9",
    "name": "🏠 个人",
    "sortOrder": -1099511627776,
    "viewMode": "list",
    "kind": "TASK"
  }
]
```

#### 获取项目及任务

```
GET /open/v1/project/{projectId}/data
```

**响应示例：**
```json
{
  "project": {
    "id": "69847732b8e5e969f70e7460",
    "name": "📋 工作",
    "sortOrder": -3298534883328,
    "viewMode": "list",
    "kind": "TASK"
  },
  "tasks": [
    {
      "id": "69847732b8e5e969f70e7464",
      "projectId": "69847732b8e5e969f70e7460",
      "title": "完成报告",
      "content": "季度总结报告",
      "priority": 0,
      "status": 0,
      "tags": [],
      "isAllDay": false
    }
  ],
  "columns": [
    {
      "id": "69847732b8e5e969f70e7463",
      "projectId": "69847732b8e5e969f70e7460",
      "name": "待办",
      "sortOrder": -2199023255552
    }
  ]
}
```

#### 创建项目

```
POST /open/v1/project
Content-Type: application/json

{
  "name": "我的新项目",
  "viewMode": "list"
}
```

**响应示例：**
```json
{
  "id": "69870cbe8f08b4a6770a38d3",
  "name": "我的新项目",
  "sortOrder": 0,
  "viewMode": "list",
  "kind": "TASK"
}
```

**viewMode 选项：**
- `list` - 列表视图
- `kanban` - 看板视图
- `timeline` - 时间线视图

#### 删除项目

```
DELETE /open/v1/project/{projectId}
```

成功时返回空响应（状态码 200）。

### 任务操作

#### 获取任务

```
GET /open/v1/project/{projectId}/task/{taskId}
```

**响应示例：**
```json
{
  "id": "69847732b8e5e969f70e7464",
  "projectId": "69847732b8e5e969f70e7460",
  "sortOrder": -1099511627776,
  "title": "任务标题",
  "content": "任务描述/备注",
  "timeZone": "Asia/Shanghai",
  "isAllDay": true,
  "priority": 0,
  "status": 0,
  "tags": [],
  "columnId": "69847732b8e5e969f70e7461",
  "etag": "2sayfdsh",
  "kind": "TEXT"
}
```

#### 创建任务

```
POST /open/v1/task
Content-Type: application/json

{
  "title": "新任务",
  "projectId": "6984773291819e6d58b746a8",
  "content": "任务描述",
  "priority": 0,
  "dueDate": "2026-03-15T10:00:00+0000",
  "isAllDay": false
}
```

**响应示例：**
```json
{
  "id": "69870cb08f08b86b38951175",
  "projectId": "6984773291819e6d58b746a8",
  "sortOrder": -1099511627776,
  "title": "新任务",
  "timeZone": "Asia/Shanghai",
  "isAllDay": false,
  "priority": 0,
  "status": 0,
  "tags": [],
  "etag": "gl7ibhor",
  "kind": "TEXT"
}
```

**优先级值：**
- `0` - 无
- `1` - 低
- `3` - 中
- `5` - 高

#### 更新任务

```
POST /open/v1/task/{id}
Content-Type: application/json

{
  "id": "69870cb08f08b86b38951175",
  "projectId": "6984773291819e6d58b746a8",
  "title": "更新后的任务标题",
  "priority": 1
}
```

**响应示例：**
```json
{
  "id": "69870cb08f08b86b38951175",
  "projectId": "6984773291819e6d58b746a8",
  "title": "更新后的任务标题",
  "priority": 1,
  "status": 0,
  "etag": "hmb7uk8c",
  "kind": "TEXT"
}
```

#### 完成任务

```
POST /open/v1/project/{projectId}/task/{taskId}/complete
```

成功时返回空响应（状态码 200）。

#### 删除任务

```
DELETE /open/v1/project/{projectId}/task/{taskId}
```

成功时返回空响应（状态码 200）。

## 任务字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 任务 ID |
| `projectId` | string | 所属项目 ID |
| `title` | string | 任务标题 |
| `content` | string | 任务描述/备注（支持 Markdown） |
| `priority` | integer | 优先级：0=无, 1=低, 3=中, 5=高 |
| `status` | integer | 状态：0=进行中, 2=已完成 |
| `dueDate` | string | 截止日期（ISO 8601 格式） |
| `startDate` | string | 开始日期（ISO 8601 格式） |
| `isAllDay` | boolean | 是否全天任务 |
| `timeZone` | string | 时区（如 "Asia/Shanghai"） |
| `tags` | array | 标签列表 |
| `columnId` | string | 看板列 ID（看板视图时使用） |
| `sortOrder` | number | 项目内的排序 |
| `kind` | string | 任务类型："TEXT"、"CHECKLIST" |

## 代码示例

### Python（requests）

```python
import os, json

# 读取 Token
with open(os.path.expanduser("~/.config/dida365/token")) as f:
    token = json.load(f)["access_token"]

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# 列出所有项目
import requests
resp = requests.get("https://api.dida365.com/open/v1/project", headers=headers)
projects = resp.json()
print(json.dumps(projects, indent=2, ensure_ascii=False))

# 创建任务
resp = requests.post("https://api.dida365.com/open/v1/task", headers=headers, json={
    "title": "新任务",
    "projectId": "YOUR_PROJECT_ID",
    "content": "通过 API 创建的任务",
    "priority": 3,
    "dueDate": "2026-04-01T09:00:00+0800"
})
print(resp.json())

# 完成任务
resp = requests.post(
    "https://api.dida365.com/open/v1/project/YOUR_PROJECT_ID/task/TASK_ID/complete",
    headers=headers
)
print(f"状态: {resp.status_code}")
```

### JavaScript（fetch）

```javascript
import { readFileSync } from "fs";

// 读取 Token
const { access_token: token } = JSON.parse(
  readFileSync(process.env.HOME + "/.config/dida365/token", "utf-8")
);

const headers = {
  Authorization: `Bearer ${token}`,
  "Content-Type": "application/json",
};

// 列出所有项目
const projects = await fetch("https://api.dida365.com/open/v1/project", {
  headers,
}).then((r) => r.json());
console.log(projects);

// 创建任务
const task = await fetch("https://api.dida365.com/open/v1/task", {
  method: "POST",
  headers,
  body: JSON.stringify({
    title: "新任务",
    projectId: "YOUR_PROJECT_ID",
    content: "通过 API 创建的任务",
    priority: 3,
  }),
}).then((r) => r.json());
console.log(task);

// 完成任务
await fetch(
  `https://api.dida365.com/open/v1/project/YOUR_PROJECT_ID/task/TASK_ID/complete`,
  { method: "POST", headers }
);
```

### curl 示例

```bash
# 读取 Token
TOKEN=$(cat ~/.config/dida365/token | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# 列出项目
curl -s -H "Authorization: Bearer $TOKEN" https://api.dida365.com/open/v1/project | python3 -m json.tool

# 创建任务
curl -s -X POST https://api.dida365.com/open/v1/task \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"测试任务","projectId":"YOUR_PROJECT_ID"}' | python3 -m json.tool
```

## 注意事项

- Open API 仅提供任务和项目的访问
- 习惯、专注/番茄钟等功能不通过 Open API 提供
- 任务 `status` 值：0 = 进行中，2 = 已完成
- 优先级值：0 = 无，1 = 低，3 = 中，5 = 高
- 日期使用 ISO 8601 格式带时区偏移（如 `2026-03-15T10:00:00+0800`）
- 项目的 `viewMode` 选项：`list`、`kanban`、`timeline`
- `columns` 字段用于看板视图的列定义
- **Token 有效期约 180 天，无 refresh_token，过期需重新授权**

## 错误处理

| 状态码 | 含义 | 处理方式 |
|--------|------|----------|
| 400 | 请求参数错误 | 检查请求体格式和必填字段 |
| 401 | Token 无效或已过期 | 重新执行 OAuth 授权流程获取新 Token |
| 404 | 资源未找到 | 确认项目 ID / 任务 ID 是否正确 |
| 429 | 请求频率超限 | 降低请求频率，等待后重试 |
| 5xx | 服务端错误 | 稍后重试 |

### 故障排除

**Token 过期（401 错误）：**
```bash
# 重新运行授权脚本获取新 Token
# 参考上方「获取 Access Token」章节
```

**检查 Token 有效性：**
```bash
TOKEN=$(cat ~/.config/dida365/token | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer $TOKEN" https://api.dida365.com/open/v1/project
# 返回 200 表示有效，返回 401 表示已过期
```

**环境变量未设置：**
```bash
echo $DIDA365_CLIENT_ID
echo $DIDA365_CLIENT_SECRET
```

## 资源

- [Dida365 开发者平台](https://developer.dida365.com)
- [滴答清单官网](https://dida365.com)
- [滴答清单帮助中心](https://help.dida365.com)
