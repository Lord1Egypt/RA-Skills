---
name: easy-english-tool
description: Zero-dependency embedded MCP server for English learning — 22 tools covering vocab, articles, quizzes, copy practice, TTS, and pronunciation eval, all served directly from the Express process with no separate MCP instance. Dual transport (SSE + Streamable HTTP). Production-ready at https://english.geeyo.com. REST fallback included for agents without MCP config. 英语进阶营 MCP 服务：零依赖、嵌入式，22 个工具覆盖单词本、文章、测验、抄写、TTS 朗读、跟读评测全流程。触发词：英语学习, 单词本, 打卡, 测验, 生词, study English, my vocab, my progress.
metadata:
  origin: project
  mcp: easy-english-tool
  server_url: https://english.geeyo.com
---

# Easy English Tool (英语进阶营)

This skill gives you access to the user's personal English learning data and actions. The backend is an Express server serving both REST APIs and MCP endpoints on the same port — no separate MCP process needed.

## Quick check: is MCP configured?

Before using this skill, check your available tools. If you see any tool named `account_login`, `get_profile`, `get_today`, `vocab_add`, etc. — the MCP server is configured. Jump to **Path A**. If none of these tools exist, use **Path B** (REST fallback).

---

## Path A: MCP is configured (preferred)

The MCP server is named `easy-english-tool` and exposes **22 tools** on `https://english.geeyo.com`. The MCP endpoints are served in-process by the Express backend — no separate MCP process needed.

### Authentication flow

1. The user sets a username/password on the web "My" page (`POST /api/users/bind`).
2. Call `account_login` with those credentials. The MCP session caches `userId`, and all subsequent tools automatically use it.
3. If the user has no account yet, guide them to the web page first, then come back.

### Tool reference

#### Account
| Tool | Params | Description |
|------|--------|-------------|
| `account_login` | `username`, `password` | Login to cache userId for the session |
| `account_whoami` | (none) | Returns cached {userId, username} or {userId: null} |

#### Profile & Learning
| Tool | Params | Description |
|------|--------|-------------|
| `get_profile` | (none) | Learning profile: level, streak, total points, vocab count, accuracy, nickname |
| `get_today` | (none) | Today's recommended article + pending review vocab count. Returns `needLevel:true` if level not set. |
| `get_history` | (none) | Study history (check-ins, quizzes, learning tracks) |
| `level_set` | `level` | Set English level, e.g. "七年级上", "高一必修一" |
| `levels_list` | (none) | List all 12 available levels in order |
| `diagnose` | (none) | Diagnostic entry: ensures user record exists |

#### Vocabulary
| Tool | Params | Description |
|------|--------|-------------|
| `vocab_add` | `word`, `chinese`, `context?` | Add a word to personal vocab list |
| `vocab_list` | (none) | List all saved vocabulary |
| `vocab_review` | `id` | Mark a vocab word as reviewed |

#### Articles
| Tool | Params | Description |
|------|--------|-------------|
| `articles_create` | `title`, `content` | Create a custom study article |
| `articles_list` | (none) | List user's custom articles |
| `articles_get` | `id` | Get article details by id |
| `articles_delete` | `id` | Delete an article by id |

#### Study Actions
| Tool | Params | Description |
|------|--------|-------------|
| `quiz_submit` | `correctCount`, `totalCount`, `points?`, `articleId?` | Submit quiz results, auto-updates points and streak |
| `copy_load` | `articleId`, `source?` | Load copy-writing record (count + draft) |
| `copy_submit` | `articleId`, `source?` | Submit a copy, count+1, auto-adds points (max 5/day) |
| `copy_stash` | `articleId`, `draft`, `source?` | Save a copy draft without incrementing count |
| `evaluate` | `text`, `articleId?` | Pronunciation evaluation (stub; ISE coming in next phase) |

#### Media
| Tool | Params | Description |
|------|--------|-------------|
| `tts` | `text`, `speed?` (slow/normal/fast) | Text-to-speech, returns MP3 URL |
| `checkin_poster` | (none) | Generate check-in poster QR code (PNG) |

---

## Path B: MCP is NOT configured (REST fallback)

If the MCP server is not registered in your agent config, call the REST API directly at `https://english.geeyo.com`.

### Configuring MCP (recommended)

To add the MCP server permanently, add this to your agent's MCP config:

```json
{
  "mcpServers": {
    "easy-english-tool": {
      "type": "streamableHttp",
      "url": "https://english.geeyo.com/api/mcp/http"
    }
  }
}
```

Or for SSE-based clients:

```json
{
  "mcpServers": {
    "easy-english-tool": {
      "type": "sse",
      "url": "https://english.geeyo.com/api/mcp/sse"
    }
  }
}
```

After adding, restart the agent and return to **Path A**.

### REST API fallback mapping

All endpoints share the same base: `https://english.geeyo.com`. Anonymous auth: include header `x-user-id: <userId>`. Get a userId by calling `POST /api/users/ensure`.

| MCP Tool | REST Equivalent |
|----------|----------------|
| `account_login` | `POST /api/users/login` `{username, password}` |
| `get_profile` | `GET /api/profile` |
| `get_today` | `GET /api/today` |
| `vocab_add` | `POST /api/vocab` `{word, chinese, context?}` |
| `vocab_list` | `GET /api/vocab` |
| `vocab_review` | `POST /api/vocab/review` `{id}` |
| `articles_create` | `POST /api/user-articles` `{title, content}` |
| `articles_list` | `GET /api/user-articles` |
| `articles_get` | `GET /api/user-articles/:id` |
| `articles_delete` | `DELETE /api/user-articles/:id` |
| `tts` | `POST /api/tts` `{text, speed?}` |
| `checkin_poster` | `GET /api/checkin/poster` → PNG binary |
| `get_history` | `GET /api/history` |
| `quiz_submit` | `POST /api/quiz` `{correctCount, totalCount, points?, articleId?}` |
| `level_set` | `POST /api/level` `{level}` |
| `levels_list` | `GET /api/levels` |
| `diagnose` | `POST /api/diagnose` `{}` |
| `copy_load` | `POST /api/copy` `{articleId, source?, action:"load"}` |
| `copy_submit` | `POST /api/copy` `{articleId, source?, action:"submit"}` |
| `copy_stash` | `POST /api/copy` `{articleId, draft, source?, action:"stash"}` |
| `evaluate` | `POST /api/evaluate` `{text, articleId?}` |

### Server lifecycle

- **Production**: `https://english.geeyo.com`
- **Local dev**: `cd C:\projects\Node.js\H5\server && npm run dev` (listens on `:3001`)
- **Health check**: `GET https://english.geeyo.com/api/health` → `{"ok":true}`
- **Zero extra deps**: MCP runs in-process with Express, no `@modelcontextprotocol/sdk` needed.

### Common workflows

**First-time setup for a user:**
1. Call `POST /api/users/ensure` with `x-user-id: <uuid>` → get userId
2. Call `POST /api/diagnose` → ensure user record
3. Call `GET /api/levels` → pick a level
4. Call `POST /api/level` `{level}` → set level
5. Optionally call `POST /api/users/bind` `{username, password}` → bind account for cross-device

**Daily study session:**
1. `GET /api/today` → get today's article
2. `GET /api/vocab` → review vocabulary
3. `POST /api/tts` → listen to article
4. `POST /api/copy` `{action:"submit"}` or `{action:"load"}` → practice writing
5. `POST /api/quiz` → submit quiz
6. `GET /api/checkin/poster` → generate sharing poster
7. `GET /api/profile` → check updated stats
