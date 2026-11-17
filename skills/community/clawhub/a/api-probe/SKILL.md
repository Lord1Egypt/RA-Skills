---
name: api-probe
description: 专业的 API 接口测试与验证工具。支持 REST API、GraphQL、WebSocket 测试，自动生成测试用例，验证接口契约，模拟 Mock 服务。当用户需要测试 API 接口、验证接口参数、测试接口性能、生成接口测试报告、Mock 接口数据、或进行接口契约测试时使用此技能。也适用于用户提到"接口测试"、"API测试"、"REST测试"、"接口验证"、"Mock服务"、"契约测试"、"Postman"、"Swagger"、"OpenAPI"等场景。
---

# API 探针

你是一个专业的 API 测试工程师，帮助用户进行全面的接口测试、契约验证和 Mock 服务搭建。

## 核心能力

1. **接口测试**：REST API、GraphQL、WebSocket 全面测试
2. **用例生成**：根据 Swagger/OpenAPI 文档自动生成测试用例
3. **契约测试**：验证接口是否符合契约定义
4. **Mock 服务**：快速搭建 Mock 接口进行联调测试
5. **性能测试**：接口性能基准测试和压测
6. **安全测试**：接口安全漏洞扫描和验证

## 工作流程

### 1. 输入接收

确认用户提供的信息：

| 输入类型 | 内容 | 处理方式 |
|---------|------|---------|
| Swagger/OpenAPI 文档 | JSON/YAML 格式 | 解析接口定义，生成测试用例 |
| 接口文档 | Markdown/HTML | 提取接口信息，构建测试 |
| 接口地址 | URL + 方法 | 直接发起请求测试 |
| cURL 命令 | shell 命令 | 解析并转换为测试脚本 |
| Postman Collection | JSON 导出 | 导入并执行测试 |

### 2. 接口测试框架

#### 2.1 REST API 测试

**基础测试模板（Python + requests + pytest）：**

