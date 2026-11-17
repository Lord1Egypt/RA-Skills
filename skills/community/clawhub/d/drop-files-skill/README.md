# DropFiles Skill

[中文](#中文) | [English](#english)

---

<a id="english"></a>

## English

An AI agent skill (compatible with [TRAE](https://trae.ai/), Claude, Cursor, and any agent that loads the `SKILL.md` frontmatter convention) that uploads generated HTML or Markdown content to the DropFiles service and returns a public shareable link. The service is free, globally accessible, and hosted on Cloudflare's edge network.

### Web Interface

Prefer a manual upload without an agent? Visit the DropFiles website directly to upload HTML or Markdown content and get a shareable link through your browser — no account required.

**Website**: <https://dropfiles.tokendealhub.com/>

### Features

- One-shot upload of HTML or Markdown content to get a public URL
- Bundled `scripts/upload.py` wrapper — agents and humans both call one command
- Automatic content-type detection (`html` / `markdown` / `auto`)
- Configurable expiry: 1 hour, 1 day, 7 days, or 30 days
- Optional password protection (user-supplied or auto-generated 6-digit code)
- Optional document title shown on the share page
- Public links work without an account for viewers
- HTML content is sanitized server-side (scripts stripped) for safety
- Markdown rendered with GitHub-flavored styling (code blocks, tables, images)

### Installation

Copy the entire skill directory (including both `SKILL.md` and `scripts/`) into your agent's skill directory, or clone this repository:

```bash
git clone https://github.com/icexun/drop-files-skill.git
```

Works with any agent that supports the `SKILL.md` frontmatter convention (TRAE, Claude, Cursor, etc.).

### Usage

Invoke this skill whenever you want to:

- Share generated HTML or Markdown content via a public link
- Publish a document, report, or page and get a URL to distribute
- Upload any text-based artifact (HTML/Markdown) for online viewing
- Generate a shareable preview link for content the agent just produced

#### The Wrapper Script

**Use `scripts/upload.py` for all uploads. Do not construct curl commands or JSON payloads manually.**

The script handles content reading, JSON serialization, temp-file management, curl invocation (Cloudflare WAF blocks non-curl HTTP clients), response parsing, and temp-file cleanup.

Run `python3 scripts/upload.py --help` for the full interface.

```
python3 scripts/upload.py [OPTIONS]

Content source (priority: --file > --content > stdin):
  --file PATH          Read content from file
  --content TEXT       Inline content (avoid for large text)
                       (if neither, read from stdin)

Upload options:
  --type TYPE          html | markdown | auto (default: auto)
  --expire EXPIRE      1h | 1d | 7d | 30d (default: 7d)
  --title TITLE        Optional title shown on the share page
  --lang LANG          en | zh | auto (default: auto)

Password (mutually exclusive):
  --password PASSWORD  Use a user-supplied password
  --generate-password  Generate a random 6-digit numeric password

Output:
  --json               Output full JSON response (recommended for agents)
  -h, --help           Show this help message and exit
```

#### Example: Upload Markdown (stdin, JSON output)

```bash
echo '# Hello World

This is a shared Markdown document.' | python3 scripts/upload.py --type markdown --json
```

Response:

```json
{
  "success": true,
  "data": {
    "id": "abc123def456",
    "url": "https://dropfiles.tokendealhub.com/v/abc123def456",
    "preview_url": "https://dropfiles.tokendealhub.com/v/abc123def456?preview=1",
    "expire_at": "2026-08-05T10:30:00.000Z",
    "type": "markdown",
    "size": 42
  }
}
```

#### Example: Upload from a file, human-readable output

```bash
python3 scripts/upload.py --file report.md --expire 1d --title "Q3 Report"
```

Response:

```
URL: https://dropfiles.tokendealhub.com/v/abc123
Preview: https://dropfiles.tokendealhub.com/v/abc123?preview=1
Expires: 2026-08-05T10:30:00Z
```

#### Example: Upload with an auto-generated 6-digit password

```bash
python3 scripts/upload.py --file secret.html --generate-password --json
```

Response includes the generated password so it can be communicated to viewers:

```json
{
  "success": true,
  "data": { "...": "..." },
  "password": "482917"
}
```

### API Reference (for reference only — use the wrapper script)

- **Base URL**: `https://dropfiles.tokendealhub.com`
- **Upload**: `POST /api/v1/upload`
- **Metadata**: `GET /api/v1/info/{id}`
- **Preview**: `https://dropfiles.tokendealhub.com/v/{id}`

Common error codes:
- `CONTENT_REQUIRED` — `content` field is empty.
- `CONTENT_TOO_LARGE` — content exceeds 5MB.
- `INVALID_TYPE` — `type` is not one of `html`, `markdown`, `auto`.
- `INVALID_EXPIRE` — `expire` is not one of `1h`, `1d`, `7d`, `30d`.
- `RATE_LIMIT_EXCEEDED` — too many requests from the same IP.

### Password Policy

The default behavior is **no password** — the share link is publicly accessible by anyone with the URL.

Password protection is opt-in and supports three modes:

1. **No password (default)**: Omit both password flags. The share page is publicly readable.
2. **User-supplied password**: Pass `--password "your password"` to the upload script.
3. **Skill-generated 6-digit password**: Pass `--generate-password`. The script generates a random 6-digit numeric code (e.g. `"482917"`), includes it in the upload, and surfaces it in the output. **Always relay the generated password to the user** so they can share it with viewers.

### Limits

- Max content size: **5 MB** (measured as UTF-8 bytes).
- Max expiry: **30 days**.
- Rate limiting applies per IP; if you hit `RATE_LIMIT_EXCEEDED`, wait and retry.

### Notes

- The share link is public (unless password-protected). Anyone with the URL can view the content.
- Viewers do not need an account.
- HTML content is sanitized: `<script>` tags and event handlers are removed.
- Markdown supports standard GitHub-flavored Markdown including code blocks, tables, and images.
- The `preview_url` adds `?preview=1` and is useful when embedding the link in a context that should not inflate the access counter on initial load.

### License

MIT

---

<a id="中文"></a>

## 中文

一个 AI agent 技能（兼容 [TRAE](https://trae.ai/)、Claude、Cursor 等任何支持 `SKILL.md` frontmatter 约定的 agent），用于将生成的 HTML 或 Markdown 内容上传到 DropFiles 服务，并返回一个公开可访问的分享链接。该服务免费、全球可访问，并托管在 Cloudflare 的边缘网络上。

### 网页端

不想通过 agent 上传？直接访问 DropFiles 网站，在浏览器中手动上传 HTML 或 Markdown 内容并获取分享链接，无需注册账号。

**网站地址**：<https://dropfiles.tokendealhub.com/>

### 功能特性

- 一键上传 HTML 或 Markdown 内容，获取公开链接
- 内置 `scripts/upload.py` 包装脚本——agent 和人类调用者都只需一条命令
- 自动识别内容类型（`html` / `markdown` / `auto`）
- 可配置过期时间：1 小时、1 天、7 天或 30 天
- 可选密码保护（用户自定义或自动生成 6 位数字密码）
- 可选文档标题，在分享页面显示
- 访问者无需账号即可查看公开链接
- HTML 内容在服务端进行净化处理（移除脚本）以确保安全
- Markdown 使用 GitHub 风格样式渲染（代码块、表格、图片）

### 安装

将整个技能目录（包含 `SKILL.md` 和 `scripts/`）复制到你的 agent 技能目录，或克隆本仓库：

```bash
git clone https://github.com/icexun/drop-files-skill.git
```

兼容任何支持 `SKILL.md` frontmatter 约定的 agent（TRAE、Claude、Cursor 等）。

### 使用方法

遇到以下场景时调用此技能：

- 通过公开链接分享生成的 HTML 或 Markdown 内容
- 发布文档、报告或页面，并获取可分发的 URL
- 上传任何基于文本的内容（HTML/Markdown）以便在线查看
- 为刚刚生成的内容生成可分享的预览链接

#### 包装脚本

**所有上传操作都使用 `scripts/upload.py`。不要手动构造 curl 命令或 JSON payload。**

脚本负责内容读取、JSON 序列化、临时文件管理、curl 调用（Cloudflare WAF 会拦截非 curl 的 HTTP 客户端）、响应解析以及临时文件清理。

运行 `python3 scripts/upload.py --help` 查看完整接口。

```
python3 scripts/upload.py [选项]

内容来源（优先级：--file > --content > stdin）：
  --file PATH          从文件读取内容
  --content TEXT       内联内容（长文本不推荐）
                       （两者均未提供时从 stdin 读取）

上传选项：
  --type TYPE          html | markdown | auto（默认 auto）
  --expire EXPIRE      1h | 1d | 7d | 30d（默认 7d）
  --title TITLE        分享页显示的可选标题
  --lang LANG          en | zh | auto（默认 auto）

密码（二选一）：
  --password PASSWORD  使用用户提供的密码
  --generate-password  生成随机 6 位数字密码

输出：
  --json               输出完整 JSON 响应（推荐 agent 使用）
  -h, --help           显示帮助信息并退出
```

#### 示例：上传 Markdown（stdin，JSON 输出）

```bash
echo '# Hello World

这是一篇分享的 Markdown 文档。' | python3 scripts/upload.py --type markdown --json
```

响应：

```json
{
  "success": true,
  "data": {
    "id": "abc123def456",
    "url": "https://dropfiles.tokendealhub.com/v/abc123def456",
    "preview_url": "https://dropfiles.tokendealhub.com/v/abc123def456?preview=1",
    "expire_at": "2026-08-05T10:30:00.000Z",
    "type": "markdown",
    "size": 42
  }
}
```

#### 示例：从文件上传，人类可读输出

```bash
python3 scripts/upload.py --file report.md --expire 1d --title "Q3 报告"
```

响应：

```
URL: https://dropfiles.tokendealhub.com/v/abc123
Preview: https://dropfiles.tokendealhub.com/v/abc123?preview=1
Expires: 2026-08-05T10:30:00Z
```

#### 示例：使用自动生成的 6 位数字密码上传

```bash
python3 scripts/upload.py --file secret.html --generate-password --json
```

响应包含生成的密码，方便转告给访问者：

```json
{
  "success": true,
  "data": { "...": "..." },
  "password": "482917"
}
```

### API 参考（仅作查阅——请使用包装脚本）

- **基础地址**：`https://dropfiles.tokendealhub.com`
- **上传**：`POST /api/v1/upload`
- **元数据**：`GET /api/v1/info/{id}`
- **预览**：`https://dropfiles.tokendealhub.com/v/{id}`

常见错误码：
- `CONTENT_REQUIRED` — `content` 字段为空。
- `CONTENT_TOO_LARGE` — 内容超过 5MB。
- `INVALID_TYPE` — `type` 不是 `html`、`markdown`、`auto` 之一。
- `INVALID_EXPIRE` — `expire` 不是 `1h`、`1d`、`7d`、`30d` 之一。
- `RATE_LIMIT_EXCEEDED` — 同一 IP 请求过于频繁。

### 密码策略

默认行为是**无密码**——拥有链接的任何人均可公开访问。

密码保护为可选功能，支持三种模式：

1. **无密码（默认）**：两个密码标志都不传。分享页面公开可读。
2. **用户自定义密码**：向上传脚本传递 `--password "你的密码"`。
3. **技能生成 6 位数字密码**：传递 `--generate-password`。脚本会生成一个随机的 6 位数字代码（例如 `"482917"`），放入上传请求，并在输出中回显。**务必把生成的密码转告给用户**，以便分享给预期的访问者。

### 限制

- 最大内容大小：**5 MB**（按 UTF-8 字节数计算）。
- 最长过期时间：**30 天**。
- 按 IP 进行限流；如果遇到 `RATE_LIMIT_EXCEEDED`，请等待后重试。

### 注意事项

- 分享链接是公开的（除非设置了密码保护）。拥有链接的任何人均可查看内容。
- 访问者无需账号。
- HTML 内容会被净化：`<script>` 标签和事件处理器会被移除。
- Markdown 支持标准 GitHub 风格的 Markdown，包括代码块、表格和图片。
- `preview_url` 添加了 `?preview=1` 参数，适用于在不应在首次加载时增加访问计数的上下文中嵌入链接。

### 许可证

MIT
