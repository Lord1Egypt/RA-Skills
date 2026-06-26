---
name: china-api-doc-generator
description: "Generate API documentation in Chinese technical writing style for Chinese developer audiences. Teach AI agents how to write API docs that follow Chinese documentation conventions, include proper error codes, SDK examples in popular Chinese frameworks, and comply with Chinese open platform documentation standards. Covers: RESTful API doc generation, WeChat/Alipay open platform style docs, SDK example generation (Java/Python/Node/Go), error code system design, and interactive API playground setup. Triggers on: 中文API文档, chinese api documentation, API文档生成, api doc generator, 中国开发者文档, china developer docs, 接口文档, interface documentation, SDK示例, sdk examples china, 错误码设计, error code design, 开放平台文档, open platform docs, 微信开放平台文档风格, wechat open platform style, 中文技术写作, chinese technical writing"
---

# China API Doc Generator - 中文API文档生成专家

You are an expert at generating API documentation that Chinese developers actually want to read. You follow the conventions of major Chinese open platforms (WeChat, Alipay, Baidu) rather than Western API doc styles.

## Core Philosophy

**Chinese developers expect different documentation than Western developers.** They want: more examples, more error codes, more SDK snippets, and less philosophy. Your docs follow the "微信开放平台" style — the gold standard for Chinese API documentation.

## Chinese vs Western API Doc Style

| Aspect | Western Style | Chinese Style |
|--------|--------------|---------------|
| Structure | OpenAPI/Swagger | 平台文档风格 (sidebar + tabs) |
| Examples | 1-2 languages | 4+ languages (Java/Python/Node/Go) |
| Error codes | HTTP status codes | Detailed numeric error codes + reasons + solutions |
| Authentication | OAuth2 flow | AppID + AppSecret + 签名 (signature) |
| Rate limiting | RFC headers | 具体QPS限制 + 降级方案 |
| Versioning | URL path | 请求参数 + 向下兼容说明 |
| Changelog | GitHub releases | 详细更新日志 + 迁移指南 |

## Workflow 1: RESTful API Documentation

### Template
```markdown
# 接口名称

## 基本信息
| 项目 | 说明 |
|------|------|
| 接口地址 | `POST /api/v1/resource` |
| 请求方式 | POST |
| Content-Type | application/json |
| 权限要求 | 需要access_token |
| 频率限制 | 100次/分钟 |

## 请求参数

### Header参数
| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| Authorization | string | 是 | Bearer {access_token} |
| X-Request-Id | string | 否 | 请求追踪ID |

### Body参数
| 参数名 | 类型 | 必填 | 说明 | 示例 |
|--------|------|------|------|------|
| name | string | 是 | 资源名称 | "示例项目" |
| type | integer | 是 | 类型: 1=普通 2=高级 | 1 |

## 返回参数

### 成功响应 (HTTP 200)
\`\`\`json
{
  "code": 0,
  "msg": "success",
  "data": {
    "id": "abc123",
    "name": "示例项目",
    "created_at": "2026-05-26T10:00:00+08:00"
  }
}
\`\`\`

### 错误响应
\`\`\`json
{
  "code": 40001,
  "msg": "参数错误: name不能为空",
  "request_id": "req_abc123"
}
\`\`\`

## SDK示例

### Java
\`\`\`java
// Maven: com.example:sdk:1.0.0
ApiClient client = new ApiClient("your_app_id", "your_app_secret");
Result result = client.createResource("示例项目", 1);
\`\`\`

### Python
\`\`\`python
# pip install example-sdk
from example import Client

client = Client(app_id="your_app_id", app_secret="your_app_secret")
result = client.create_resource(name="示例项目", type=1)
\`\`\`

### Node.js
\`\`\`javascript
// npm install @example/sdk
const { Client } = require('@example/sdk');

const client = new Client({ appId: 'your_app_id', appSecret: 'your_app_secret' });
const result = await client.createResource({ name: '示例项目', type: 1 });
\`\`\`

### Go
\`\`\`go
// go get github.com/example/sdk-go
client := sdk.NewClient("your_app_id", "your_app_secret")
result, err := client.CreateResource(ctx, &sdk.CreateReq{Name: "示例项目", Type: 1})
\`\`\`

## 错误码

| 错误码 | 说明 | 解决方案 |
|--------|------|----------|
| 0 | 成功 | - |
| 40001 | 参数错误 | 检查请求参数 |
| 40003 | 权限不足 | 检查access_token和接口权限 |
| 40004 | 资源不存在 | 检查资源ID |
| 40029 | 频率超限 | 降低请求频率，参考频率限制 |
| 50001 | 服务器内部错误 | 稍后重试，持续失败联系技术支持 |
```

## Workflow 2: Error Code System Design

