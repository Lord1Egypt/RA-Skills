# 产品部数据平台 API 文档

## 推送接口

### 接口信息

- **URL**: `http://test-gateway.jinyi999.cn/rjhy-test-compliance-utils-api/api/v1/aitest/backend/message`
- **方法**: `POST`
- **Content-Type**: `application/json`

### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| prdid | string | 是 | 产品需求 ID |
| content | object | 是 | 接口文档 JSON 数据 |

### 请求示例

```json
{
  "prdid": "PRD-2026-001",
  "content": {
    "apis": [
      {
        "method": "GET",
        "path": "/api/users/{id}",
        "description": "获取用户详情",
        "parameters": [
          {
            "name": "id",
            "in": "path",
            "required": true,
            "type": "string",
            "description": "用户 ID"
          }
        ],
        "response": {
          "type": "object",
          "properties": {
            "id": {"type": "string"},
            "name": {"type": "string"},
            "email": {"type": "string"}
          }
        }
      }
    ]
  }
}
```

### 响应示例

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "pushId": "push_123456",
    "timestamp": "2026-06-12T10:30:00Z"
  }
}
```

## 接口定义格式规范

### 标准格式

```json
{
  "apis": [
    {
      "method": "HTTP 方法 (GET/POST/PUT/DELETE/PATCH)",
      "path": "/api/路径",
      "description": "接口描述",
      "parameters": [
        {
          "name": "参数名",
          "in": "path|query|body|header",
          "required": true/false,
          "type": "string|number|boolean|object|array",
          "description": "参数描述"
        }
      ],
      "response": {
        "type": "返回类型",
        "properties": {
          "字段名": {"type": "类型", "description": "描述"}
        }
      }
    }
  ]
}
```

### 从 Java Controller 提取

```java
// 示例：Spring Boot Controller
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    @GetMapping("/{id}")
    public UserDTO getUser(@PathVariable String id) {
        // ...
    }
    
    @PostMapping
    public UserDTO createUser(@RequestBody CreateUserRequest request) {
        // ...
    }
}
```

转换为 JSON:

```json
{
  "apis": [
    {
      "method": "GET",
      "path": "/api/users/{id}",
      "description": "获取用户详情",
      "parameters": [
        {
          "name": "id",
          "in": "path",
          "required": true,
          "type": "string",
          "description": "用户 ID"
        }
      ],
      "response": {
        "type": "UserDTO",
        "properties": {
          "id": {"type": "string"},
          "name": {"type": "string"}
        }
      }
    },
    {
      "method": "POST",
      "path": "/api/users",
      "description": "创建用户",
      "parameters": [
        {
          "name": "request",
          "in": "body",
          "required": true,
          "type": "CreateUserRequest"
        }
      ],
      "response": {
        "type": "UserDTO"
      }
    }
  ]
}
```

## 最佳实践

### 1. 推送前检查清单

- [ ] PRD ID 是否正确
- [ ] 接口定义是否完整（方法、路径、参数、响应）
- [ ] 参数描述是否清晰
- [ ] 响应结构是否明确
- [ ] JSON 格式是否有效

### 2. 批量推送策略

- 按业务模块分组
- 每组不超过 50 个接口
- 标注接口状态（新增/修改/废弃）
- 提供变更说明文档

### 3. 版本管理

在接口定义中添加版本信息：

```json
{
  "version": "1.0.0",
  "changeLog": "新增用户管理模块接口",
  "apis": [...]
}
```

### 4. 错误处理

- 网络错误：自动重试（最多 3 次）
- 参数错误：检查 JSON 格式和必填字段
- PRD 不存在：联系产品管理员确认 ID
- 服务器错误：记录日志并联系平台管理员

## CI/CD 集成示例

### GitHub Actions

```yaml
name: Push API Docs

on:
  push:
    branches: [main]
    paths:
      - 'src/main/java/**/controller/**'

jobs:
  push-api-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Extract API definitions
        run: |
          python3 scripts/extract_java_api.py \
            --src src/main/java \
            --output api-definitions.json
      
      - name: Push to platform
        run: |
          python3 scripts/push_api_to_product_platform.py \
            --prdid "${{ secrets.PRD_ID }}" \
            --file api-definitions.json
```

### Git Hook (pre-push)

```bash
#!/bin/bash
# .git/hooks/pre-push

echo "📋 检查接口定义变更..."

# 提取变更的 Controller 文件
CHANGED_FILES=$(git diff --name-only --cached | grep -E 'controller|api' || true)

if [ -n "$CHANGED_FILES" ]; then
  echo "🔄 发现接口变更，自动提取并推送..."
  python3 scripts/extract_java_api.py --src src/main/java --output api-definitions.json
  python3 scripts/push_api_to_product_platform.py --prdid "PRD-2026-001" --file api-definitions.json
fi
```

## 常见问题

### Q: PRD ID 从哪里获取？
A: 从产品需求管理系统（如 Jira、禅道）中获取对应需求的 ID。

### Q: 支持哪些接口定义格式？
A: 支持标准 JSON、Swagger/OpenAPI 3.0、Spring Boot Controller 注解提取。

### Q: 推送失败怎么办？
A: 
1. 检查网络连接
2. 验证 PRD ID 是否正确
3. 检查 JSON 格式
4. 查看详细错误日志
5. 联系平台管理员

### Q: 如何查看推送历史？
A: 查看 `references/push-history.md` 文件。