```python
"""
API 接口测试模块
"""
import pytest
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class TestUserAPI:
    """用户接口测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self, base_url):
        self.base_url = base_url
        self.api_url = f"{base_url}/api/v1/users"
        
        # 配置重试策略
        self.session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        
        # 认证
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.get_token()}"
        }
    
    def get_token(self):
        """获取认证 Token"""
        response = requests.post(f"{self.base_url}/auth/login", json={
            "username": "testuser",
            "password": "Test1234"
        })
        return response.json()["access_token"]
    
    # ==================== 正向测试 ====================
    
    def test_create_user_success(self):
        """测试创建用户 - 正常场景"""
        # Arrange
        payload = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "Password123"
        }
        
        # Act
        response = self.session.post(self.api_url, json=payload, headers=self.headers)
        
        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "newuser@example.com"
        assert "id" in data
        assert "password" not in data  # 不应返回密码
    
    def test_get_user_list(self):
        """测试获取用户列表"""
        # Act
        response = self.session.get(self.api_url, headers=self.headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
    
    def test_get_user_by_id(self):
        """测试根据 ID 获取用户"""
        # Arrange
        user_id = 1
        
        # Act
        response = self.session.get(f"{self.api_url}/{user_id}", headers=self.headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
    
    def test_update_user(self):
        """测试更新用户"""
        # Arrange
        user_id = 1
        payload = {"email": "updated@example.com"}
        
        # Act
        response = self.session.put(f"{self.api_url}/{user_id}", json=payload, headers=self.headers)
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "updated@example.com"
    
    def test_delete_user(self):
        """测试删除用户"""
        # Arrange
        user_id = 999  # 使用测试用户 ID
        
        # Act
        response = self.session.delete(f"{self.api_url}/{user_id}", headers=self.headers)
        
        # Assert
        assert response.status_code in [200, 204]
    
    # ==================== 参数校验测试 ====================
    
    @pytest.mark.parametrize("username,error_msg", [
        ("", "用户名不能为空"),
        ("ab", "用户名长度至少3位"),
        ("a" * 51, "用户名长度不能超过50"),
        ("user@#$", "用户名包含非法字符"),
    ])
    def test_create_user_invalid_username(self, username, error_msg):
        """测试创建用户 - 无效用户名"""
        payload = {"username": username, "email": "test@example.com", "password": "Password123"}
        response = self.session.post(self.api_url, json=payload, headers=self.headers)
        
        assert response.status_code == 400
        assert error_msg in response.json().get("message", "")
    
    @pytest.mark.parametrize("email,error_msg", [
        ("", "邮箱不能为空"),
        ("invalid", "邮箱格式不正确"),
        ("test@", "邮箱格式不正确"),
    ])
    def test_create_user_invalid_email(self, email, error_msg):
        """测试创建用户 - 无效邮箱"""
        payload = {"username": "testuser", "email": email, "password": "Password123"}
        response = self.session.post(self.api_url, json=payload, headers=self.headers)
        
        assert response.status_code == 400
    
    # ==================== 异常场景测试 ====================
    
    def test_get_user_not_found(self):
        """测试获取不存在的用户"""
        response = self.session.get(f"{self.api_url}/99999", headers=self.headers)
        assert response.status_code == 404
    
    def test_create_duplicate_user(self):
        """测试创建重复用户"""
        payload = {"username": "existing_user", "email": "existing@example.com", "password": "Password123"}
        
        # 第一次创建
        self.session.post(self.api_url, json=payload, headers=self.headers)
        
        # 第二次创建（应该失败）
        response = self.session.post(self.api_url, json=payload, headers=self.headers)
        assert response.status_code == 409  # Conflict
    
    def test_unauthorized_access(self):
        """测试未授权访问"""
        response = requests.get(self.api_url)  # 不带 Token
        assert response.status_code == 401
    
    # ==================== 性能基准测试 ====================
    
    def test_response_time(self):
        """测试接口响应时间"""
        import time
        
        start = time.time()
        response = self.session.get(self.api_url, headers=self.headers)
        duration = time.time() - start
        
        assert response.status_code == 200
        assert duration < 1.0  # 响应时间应小于 1 秒
```

#### 2.2 GraphQL 测试

```python
class TestGraphQLAPI:
    """GraphQL 接口测试"""
    
    @pytest.fixture(autouse=True)
    def setup(self, base_url):
        self.graphql_url = f"{base_url}/graphql"
        self.headers = {"Content-Type": "application/json"}
    
    def test_query_users(self):
        """测试查询用户列表"""
        query = """
        query {
            users {
                id
                username
                email
            }
        }
        """
        response = requests.post(self.graphql_url, json={"query": query}, headers=self.headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "data" in data
        assert "users" in data["data"]
    
    def test_mutation_create_user(self):
        """测试创建用户 Mutation"""
        mutation = """
        mutation CreateUser($input: CreateUserInput!) {
            createUser(input: $input) {
                id
                username
                email
            }
        }
        """
        variables = {
            "input": {
                "username": "newuser",
                "email": "new@example.com",
                "password": "Password123"
            }
        }
        
        response = requests.post(
            self.graphql_url,
            json={"query": mutation, "variables": variables},
            headers=self.headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["data"]["createUser"]["username"] == "newuser"
```

#### 2.3 WebSocket 测试

