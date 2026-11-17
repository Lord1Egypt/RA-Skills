# AgentLens API 参考

当需要实现或调试 AgentLens API 调用时使用本文档。

## 接口地址

```http
POST https://agentlensapi.io/api/v1/fetch
Authorization: Bearer $AGENT_LENS_API_KEY
Content-Type: application/json

{ "url": "https://..." }
```

必须使用上方完全一致的接口地址。不要添加 API 子域名，不要修改域名后缀，不要移除 `/api`，也不要改写 path。如果准备使用的地址与上方值不是逐字节一致，发送请求前先停止并重新读取本文档。

如果用户提供的是短链或平台分享链接，先把这个原始 URL 交给 AgentLens API。不要先通过搜索、浏览器会话或其他平台展开替换；只有 AgentLens API 请求失败且用户明确同意时，才考虑其他来源。

## 请求前检查

每次 AgentLens API 请求前，内部确认：

```text
- 已加载必要 reference：references/agentlens-api_cn.md
- Endpoint 来源：本文档或用户批准的 connector 配置
- Endpoint：https://agentlensapi.io/api/v1/fetch
- Method：POST
- Auth：使用 AgentLens API key 作为 Bearer token
- Body 形状：{"url": "<original user URL>"}
- 未经用户批准，不使用其他来源替代原始链接
```

## curl 示例

```bash
curl -sS -X POST "https://agentlensapi.io/api/v1/fetch" \
  -H "Authorization: Bearer $AGENT_LENS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/post"}'
```

## Python 辅助代码

```python
import json
import urllib.error
import urllib.request


AGENTLENS_FETCH_ENDPOINT = "https://agentlensapi.io/api/v1/fetch"


def assert_agentlens_endpoint(endpoint):
    if endpoint != AGENTLENS_FETCH_ENDPOINT:
        raise ValueError(
            "AgentLens API endpoint must exactly match references/agentlens-api_cn.md: "
            f"{AGENTLENS_FETCH_ENDPOINT}"
        )


def fetch_with_agentlens(url, agentlens_key, timeout=60):
    endpoint = AGENTLENS_FETCH_ENDPOINT
    assert_agentlens_endpoint(endpoint)
    req = urllib.request.Request(
        endpoint,
        data=json.dumps({"url": url}).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {agentlens_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result = json.load(resp)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        try:
            result = json.loads(body)
            result.setdefault("_http_status", exc.code)
        except json.JSONDecodeError:
            return {
                "ok": False,
                "status": exc.code,
                "code": f"HTTP_{exc.code}",
                "message": body[:500],
            }
    except Exception as exc:
        return {
            "ok": False,
            "code": type(exc).__name__,
            "message": str(exc),
        }

    # 当前 AgentLens API 成功响应是顶层 success + 扁平 data。
    content = result.get("data") if isinstance(result.get("data"), dict) else {}
    status = result.get("status") or result.get("_http_status")

    if result.get("success") is True or str(status) == "200":
        return {
            "ok": True,
            "platform": result.get("platform") or content.get("platform"),
            "author": content.get("authorName"),
            "author_id": content.get("authorId"),
            "published_at": content.get("publishedAt"),
            "title": content.get("title"),
            "text": content.get("text") or "",
            "subtitle": content.get("subtitle"),
            "media": content.get("media") or [],
            "raw": result,
        }

    envelope = result.get("data", result)
    error = result.get("error") or {}
    code = error.get("code") or (envelope.get("code") if isinstance(envelope, dict) else None) or status
    message = (
        error.get("message")
        or (envelope.get("message") if isinstance(envelope, dict) else None)
        or result.get("message")
        or "AgentLens API request failed"
    )
    return {
        "ok": False,
        "status": status,
        "code": code,
        "message": message,
        "raw": result,
    }
```

## 响应字段

成功响应通常包含：

```yaml
success: true
requestId: 请求关联 id，如返回
platform: 检测出的来源平台
creditsUsed: 成功请求消耗的额度
subscription: 套餐和额度状态
data.authorName: 作者、频道或账号名
data.authorId: 来源平台内的作者 ID，如有
data.publishedAt: 发布时间，如有
data.text: 正文、说明文案、文章内容或标题文本，如有
data.subtitle: 字幕或转写文本，如有
data.media[].type: 媒体类型；当前已观察到的单作品成功响应使用 image 或 video
data.media[].source_url: 优先使用的直接媒体 URL，如返回
data.media[].cdn_url: source_url 缺失时的备用直接媒体 URL，如返回
data.media[].cover: 可选封面或缩略图 URL，如返回
```

部分错误响应使用以下结构：

```yaml
success: false
error.code: AUTH_FAILED
error.message: API key invalid or disabled
```

当前 AgentLens API 成功响应不要假设存在嵌套成功载荷。当前解析必须使用上方扁平 `data` 对象。

