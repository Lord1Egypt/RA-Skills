# ClawHub API 接口参考文档

## 技能相关接口

### 1. 搜索技能

```http
GET /api/v1/search?q=...
```

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| q | string | 是 | 搜索查询 |
| limit | integer | 否 | 结果数量限制 |
| highlightedOnly | boolean | 否 | 仅显示高亮结果 |
| nonSuspiciousOnly | boolean | 否 | 仅显示非可疑技能 |
| nonSuspicious | boolean | 否 | nonSuspiciousOnly的旧别名 |

**响应**: `SearchResponse`

**cURL 示例**
```bash
curl -X GET "https://clawhub.ai/api/v1/search?q=example&limit=10"
```

**Python 示例**
```python
import requests

response = requests.get(
    "https://clawhub.ai/api/v1/search",
    params={"q": "example", "limit": 10}
)
print(response.json())
```

---

### 2. 列出技能

```http
GET /api/v1/skills?limit=&cursor=&sort=
```

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| limit | integer | 否 | 每页数量 |
| cursor | string | 否 | 分页游标（仅用于非trending排序） |
| sort | string | 否 | 排序方式 |
| nonSuspiciousOnly | boolean | 否 | 隐藏可疑技能 |
| nonSuspicious | boolean | 否 | nonSuspiciousOnly的旧别名 |

**sort 可选值**
- `updated` (默认)
- `recommended` / `default`
- `createdAt` / `newest`
- `downloads`
- `stars` / `rating`
- `installsCurrent` / `installs`
- `installsAllTime`
- `trending`

**响应**: `SkillListResponse`

**cURL 示例**
```bash
curl -X GET "https://clawhub.ai/api/v1/skills?sort=recommended&limit=20"
```

**Python 示例**
```python
import requests

response = requests.get(
    "https://clawhub.ai/api/v1/skills",
    params={"sort": "recommended", "limit": 20}
)
print(response.json())
```

---

### 3. 获取技能详情

```http
GET /api/v1/skills/{slug}
```

**路径参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| slug | string | 是 | 技能标识符 |

**响应**: `SkillResponse`

**cURL 示例**
```bash
curl -X GET "https://clawhub.ai/api/v1/skills/example-skill"
```

**Python 示例**
```python
import requests

response = requests.get("https://clawhub.ai/api/v1/skills/example-skill")
print(response.json())
```

---

### 4. 获取技能审核详情

```http
GET /api/v1/skills/{slug}/moderation
```

**路径参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| slug | string | 是 | 技能标识符 |

**响应**: 包含 moderation 对象的 JSON

**cURL 示例**
```bash
curl -X GET "https://clawhub.ai/api/v1/skills/example-skill/moderation"
```

**Python 示例**
```python
import requests

response = requests.get("https://clawhub.ai/api/v1/skills/example-skill/moderation")
print(response.json())
```

---

### 5. 获取技能安全扫描详情

```http
GET /api/v1/skills/{slug}/scan?version=&tag=
```

**路径参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| slug | string | 是 | 技能标识符 |

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| version | string | 否 | 版本号 |
| tag | string | 否 | 分发标签 |

**响应**: `SkillScanResponse`

**cURL 示例**
```bash
curl -X GET "https://clawhub.ai/api/v1/skills/example-skill/scan"
```

**Python 示例**
```python
import requests

response = requests.get("https://clawhub.ai/api/v1/skills/example-skill/scan")
print(response.json())
```

---

### 6. 获取技能原始文件

```http
GET /api/v1/skills/{slug}/file?path=&version=&tag=
```

**路径参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| slug | string | 是 | 技能标识符 |

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| path | string | 是 | 文件路径 |
| version | string | 否 | 版本号 |
| tag | string | 否 | 分发标签 |

**响应**: 文件内容 (text/plain)

**cURL 示例**
```bash
curl -X GET "https://clawhub.ai/api/v1/skills/example-skill/file?path=README.md"
```

