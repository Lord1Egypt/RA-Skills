---
name: clh-api-guidance
description: "提供ClawHub API的详细使用指南，包括认证、接口文档、示例代码、限流处理和安全最佳实践，助力开发者高效集成。"
source: ClawHub
version: 1.0.0
tags: []
compatible: [claude-code, openai-agents, hermes-agent, any-llm]
---

# ClawHub API Guidance

# ClawHub API Guidance

## 技能描述

ClawHub API Guidance 技能是一个全面的 API 使用指南，帮助开发者快速上手并熟练使用 ClawHub API。本技能提供了详细的 API 文档、认证说明、使用场景、最佳实践和错误处理指南。

## 最后更新日期

2026-06-03

---

## 快速开始

### 5分钟快速上手

欢迎使用 ClawHub API！本指南将帮助您在 5 分钟内完成第一个 API 调用。

#### 环境准备

1. **获取 API Key**
   - 访问 [ClawHub](https://clawhub.ai) 并登录您的账户
   - 进入设置页面，生成您的 API Key
   - 保存您的 API Key，格式为 `clh_...`

2. **安装依赖**
   - 确保您的环境支持 HTTP 请求
   - 推荐使用 `curl` 或 `requests` (Python) 等工具

#### 第一个 API 调用

```bash
curl -X GET "https://clawhub.ai/api/v1/search?q=example&limit=10"
```

```python
import requests

response = requests.get(
    "https://clawhub.ai/api/v1/search",
    params={"q": "example", "limit": 10}
)
print(response.json())
```

#### 常见问题

**Q: 我需要认证吗？**
A: 公开读取端点（如搜索、列表）无需认证。写入和账户操作需要 Bearer Token。

**Q: 如何处理限流？**
A: 监控响应头中的 `X-RateLimit-Remaining`，在接近限制时减慢请求速度。

---

## 认证说明

### 认证方式

ClawHub API 使用 **Bearer Token** 认证。

- **公开读取端点**: 无需认证 token
- **写入和账户操作**: 需要Bearer Token

```http
Authorization: Bearer clh_...
```

### 获取和管理 API Key

1. **获取 API Key**: 登录 [ClawHub](https://clawhub.ai) → 账户设置 → 生成新的 API Key
2. **管理 API Key**: 定期轮换、不要硬编码、使用环境变量存储

### 认证失败处理

- **401 Unauthorized**: Token 无效或已过期，检查格式或重新生成
- **403 Forbidden**: 权限不足，确认账户权限和资源归属

---

## API接口文档

详细的API接口文档已移至 [reference/api-reference.md](reference/api-reference.md)，包含41个接口的完整说明。

### 快速参考

| 接口分类 | 主要端点 |
|---------|---------|
| 技能搜索 | `GET /api/v1/search` |
| 技能列表 | `GET /api/v1/skills` |
| 技能详情 | `GET /api/v1/skills/{slug}` |
| 包列表 | `GET /api/v1/packages` |
| 包详情 | `GET /api/v1/packages/{name}` |
| 包下载 | `GET /api/v1/packages/{name}/download` |
| 用户信息 | `GET /api/v1/whoami` |

### 接口分类

- **技能相关接口**: 搜索、列表、详情、审核、扫描、文件、版本、发布、删除等
- **统一包目录接口**: 包列表、详情、下载、文件、就绪状态、版本、工件、安全、搜索等
- **插件相关接口**: 代码插件、bundle插件、插件目录、搜索等
- **其他接口**: 哈希解析、下载、用户信息、删除、重命名、合并、转移等

---

## 使用场景

### 场景1：构建第三方技能目录

**适用API**: `GET /api/v1/skills`, `GET /api/v1/skills/{slug}`, `GET /api/v1/search`

**实现步骤**:
1. 使用 `GET /api/v1/skills` 获取技能列表
2. 使用 `GET /api/v1/skills/{slug}` 获取详细信息
3. 使用 `GET /api/v1/search` 实现搜索功能
4. 尊重限流响应头，避免激进轮询
5. 链接回源到规范的ClawHub技能URL

```python
import requests
import time

BASE_URL = "https://clawhub.ai/api/v1"

def get_skills(limit=20, cursor=None):
    params = {"limit": limit}
    if cursor:
        params["cursor"] = cursor

    response = requests.get(f"{BASE_URL}/skills", params=params)

    if response.status_code == 429:
        retry_after = int(response.headers.get("Retry-After", 5))
        time.sleep(retry_after)
        return get_skills(limit, cursor)

    return response.json()

def search_skills(query, limit=10):
    response = requests.get(
        f"{BASE_URL}/search",
        params={"q": query, "limit": limit}
    )
    return response.json()

# 使用示例
skills = get_skills(limit=20)
print(f"获取到 {len(skills.get('items', []))} 个技能")
```

---

### 场景2：技能安全检查

**适用API**: `GET /api/v1/skills/{slug}/moderation`, `GET /api/v1/skills/{slug}/scan`, `GET /api/v1/packages/{name}/versions/{version}/security`

**实现步骤**:
1. 获取技能的审核状态
2. 获取技能的安全扫描结果
3. 检查包版本的信任摘要
4. 根据结果决定是否使用该技能

```python
import requests

BASE_URL = "https://clawhub.ai/api/v1"

def is_skill_safe(slug, version):
    # 检查审核状态
    moderation = requests.get(f"{BASE_URL}/skills/{slug}/moderation").json()
    if moderation.get('isMalwareBlocked') or moderation.get('isSuspicious'):
        return False

    # 检查安全扫描
    scan = requests.get(f"{BASE_URL}/skills/{slug}/scan").json()
    if scan.get('status') in ['malicious', 'suspicious']:
        return False

    # 检查包信任摘要
    security = requests.get(f"{BASE_URL}/packages/@owner/{slug}/versions/{version}/security").json()
    trust = security.get('trust', {})

    if trust.get('blockedFromDownload'):
        return False
    if trust.get('scanStatus') != 'clean':
        return False
    if trust.get('moderationState') != 'approved':
        return False

    return True

# 使用示例
is_safe = is_skill_safe("example-skill", "1.0.0")
```

---

### 场景3：下载和使用技能

**适用API**: `GET /api/v1/download`, `GET /api/v1/packages/{name}/download`, `GET /api/v1/skills/{slug}/file`

**实现步骤**:
1. 验证技能安全性
2. 下载技能ZIP文件
3. 解压并查看技能文件
4. 读取README等文档文件

```python
import requests
import zipfile

BASE_URL = "https://clawhub.ai/api/v1"

def download_skill(slug, version=None):
    params = {"slug": slug}
    if version:
        params["version"] = version

    response = requests.get(
        f"{BASE_URL}/download",
        params=params,
        stream=True
    )

    if response.status_code == 200:
        filename = f"{slug}.zip"
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return filename
    return None

def get_skill_file(slug, file_path, version=None):
    params = {"path": file_path}
    if version:
        params["version"] = version

    response = requests.get(
        f"{BASE_URL}/skills/{slug}/file",
        params=params
    )

    if response.status_code == 200:
        return response.text
    return None

# 使用示例
zip_path = download_skill("example-skill", version="1.0.0")
readme = get_skill_file("example-skill", "README.md", version="1.0.0")
```

---

## 最佳实践

### 错误处理

```python
import requests
from requests.exceptions import RequestException

try:
    response = requests.get("https://clawhub.ai/api/v1/skills", timeout=10)
    response.raise_for_status()
    data = response.json()
except RequestException as e:
    print(f"请求异常: {e}")
```

### 429限流处理

```python
import time
import random

def request_with_retry(url, params=None, max_retries=3):
    for attempt in range(max_retries):
        response = requests.get(url, params=params)

        if response.status_code != 429:
            return response

        retry_after = int(response.headers.get("Retry-After", 2))
        jitter = random.uniform(0, 1)
        wait_time = retry_after + jitter

        print(f"限流中，等待 {wait_time:.1f} 秒后重试...")
        time.sleep(wait_time)

    return response
```

### 性能优化

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_skill_detail_cached(slug):
    response = requests.get(f"https://clawhub.ai/api/v1/skills/{slug}")
    return response.json()
```

### 安全建议

```python
import os

# ✅ 推荐：使用环境变量
API_KEY = os.getenv("CLAWHUB_API_KEY")

# ❌ 不推荐：硬编码
API_KEY = "clh_abc123..."
```

---

## 错误处理

### 错误码列表

| 状态码 | 含义 | 处理建议 |
|-------|------|---------|
| 400 | Bad Request | 检查参数格式和值是否正确 |
| 401 | Unauthorized | 重新获取有效的Bearer Token |
| 403 | Forbidden | 检查账户权限，确认资源未被审核阻止 |
| 404 | Not Found | 确认slug、version等参数正确 |
| 413 | Payload Too Large | 减小文件大小或分批上传 |
| 415 | Unsupported Media Type | 检查Content-Type是否正确 |
| 429 | Too Many Requests | 实现指数退避重试，尊重Retry-After头 |

---

## 限流说明

### 请求频率限制

| 操作类型 | 每IP限制 | 每Key限制 |
|---------|---------|----------|
| 读取 | 3000/分钟 | 12000/分钟 |
| 写入 | 300/分钟 | 3000/分钟 |
| 下载 | 1200/分钟 | 6000/分钟 |

### 限流响应头

| 响应头 | 说明 |
|-------|------|
| `X-RateLimit-Limit` | 限流配额总数 |
| `X-RateLimit-Remaining` | 剩余配额 |
| `X-RateLimit-Reset` | Unix时间戳（绝对重置时间） |
| `Retry-After` | 429状态码时建议等待的秒数 |

### 应对策略

```python
import time
import random

def handle_rate_limit(response):
    retry_after = response.headers.get("Retry-After")
    if retry_after:
        wait_time = int(retry_after)
    else:
        reset = response.headers.get("RateLimit-Reset")
        if reset:
            wait_time = int(reset)
        else:
            wait_time = 5

    jitter = random.uniform(0, 1)
    wait_time += jitter

    print(f"速率限制，等待 {wait_time:.1f} 秒...")
    time.sleep(wait_time)
```

---

## 公共目录复用指南

### 使用指南

1. **使用公共读取端点**: `GET /api/v1/skills`, `GET /api/v1/search`, `GET /api/v1/skills/{slug}`
2. **缓存响应**: 尊重 `429`、`Retry-After` 和限流响应头，避免激进轮询
3. **链接回源**: 使用规范的页面URL格式 `https://clawhub.ai/<owner>/<slug>`
4. **避免误导**: 不要暗示ClawHub认可、验证或运营第三方站点
5. **内容限制**: 不要通过绕过公共API过滤器或认证边界来镜像隐藏、私有或被审核阻止的内容

---

## 参考文档

- [API接口参考](reference/api-reference.md) - 41个API接口的详细文档
- [数据模型](reference/data-models.md) - 所有数据结构的JSON示例
- [枚举值说明](reference/enums.md) - 所有枚举类型的可选值

---

## 总结

ClawHub API Guidance 技能提供了完整的 ClawHub API 使用指南：

- ✅ 快速开始：5分钟上手指南
- ✅ 认证说明：Bearer Token 认证机制
- ✅ API接口文档：41个完整接口（详见reference）
- ✅ 使用场景：3个典型应用场景的代码示例
- ✅ 最佳实践：错误处理、性能优化、安全建议
- ✅ 错误处理：完整的错误码列表和处理方法
- ✅ 限流说明：速率限制规则和应对策略
- ✅ 公共目录复用指南：构建第三方目录的最佳实践

开发者可以参考本技能文档，快速集成和使用 ClawHub API。

---

🎯