## 规范化

回答前，将成功内容规范化为以下内部结构：

```json
{
  "platform": "",
  "author": "",
  "title": "",
  "text": "",
  "subtitle": "",
  "media": []
}
```

将 `data.text` 作为主要文本。如果存在 `data.subtitle`，视频总结时必须纳入。如果只返回媒体而没有文本/字幕，告诉用户 API 返回了哪些来源信息和媒体链接，并说明没有可用正文或转写。

## 平台链接补充说明

小红书链接如果使用 `xhslink.cn` 短链或裸 `xiaohongshu.com/explore/...` 链接时返回 `PLATFORM_NOT_SUPPORTED`、`PROVIDER_ALL_FAILED` 或持续解析失败，优先请用户提供 App 分享出来的完整带参数链接。带有 `xsec_token`、`xsec_source=app_share` 以及相关 App 分享参数的链接，可能在去参数链接失败时成功。不要承诺这种方式一定修复，也不要无限重试。

如果小红书响应成功但 `data.text` 为空，明确说明 API 未返回笔记正文，当前总结仅基于返回图片/媒体和元数据。不要编造缺失的正文或标题文案。

## 响应复用

成功调用后，保留本次任务的规范化内容和原始 JSON 响应。如果运行环境允许，写入当前任务产物，例如 `/tmp/agentlens_{platform}_{timestamp}_response.json`。后续媒体处理、转写说明和知识库保存应复用这份结果。不要因为用户稍后要求保存就重新 fetch。只有结果缺失、损坏、过期、URL 不匹配，或用户要求刷新时才重新调用；再次发起可能成功的 API 调用前，说明可能消耗额度。

## 错误映射

| Code / HTTP | 含义 | 客户端/面向用户的处理 |
|:--|:--|:--|
| `success=true` 或 HTTP 200 | 成功 | 正常总结/提取 |
| `VALIDATION_ERROR` / HTTP 400 | 必填请求字段校验失败 | 修正请求；不要原样重试 |
| `INVALID_JSON` / HTTP 400 | 请求体不是合法 JSON | 修正 JSON；不要原样重试 |
| `INVALID_URL` / HTTP 400 | URL 格式错误，或不匹配已配置来源 | 请用户提供有效 URL；不要原样重试 |
| `AUTH_FAILED` / HTTP 401 | API key 缺失、无效或已停用 | 请用户提供或替换 AgentLens API key |
| `RESOURCE_NOT_FOUND` / HTTP 404 | 资源不存在或已不可用 | 告知用户内容可能已删除/不可用；不要原样重试 |
| `PLATFORM_NOT_SUPPORTED` / HTTP 422 | 上游解析器不支持该平台或 URL 类型 | 说明暂不支持；可提出反馈平台/链接类型；不支持的平台不会扣除 AgentLens API 调用额度 |
| `UNSUPPORTED_MEDIA_TYPE` / HTTP 415 | 请求不是 `application/json` | 修正 `Content-Type`；不要原样重试 |
| `RATE_LIMIT_EXCEEDED` / HTTP 403 | 订阅缺失或已过期 | 请用户激活或续订套餐；不要原样重试 |
| `RATE_LIMIT_EXCEEDED` / HTTP 429 | 当前月度额度已用尽 | 请用户等待 `quotaRefreshAt` 或更换套餐 |
| `RATE_LIMITED` / HTTP 429 | 短时间请求频率窗口超限 | 稍后使用有限指数退避和 jitter 重试 |
| `PROVIDER_ALL_FAILED` / HTTP 502 | 所有已配置上游解析服务都失败 | 有限重试后报告受影响 URL |
| `UPSTREAM_PARSE_FAILED` / HTTP 502 | 上游服务无法解析该 URL | 谨慎重试；持续失败可能与该 URL 有关 |
| `UPSTREAM_INVALID_RESPONSE` / HTTP 502 | 上游服务返回无效或不完整响应 | 使用退避和 jitter 进行有限重试 |
| `UPSTREAM_ERROR` / HTTP 502 | 已配置上游解析器未能完成请求 | 使用退避和 jitter 进行有限重试 |
| `UPSTREAM_TIMEOUT` / HTTP 504 | 已配置上游解析器超时 | 使用退避和 jitter 进行有限重试 |
| `INTERNAL_ERROR` / HTTP 500 | AgentLens 发生未预期错误 | 谨慎重试；持续失败时联系支持 |
| `data.text` 为空且没有 `data.subtitle` | 未返回可读文本 | 说明 API 返回的文本有限；如有媒体，按媒体处理规则继续 |

当原始 URL 没有成功取回时，明确报告：

