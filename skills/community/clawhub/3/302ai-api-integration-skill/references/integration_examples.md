# 302.AI API 集成代码模板

本文档提供各种编程语言的 302.AI API 集成代码模板。

## Python 集成模板

### 基础请求模板

```python
import requests
import json

# 302.AI API 配置
API_KEY = "your_api_key_here"
BASE_URL = "https://api.302.ai"

def call_302ai_api(endpoint, data):
    """
    调用 302.AI API 的通用函数

    Args:
        endpoint: API 端点路径
        data: 请求数据（字典格式）

    Returns:
        API 响应结果
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    url = f"{BASE_URL}{endpoint}"

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API 调用失败: {e}")
        return None

# 使用示例
if __name__ == "__main__":
    # 替换为实际的端点和数据
    result = call_302ai_api("/v1/endpoint", {
        "param1": "value1",
        "param2": "value2"
    })

    if result:
        print(json.dumps(result, indent=2, ensure_ascii=False))
```

### 流式响应模板

```python
import requests
import json

def call_302ai_stream(endpoint, data):
    """
    调用 302.AI 流式 API

    Args:
        endpoint: API 端点路径
        data: 请求数据（字典格式）

    Yields:
        流式响应的每个数据块
    """
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    url = f"{BASE_URL}{endpoint}"

    try:
        response = requests.post(url, headers=headers, json=data, stream=True)
        response.raise_for_status()

        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    data = line[6:]  # 移除 'data: ' 前缀
                    if data != '[DONE]':
                        yield json.loads(data)
    except requests.exceptions.RequestException as e:
        print(f"流式 API 调用失败: {e}")

# 使用示例
for chunk in call_302ai_stream("/v1/stream-endpoint", {"prompt": "Hello"}):
    print(chunk)
```

## JavaScript/Node.js 集成模板

### 基础请求模板

```javascript
const axios = require('axios');

// 302.AI API 配置
const API_KEY = 'your_api_key_here';
const BASE_URL = 'https://api.302.ai';

/**
 * 调用 302.AI API 的通用函数
 * @param {string} endpoint - API 端点路径
 * @param {object} data - 请求数据
 * @returns {Promise<object>} API 响应结果
 */
async function call302aiAPI(endpoint, data) {
    try {
        const response = await axios.post(`${BASE_URL}${endpoint}`, data, {
            headers: {
                'Authorization': `Bearer ${API_KEY}`,
                'Content-Type': 'application/json'
            }
        });
        return response.data;
    } catch (error) {
        console.error('API 调用失败:', error.message);
        return null;
    }
}

// 使用示例
(async () => {
    const result = await call302aiAPI('/v1/endpoint', {
        param1: 'value1',
        param2: 'value2'
    });

    if (result) {
        console.log(JSON.stringify(result, null, 2));
    }
})();
```

### Fetch API 模板

```javascript
// 302.AI API 配置
const API_KEY = 'your_api_key_here';
const BASE_URL = 'https://api.302.ai';

/**
 * 使用 Fetch API 调用 302.AI
 * @param {string} endpoint - API 端点路径
 * @param {object} data - 请求数据
 * @returns {Promise<object>} API 响应结果
 */
async function call302aiAPI(endpoint, data) {
    try {
        const response = await fetch(`${BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${API_KEY}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API 调用失败:', error.message);
        return null;
    }
}

// 使用示例
call302aiAPI('/v1/endpoint', {
    param1: 'value1',
    param2: 'value2'
}).then(result => {
    if (result) {
        console.log(JSON.stringify(result, null, 2));
    }
});
```

## cURL 命令模板

### 基础请求

```bash
curl -X POST "https://api.302.ai/v1/endpoint" \
  -H "Authorization: Bearer your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "param1": "value1",
    "param2": "value2"
  }'
```

### 流式请求

```bash
curl -X POST "https://api.302.ai/v1/stream-endpoint" \
  -H "Authorization: Bearer your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Hello",
    "stream": true
  }' \
  --no-buffer
```

## TypeScript 集成模板

```typescript
import axios, { AxiosResponse } from 'axios';