```python
import pytest
import asyncio
import websockets
import json


class TestWebSocketAPI:
    """WebSocket 接口测试"""
    
    @pytest.fixture
    def ws_url(self):
        return "ws://localhost:8080/ws"
    
    @pytest.mark.asyncio
    async def test_ws_connect(self, ws_url):
        """测试 WebSocket 连接建立"""
        async with websockets.connect(ws_url) as ws:
            assert ws.open
            # 验证连接成功后的初始消息
            msg = await asyncio.wait_for(ws.recv(), timeout=5)
            data = json.loads(msg)
            assert data["type"] == "connected"
    
    @pytest.mark.asyncio
    async def test_ws_send_receive(self, ws_url):
        """测试消息发送与接收"""
        async with websockets.connect(ws_url) as ws:
            # 发送消息
            await ws.send(json.dumps({
                "action": "subscribe",
                "channel": "updates"
            }))
            
            # 接收确认
            response = await asyncio.wait_for(ws.recv(), timeout=5)
            data = json.loads(response)
            assert data["action"] == "subscribed"
            assert data["channel"] == "updates"
    
    @pytest.mark.asyncio
    async def test_ws_broadcast(self, ws_url):
        """测试多客户端广播"""
        async with websockets.connect(ws_url) as ws1, \
                     websockets.connect(ws_url) as ws2:
            # ws1 发送消息
            await ws1.send(json.dumps({
                "action": "broadcast",
                "message": "hello"
            }))
            
            # ws2 应收到广播
            response = await asyncio.wait_for(ws2.recv(), timeout=5)
            data = json.loads(response)
            assert data["message"] == "hello"
    
    @pytest.mark.asyncio
    async def test_ws_invalid_message(self, ws_url):
        """测试发送无效消息格式"""
        async with websockets.connect(ws_url) as ws:
            await ws.send("invalid json{{{")
            response = await asyncio.wait_for(ws.recv(), timeout=5)
            data = json.loads(response)
            assert data["type"] == "error"
            assert "invalid" in data.get("message", "").lower()
    
    @pytest.mark.asyncio
    async def test_ws_unauthorized(self):
        """测试未认证的 WebSocket 连接"""
        ws_url_no_auth = "ws://localhost:8080/ws/protected"
        with pytest.raises(websockets.exceptions.InvalidStatusCode) as exc_info:
            async with websockets.connect(ws_url_no_auth):
                pass
        assert exc_info.value.status_code == 401
    
    @pytest.mark.asyncio
    async def test_ws_heartbeat(self, ws_url):
        """测试心跳保活机制"""
        async with websockets.connect(ws_url) as ws:
            # 等待心跳 ping（通常 30s 一次）
            for _ in range(3):
                msg = await asyncio.wait_for(ws.recv(), timeout=35)
                data = json.loads(msg)
                if data.get("type") == "ping":
                    # 回复 pong
                    await ws.send(json.dumps({"type": "pong"}))
    
    @pytest.mark.asyncio
    async def test_ws_concurrent_connections(self, ws_url):
        """测试大量并发连接"""
        connections = []
        for _ in range(100):
            ws = await websockets.connect(ws_url)
            connections.append(ws)
        
        # 所有连接应正常建立
        assert all(ws.open for ws in connections)
        
        # 关闭所有连接
        for ws in connections:
            await ws.close()
```

#### 2.4 从 Swagger/OpenAPI 生成测试

```python
import json
import yaml

def generate_tests_from_openapi(spec_path):
    """从 OpenAPI 文档生成测试用例"""
    # 加载文档
    with open(spec_path) as f:
        if spec_path.endswith('.yaml'):
            spec = yaml.safe_load(f)
        else:
            spec = json.load(f)
    
    tests = []
    base_url = spec.get('servers', [{}])[0].get('url', '')
    
    for path, methods in spec.get('paths', {}).items():
        for method, details in methods.items():
            if method not in ['get', 'post', 'put', 'delete', 'patch']:
                continue
            
            test = {
                "path": path,
                "method": method.upper(),
                "summary": details.get('summary', ''),
                "parameters": [],
                "request_body": None,
                "responses": details.get('responses', {})
            }
            
            # 提取参数
            for param in details.get('parameters', []):
                test["parameters"].append({
                    "name": param.get('name'),
                    "in": param.get('in'),  # path, query, header
                    "required": param.get('required', False),
                    "type": param.get('schema', {}).get('type', 'string')
                })
            
            # 提取请求体
            if 'requestBody' in details:
                content = details['requestBody'].get('content', {})
                if 'application/json' in content:
                    test["request_body"] = content['application/json'].get('schema', {})
            
            tests.append(test)
    
    return tests
```

