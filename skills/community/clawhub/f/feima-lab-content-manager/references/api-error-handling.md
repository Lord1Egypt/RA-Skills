# API 脚本错误处理对照表

所有 `scripts/api/*.mjs` 脚本遇到错误时输出一行 JSON 到 **stderr**，然后 `exit 1`。格式：

    {"status":"error","error_type":"<type>","message":"...","suggestion":"..."}

Claude 读到 stderr 的 error JSON 后，根据 `error_type` 决定下一步：

## error_type 清单

### `missing_api_key`

**含义**：shell 的 `FX_AI_API_KEY` 环境变量未设置或为空。

**Claude 行动**：
- 停止所有 API 调用
- 告诉用户："请在 shell 中执行 `export FX_AI_API_KEY=<你的 key>` 然后重新运行。key 从 https://platform.fenxiang-ai.com/ 登录后获取。"
- **不要**尝试把 key 写入 MEMORY.md、.env、或任何持久化位置——env var 应由用户在 shell 管理

---

### `invalid_argument`

**含义**：CLI 参数缺失或格式错。

**Claude 行动**：
- 读 `message` 看缺什么，补参数后重试
- 如果是内部拼命令时的 bug，停下让用户人工复核

---

### `invalid_meta`

**含义**：`meta.json` 缺必填字段或字段格式错。

**常见子情况**：
- "缺少 slug / title / description / author" → 补全 meta.json 对应字段
- "缺少 category 或 categoryId" → 填 `category: "AI 实战"` 或 `categoryId: 3`
- "meta.category 在后端列表中不存在" → `message` 里会列出所有可选分类，选一个正确的填回
- "meta.publish.remote_id 未填" → 说明还没 save 过，先跑 save-article

**Claude 行动**：读 suggestion 按提示改 meta.json，重试

---

### `file_not_found`

**含义**：文件路径在磁盘上不存在。

**常见子情况**：
- `article.mdx 不存在` → 先写文章，或检查 --post-dir 路径拼写
- `meta.coverImage 指向的本地文件不存在` → 先跑 `scripts/image-localize.mjs` 本地化图片
- `meta.json 不存在` → 先跑 `scripts/new-post.mjs` 建骨架

**Claude 行动**：按 suggestion 执行前置步骤，重试

---

### `api_unavailable`

**含义**：网络层问题。包括：

- 请求超时（30s）
- DNS / 连接失败
- HTTP 5xx
- 响应不是合法 JSON

**Claude 行动**：
- 告诉用户"服务暂时不可用"
- **最多重试 1 次**
- 连续失败就停下来，让用户检查网络/代理/后端状态，不要无限重试

---

### `api_error`

**含义**：HTTP 200 + 合法 JSON，但 `code != 200`，即后端业务错误。

**常见子情况**（根据 message 判断）：
- "slug 已存在" → 改 slug 或走 update 模式
- "categoryId 不存在" → 重查 list-categories
- "权限不足" → API Key 可能已失效，提示用户重新获取
- "参数校验失败" → message 通常会指明具体字段

**Claude 行动**：读 message 按后端提示改输入，重试

---

### `not_found`（仅 `get-article.mjs`）

**含义**：按 slug 查询时后端没这篇文章。exit 2（区别于 exit 1 的真错误）。

**Claude 行动**：
- 告诉用户："slug `<x>` 在后端不存在"
- 如果当前意图是"发布"，改为走 save 路径先创建
- 如果当前意图是"查看远程版本"，告诉用户还没发布过

---

### `unexpected`

**含义**：脚本自身 bug（未被预期的抛错）。message 里会有 stack trace。

**Claude 行动**：
- 把完整 JSON 给用户看
- 停下，不要继续调用
- 这是脚本 bug，可能需要改源码

---

## 重试策略总结

| error_type | 是否重试 | 重试前要做的事 |
|---|---|---|
| `missing_api_key` | ❌ 不重试 | 用户必须手工设 env |
| `invalid_argument` | ❌ 不重试 | 修参数 |
| `invalid_meta` | ✅ 修好后重试 1 次 | 按 suggestion 改 meta.json |
| `file_not_found` | ✅ 跑前置脚本后重试 | 建文件/跑 image-localize |
| `api_unavailable` | ✅ 最多 1 次 | 稍等 |
| `api_error` | ✅ 修正输入后重试 1 次 | 按 message 改 |
| `not_found` | ❌ 不重试（不是错） | 换路径（save 代替 get） |
| `unexpected` | ❌ 不重试 | 报告给用户 |

## 脚本退出码

| 退出码 | 含义 |
|---|---|
| 0 | 成功（JSON 到 stdout） |
| 1 | 任何错误（JSON 到 stderr） |
| 2 | `get-article.mjs` 专属：slug 在后端不存在 |
