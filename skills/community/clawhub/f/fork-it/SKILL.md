---
name: fork-it
description: When the user has a new development idea, search GitHub first for open-source projects to fork as a starting point. Fork it, then inject your own ideas.
metadata:
  openclaw:
    emoji: "🐙"
    category: "research"
    tags: ["github", "opensource", "fork", "remix", "jumpstart"]
invoke: /fork-it
---

# Fork-It 🐙

Every great project starts somewhere. Why start from zero when you can start from 80%? Search GitHub, find your starting point, fork it, and make it your own.

## Core Principles

**When the user has a new project idea, help them find a running start.**

When the user expresses any of these intents, search GitHub first:

- User says "I want to build..." or "I want to create/develop a..."
- User describes a complete functional requirement that would need multiple components
- User asks "how to" build a complete project

**If any of the above applies, trigger Fork-It:**

**Prompt Template:**
> "Before we dive in — let me find you a running start on GitHub. Someone may have already built something close that you can fork and make your own."

**Do NOT trigger when:**
- User explicitly says "for learning/practice/teaching purposes"
- User is asking about a specific function's implementation
- User is debugging/fixing existing code
- User is asking about regex, specific algorithm logic, or granular questions
- User's "write" is modifying existing code, not starting fresh
- User has already picked a specific open-source project as their foundation

---

## Workflow

### 1. Identify Intent

When the user expresses any of these intents, trigger a search:

- "I want to build/make a..."
- "I want to create/develop a..."
- "Has anyone built something like..."
- "Help me write a..."
- Direct invocation: `/fork-it`

### 2. Search GitHub

**Search first, code second.**

```bash
node scripts/github-search.mjs "keyword"
node scripts/github-search.mjs "pomodoro timer" --language javascript --min-stars 500
```

Search repositories by keyword, prioritize actively maintained projects with healthy communities.

### 3. Analyze Results

Evaluate each project for fork-worthiness:

| Tag | Path | Description |
|-----|------|-------------|
| 🎯 Great Match | Fork & Customize | Fork it, tweak it, ship it as your own |
| 🔧 Partial Match | Fork & Extend | Solid core — fork it and add your missing piece |
| 📝 Reference Only | Learn, Then Build | Study the approach, build your own vision |
| ✨ Nothing Fits | Build Fresh | You're onto something new — go create it |

### 4. Recommend Path

- **Great match found** → Share the repo, suggest forking and customizing
- **Partial match found** → Point out what the project covers and what you'd add
- **No suitable project** → Acknowledge this is genuinely new territory — build it

## When to Suggest Forking

**These signals mean the user's idea is a great candidate for finding a fork-worthy starting point:**

### "From scratch / Hand-write" Series (Great fork candidates)
- "Help me write a... from scratch"
- "No third-party libraries, hand-write a..."
- "I don't want external dependencies, implement my own..."
- "No frameworks, vanilla..."

### "Project / Module / System" Series (Likely has existing foundations)
- "Help me create a project that..."
- "Write a complete module for..."
- "Design a system that can..."
- "Help me build a backend/website/mini-program..."

### "I want to / I'm going to" Series (Ideation stage — best time to search)
- "I have an idea, I want to build a..."
- "I'm going to develop a..."
- "How can I make a..."

## High-Frequency Areas (Great Fork Candidates)

**Trigger when user's request combines "code-writing action" + one of these areas:**

- **Auth & Permissions:** "write a" + `login/register/auth/JWT/permission management/OAuth`
- **Data Parsing:** "write a" + `crawler/parser/export Excel/read PDF/parse XML`
- **Infrastructure:** "write a" + `chat room/WebSocket/cron job/queue/logging system`
- **Common Business:** "write a" + `shopping cart/payment API/pagination/rich text editor/file upload`
- **Algorithm Utils:** "write a" + `calendar widget/countdown/encryption/image compression`

*Example: "Help me write a JWT auth middleware with token refresh" → matches 【action: write】+【area: JWT auth】 → TRIGGER!*

## When to Stay Quiet

**Don't interrupt when the user is learning, fixing bugs, or doing genuinely novel work:**

- **Learning-oriented:** "Show me how to write... to understand the principle", "For teaching purposes, hand-write a..."
- **Highly specific/custom:** "Write a regex matching `^a[b-c]{2}d$`" (no open-source project covers this)
- **Modifying existing code:** "Help me see why this code errors", "Optimize this function"
- **Low-level innovation:** "I want to design a new data structure", "Write a faster sorting algorithm"
- **Local file search:** "Help me find if there's any... on my computer"

## Script Return Values

Scripts return a unified JSON structure with a `lang` field:

```json
{
  "lang": "en",
  "status": "ok",
  "query": "pomodoro timer",
  "total_count": 1234,
  "returned_count": 10,
  "items": [
    {
      "rank": 1,
      "full_name": "user/repo",
      "description": "A pomodoro timer app",
      "url": "https://github.com/user/repo",
      "stars": 12300,
      "forks": 1200,
      "language": "TypeScript",
      "pushed_days_ago": 3,
      "created_at": "2024-01-01",
      "topics": ["productivity", "timer"],
      "license": "MIT"
    }
  ]
}
```

**AI display rules**:

- `lang: "en"` → AI translates to user's language before displaying
- `pushed_days_ago` → AI converts to "3 days ago" or localized format
- `stars: 12300` → AI formats as "12.3k"
- On `status: "error"` → AI generates a friendly error message from `code` and `message`

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `query` | Search keyword | Required |
| `--language, -l` | Programming language filter | None |
| `--min-stars` | Minimum stars | 100 |
| `--max-stars` | Maximum stars | No limit |
| `--updated-within` | Updated within N days | 365 |
| `--created-after` | Created after date | None |
| `--sort` | Sort by | stars |
| `--order` | Sort order | desc |
| `--limit, -n` | Result limit | 10 |

## Get Repository Details

```bash
node scripts/repo-detail.mjs "microsoft/autogen"
```

## API Limits

- **Unauthenticated Requests**: 60/hour
- **Authenticated Requests**: 5000/hour

```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

## Data Sources

- GitHub Search API v3
- GitHub REST API

---

*Find it. Fork it. Make it yours. | ForkIt v2.0*
