# 接口自动化测试模块使用指南

## 📖 概述

接口自动化测试模块基于 **Pytest + Requests** 框架，提供完整的API测试解决方案：
- 测试脚本管理和版本控制
- 环境配置管理（支持多环境切换）
- 实时调试功能
- 异步批量执行
- 测试报告自动生成
- 执行记录和历史追溯

## 🚀 快速开始

### 1. 创建测试脚本

**手动创建：**

```python
import pytest
import requests

class TestUserAPI:
    """用户API测试"""

    base_url = "http://localhost:8000"

    def test_get_user_list(self):
        """测试获取用户列表"""
        response = requests.get(f"{self.base_url}/api/users")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_create_user(self):
        """测试创建用户"""
        data = {
            "username": "testuser",
            "email": "test@example.com"
        }
        response = requests.post(f"{self.base_url}/api/users", json=data)
        assert response.status_code in [200, 201]
        assert response.json()["username"] == "testuser"

    def test_update_user(self):
        """测试更新用户"""
        user_id = 1
        data = {"username": "updateduser"}
        response = requests.put(f"{self.base_url}/api/users/{user_id}", json=data)
        assert response.status_code == 200

    def test_delete_user(self):
        """测试删除用户"""
        user_id = 1
        response = requests.delete(f"{self.base_url}/api/users/{user_id}")
        assert response.status_code in [200, 204]
```

**通过API创建：**

```bash
POST http://localhost:8000/api/script
Authorization: Bearer your_auth_code

{
  "name": "用户API测试",
  "content": "import pytest\nimport requests\n...",
  "type": "api"
}
```

### 2. 配置测试环境

**配置开发环境：**

```bash
POST http://localhost:8000/api/environment

{
  "name": "dev",
  "base_url": "http://localhost:8000",
  "headers": {
    "Authorization": "Bearer dev_token"
  },
  "params": {}
}
```

**配置测试环境：**

```bash
POST http://localhost:8000/api/environment

{
  "name": "test",
  "base_url": "http://test.example.com",
  "headers": {
    "Authorization": "Bearer test_token"
  }
}
```

### 3. 调试脚本

在正式执行前，可以先调试脚本：

```bash
POST http://localhost:8000/api/script/1/debug?environment=dev
Authorization: Bearer your_auth_code
```

**响应示例：**

```json
{
  "code": 200,
  "msg": "调试完成",
  "data": {
    "success": true,
    "log": "test_get_user_list PASSED\ntest_create_user PASSED\n...",
    "duration": 2,
    "request": {
      "method": "GET",
      "url": "http://localhost:8000/api/users"
    },
    "response": {
      "status_code": 200,
      "body": [...]
    }
  }
}
```

### 4. 执行测试

**执行单个脚本：**

```bash
POST http://localhost:8000/execute/run
Authorization: Bearer your_auth_code

{
  "script_id": 1,
  "environment": "dev",
  "timeout": 300
}
```

**响应：**

```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "message": "测试执行任务已创建，请通过task_id查询进度"
}
```

**批量执行：**

```bash
POST http://localhost:8000/execute/batch
Authorization: Bearer your_auth_code

{
  "script_ids": [1, 2, 3],
  "environment": "test",
  "timeout": 600
}
```

### 5. 查询执行进度

```bash
GET http://localhost:8000/execute/progress/{task_id}
```

**响应示例：**

```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "task_type": "execute",
  "status": "completed",
  "progress": 100,
  "message": "执行完成",
  "result_data": "{\"success\": true, \"duration\": 5}",
  "create_time": "2026-03-23 10:00:00",
  "update_time": "2026-03-23 10:00:05"
}
```

### 6. 查看执行记录

**获取执行记录列表：**

```bash
GET http://localhost:8000/execute/records?script_id=1&limit=50
Authorization: Bearer your_auth_code
```

**获取执行记录详情：**

```bash
GET http://localhost:8000/execute/record/123
```

## 📝 完整示例

### 示例1：用户登录API测试

```python
import pytest
import requests

class TestLoginAPI:
    """登录API测试"""

    base_url = "http://localhost:8000"

    @pytest.fixture(autouse=True)
    def setup(self):
        """每个测试前的初始化"""
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })

    def test_login_success(self):
        """测试登录成功"""
        data = {
            "username": "admin",
            "password": "password123"
        }
        response = self.session.post(f"{self.base_url}/api/login", json=data)

        assert response.status_code == 200
        result = response.json()
        assert "token" in result
        assert result["username"] == "admin"

    def test_login_invalid_password(self):
        """测试密码错误"""
        data = {
            "username": "admin",
            "password": "wrong_password"
        }
        response = self.session.post(f"{self.base_url}/api/login", json=data)

        assert response.status_code == 401
        assert "error" in response.json()

    def test_login_missing_username(self):
        """测试缺少用户名"""
        data = {"password": "password123"}
        response = self.session.post(f"{self.base_url}/api/login", json=data)

        assert response.status_code == 400

    def teardown_method(self):
        """清理资源"""
        self.session.close()
```

