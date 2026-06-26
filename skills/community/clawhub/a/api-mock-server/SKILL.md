# api-mock-server - API Mock服务器

## Metadata

| Field | Value |
|-------|-------|
| **Name** | api-mock-server |
| **Slug** | api-mock-server |
| **Version** | 1.0.0 |
| **Homepage** | https://github.com/openclaw/api-mock-server |
| **Category** | development |
| **Tags** | api, mock, server, testing, stub, http, rest, json |

## Description

### English
A lightweight API mock server for rapid prototyping and testing. Define routes with JSON/JSON Schema responses, support dynamic data generation, request validation, latency simulation, and webhook simulation.

### 中文
轻量级API Mock服务器，用于快速原型开发和测试。支持JSON/JSON Schema响应定义、动态数据生成、请求验证、延迟模拟和Webhook模拟。

## Requirements

- Python 3.8+
- Flask >= 2.3.0
- Faker >= 19.0.0
- jsonschema >= 4.17.0
- requests >= 2.31.0

## Configuration

### Environment Variables
```bash
MOCK_PORT=3000
MOCK_HOST=0.0.0.0
MOCK_LATENCY=0
```

## Usage

### Define Routes

```python
from api_mock_server import MockServer

server = MockServer(port=3000)

# Simple JSON response
server.get("/users", {"users": [{"id": 1, "name": "Alice"}]})

# Dynamic response with path params
server.get("/users/{id}", lambda req: {
    "id": req.params["id"],
    "name": f"User_{req.params['id']}"
})

# POST with validation
server.post("/users", 
    response={"id": 123, "created": True},
    validate_schema={
        "type": "object",
        "required": ["name", "email"],
        "properties": {
            "name": {"type": "string"},
            "email": {"type": "string", "format": "email"}
        }
    }
)

server.start()
```

### Load from Config File

```python
from api_mock_server import MockServer

server = MockServer.from_config("mock-routes.json")
server.start()
```

## API Reference

### MockServer
- `get(path, response)` - Define GET route
- `post(path, response, validate_schema)` - Define POST route
- `put(path, response)` - Define PUT route
- `delete(path, response)` - Define DELETE route
- `patch(path, response)` - Define PATCH route
- `from_config(path)` - Load routes from JSON config
- `start()` - Start the server
- `stop()` - Stop the server

### MockRequest
- `params` - URL path parameters
- `query` - Query string parameters
- `body` - Request body
- `headers` - Request headers

## Examples

See `examples/` directory for complete examples.

## Testing

```bash
cd /root/.openclaw/workspace/skills/api-mock-server
python -m pytest tests/ -v
```

## License

MIT License
