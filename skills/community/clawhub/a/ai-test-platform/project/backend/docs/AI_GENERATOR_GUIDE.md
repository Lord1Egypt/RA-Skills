# AI 生成模块使用指南

## 📖 概述

AI生成模块是AI自动化测试平台的核心功能之一，支持：
- 智能测试用例生成（功能、边界、异常用例）
- API自动化脚本生成（Pytest + Requests）
- UI自动化脚本生成（Playwright）
- 多格式文档解析（Word/Excel/PDF/Markdown）
- 异步任务进度追踪

## 🚀 快速开始

### 1. 配置 DeepSeek API

在 `.env` 文件中配置API密钥：

```bash
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

### 2. 创建授权码

```bash
# 方式1：使用脚本生成
python scripts/generate_auth.py

# 方式2：调用API生成
POST http://localhost:8000/api/admin/create_auth
{
  "permission": "all",
  "max_days": 365,
  "max_count": 100
}
```

响应示例：
```json
{
  "encrypted_code": "abcd1234...",
  "permission": "all",
  "expire_time": "2027-03-23 12:00:00",
  "max_count": 100
}
```

### 3. 启动后端服务

```bash
cd project/backend
uvicorn app.main:app --reload
```

访问 API 文档：http://localhost:8000/docs

## 📝 API 使用示例

### 生成测试用例

**接口：** `POST /api/generate/case`

**请求示例：**

```bash
curl -X POST "http://localhost:8000/api/generate/case" \
  -H "Authorization: Bearer your_encrypted_code" \
  -F "document_content=用户登录功能：用户输入正确的用户名和密码后，系统应该允许登录。" \
  -F "requirements=重点关注安全性测试"
```

**Python 示例：**

```python
import requests

url = "http://localhost:8000/api/generate/case"
headers = {"Authorization": "Bearer your_encrypted_code"}
data = {
    "document_content": "用户登录功能：用户输入正确的用户名和密码后，系统应该允许登录。",
    "requirements": "重点关注安全性测试"
}

response = requests.post(url, data=data, headers=headers)
result = response.json()
print(f"任务ID: {result['task_id']}")
```

**响应：**

```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "message": "测试用例生成任务已创建，请通过task_id查询进度"
}
```

### 生成 API 测试脚本

**接口：** `POST /api/generate/api`

**请求示例：**

```python
import requests

url = "http://localhost:8000/api/generate/api"
headers = {"Authorization": "Bearer your_encrypted_code"}
data = {
    "document_content": "API接口：GET /api/users - 获取用户列表，返回JSON格式数据",
    "api_info": "需要验证返回状态码和数据格式"
}

response = requests.post(url, data=data, headers=headers)
task_id = response.json()["task_id"]
```

### 生成 UI 测试脚本

**接口：** `POST /api/generate/ui`

**请求示例：**

```python
url = "http://localhost:8000/api/generate/ui"
headers = {"Authorization": "Bearer your_encrypted_code"}
data = {
    "document_content": "登录页面：用户输入用户名、密码，点击登录按钮",
    "ui_info": "使用Chrome浏览器，headless模式"
}

response = requests.post(url, data=data, headers=headers)
```

### 上传文档文件

支持上传 Word/Excel/PDF/Markdown 文件：

```python
url = "http://localhost:8000/api/generate/case"
headers = {"Authorization": "Bearer your_encrypted_code"}

# 上传文件
with open("需求文档.docx", "rb") as f:
    files = {"file": f}
    data = {"requirements": "生成完整的测试用例"}

    response = requests.post(url, files=files, data=data, headers=headers)
```

### 查询任务进度

**接口：** `GET /api/generate/progress/{task_id}`

**轮询示例：**

```python
import time

task_id = "550e8400-e29b-41d4-a716-446655440000"
url = f"http://localhost:8000/api/generate/progress/{task_id}"

while True:
    response = requests.get(url)
    result = response.json()

    print(f"状态: {result['status']}, 进度: {result['progress']}%, 消息: {result['message']}")

    if result['status'] == 'completed':
        print("生成完成！")
        print(f"结果: {result['result_data']}")
        break
    elif result['status'] == 'failed':
        print("生成失败！")
        break

    time.sleep(2)  # 每2秒查询一次
```

**响应示例：**

```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "task_type": "generate",
  "status": "completed",
  "progress": 100,
  "message": "生成完成",
  "result_data": "{\"test_case_id\": 1, \"content\": \"# 测试用例\\n\\n## TC-001...\"}",
  "create_time": "2026-03-23 10:00:00",
  "update_time": "2026-03-23 10:00:05"
}
```

## 📂 生成的文件存储

生成的脚本和用例会自动保存到：

- **测试用例：** 数据库 `test_cases` 表
- **API脚本：**
  - 数据库：`auto_scripts` 表
  - 文件：`data/scripts/api_script_{task_id}.py`
- **UI脚本：**
  - 数据库：`auto_scripts` 表
  - 文件：`data/scripts/ui_script_{task_id}.py`

## 🎯 最佳实践

### 1. 文档格式建议

**API文档（Swagger）：**
```
接口：GET /api/users
描述：获取用户列表
请求参数：
  - page: 页码（可选）
  - size: 每页数量（可选）
返回：JSON格式的用户列表
状态码：200（成功），401（未授权）
```

**UI文档：**
```
页面：登录页面
URL：http://example.com/login
操作流程：
1. 输入用户名（输入框ID：username）
2. 输入密码（输入框ID：password）
3. 点击登录按钮（按钮ID：login-btn）
预期结果：跳转到首页
```

### 2. 提高生成质量的技巧

- 提供详细的文档描述
- 明确指定测试重点
- 包含接口参数、返回值、异常情况
- 提供页面元素定位信息
- 说明业务逻辑和约束条件

### 3. 权限控制

- **全功能权限（all）：** 可生成所有类型内容
- **仅生成权限（generate）：** 只能生成测试用例和脚本
- **仅执行权限（execute）：** 不能使用生成功能

## ⚠️ 注意事项

1. **API调用限制：**
   - 最大重试次数：2次
   - 超时时间：30秒
   - 建议每天调用≤20次

2. **文件大小限制：**
   - Word文档：≤10MB
   - Excel文档：≤10MB
   - PDF文档：≤20MB
   - Markdown：无限制

3. **异步处理：**
   - 所有生成接口都是异步的
   - 必须通过轮询 `/generate/progress/{task_id}` 获取结果
   - 建议轮询间隔：2秒

4. **授权验证：**
   - 所有生成接口都需要授权码
   - 每次生成会消耗1次使用次数
   - 注意授权码有效期和权限类型

## 🐛 故障排查

### 生成失败

**可能原因：**
1. DeepSeek API密钥无效或过期
2. 网络连接问题
3. 文档内容为空或格式错误
4. API调用超时

**解决方法：**
1. 检查 `.env` 文件中的 `DEEPSEEK_API_KEY`
2. 查看后端日志：`logs/app.log`
3. 确认文档内容不为空
4. 重试生成任务

### 任务一直处于processing状态

**可能原因：**
1. 后台任务崩溃
2. 数据库连接失败

**解决方法：**
1. 重启后端服务
2. 检查数据库连接
3. 查看错误日志

## 📚 完整示例

查看 `tests/test_api_example.py` 获取完整的测试示例代码。

---

**版本：** v1.0.0
**更新时间：** 2026-03-23