**Python 示例**
```python
import requests

response = requests.get(
    "https://clawhub.ai/api/v1/skills/example-skill/file",
    params={"path": "README.md"}
)
print(response.text)
```

---

### 7. 列出技能版本

```http
GET /api/v1/skills/{slug}/versions?limit=&cursor=
```

**路径参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| slug | string | 是 | 技能标识符 |

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| limit | integer | 否 | 每页数量 |
| cursor | string | 否 | 分页游标 |

**响应**: `SkillVersionListResponse`

**cURL 示例**
```bash
curl -X GET "https://clawhub.ai/api/v1/skills/example-skill/versions"
```

**Python 示例**
```python
import requests

response = requests.get("https://clawhub.ai/api/v1/skills/example-skill/versions")
print(response.json())
```

---

### 8. 获取技能版本详情

```http
GET /api/v1/skills/{slug}/versions/{version}
```

**路径参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| slug | string | 是 | 技能标识符 |
| version | string | 是 | 版本号 |

**响应**: `SkillVersionResponse`

**cURL 示例**
```bash
curl -X GET "https://clawhub.ai/api/v1/skills/example-skill/versions/1.0.0"
```

**Python 示例**
```python
import requests

response = requests.get("https://clawhub.ai/api/v1/skills/example-skill/versions/1.0.0")
print(response.json())
```

---

### 9. 发布技能版本

```http
POST /api/v1/skills
```

**认证**: 需要Bearer Token

**请求体** (multipart/form-data - 推荐)

| 字段 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| payload | string | 是 | JSON载荷 |
| files | array | 是 | 文件数组 |

**请求体** (application/json)

| 字段 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| slug | string | 是 | 技能标识符 |
| displayName | string | 是 | 显示名称 |
| version | string | 是 | 版本号 |
| changelog | string | 是 | 更新日志 |
| tags | array | 否 | 标签数组 |
| forkOf | object | 否 | 分支信息 |
| files | array | 是 | 文件信息数组 |

**响应**: `PublishResponse`
```json
{
  "ok": true,
  "skillId": "string",
  "versionId": "string"
}
```

**cURL 示例**
```bash
curl -X POST "https://clawhub.ai/api/v1/skills" \
  -H "Authorization: Bearer clh_your_token_here" \
  -F "payload=@payload.json" \
  -F "files=@skill.zip"
```

**Python 示例**
```python
import requests

headers = {
    "Authorization": "Bearer clh_your_token_here"
}
files = {
    "payload": ("payload.json", open("payload.json", "rb")),
    "files": ("skill.zip", open("skill.zip", "rb"))
}
response = requests.post("https://clawhub.ai/api/v1/skills", headers=headers, files=files)
print(response.json())
```

---

### 10. 软删除技能

```http
DELETE /api/v1/skills/{slug}
```

**认证**: 需要Bearer Token

**路径参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| slug | string | 是 | 技能标识符 |

**响应**: `DeleteResponse`
```json
{
  "ok": true
}
```

**cURL 示例**
```bash
curl -X DELETE "https://clawhub.ai/api/v1/skills/example-skill" \
  -H "Authorization: Bearer clh_your_token_here"
```

**Python 示例**
```python
import requests

headers = {
    "Authorization": "Bearer clh_your_token_here"
}
response = requests.delete("https://clawhub.ai/api/v1/skills/example-skill", headers=headers)
print(response.json())
```

---

### 11. 恢复已删除技能

```http
POST /api/v1/skills/{slug}/undelete
```

**认证**: 需要Bearer Token

**路径参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| slug | string | 是 | 技能标识符 |

**响应**: `DeleteResponse`

**cURL 示例**
```bash
curl -X POST "https://clawhub.ai/api/v1/skills/example-skill/undelete" \
  -H "Authorization: Bearer clh_your_token_here"
```

**Python 示例**
```python
import requests

headers = {
    "Authorization": "Bearer clh_your_token_here"
}
response = requests.post("https://clawhub.ai/api/v1/skills/example-skill/undelete", headers=headers)
print(response.json())
```