### 示例2：参数化测试

```python
import pytest
import requests

class TestUserAPI:
    """用户API参数化测试"""

    base_url = "http://localhost:8000"

    @pytest.mark.parametrize("user_id,expected_status", [
        (1, 200),
        (2, 200),
        (999, 404),
        (-1, 400)
    ])
    def test_get_user_by_id(self, user_id, expected_status):
        """测试根据ID获取用户"""
        response = requests.get(f"{self.base_url}/api/users/{user_id}")
        assert response.status_code == expected_status

    @pytest.mark.parametrize("username,email,expected_status", [
        ("user1", "user1@example.com", 201),
        ("user2", "user2@example.com", 201),
        ("", "user3@example.com", 400),
        ("user4", "", 400)
    ])
    def test_create_user_validation(self, username, email, expected_status):
        """测试创建用户的数据验证"""
        data = {"username": username, "email": email}
        response = requests.post(f"{self.base_url}/api/users", json=data)
        assert response.status_code == expected_status
```

### 示例3：使用环境配置

```python
import pytest
import requests

# 环境配置会自动注入到脚本开头
# TEST_BASE_URL = "http://test.example.com"
# TEST_HEADERS = {"Authorization": "Bearer test_token"}
# TEST_PARAMS = {}

class TestAPIWithEnv:
    """使用环境配置的API测试"""

    def test_with_environment(self):
        """测试使用环境配置"""
        response = requests.get(
            f"{TEST_BASE_URL}/api/users",
            headers=TEST_HEADERS,
            params=TEST_PARAMS
        )
        assert response.status_code == 200
```

## 🔧 API 接口列表

### 脚本管理

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/script` | POST | 创建测试脚本 |
| `/api/script/list` | GET | 获取脚本列表 |
| `/api/script/{id}` | GET | 获取脚本详情 |
| `/api/script/{id}` | PUT | 更新脚本 |
| `/api/script/{id}` | DELETE | 删除脚本 |
| `/api/script/{id}/debug` | POST | 调试脚本 |

### 环境管理

| 接口 | 方法 | 描述 |
|------|------|------|
| `/api/environment` | POST | 配置测试环境 |
| `/api/environment/{name}` | GET | 获取环境配置 |

### 测试执行

| 接口 | 方法 | 描述 |
|------|------|------|
| `/execute/run` | POST | 执行单个脚本 |
| `/execute/batch` | POST | 批量执行脚本 |
| `/execute/progress/{task_id}` | GET | 查询执行进度 |
| `/execute/records` | GET | 获取执行记录列表 |
| `/execute/record/{id}` | GET | 获取执行记录详情 |

## 💡 最佳实践

### 1. 脚本组织

- 每个API模块创建独立的测试类
- 使用fixture管理公共资源和初始化
- 合理使用参数化减少代码重复
- 添加详细的断言和错误提示

### 2. 环境管理

- 为不同环境（dev/test/prod）创建独立配置
- 使用环境变量存储敏感信息（token等）
- 统一管理base_url和全局headers

### 3. 执行策略

- 开发阶段使用调试功能快速验证
- 测试阶段使用批量执行提高效率
- 设置合理的超时时间避免长时间等待
- 定期清理历史执行记录

### 4. 结果分析

- 查看执行日志定位失败原因
- 分析执行趋势发现潜在问题
- 保存重要的测试报告用于追溯

## ⚠️ 注意事项

1. **执行环境**
   - 确保pytest已安装：`pip install pytest pytest-json-report`
   - 目标API服务正常运行
   - 网络连接正常

2. **超时设置**
   - 单脚本默认300秒
   - 批量执行默认600秒
   - 根据实际情况调整

3. **并发限制**
   - 同一时间最多5个并发执行任务
   - 避免对目标服务造成过大压力

4. **授权验证**
   - 所有执行接口需要授权码
   - 每次执行消耗1次使用次数

## 🐛 故障排查

### 执行失败

**可能原因：**
1. 脚本语法错误
2. 目标API不可访问
3. 环境配置错误
4. 超时时间不足

**解决方法：**
1. 使用调试功能验证脚本
2. 检查网络连接和API状态
3. 验证环境配置是否正确
4. 增加超时时间

### 调试失败

**可能原因：**
1. pytest未正确安装
2. 依赖包缺失
3. Python环境问题

**解决方法：**
```bash
pip install pytest pytest-json-report requests
```

## 📊 性能优化

1. **使用Session**：复用TCP连接，提高性能
2. **批量断言**：减少HTTP请求次数
3. **异步执行**：充分利用后台任务
4. **缓存数据**：避免重复创建测试数据

---

**版本：** v1.0.0
**更新时间：** 2026-03-23
