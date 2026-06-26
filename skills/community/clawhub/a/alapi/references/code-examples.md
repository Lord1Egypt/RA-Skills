# ALAPI 多语言对接代码模板

> 以下模板用于生成对接代码。将 `{PATH}` 替换为接口路径，`{PARAMS}` 替换为实际参数。

Token 约定：

- 默认使用环境变量 `ALAPI_TOKEN`
- 如果同时有显式 token 和环境变量，显式 token 优先
- 生成代码时优先展示环境变量读取方式，避免硬编码密钥

---

## cURL

```bash
# GET
curl "https://v3.alapi.cn/api/{PATH}?token=${ALAPI_TOKEN}&key=value"

# POST
curl -X POST "https://v3.alapi.cn/api/{PATH}" \
  -H "Content-Type: application/json" \
  -d '{"token": "'"${ALAPI_TOKEN}"'", "key": "value"}'
```

---

## Python (requests)

```python
import os
import requests

BASE_URL = "https://v3.alapi.cn/api"
TOKEN = os.environ["ALAPI_TOKEN"]


def call_alapi(path: str, params: dict = None, method: str = "GET") -> dict:
    """调用 ALAPI 接口。"""
    if params is None:
        params = {}
    params["token"] = TOKEN
    url = f"{BASE_URL}/{path}"

    if method == "POST":
        resp = requests.post(url, json=params, timeout=10)
    else:
        resp = requests.get(url, params=params, timeout=10)

    resp.raise_for_status()
    result = resp.json()
    if not result.get("success"):
        raise Exception(f"ALAPI Error {result.get('code')}: {result.get('message')}")
    return result["data"]


# 示例调用
data = call_alapi("{PATH}", {"{PARAMS}"})
print(data)
```

---

## JavaScript / TypeScript (fetch)

```typescript
const BASE_URL = "https://v3.alapi.cn/api";
const TOKEN = process.env.ALAPI_TOKEN;

if (!TOKEN) {
  throw new Error("Missing ALAPI_TOKEN environment variable");
}

async function callAlapi<T = any>(
  path: string,
  params: Record<string, string | number> = {}
): Promise<T> {
  const url = new URL(`${BASE_URL}/${path}`);
  url.searchParams.set("token", TOKEN);
  for (const [k, v] of Object.entries(params)) {
    url.searchParams.set(k, String(v));
  }

  const res = await fetch(url.toString());
  const json = await res.json();
  if (!json.success) {
    throw new Error(`ALAPI Error ${json.code}: ${json.message}`);
  }
  return json.data as T;
}

// 示例调用
const data = await callAlapi("{PATH}", { /* {PARAMS} */ });
console.log(data);
```

---

## PHP (curl)

```php
<?php

function callAlapi(string $path, array $params = [], string $method = 'GET'): array
{
    $baseUrl = 'https://v3.alapi.cn/api';
    $token = getenv('ALAPI_TOKEN');
    if (!$token) {
        throw new RuntimeException('Missing ALAPI_TOKEN environment variable');
    }
    $params['token'] = $token;

    if ($method === 'POST') {
        $url = $baseUrl . '/' . $path;
        $ch = curl_init($url);
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT => 10,
            CURLOPT_POST => true,
            CURLOPT_HTTPHEADER => ['Content-Type: application/json'],
            CURLOPT_POSTFIELDS => json_encode($params),
        ]);
    } else {
        $url = $baseUrl . '/' . $path . '?' . http_build_query($params);
        $ch = curl_init($url);
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_TIMEOUT => 10,
        ]);
    }

    $response = curl_exec($ch);
    curl_close($ch);

    $result = json_decode($response, true);
    if (!$result['success']) {
        throw new RuntimeException("ALAPI Error {$result['code']}: {$result['message']}");
    }
    return $result['data'];
}

// 示例调用
$data = callAlapi('{PATH}', [/* {PARAMS} */]);
print_r($data);
```

---

## Go (net/http)

```go
package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"net/url"
	"os"
)

const (
	baseURL = "https://v3.alapi.cn/api"
)

type Response struct {
	Success bool            `json:"success"`
	Code    int             `json:"code"`
	Message string          `json:"message"`
	Data    json.RawMessage `json:"data"`
}

func callAlapi(path string, params url.Values) (json.RawMessage, error) {
	token := os.Getenv("ALAPI_TOKEN")
	if token == "" {
		return nil, fmt.Errorf("missing ALAPI_TOKEN environment variable")
	}
	params.Set("token", token)
	endpoint := fmt.Sprintf("%s/%s?%s", baseURL, path, params.Encode())

	resp, err := http.Get(endpoint)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	body, _ := io.ReadAll(resp.Body)
	var result Response
	if err := json.Unmarshal(body, &result); err != nil {
		return nil, err
	}
	if !result.Success {
		return nil, fmt.Errorf("ALAPI Error %d: %s", result.Code, result.Message)
	}
	return result.Data, nil
}

func main() {
	params := url.Values{}
	// params.Set("key", "value")  // {PARAMS}
	data, err := callAlapi("{PATH}", params)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(data))
}
```

---

## Java (OkHttp)

```java
import okhttp3.*;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

public class AlapiClient {
    private static final String BASE_URL = "https://v3.alapi.cn/api";
    private static final String TOKEN = System.getenv("ALAPI_TOKEN");
    private final OkHttpClient client = new OkHttpClient();
    private final ObjectMapper mapper = new ObjectMapper();

    public JsonNode callAlapi(String path, java.util.Map<String, String> params) throws Exception {
        if (TOKEN == null || TOKEN.isBlank()) {
            throw new IllegalStateException("Missing ALAPI_TOKEN environment variable");
        }
        HttpUrl.Builder urlBuilder = HttpUrl.parse(BASE_URL + "/" + path).newBuilder();
        urlBuilder.addQueryParameter("token", TOKEN);
        params.forEach(urlBuilder::addQueryParameter);

        Request request = new Request.Builder().url(urlBuilder.build()).build();
        try (Response response = client.newCall(request).execute()) {
            JsonNode json = mapper.readTree(response.body().string());
            if (!json.get("success").asBoolean()) {
                throw new RuntimeException("ALAPI Error " + json.get("code") + ": " + json.get("message").asText());
            }
            return json.get("data");
        }
    }
}
```

---

## 通用建议

- **Token 安全**: 不要在前端硬编码 token，使用环境变量或后端代理
- **Token 优先级**: 显式传入 token 高于环境变量 `ALAPI_TOKEN`
- **重试**: 对 5xx 错误做指数退避重试（最多 3 次）
- **缓存**: 行情类数据缓存 60s，内容类缓存 5min
- **超时**: 建议设置 10s 超时