---

## 统一包目录接口

### 12. 列出统一包目录

```http
GET /api/v1/packages
```

**说明**: 列出技能、代码插件和bundle插件。匿名调用者只能看到公共包渠道；已认证调用者还可以看到可读的私有包。

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| limit | integer | 否 | 1-100 |
| cursor | string | 否 | 分页游标 |
| family | string | 否 | skill/code-plugin/bundle-plugin |
| channel | string | 否 | official/community/private |
| isOfficial | boolean | 否 | 是否官方 |
| executesCode | boolean | 否 | 是否执行代码 |
| capabilityTag | string | 否 | 能力标签 |
| target | string | 否 | host能力标签简写 |
| hostTarget | string | 否 | host能力标签简写 |
| os | string | 否 | host OS能力标签简写 |
| arch | string | 否 | host架构能力标签简写 |
| libc | string | 否 | host libc能力标签简写 |
| requiresBrowser | boolean | 否 | 是否需要浏览器 |
| requiresDesktop | boolean | 否 | 是否需要桌面 |
| requiresNativeDeps | boolean | 否 | 是否需要原生依赖 |
| requiresExternalService | boolean | 否 | 是否需要外部服务 |
| requiresBinary | boolean | 否 | 是否需要二进制 |
| requiresOsPermission | boolean | 否 | 是否需要OS权限 |
| externalService | string | 否 | 外部服务 |
| binary | string | 否 | 二进制 |
| osPermission | string | 否 | OS权限 |
| artifactKind | string | 否 | legacy-zip/npm-pack |
| npmMirror | boolean | 否 | 是否通过npm镜像 |

**响应**: `PackageListResponse`

**cURL 示例**
```bash
curl -X GET "https://clawhub.ai/api/v1/packages?family=skill&limit=20"
```

**Python 示例**
```python
import requests

response = requests.get(
    "https://clawhub.ai/api/v1/packages",
    params={"family": "skill", "limit": 20}
)
print(response.json())
```

---

### 13. 获取包详情

```http
GET /api/v1/packages/{name}
```

**说明**: 返回包详情元数据。技能也可以通过此统一目录路由解析。

**路径参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| name | string | 是 | 包名（作用域名必须URL路径编码） |

**响应**: `PackageResponse`

**cURL 示例**
```bash
curl -X GET "https://clawhub.ai/api/v1/packages/example-skill"
```

**Python 示例**
```python
import requests

response = requests.get("https://clawhub.ai/api/v1/packages/example-skill")
print(response.json())
```

---

### 14. 下载包ZIP归档

```http
GET /api/v1/packages/{name}/download
```

**说明**: 下载包版本的legacy确定性ZIP归档。此路由保持仅ZIP并使用下载速率bucket。

**路径参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| name | string | 是 | 包名 |

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| version | string | 否 | 版本号 |
| tag | string | 否 | 分发标签 |

**响应**: ZIP文件 (application/zip)

**状态码**
- `200`: ZIP归档
- `307`: 技能兼容性重定向到 /api/v1/download
- `400`: 无效请求
- `403`: 被包审核阻止
- `404`: 未找到
- `429`: 超出限流

**cURL 示例**
```bash
curl -X GET "https://clawhub.ai/api/v1/packages/example-skill/download?version=1.0.0" \
  -o skill.zip
```

**Python 示例**
```python
import requests

response = requests.get(
    "https://clawhub.ai/api/v1/packages/example-skill/download",
    params={"version": "1.0.0"}
)
with open("skill.zip", "wb") as f:
    f.write(response.content)
```

---

### 15. 获取包原始文件

```http
GET /api/v1/packages/{name}/file
```

**说明**: 返回包文件的原始文本内容。使用读取速率bucket。

**路径参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| name | string | 是 | 包名 |

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| path | string | 是 | 文件路径 |
| version | string | 否 | 版本号 |
| tag | string | 否 | 分发标签 |