### 3. 契约测试

验证接口是否符合契约定义：

```python
import jsonschema

class TestContractTesting:
    """接口契约测试"""
    
    @pytest.fixture
    def user_schema(self):
        """用户接口响应契约"""
        return {
            "type": "object",
            "required": ["id", "username", "email", "created_at"],
            "properties": {
                "id": {"type": "integer"},
                "username": {"type": "string", "minLength": 3, "maxLength": 50},
                "email": {"type": "string", "format": "email"},
                "created_at": {"type": "string", "format": "date-time"}
            },
            "additionalProperties": False
        }
    
    def test_user_response_contract(self, user_schema):
        """验证用户接口响应符合契约"""
        # Act
        response = requests.get(f"{self.base_url}/api/users/1")
        data = response.json()
        
        # Assert - 验证响应符合契约
        jsonschema.validate(instance=data, schema=user_schema)
    
    def test_user_list_response_contract(self):
        """验证用户列表接口响应符合契约"""
        response = requests.get(f"{self.base_url}/api/users")
        data = response.json()
        
        # 验证是数组
        assert isinstance(data, list)
        
        # 验证每个元素符合契约
        for user in data:
            jsonschema.validate(instance=user, schema=self.user_schema())
```

### 4. Mock 服务

快速搭建 Mock 接口：

```python
from flask import Flask, jsonify, request
import threading

class MockServer:
    """Mock API 服务"""
    
    def __init__(self, port=5001):
        self.app = Flask(__name__)
        self.port = port
        self.setup_routes()
    
    def setup_routes(self):
        """配置 Mock 路由"""
        
        @self.app.route('/api/users', methods=['GET'])
        def get_users():
            return jsonify([
                {"id": 1, "username": "user1", "email": "user1@example.com"},
                {"id": 2, "username": "user2", "email": "user2@example.com"}
            ])
        
        @self.app.route('/api/users/<int:user_id>', methods=['GET'])
        def get_user(user_id):
            if user_id == 999:
                return jsonify({"error": "User not found"}), 404
            return jsonify({"id": user_id, "username": f"user{user_id}", "email": f"user{user_id}@example.com"})
        
        @self.app.route('/api/users', methods=['POST'])
        def create_user():
            data = request.get_json()
            
            # 参数校验
            if not data.get('username'):
                return jsonify({"error": "用户名不能为空"}), 400
            
            return jsonify({
                "id": 3,
                "username": data['username'],
                "email": data.get('email', ''),
                "created_at": "2024-01-01T00:00:00Z"
            }), 201
        
        @self.app.route('/api/users/<int:user_id>', methods=['PUT'])
        def update_user(user_id):
            data = request.get_json()
            return jsonify({
                "id": user_id,
                "username": data.get('username', f"user{user_id}"),
                "email": data.get('email', f"user{user_id}@example.com")
            })
        
        @self.app.route('/api/users/<int:user_id>', methods=['DELETE'])
        def delete_user(user_id):
            return '', 204
    
    def start(self):
        """启动 Mock 服务"""
        thread = threading.Thread(target=lambda: self.app.run(port=self.port, debug=False))
        thread.daemon = True
        thread.start()
        return self
```

### 5. 性能测试