// 302.AI API 配置
const API_KEY: string = 'your_api_key_here';
const BASE_URL: string = 'https://api.302.ai';

// 定义响应类型
interface APIResponse {
    [key: string]: any;
}

/**
 * 调用 302.AI API 的通用函数
 * @param endpoint - API 端点路径
 * @param data - 请求数据
 * @returns API 响应结果
 */
async function call302aiAPI(
    endpoint: string,
    data: Record<string, any>
): Promise<APIResponse | null> {
    try {
        const response: AxiosResponse<APIResponse> = await axios.post(
            `${BASE_URL}${endpoint}`,
            data,
            {
                headers: {
                    'Authorization': `Bearer ${API_KEY}`,
                    'Content-Type': 'application/json'
                }
            }
        );
        return response.data;
    } catch (error) {
        console.error('API 调用失败:', error);
        return null;
    }
}

// 使用示例
(async () => {
    const result = await call302aiAPI('/v1/endpoint', {
        param1: 'value1',
        param2: 'value2'
    });

    if (result) {
        console.log(JSON.stringify(result, null, 2));
    }
})();
```

## Go 集成模板

```go
package main

import (
    "bytes"
    "encoding/json"
    "fmt"
    "io"
    "net/http"
)

// 302.AI API 配置
const (
    APIKey  = "your_api_key_here"
    BaseURL = "https://api.302.ai"
)

// Call302aiAPI 调用 302.AI API 的通用函数
func Call302aiAPI(endpoint string, data map[string]interface{}) (map[string]interface{}, error) {
    // 序列化请求数据
    jsonData, err := json.Marshal(data)
    if err != nil {
        return nil, fmt.Errorf("序列化数据失败: %w", err)
    }

    // 创建请求
    url := BaseURL + endpoint
    req, err := http.NewRequest("POST", url, bytes.NewBuffer(jsonData))
    if err != nil {
        return nil, fmt.Errorf("创建请求失败: %w", err)
    }

    // 设置请求头
    req.Header.Set("Authorization", "Bearer "+APIKey)
    req.Header.Set("Content-Type", "application/json")

    // 发送请求
    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        return nil, fmt.Errorf("发送请求失败: %w", err)
    }
    defer resp.Body.Close()

    // 读取响应
    body, err := io.ReadAll(resp.Body)
    if err != nil {
        return nil, fmt.Errorf("读取响应失败: %w", err)
    }

    // 解析响应
    var result map[string]interface{}
    if err := json.Unmarshal(body, &result); err != nil {
        return nil, fmt.Errorf("解析响应失败: %w", err)
    }

    return result, nil
}

func main() {
    // 使用示例
    result, err := Call302aiAPI("/v1/endpoint", map[string]interface{}{
        "param1": "value1",
        "param2": "value2",
    })

    if err != nil {
        fmt.Printf("API 调用失败: %v\n", err)
        return
    }

    // 打印结果
    jsonResult, _ := json.MarshalIndent(result, "", "  ")
    fmt.Println(string(jsonResult))
}
```

## 通用集成步骤

1. **获取 API Key**: 从 302.AI 平台获取统一的 API Key
2. **选择 API**: 根据需求从 API 列表中选择合适的接口
3. **查看文档**: 阅读该 API 的详细 MD 文档，了解参数和返回值
4. **复制模板**: 根据使用的编程语言，复制对应的代码模板
5. **替换参数**:
   - 替换 `your_api_key_here` 为实际的 API Key
   - 替换 `/v1/endpoint` 为实际的 API 端点
   - 替换请求数据为实际的参数
6. **测试调用**: 运行代码，验证 API 调用是否成功
7. **错误处理**: 根据实际情况添加适当的错误处理逻辑

## 注意事项

- **API Key 安全**: 不要在代码中硬编码 API Key，建议使用环境变量
- **速率限制**: 注意 API 的调用频率限制
- **错误重试**: 对于网络错误，建议实现重试机制
- **日志记录**: 记录 API 调用日志，便于调试和监控
- **超时设置**: 设置合理的请求超时时间
