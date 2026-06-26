# DMP API 集成指南

## API Key 配置流程

### 运行时自动注入机制

OpenClaw 在启动 agent 进程时会自动：
1. 从配置中读取 `skills.entries.dmp-persona-insight.apiKey`
2. 将其注入到环境变量 `DMP_API_KEY`
3. 脚本可直接读取使用，无需硬编码

### 脚本中的使用方式

**Python 示例：**
```python
import os
import requests

# 获取 API Key（由 OpenClaw 自动注入）
api_key = os.environ.get("DMP_API_KEY")
if not api_key:
    print("Error: DMP_API_KEY not configured")
    print("Please configure via:")
    print("  1. Dashboard Skills page")
    print("  2. ~/.openclaw/openclaw.json")
    print("  3. export DMP_API_KEY=...")
    sys.exit(1)

# 调用 DMP API
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.post(
    "https://api.mingdata.com.cn/audience/analyze",
    json={"audience_id": "12345"},
    headers=headers,
    timeout=30
)

if response.status_code == 200:
    result = response.json()
    print(json.dumps(result, ensure_ascii=False, indent=2))
else:
    print(f"API Error: {response.status_code} {response.reason}")
    sys.exit(1)
```

**Bash 示例：**
```bash
#!/bin/bash

# 读取环境变量
if [ -z "$DMP_API_KEY" ]; then
    echo "Error: DMP_API_KEY not configured"
    exit 1
fi

# 调用 API
curl -X POST https://api.mingdata.com.cn/audience/list \
  -H "Authorization: Bearer $DMP_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"limit": 10}' \
  -s | jq .
```

## 错误处理最佳实践

### 检查配置是否存在
```python
import os
import sys

def get_api_key():
    api_key = os.environ.get("DMP_API_KEY")
    if not api_key:
        print("❌ Error: DMP_API_KEY not configured")
        print("\nConfiguration options:")
        print("  1. Dashboard Skills page → dmp-persona-insight → Set API Key")
        print("  2. ~/.openclaw/openclaw.json:")
        print('     {"skills": {"entries": {"dmp-persona-insight": {"apiKey": "..."}}}}')
        print("  3. Environment variable: export DMP_API_KEY=...")
        sys.exit(1)
    return api_key
```

### API 调用异常处理
```python
import requests
import time

def call_dmp_api_with_retry(url, payload, api_key, max_retries=3):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=30
            )
            
            # 检查认证错误
            if response.status_code == 401:
                print("❌ Error: Invalid or expired API key")
                sys.exit(1)
            
            # 检查其他 HTTP 错误
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"⏱️  Timeout, retrying in {wait_time}s...")
                time.sleep(wait_time)
            else:
                print("❌ Error: API request timeout (exceeded retries)")
                sys.exit(1)
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Error: API request failed: {e}")
            sys.exit(1)
```

## 速率限制处理

明日 DMP API 可能有速率限制，建议实现指数退避重试：

```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import requests

def create_session_with_retries():
    session = requests.Session()
    
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,  # 1s, 2s, 4s
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST", "GET", "PUT"]
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

# 使用
session = create_session_with_retries()
response = session.post(
    "https://api.mingdata.com.cn/...",
    json=payload,
    headers={"Authorization": f"Bearer {api_key}"}
)
```

## 安全最佳实践

### ✅ 推荐做法

```python
# 正确：从环境变量读取
api_key = os.environ.get("DMP_API_KEY")

# 正确：日志中隐藏密钥
logger.info(f"Using API key: {api_key[:8]}...")

# 正确：验证 API 响应
if response.status_code == 401:
    print("Invalid API key")
```

### ❌ 禁止做法

```python
# 错误：硬编码密钥
api_key = "sk-xxx-xxx-xxx"

# 错误：在日志中输出完整密钥
logger.info(f"API key: {api_key}")

# 错误：在版本控制中提交密钥
# .env 或 config.py 文件包含真实 API key
```

## 配置验证

验证 API Key 是否正确配置：

```bash
#!/bin/bash
# 测试脚本：test_dmp_config.sh

echo "🔍 Checking DMP_API_KEY configuration..."

if [ -z "$DMP_API_KEY" ]; then
    echo "❌ DMP_API_KEY not set"
    exit 1
else
    echo "✅ DMP_API_KEY configured"
    echo "   Key prefix: ${DMP_API_KEY:0:8}..."
    echo "   Key length: ${#DMP_API_KEY}"
fi

# 可选：测试 API 连通性
echo ""
echo "🧪 Testing API connectivity..."
response=$(curl -s -w "\n%{http_code}" \
  -H "Authorization: Bearer $DMP_API_KEY" \
  https://api.mingdata.com.cn/health)

http_code=$(echo "$response" | tail -n1)
if [ "$http_code" = "200" ] || [ "$http_code" = "401" ]; then
    echo "✅ API endpoint reachable"
else
    echo "❌ API endpoint unreachable (HTTP $http_code)"
    exit 1
fi
```

运行：
```bash
chmod +x test_dmp_config.sh
./test_dmp_config.sh
```

## 常见问题

### Q：如何在开发时快速切换不同的 API Key？
**A：** 使用环境变量最灵活：
```bash
# 开发环境
export DMP_API_KEY="dev-key"
openclaw agent --message "test"

# 测试环境
export DMP_API_KEY="test-key"
openclaw agent --message "analyze"

# 生产环境
export DMP_API_KEY="prod-key"
openclaw agent --message "analyze"
```

### Q：API Key 过期后需要怎么更新？
**A：** 在 Dashboard Skills 页面重新配置新 key，OpenClaw 自动生效。

### Q：多个 Python 脚本都需要 API Key？
**A：** 只需在 SKILL.md 中声明一次 `primaryEnv: DMP_API_KEY`，OpenClaw 自动注入到整个 agent 进程，所有脚本都能访问。

### Q：如何禁用这个技能的 API Key 检查？
**A：** 在 `~/.openclaw/openclaw.json` 中设置：
```json
{
  "skills": {
    "entries": {
      "dmp-persona-insight": {
        "enabled": false
      }
    }
  }
}
```

### Q：能否将 API Key 存储在 vault 或密钥管理系统中？
**A：** 是的，OpenClaw 支持 SecretRef。在配置中使用：
```json
{
  "skills": {
    "entries": {
      "dmp-persona-insight": {
        "apiKey": {
          "source": "vault",
          "provider": "default",
          "id": "dmp/api-key"
        }
      }
    }
  }
}
```
具体配置方式参考 OpenClaw 官方文档。