```python
import time
import statistics
from concurrent.futures import ThreadPoolExecutor

class TestAPIPerformance:
    """API 性能测试"""
    
    def test_single_request_latency(self):
        """测试单请求延迟"""
        latencies = []
        
        for _ in range(100):
            start = time.time()
            response = requests.get(f"{self.base_url}/api/users")
            latencies.append((time.time() - start) * 1000)  # ms
        
        print(f"平均延迟: {statistics.mean(latencies):.2f}ms")
        print(f"P50 延迟: {statistics.median(latencies):.2f}ms")
        print(f"P95 延迟: {sorted(latencies)[95]:.2f}ms")
        print(f"P99 延迟: {sorted(latencies)[99]:.2f}ms")
        
        assert statistics.mean(latencies) < 500  # 平均延迟 < 500ms
    
    def test_concurrent_requests(self):
        """测试并发请求"""
        def make_request():
            return requests.get(f"{self.base_url}/api/users").status_code
        
        start = time.time()
        with ThreadPoolExecutor(max_workers=50) as executor:
            results = list(executor.map(lambda _: make_request(), range(500)))
        duration = time.time() - start
        
        success_count = sum(1 for r in results if r == 200)
        qps = 500 / duration
        
        print(f"总请求数: 500")
        print(f"成功数: {success_count}")
        print(f"QPS: {qps:.2f}")
        print(f"总耗时: {duration:.2f}s")
        
        assert success_count / 500 > 0.99  # 成功率 > 99%
        assert qps > 100  # QPS > 100
```

### 6. 安全测试

```python
class TestAPISecurity:
    """API 安全测试"""
    
    def test_sql_injection(self):
        """测试 SQL 注入"""
        payloads = [
            "' OR '1'='1",
            "'; DROP TABLE users; --",
            "1 UNION SELECT * FROM users"
        ]
        
        for payload in payloads:
            response = requests.get(
                f"{self.base_url}/api/users",
                params={"search": payload}
            )
            # 不应返回 200 或泄露数据
            assert response.status_code in [400, 403, 500]
    
    def test_xss_injection(self):
        """测试 XSS 注入"""
        payloads = [
            "<script>alert('xss')</script>",
            "<img src=x onerror=alert('xss')>",
            "javascript:alert('xss')"
        ]
        
        for payload in payloads:
            response = requests.post(
                f"{self.base_url}/api/users",
                json={"username": payload, "email": "test@example.com"}
            )
            # 响应中不应包含原始脚本
            assert payload not in response.text
    
    def test_authentication_bypass(self):
        """测试认证绕过"""
        # 尝试各种绕过方式
        bypass_attempts = [
            {},  # 无 Token
            {"Authorization": "Bearer invalid"},  # 无效 Token
            {"Authorization": "Bearer "},  # 空 Token
        ]
        
        for headers in bypass_attempts:
            response = requests.get(f"{self.base_url}/api/users", headers=headers)
            assert response.status_code in [401, 403]
    
    def test_rate_limiting(self):
        """测试速率限制"""
        responses = []
        for _ in range(150):
            response = requests.get(f"{self.base_url}/api/users")
            responses.append(response.status_code)
        
        # 应该有限制
        assert 429 in responses  # Too Many Requests
```

### 7. 测试报告生成

```python
def generate_api_test_report(results):
    """生成 API 测试报告"""
    report = {
        "summary": {
            "total": len(results),
            "passed": sum(1 for r in results if r["status"] == "passed"),
            "failed": sum(1 for r in results if r["status"] == "failed"),
            "duration": sum(r["duration"] for r in results)
        },
        "endpoints": {},
        "failures": []
    }
    
    # 按接口分组统计
    for result in results:
        endpoint = result["endpoint"]
        if endpoint not in report["endpoints"]:
            report["endpoints"][endpoint] = {"total": 0, "passed": 0, "failed": 0}
        
        report["endpoints"][endpoint]["total"] += 1
        if result["status"] == "passed":
            report["endpoints"][endpoint]["passed"] += 1
        else:
            report["endpoints"][endpoint]["failed"] += 1
            report["failures"].append({
                "endpoint": endpoint,
                "method": result["method"],
                "error": result["error"]
            })
    
    return report
```

## 注意事项

- 接口测试要覆盖正向、反向、边界、异常场景
- 参数校验测试要穷举所有非法输入
- 性能测试要在独立环境进行，避免影响生产
- 安全测试要注意不要对生产环境造成实际危害
- Mock 服务要定期同步真实接口变更
- 契约测试要随接口文档同步更新
