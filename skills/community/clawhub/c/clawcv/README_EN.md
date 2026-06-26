# WonderClaw ClawCV — WonderCV Resume AI Skills 🦞✨

[简体中文](./README.md) | [English](./README_EN.md)

> Bring resume analysis, rewriting, job matching, PDF export, and career advice directly into your AI conversations.

[![Platform: OpenClaw](https://img.shields.io/badge/Platform-OpenClaw-orange.svg)](https://github.com/WonderClaw/clawcv)
[![Platform: Claude_Code](https://img.shields.io/badge/Platform-Claude_Code-6b4fbb.svg)](https://anthropic.com/claude)
[![Version: v1.0.1](https://img.shields.io/badge/Version-v1.0.1-green.svg)](https://github.com/WonderClaw/clawcv)
[![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey.svg)](https://opensource.org/licenses/MIT)
[![Language: Node.js_18+](https://img.shields.io/badge/Node.js-18%2B-blue.svg)](https://nodejs.org/)

ClawCV is WonderCV's AI career assistant skill for AI environments such as OpenClaw, Claude Code, and Cursor that support MCP or local tool integration. Once configured, you can simply say "analyze my resume" and the AI will invoke the relevant capability automatically.

---

## 🚀 Capabilities

| Capability | Description | Example Trigger |
|------------|-------------|-----------------|
| **Resume Analysis** | Scores your resume across five dimensions and highlights prioritized issues and fixes | "Analyze this resume" / "What's wrong with my resume?" |
| **Section Rewrite** | Rewrites summary, work experience, project experience, skills, and education, returning 1-3 versions | "Rewrite my work experience" / "Improve this project section" |
| **Job Match** | Compares your resume against a JD and returns match score, strengths, gaps, and missing keywords | "Does my resume match this job?" |
| **One-Page PDF** | Organizes your content into a one-page delivery-ready PDF with four template styles | "Export PDF" / "Generate a one-page resume" |
| **AI Mentor** | Covers eight modules including assessment, optimization, job matching, interview prep, planning, salary negotiation, and multi-version strategy | "How should I prepare for interviews?" |
| **Account Linking** | Links your WonderCV account to unlock higher quotas and more complete features | "How do I upgrade?" / "Link my account" |

## 🧩 Skill Catalog

| Skill | Purpose | Entry |
|-------|---------|-------|
| `resume-analysis` | Diagnose overall resume quality and output scores, issues, and suggestions | [resume-analysis/SKILL.md](https://github.com/WonderClaw/clawcv/blob/main/resume-analysis/SKILL.md) |
| `resume-rewrite` | Rewrite summary, work experience, project experience, skills, and education | [resume-rewrite/SKILL.md](https://github.com/WonderClaw/clawcv/blob/main/resume-rewrite/SKILL.md) |
| `job-match` | Compare a resume against a JD and identify gaps and missing keywords | [job-match/SKILL.md](https://github.com/WonderClaw/clawcv/blob/main/job-match/SKILL.md) |
| `pdf-export` | Turn resume content into a one-page PDF | [pdf-export/SKILL.md](https://github.com/WonderClaw/clawcv/blob/main/pdf-export/SKILL.md) |
| `ai-mentor` | Provide interview prep, career planning, salary negotiation, and multi-version advice | [ai-mentor/SKILL.md](https://github.com/WonderClaw/clawcv/blob/main/ai-mentor/SKILL.md) |
| `account-upgrade` | Handle quota limits, account linking, upgrade flows, and PDF access issues | [account-upgrade/SKILL.md](https://github.com/WonderClaw/clawcv/blob/main/account-upgrade/SKILL.md) |

---

## 📦 Installation And Setup

### Step 1: Get an API key

Please go to [https://www.wondercv.com/clawcv](https://www.wondercv.com/clawcv) to obtain your ClawCV API Key.

> The type of your WonderCV account associated with the API Key will determine the available features and daily quota.


### Step 2: Install

Node.js 18+ is required.

#### OpenClaw

```bash
npx clawcv --api-key YOUR_API_KEY
```

#### Claude Code

```bash
claude mcp add clawcv -- npx clawcv --api-key YOUR_API_KEY
```

### Step 3: Add ClawCV to your AI tool

If you are configuring MCP manually, use the `npx` setup below. It does not require a global install.

**Claude Code** (`~/.claude/settings.json`):

```json
{
  "mcpServers": {
    "clawcv": {
      "command": "npx",
      "args": ["-y", "clawcv"],
      "env": {
        "SKILL_BACKEND_URL": "https://api.wondercv.com",
        "SKILL_BACKEND_API_KEY": "Your API Key"
      }
    }
  }
}
```

**Cursor** (Settings → MCP, or `~/.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "clawcv": {
      "command": "npx",
      "args": ["-y", "clawcv"],
      "env": {
        "SKILL_BACKEND_URL": "https://api.wondercv.com",
        "SKILL_BACKEND_API_KEY": "Your API Key"
      }
    }
  }
}
```

After saving the config, fully restart your AI tool. ClawCV will appear in the available tools list automatically.

### Step 4: Start using it

Describe your request in chat, and the AI will call ClawCV automatically:

```text
Analyze this resume for me
Rewrite my work experience for a product manager role
How well does this job description match my resume?
Turn this into a one-page PDF resume
Give me interview prep suggestions
```

---

## 🌟 Access And Quotas

| User Tier | Resume Analysis | Section Rewrite | Job Match | PDF Export | AI Mentor |
|-----------|-----------------|-----------------|-----------|------------|-----------|
| Standard User | 20/day | 20/day | 20/day | 10/day | Lite version |
| Member | 50/day | 50/day | 50/day | 50/day | Full version (8 modules) |
| Lifetime Member | 100/day | 100/day | 100/day | 100/day | Full version (8 modules) |

Quotas reset every day at 00:00 UTC. Say "link my account" in chat to start the account binding flow.

---

## 🤖 Typical Workflows

### Resume Optimization

```text
1. Analyze the resume     → Review overall score and high-priority issues
2. Rewrite key sections   → Improve content module by module
3. Export PDF             → Generate a one-page delivery-ready version
```

### JD-Based Tailoring

```text
1. Run job matching       → Identify gaps and missing keywords
2. Rewrite target areas   → Add the right keywords and outcomes
3. Export PDF             → Produce a version tailored for that role
```

### Career Coaching

```text
1. Analyze the resume     → Understand the current baseline
2. Ask AI mentor          → Get interview, salary, or planning advice
3. Apply the advice       → Turn suggestions into resume edits
```

---

## 🦞 Environment Requirements

| Environment | Support |
|-------------|---------|
| OpenClaw | ✅ Supported |
| Claude Code | ✅ Supported |
| Cursor (MCP) | ✅ Supported |
| Other MCP-compatible AI tools | ✅ Expected to work |

**Runtime requirements:**

- Node.js 18+
- A valid `SKILL_BACKEND_API_KEY`
- Network access to `https://api.wondercv.com`

---

## ❓ FAQ

**Q: Do I need to set `SKILL_BACKEND_API_KEY`?**

Yes. Please go to [https://www.wondercv.com/clawcv](https://www.wondercv.com/clawcv) to obtain your ClawCV API Key.

**Q: ClawCV is installed, but the AI does not call it automatically. What should I check?**

Verify that the MCP config is valid, then fully restart the AI tool. You can also say "use ClawCV to analyze my resume" to trigger it explicitly.

**Q: Why is the PDF export quota lower?**

Standard users get 10 PDF exports per day. Members and lifetime members get 50-100 per day. Say "I want to upgrade" in chat to view upgrade options.

**Q: What is `session_id`? Do I need to manage it myself?**

No. The AI maintains `session_id` automatically. It is used to track quotas and conversation history, and it expires after 24 hours.


**Q: Why do I only get one rewrite version back?**

Standard users receive one rewrite version per request. Members and lifetime members can receive up to three versions.

**Q: Is my resume content stored?**

Conversation data, including quota usage, is persisted in the WonderCV backend to support cross-device usage. Resume text is not stored long-term after processing.

**Q: Does ClawCV support English resumes?**

Yes. ClawCV responds in the user's language by default, and you can paste English resumes directly.

**Q: Do I need to set `SKILL_BACKEND_URL`?**

No. It defaults to `https://api.wondercv.com`. You only need to override it for private deployments or debugging.

---

## 🔗 Links

- [WonderCV Website](https://wondercv.com) — Online resume builder
- [Get an account / upgrade membership](https://wondercv.com/clawcv)
- [Main skill entry](./SKILL.md)

---

## License

MIT