**响应**: 文件内容 (text/plain)

**状态码**
- `200`: 文件内容
- `400`: 无效请求
- `404`: 未找到
- `413`: 文件过大
- `415`: 二进制文件不内联提供

**cURL 示例**
```bash
curl -X GET "https://clawhub.ai/api/v1/packages/example-skill/file?path=README.md"
```

**Python 示例**
```python
import requests

response = requests.get(
    "https://clawhub.ai/api/v1/packages/example-skill/file",
    params={"path": "README.md"}
)
print(response.text)
```

---

### 16. 获取包OpenClaw就绪状态

```http
GET /api/v1/packages/{name}/readiness
```

**说明**: 返回OpenClaw消费的计算就绪检查。

**路径参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| name | string | 是 | 包名 |

**响应**: `PackageReadinessResponse`
```json
{
  "package": {
    "name": "string",
    "displayName": "string",
    "family": "skill",
    "isOfficial": true,
    "latestVersion": "string"
  },
  "ready": true,
  "checks": [
    {
      "id": "string",
      "label": "string",
      "status": "pass",
      "message": "string"
    }
  ],
  "blockers": ["string"]
}
```

**cURL 示例**
```bash
curl -X GET "https://clawhub.ai/api/v1/packages/example-skill/readiness"
```

**Python 示例**
```python
import requests

response = requests.get("https://clawhub.ai/api/v1/packages/example-skill/readiness")
print(response.json())
```

---

### 17. 列出包版本

```http
GET /api/v1/packages/{name}/versions
```

**路径参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| name | string | 是 | 包名 |

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| limit | integer | 否 | 1-100 |
| cursor | string | 否 | 分页游标 |

**响应**: `PackageVersionListResponse`

**cURL 示例**
```bash
curl -X GET "https://clawhub.ai/api/v1/packages/example-skill/versions"
```

**Python 示例**
```python
import requests

response = requests.get("https://clawhub.ai/api/v1/packages/example-skill/versions")
print(response.json())
```

---

### 18. 获取包版本详情

```http
GET /api/v1/packages/{name}/versions/{version}
```

**说明**: 返回一个包版本的文件元数据、兼容性、能力、验证、工件元数据和扫描数据。

**路径参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| name | string | 是 | 包名 |
| version | string | 是 | 版本号 |

**响应**: `PackageVersionResponse`

**cURL 示例**
```bash
curl -X GET "https://clawhub.ai/api/v1/packages/example-skill/versions/1.0.0"
```

**Python 示例**
```python
import requests

response = requests.get("https://clawhub.ai/api/v1/packages/example-skill/versions/1.0.0")
print(response.json())
```

---

### 19. 获取包工件解析器元数据

```http
GET /api/v1/packages/{name}/versions/{version}/artifact
```

**说明**: 返回包版本的显式工件解析器元数据，包括格式特定的下载URL。

**路径参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| name | string | 是 | 包名 |
| version | string | 是 | 版本号 |

**响应**: `PackageArtifactResponse`
```json
{
  "package": {
    "name": "string",
    "displayName": "string",
    "family": "skill"
  },
  "version": "string",
  "artifact": {
    "kind": "legacy-zip",
    "sha256": "string",
    "size": 0,
    "format": "string",
    "npmIntegrity": "string",
    "npmShasum": "string",
    "npmTarballName": "string",
    "npmUnpackedSize": 0,
    "npmFileCount": 0,
    "source": "clawhub",
    "artifactKind": "legacy-zip",
    "artifactSha256": "string",
    "packageName": "string",
    "version": "string",
    "downloadUrl": "string",
    "tarballUrl": "string",
    "legacyDownloadUrl": "string"
  }
}
```

**cURL 示例**
```bash
curl -X GET "https://clawhub.ai/api/v1/packages/example-skill/versions/1.0.0/artifact"
```

