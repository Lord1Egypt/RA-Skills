---
name: api-debugger-cn
version: 1.0.0
description: API 调试工具 - 快速测试 API、生成请求代码、分析响应。适合：后端开发者、前端工程师、QA。
metadata:
  openclaw:
    emoji: "🔌"
    requires:
      bins: ["curl"]
---

# API 调试工具 Skill

快速测试 API、生成请求代码、分析响应数据。

## 核心功能

| 功能 | 描述 |
|------|------|
| 快速测试 | 发送 GET/POST/PUT/DELETE 请求 |
| 代码生成 | 生成 curl/Python/Node.js/fetch 代码 |
| 响应分析 | 格式化 JSON、提取字段、对比差异 |
| 认证支持 | Bearer Token、Basic Auth、API Key |

## 使用方法

### 测试 API

```
测试 API: GET https://api.example.com/users
```

### 生成请求代码

```
为这个 API 生成 Python 代码: POST https://api.example.com/login
```

### 分析响应

```
分析这个 JSON 响应的结构
```

## 快速命令

### GET 请求

```bash
# 基础 GET
curl -s "https://api.example.com/users"

# 带参数
curl -s "https://api.example.com/users?page=1&limit=10"

# 带 Header
curl -s -H "Authorization: Bearer TOKEN" \
  "https://api.example.com/users"

# 保存响应
curl -s "https://api.example.com/users" -o response.json
```

### POST 请求

```bash
# JSON Body
curl -s -X POST "https://api.example.com/users" \
  -H "Content-Type: application/json" \
  -d '{"name": "张三", "email": "zhangsan@example.com"}'

# Form Data
curl -s -X POST "https://api.example.com/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=123456"

# 文件上传
curl -s -X POST "https://api.example.com/upload" \
  -F "file=@/path/to/file.jpg"
```

### PUT/PATCH/DELETE

```bash
# PUT（完整更新）
curl -s -X PUT "https://api.example.com/users/1" \
  -H "Content-Type: application/json" \
  -d '{"name": "李四", "email": "lisi@example.com"}'

# PATCH（部分更新）
curl -s -X PATCH "https://api.example.com/users/1" \
  -H "Content-Type: application/json" \
  -d '{"name": "王五"}'

# DELETE
curl -s -X DELETE "https://api.example.com/users/1"
```

## 认证方式

### Bearer Token

```bash
curl -s -H "Authorization: Bearer YOUR_TOKEN" \
  "https://api.example.com/protected"
```

### Basic Auth

```bash
curl -s -u "username:password" \
  "https://api.example.com/protected"
```

### API Key

```bash
# Header 方式
curl -s -H "X-API-Key: YOUR_KEY" \
  "https://api.example.com/protected"

# Query 参数方式
curl -s "https://api.example.com/protected?api_key=YOUR_KEY"
```

## 代码生成

### Python (requests)

```python
import requests

url = "https://api.example.com/users"
headers = {
    "Authorization": "Bearer TOKEN",
    "Content-Type": "application/json"
}

# GET
response = requests.get(url, headers=headers)
print(response.json())

# POST
data = {"name": "张三", "email": "zhangsan@example.com"}
response = requests.post(url, headers=headers, json=data)
print(response.json())
```

### Node.js (fetch)

```javascript
const url = 'https://api.example.com/users';
const headers = {
  'Authorization': 'Bearer TOKEN',
  'Content-Type': 'application/json'
};

// GET
fetch(url, { headers })
  .then(res => res.json())
  .then(data => console.log(data));

// POST
fetch(url, {
  method: 'POST',
  headers,
  body: JSON.stringify({ name: '张三', email: 'zhangsan@example.com' })
})
  .then(res => res.json())
  .then(data => console.log(data));
```

### Node.js (axios)

```javascript
const axios = require('axios');

const api = axios.create({
  baseURL: 'https://api.example.com',
  headers: { 'Authorization': 'Bearer TOKEN' }
});

// GET
const { data } = await api.get('/users');

// POST
const { data: created } = await api.post('/users', {
  name: '张三',
  email: 'zhangsan@example.com'
});
```

### JavaScript (浏览器 fetch)

```javascript
const url = 'https://api.example.com/users';

// GET
fetch(url, {
  headers: { 'Authorization': 'Bearer TOKEN' }
})
  .then(r => r.json())
  .then(console.log);

// POST
fetch(url, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name: '张三' })
})
  .then(r => r.json())
  .then(console.log);
```

## 响应处理

### 格式化 JSON

```bash
# 使用 jq
curl -s "https://api.example.com/users" | jq .

# 提取字段
curl -s "https://api.example.com/users" | jq '.data[].name'

# 提取数组
curl -s "https://api.example.com/users" | jq '.data | length'
```

### Python 处理

```python
import requests
import json

response = requests.get("https://api.example.com/users")
data = response.json()

# 美化输出
print(json.dumps(data, indent=2, ensure_ascii=False))

# 提取字段
names = [item['name'] for item in data['data']]
print(names)

# 计算统计
print(f"Total: {len(data['data'])}")
```

## 调试技巧

### 查看请求详情

```bash
# 显示响应头
curl -i "https://api.example.com/users"

# 显示详细信息
curl -v "https://api.example.com/users"

# 显示时间统计
curl -w "\nTime: %{time_total}s\n" "https://api.example.com/users"
```

### 测试性能

```bash
# 测试响应时间
curl -w "DNS: %{time_namelookup}s\nConnect: %{time_connect}s\nTTFB: %{time_starttransfer}s\nTotal: %{time_total}s\n" -o /dev/null -s "https://api.example.com/users"

# 批量测试
for i in {1..10}; do
  curl -w "$i: %{time_total}s\n" -o /dev/null -s "https://api.example.com/users"
done
```

### 错误处理

```bash
# 检查状态码
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "https://api.example.com/users")

if [ "$HTTP_CODE" -eq 200 ]; then
  echo "成功"
else
  echo "失败: $HTTP_CODE"
fi

# 重试机制
for i in {1..3}; do
  response=$(curl -s "https://api.example.com/users")
  if [ $? -eq 0 ]; then
    echo "$response"
    break
  fi
  echo "重试 $i/3..."
  sleep 2
done
```

## 常用 API 测试

### 测试 REST API

```bash
# 列表
curl -s "https://jsonplaceholder.typicode.com/posts" | jq '.[0:3]'

# 详情
curl -s "https://jsonplaceholder.typicode.com/posts/1" | jq .

# 创建
curl -s -X POST "https://jsonplaceholder.typicode.com/posts" \
  -H "Content-Type: application/json" \
  -d '{"title": "测试", "body": "内容", "userId": 1}' | jq .

# 更新
curl -s -X PUT "https://jsonplaceholder.typicode.com/posts/1" \
  -H "Content-Type: application/json" \
  -d '{"title": "更新后"}' | jq .

# 删除
curl -s -X DELETE "https://jsonplaceholder.typicode.com/posts/1"
```

### 测试 GraphQL

```bash
curl -s -X POST "https://graphql.example.com" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ users { id name } }"}' | jq .
```

## 注意事项

- 敏感信息不要硬编码，使用环境变量
- 测试环境与生产环境分开
- 记录 API 调用日志
- 注意 API 限流

---

创建：2026-03-12
版本：1.0