```markdown
我没有成功获取你提供的原始链接内容。

已尝试：
- Skill: agentlens-social-connector
- Endpoint: https://agentlensapi.io/api/v1/fetch
- URL: {original_url}
- Attempts: {attempt_count}

失败原因：{normalized_error}

除非你明确批准，否则我不会用其他平台、搜索结果或相似主题内容替代总结。
```

## AgentLens API 重试策略

AgentLens API 是本 Skill 的唯一检索接口。在向用户报告失败前，对临时性失败进行有限重试。

- 先执行 1 次初始请求。
- 如果失败属于临时性失败，最多额外重试 2 次，总计 3 次。
- 网络超时、连接重置、HTTP 408、`RATE_LIMITED` / HTTP 429、`PROVIDER_ALL_FAILED`、`UPSTREAM_INVALID_RESPONSE`、`UPSTREAM_ERROR`、`UPSTREAM_TIMEOUT` 和可重试 HTTP 5xx 视为临时性失败。
- `VALIDATION_ERROR`、`INVALID_JSON`、`INVALID_URL`、`AUTH_FAILED`、`RESOURCE_NOT_FOUND`、`PLATFORM_NOT_SUPPORTED` / HTTP 422、`UNSUPPORTED_MEDIA_TYPE`、`RATE_LIMIT_EXCEEDED` / HTTP 403、`RATE_LIMIT_EXCEEDED` / HTTP 429、私密/已删除/需登录内容、URL 格式错误，以及不可重试 HTTP 4xx，视为不可重试。
- 注意：`RATE_LIMIT_EXCEEDED` 可能以 HTTP 403 表示订阅/套餐问题，也可能以 HTTP 429 表示月度额度已用尽，二者都不可自动重试。`RATE_LIMITED` / HTTP 429 才表示短时间请求频率窗口超限，是可重试的限流场景。
- 对 HTTP 429 或 5xx，如果响应里有 `Retry-After` header，优先遵守。否则在重试之间使用短指数退避，例如第 2 次请求前等待 1 秒，第 3 次请求前等待 2 秒。
- 自动重试之间不要询问用户，除非重试需要下载大媒体文件，或会消耗 AgentLens API 之外的付费/有限外部额度。
- 如果所有尝试都失败，报告最后一次错误，说明 AgentLens API 已尝试 3 次，并建议稍后重试或换一个可访问 URL。
- 总计 3 次后不要继续循环。

## 媒体处理

当存在 `data.media[]`：

- `type=video` 表示视频媒体。
- `type=image` 表示图片。
- 直接媒体 URL 按以下顺序选择：非空 `source_url`，其次是非空 `cdn_url`。
- `cover` 只作为封面/缩略图证据。当 `source_url` 和 `cdn_url` 都缺失时，不要把 `cover` 当作原始媒体下载地址。
- 如果某个媒体项同时缺少 `source_url` 和 `cdn_url`，记录 `media_url_missing`，并只基于已有元数据/封面继续处理。
- 不要假设主页/列表类响应中的每个媒体项都可下载；即使存在 `cover`，直接媒体 URL 也可能缺失。
- 除非用户要求下载、理解媒体文件或更深入分析，否则不要下载媒体。
- 如需下载，只写入 `/tmp/agentlens_{platform}_{timestamp}.{ext}`。
- 不要把媒体 URL 当作长期可用的归档链接。
- 对媒体主导内容的总结/分析，默认处理所有带直接 URL 的返回媒体项。对窄任务，例如只转写一个视频或只查看用户指定图片，则只使用当前任务需要的媒体。
- 不要在未展示受影响临时文件并获得用户确认前执行批量清理命令。

## 知识库整理稿结构

当用户要求保存检索内容时，先准备以下结构的整理稿，再传给当前环境中的目的地写入工具：

面向用户阅读的字段标签和小节标题，默认跟随用户当前对话语言。下面示例使用中文；用户提供的模板、目标工具字段名和 API/schema 字段名/key 必须原样保留，不要翻译。不要在整理稿中保留或回显任何凭据值。

```markdown
# {title or concise source label}

原始链接：{url}
平台：{platform}
作者/来源：{author}
账号/Handle：{handle_or_author_id，如有}
标题：{title}
发布日期：{published_at or unknown}
获取日期：{date}

## 摘要
...

## 要点
- ...

## 字幕或说明文案
...

## 媒体解读
...
```

只有当当前请求明确目的地或用户已确认时，才写入外部服务、本地笔记或工作区文件。不要创建后台归档或周期性保存。

## 安全说明

- 绝不回显完整 API key。
- 将 key redact 为 `[redacted-last4]` 或 `[redacted]`。
- 除非用户明确批准，否则不要保存 key。
- 不要在 AgentLens API 请求中使用 cookie、社交账号凭据或浏览器 session。
- 除非用户已批准本地配置，或当前工作流要求，否则不要读取本地 AgentLens 配置文件。