**Python 示例**
```python
import requests

response = requests.get("https://clawhub.ai/api/v1/packages/example-skill/versions/1.0.0/artifact")
print(response.json())
```

---

### 20. 下载包版本工件

```http
GET /api/v1/packages/{name}/versions/{version}/artifact/download
```

**说明**: 流式传输npm-pack ClawPack字节或将legacy ZIP版本重定向到包下载端点。使用下载速率bucket。

**路径参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| name | string | 是 | 包名 |
| version | string | 是 | 版本号 |

**响应**: 工件字节 (application/octet-stream)

**状态码**
- `200`: 工件字节
- `307`: 重定向到legacy ZIP下载
- `400`: 无效请求
- `403`: 被包审核阻止
- `404`: 未找到
- `429`: 超出限流

**cURL 示例**
```bash
curl -X GET "https://clawhub.ai/api/v1/packages/example-skill/versions/1.0.0/artifact/download" \
  -o artifact.zip
```

**Python 示例**
```python
import requests

response = requests.get("https://clawhub.ai/api/v1/packages/example-skill/versions/1.0.0/artifact/download")
with open("artifact.zip", "wb") as f:
    f.write(response.content)
```

---

### 21. 获取精确包版本信任摘要

```http
GET /api/v1/packages/{name}/versions/{version}/security
```

**路径参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| name | string | 是 | 包名 |
| version | string | 是 | 版本号 |

**响应**: `PackageSecurityResponse`
```json
{
  "package": {
    "name": "string",
    "displayName": "string",
    "family": "skill"
  },
  "release": {
    "releaseId": "string",
    "version": "string",
    "artifactKind": "legacy-zip",
    "artifactSha256": "string",
    "npmIntegrity": "string",
    "npmShasum": "string",
    "npmTarballName": "string",
    "createdAt": 0
  },
  "trust": {
    "scanStatus": "clean",
    "moderationState": "approved",
    "blockedFromDownload": false,
    "reasons": ["string"],
    "pending": false,
    "stale": false
  }
}
```

**cURL 示例**
```bash
curl -X GET "https://clawhub.ai/api/v1/packages/example-skill/versions/1.0.0/security"
```

**Python 示例**
```python
import requests

response = requests.get("https://clawhub.ai/api/v1/packages/example-skill/versions/1.0.0/security")
print(response.json())
```

---

### 22. 搜索统一包目录

```http
GET /api/v1/packages/search
```

**说明**: 搜索技能和插件包。

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| q | string | 是 | 搜索查询 |
| limit | integer | 否 | 1-100 |
| family | string | 否 | skill/code-plugin/bundle-plugin |
| channel | string | 否 | official/community/private |
| isOfficial | boolean | 否 | 是否官方 |
| executesCode | boolean | 否 | 是否执行代码 |
| capabilityTag | string | 否 | 能力标签 |
| artifactKind | string | 否 | legacy-zip/npm-pack |
| npmMirror | boolean | 否 | npm镜像 |

**响应**: `PackageSearchResponse`

**cURL 示例**
```bash
curl -X GET "https://clawhub.ai/api/v1/packages/search?q=example&limit=10"
```

**Python 示例**
```python
import requests

response = requests.get(
    "https://clawhub.ai/api/v1/packages/search",
    params={"q": "example", "limit": 10}
)
print(response.json())
```

---

## 插件相关接口

### 23. 列出代码插件目录

```http
GET /api/v1/code-plugins
```

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| limit | integer | 否 | 1-100 |
| cursor | string | 否 | 分页游标 |
| channel | string | 否 | official/community/private |
| isOfficial | boolean | 否 | 是否官方 |
| executesCode | boolean | 否 | 是否执行代码 |
| capabilityTag | string | 否 | 能力标签 |

**响应**: `PackageListResponse`

**cURL 示例**
```bash
curl -X GET "https://clawhub.ai/api/v1/code-plugins?limit=20"
```