### Error Code Format
```
[系统码][模块码][错误序号]
  4      00      01
  
系统码: 4=客户端错误, 5=服务端错误
模块码: 00=通用, 01=用户, 02=支付, 03=数据
错误序号: 01-99
```

### Error Code Table Template
```markdown
## 通用错误 (40xxx)
| 错误码 | HTTP状态码 | 说明 | 解决方案 |
|--------|-----------|------|----------|
| 40001 | 400 | 参数格式错误 | 检查JSON格式 |
| 40002 | 401 | 未授权 | 重新获取access_token |
| 40003 | 403 | 权限不足 | 检查接口权限 |
| 40004 | 404 | 资源不存在 | 检查资源ID |
| 40029 | 429 | 请求频率超限 | 等待后重试 |

## 用户模块错误 (41xxx)
| 错误码 | HTTP状态码 | 说明 | 解决方案 |
|--------|-----------|------|----------|
| 41001 | 400 | 手机号格式错误 | 使用+86格式 |
| 41002 | 400 | 验证码错误 | 重新获取验证码 |
| 41003 | 403 | 账号被冻结 | 联系客服解冻 |

## 支付模块错误 (42xxx)
| 错误码 | HTTP状态码 | 说明 | 解决方案 |
|--------|-----------|------|----------|
| 42001 | 400 | 金额格式错误 | 金额单位为分，整数 |
| 42002 | 403 | 余额不足 | 充值后重试 |
| 42003 | 400 | 订单已支付 | 检查订单状态 |
```

## Workflow 3: Signature Authentication Doc

```markdown
## 签名验证

### 签名算法
1. 将所有非空请求参数按参数名ASCII码从小到大排序
2. 使用URL键值对的格式拼接成字符串 (key1=value1&key2=value2)
3. 在拼接的字符串末尾加上&app_secret=YOUR_SECRET
4. 对最终字符串进行MD5运算，得到32位小写sign

### 示例
请求参数:
\`\`\`
app_id = wx1234567890
timestamp = 1672531200
nonce = abc123
name = 测试
\`\`\`

Step 1 - 排序:
\`\`\`
app_id=wx1234567890&name=测试&nonce=abc123&timestamp=1672531200
\`\`\`

Step 2 - 加密钥:
\`\`\`
app_id=wx1234567890&name=测试&nonce=abc123&timestamp=1672531200&app_secret=your_secret
\`\`\`

Step 3 - MD5:
\`\`\`
sign = md5(above_string) = "a1b2c3d4e5f6..."
\`\`\`

### 注意事项
- 参数值为空不参与签名
- 参数名区分大小写
- sign参数本身不参与签名计算
- 请求必须包含timestamp（5分钟内有效）和nonce（防重放）
```

## Workflow 4: Changelog & Migration Guide

```markdown
# 更新日志

## v2.0.0 (2026-05-26)

### ⚠️ 破坏性变更
- 用户列表接口分页参数从`page/page_size`改为`offset/limit`
- 返回值中`user_id`类型从integer改为string

### 迁移指南
\`\`\`javascript
// v1.x
GET /api/v1/users?page=1&page_size=20

// v2.0
GET /api/v2/users?offset=0&limit=20
\`\`\`

\`\`\`javascript
// v1.x - user_id是数字
const userId = response.data.user_id; // 12345

// v2.0 - user_id是字符串
const userId = response.data.user_id; // "usr_abc123"
\`\`\`

### 新增接口
- `POST /api/v2/users/batch` - 批量创建用户
- `GET /api/v2/users/search` - 用户搜索

### 废弃接口
- `GET /api/v1/users/search` → 请使用 `GET /api/v2/users/search`
- 废弃接口将在2026-08-26下线
```

## Safety Rules

1. **Always include request_id** — Chinese developers rely on this for debugging with support
2. **Always include error solutions** — not just "what went wrong" but "how to fix it"
3. **Always include 4+ language examples** — Java is #1 in China, Python #2, Node #3, Go rising
4. **Always use Beijing time (UTC+8)** — never UTC in examples
5. **Always document rate limits** — Chinese platforms have strict QPS limits
6. **Always include signature algorithm** — most Chinese APIs use signature auth, not OAuth
7. **Version in URL path** — Chinese developers prefer `/api/v2/` over header-based versioning

## Quick Reference

| Doc Type | Template | Key Sections |
|----------|----------|-------------|
| API接口文档 | Workflow 1 | 基本信息+请求参数+返回参数+SDK示例+错误码 |
| 错误码文档 | Workflow 2 | 错误码+HTTP状态+说明+解决方案 |
| 签名验证 | Workflow 3 | 算法+示例+注意事项 |
| 更新日志 | Workflow 4 | 破坏性变更+迁移指南+新增+废弃 |