**Python 示例**
```python
import requests

response = requests.get(
    "https://clawhub.ai/api/v1/code-plugins",
    params={"limit": 20}
)
print(response.json())
```

---

### 24. 列出bundle插件目录

```http
GET /api/v1/bundle-plugins
```

**查询参数**: 同code-plugins

**响应**: `PackageListResponse`

**cURL 示例**
```bash
curl -X GET "https://clawhub.ai/api/v1/bundle-plugins?limit=20"
```

**Python 示例**
```python
import requests

response = requests.get(
    "https://clawhub.ai/api/v1/bundle-plugins",
    params={"limit": 20}
)
print(response.json())
```

---

### 25. 列出插件目录包

```http
GET /api/v1/plugins
```

**说明**: 列出code-plugin和bundle-plugin目录条目。

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| limit | integer | 否 | 1-100 |
| cursor | string | 否 | 分页游标 |
| channel | string | 否 | official/community/private |
| isOfficial | boolean | 否 | 是否官方 |
| executesCode | boolean | 否 | 是否执行代码 |
| capabilityTag | string | 否 | 能力标签 |
| artifactKind | string | 否 | legacy-zip/npm-pack |
| npmMirror | boolean | 否 | npm镜像 |

**响应**: `PackageListResponse`

**cURL 示例**
```bash
curl -X GET "https://clawhub.ai/api/v1/plugins?limit=20"
```

**Python 示例**
```python
import requests

response = requests.get(
    "https://clawhub.ai/api/v1/plugins",
    params={"limit": 20}
)
print(response.json())
```

---

### 26. 搜索插件目录包

```http
GET /api/v1/plugins/search
```

**说明**: 搜索code-plugin和bundle-plugin目录条目。

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| q | string | 是 | 搜索查询 |
| limit | integer | 否 | 1-100 |
| channel | string | 否 | official/community/private |
| isOfficial | boolean | 否 | 是否官方 |
| executesCode | boolean | 否 | 是否执行代码 |
| capabilityTag | string | 否 | 能力标签 |
| artifactKind | string | 否 | legacy-zip/npm-pack |
| npmMirror | boolean | 否 | npm镜像 |

**响应**: `PackageSearchResponse`

**cURL 示例**
```bash
curl -X GET "https://clawhub.ai/api/v1/plugins/search?q=example&limit=10"
```

**Python 示例**
```python
import requests

response = requests.get(
    "https://clawhub.ai/api/v1/plugins/search",
    params={"q": "example", "limit": 10}
)
print(response.json())
```

---

## 其他接口

### 27. 通过哈希解析版本

```http
GET /api/v1/resolve
```

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| slug | string | 是 | 技能标识符 |
| hash | string | 是 | SHA256哈希 |

**响应**: `ResolveResponse`
```json
{
  "match": {
    "version": "string"
  },
  "latestVersion": {
    "version": "string"
  }
}
```

**cURL 示例**
```bash
curl -X GET "https://clawhub.ai/api/v1/resolve?slug=example-skill&hash=abc123"
```

**Python 示例**
```python
import requests

response = requests.get(
    "https://clawhub.ai/api/v1/resolve",
    params={"slug": "example-skill", "hash": "abc123"}
)
print(response.json())
```

---

### 28. 下载ZIP

```http
GET /api/v1/download
```

**查询参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| slug | string | 是 | 技能标识符 |
| version | string | 否 | 版本号 |
| tag | string | 否 | 分发标签 |

**响应**: ZIP文件 (application/zip)

**cURL 示例**
```bash
curl -X GET "https://clawhub.ai/api/v1/download?slug=example-skill&version=1.0.0" \
  -o skill.zip
```

**Python 示例**
```python
import requests

response = requests.get(
    "https://clawhub.ai/api/v1/download",
    params={"slug": "example-skill", "version": "1.0.0"}
)
with open("skill.zip", "wb") as f:
    f.write(response.content)
```

---

### 29. 获取当前用户信息

```http
GET /api/v1/whoami
```

**认证**: 需要Bearer Token

**响应**: `WhoamiResponse`
```json
{
  "user": {
    "handle": "string",
    "displayName": "string",
    "image": "string"
  }
}
```

**cURL 示例**
```bash
curl -X GET "https://clawhub.ai/api/v1/whoami" \
  -H "Authorization: Bearer clh_your_token_here"
```

**Python 示例**
```python
import requests

headers = {
    "Authorization": "Bearer clh_your_token_here"
}
response = requests.get("https://clawhub.ai/api/v1/whoami", headers=headers)
print(response.json())
```

---

### 30. 软删除包

```http
DELETE /api/v1/packages/{name}
```

**认证**: 需要Bearer Token

**路径参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| name | string | 是 | 包名 |

**响应**: `DeleteResponse`

**cURL 示例**
```bash
curl -X DELETE "https://clawhub.ai/api/v1/packages/example-skill" \
  -H "Authorization: Bearer clh_your_token_here"
```

**Python 示例**
```python
import requests

headers = {
    "Authorization": "Bearer clh_your_token_here"
}
response = requests.delete("https://clawhub.ai/api/v1/packages/example-skill", headers=headers)
print(response.json())
```

---

### 31. 恢复已删除包

```http
POST /api/v1/packages/{name}/undelete
```

**认证**: 需要Bearer Token

**路径参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| name | string | 是 | 包名 |

**响应**: `DeleteResponse`

**cURL 示例**
```bash
curl -X POST "https://clawhub.ai/api/v1/packages/example-skill/undelete" \
  -H "Authorization: Bearer clh_your_token_here"
```

**Python 示例**
```python
import requests

headers = {
    "Authorization": "Bearer clh_your_token_here"
}
response = requests.post("https://clawhub.ai/api/v1/packages/example-skill/undelete", headers=headers)
print(response.json())
```

---

### 32. 技能重命名

```http
POST /api/v1/skills/{slug}/rename
```

**认证**: 需要Bearer Token

**路径参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| slug | string | 是 | 技能标识符 |

**cURL 示例**
```bash
curl -X POST "https://clawhub.ai/api/v1/skills/example-skill/rename" \
  -H "Authorization: Bearer clh_your_token_here"
```

**Python 示例**
```python
import requests

headers = {
    "Authorization": "Bearer clh_your_token_here"
}
response = requests.post("https://clawhub.ai/api/v1/skills/example-skill/rename", headers=headers)
print(response.json())
```

---

### 33. 技能合并

```http
POST /api/v1/skills/{slug}/merge
```

**认证**: 需要Bearer Token

**路径参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| slug | string | 是 | 技能标识符 |

**cURL 示例**
```bash
curl -X POST "https://clawhub.ai/api/v1/skills/example-skill/merge" \
  -H "Authorization: Bearer clh_your_token_here"
```

**Python 示例**
```python
import requests

headers = {
    "Authorization": "Bearer clh_your_token_here"
}
response = requests.post("https://clawhub.ai/api/v1/skills/example-skill/merge", headers=headers)
print(response.json())
```

---

### 34. 转移技能

```http
POST /api/v1/skills/{slug}/transfer
```

**认证**: 需要Bearer Token

**路径参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| slug | string | 是 | 技能标识符 |

**cURL 示例**
```bash
curl -X POST "https://clawhub.ai/api/v1/skills/example-skill/transfer" \
  -H "Authorization: Bearer clh_your_token_here"
```

**Python 示例**
```python
import requests

headers = {
    "Authorization": "Bearer clh_your_token_here"
}
response = requests.post("https://clawhub.ai/api/v1/skills/example-skill/transfer", headers=headers)
print(response.json())
```

---

### 35. 转移包

```http
POST /api/v1/packages/{name}/transfer
```

**认证**: 需要Bearer Token

**路径参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| name | string | 是 | 包名 |

**cURL 示例**
```bash
curl -X POST "https://clawhub.ai/api/v1/packages/example-skill/transfer" \
  -H "Authorization: Bearer clh_your_token_here"
```

**Python 示例**
```python
import requests

headers = {
    "Authorization": "Bearer clh_your_token_here"
}
response = requests.post("https://clawhub.ai/api/v1/packages/example-skill/transfer", headers=headers)
print(response.json())
```

---

### 36. 接受技能转移

```http
POST /api/v1/skills/{slug}/transfer/accept
```

**认证**: 需要Bearer Token

**路径参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| slug | string | 是 | 技能标识符 |

**cURL 示例**
```bash
curl -X POST "https://clawhub.ai/api/v1/skills/example-skill/transfer/accept" \
  -H "Authorization: Bearer clh_your_token_here"
```

**Python 示例**
```python
import requests

headers = {
    "Authorization": "Bearer clh_your_token_here"
}
response = requests.post("https://clawhub.ai/api/v1/skills/example-skill/transfer/accept", headers=headers)
print(response.json())
```

---

### 37. 拒绝技能转移

```http
POST /api/v1/skills/{slug}/transfer/reject
```

**认证**: 需要Bearer Token

**路径参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| slug | string | 是 | 技能标识符 |

**cURL 示例**
```bash
curl -X POST "https://clawhub.ai/api/v1/skills/example-skill/transfer/reject" \
  -H "Authorization: Bearer clh_your_token_here"
```

**Python 示例**
```python
import requests

headers = {
    "Authorization": "Bearer clh_your_token_here"
}
response = requests.post("https://clawhub.ai/api/v1/skills/example-skill/transfer/reject", headers=headers)
print(response.json())
```

---

### 38. 取消技能转移

```http
POST /api/v1/skills/{slug}/transfer/cancel
```

**认证**: 需要Bearer Token

**路径参数**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| slug | string | 是 | 技能标识符 |

**cURL 示例**
```bash
curl -X POST "https://clawhub.ai/api/v1/skills/example-skill/transfer/cancel" \
  -H "Authorization: Bearer clh_your_token_here"
```

**Python 示例**
```python
import requests

headers = {
    "Authorization": "Bearer clh_your_token_here"
}
response = requests.post("https://clawhub.ai/api/v1/skills/example-skill/transfer/cancel", headers=headers)
print(response.json())
```

---

### 39. 获取传入转移

```http
GET /api/v1/transfers/incoming
```

**认证**: 需要Bearer Token

**cURL 示例**
```bash
curl -X GET "https://clawhub.ai/api/v1/transfers/incoming" \
  -H "Authorization: Bearer clh_your_token_here"
```

**Python 示例**
```python
import requests

headers = {
    "Authorization": "Bearer clh_your_token_here"
}
response = requests.get("https://clawhub.ai/api/v1/transfers/incoming", headers=headers)
print(response.json())
```

---

### 40. 获取传出转移

```http
GET /api/v1/transfers/outgoing
```

**认证**: 需要Bearer Token

**cURL 示例**
```bash
curl -X GET "https://clawhub.ai/api/v1/transfers/outgoing" \
  -H "Authorization: Bearer clh_your_token_here"
```

**Python 示例**
```python
import requests

headers = {
    "Authorization": "Bearer clh_your_token_here"
}
response = requests.get("https://clawhub.ai/api/v1/transfers/outgoing", headers=headers)
print(response.json())
```

---

### 41. 保留用户根标识符（管理员）

```http
POST /api/v1/users/reserve
```

**认证**: 需要Bearer Token（管理员）

**说明**: 为所有者句柄保留根标识符和私有no-release包占位符。

**cURL 示例**
```bash
curl -X POST "https://clawhub.ai/api/v1/users/reserve" \
  -H "Authorization: Bearer clh_your_token_here"
```

**Python 示例**
```python
import requests

headers = {
    "Authorization": "Bearer clh_your_token_here"
}
response = requests.post("https://clawhub.ai/api/v1/users/reserve", headers=headers)
print(response.json())
```

