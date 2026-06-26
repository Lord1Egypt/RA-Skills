# FactoriaGo Skill — User Guide

> Version: v1.0 | Platform: OpenClaw | Updated: 2026-03-18

---

## 1. What is the FactoriaGo Skill?

This Skill enables your OpenClaw AI assistant to directly operate the [FactoriaGo](https://factoriago.com) platform, helping academic researchers complete the full paper revision and resubmission workflow, including:

- 📋 Analyzing reviewer comments and generating structured revision checklists
- ✉️ Writing point-by-point reviewer response letters
- 🤖 AI-assisted chat for revision discussions
- 📁 Managing projects, files, and revision tasks
- 🔧 LaTeX compilation and verification

---

## 2. Prerequisites

### 1. Create a FactoriaGo Account

Visit 👉 https://factoriago.com to register (free tier available)

### 2. Configure an AI Model API Key

> ⚠️ **All AI features (review analysis, chat, revision suggestions) require an API key to be configured first.**

FactoriaGo uses a BYOK model (Bring Your Own Key) — you provide your own API key from your preferred AI provider.

**Supported AI Providers:**

| Provider | Recommended Model | Best For | Get API Key |
|----------|------------------|----------|-------------|
| Anthropic | Claude Sonnet | English writing | https://console.anthropic.com/keys |
| OpenAI | GPT-4o | General purpose | https://platform.openai.com/api-keys |
| Google | Gemini 2.0 Flash | Speed | https://aistudio.google.com/app/apikey |
| Moonshot (Kimi) | kimi-k2 | Chinese papers | https://platform.moonshot.cn/console/api-keys |
| Zhipu (GLM) | GLM-4 Plus | Chinese papers | https://open.bigmodel.cn/usercenter/apikeys |
| MiniMax | MiniMax-Text | Chinese papers | https://platform.minimaxi.com/user-center/basic-information/interface-key |

**Two ways to configure:**

- **Web UI**: Log in at editor.factoriago.com → Profile icon (top right) → Settings → AI Model
- **Via AI assistant**: Tell your OpenClaw assistant your key and ask it to configure it for you

---

## 3. Core Features

### Feature 1: Reviewer Comment Analysis

**How to trigger:** Paste your reviewer comments and say "Analyze these reviewer comments"

**What the AI assistant does:**
1. Identifies each specific concern (auto-grouped by Reviewer 1 / Reviewer 2)
2. Classifies by importance: 🔴 Major / 🟡 Minor / 🟢 Optional
3. Suggests revision actions and priority order for each comment
4. Automatically calls `POST /api/paper/:id/analyze` to save the analysis to your project

**Example prompt:**
```
Please analyze these reviewer comments for my paper:
[paste full reviewer comments here]
```

---

### Feature 2: Reviewer Response Letter

**How to trigger:** "Write a reviewer response letter" / "Generate a point-by-point response"

**Three tone modes:**
- **Collaborative** (default): Grateful + explanatory + acknowledging
- **Assertive**: Politely maintaining your position
- **Technical**: Detail-focused, ideal for methodological concerns

**Example prompt:**
```
Write a reviewer response letter using collaborative tone.
Reviewer 1 said the sample size was insufficient — I have expanded it to 200 participants.
```

---

### Feature 3: AI Chat

**How to trigger:** "Ask AI in my FactoriaGo project..."

**What you can do:**
- Ask questions about your manuscript content
- Ask AI to help rewrite a specific paragraph
- Discuss revision strategy

**Example prompt:**
```
In my FactoriaGo project [project ID],
ask the AI: How can I improve the Related Work section?
```

---

### Feature 4: Project and File Management

| Action | Example Prompt |
|--------|---------------|
| List all projects | "List my FactoriaGo projects" |
| View project files | "Show the file list for project [ID]" |
| Create revision tasks | "Create revision tasks for project [ID]" |
| View revision tasks | "Show tasks for project [ID]" |
| Compile LaTeX | "Compile project [ID]" |

---

## 4. End-to-End Workflow (From Receiving Reviews to Resubmission)

```
① Receive journal reviewer comments
          ↓
② Tell the AI assistant: "Analyze these reviewer comments" + paste full text
          ↓
③ AI generates a structured checklist (Major / Minor / Optional categories)
          ↓
④ Say: "Create revision tasks in my FactoriaGo project [ID]"
          ↓
⑤ Edit LaTeX files at editor.factoriago.com
   (Ask AI anytime: "Help me rewrite paragraph 3")
          ↓
⑥ Say: "Write a reviewer response letter"
          ↓
⑦ Compile and verify ("Compile project [ID]")
          ↓
⑧ Download PDF + response letter, submit to journal
```

---

## 5. FAQ

**Q: AI features say "API key not configured" — what do I do?**

A: You need to configure an API key first. Tell the assistant which AI provider you want to use (Anthropic or OpenAI recommended), then share your key and ask it to configure it — or go directly to editor.factoriago.com → Settings → AI Model.

**Q: Where do I find my project ID?**

A: After logging into editor.factoriago.com, click on a project and look at the URL — the alphanumeric string is the project ID (e.g. `96efa8fe-83ee-4ff7-9552-0a6ac3847efd`). You can also ask the assistant "List my projects" and it will display all project IDs.

**Q: Do I need to install anything locally?**

A: No. FactoriaGo is fully browser-based — LaTeX compilation also runs in the cloud.

**Q: Is my API key secure?**

A: Keys are encrypted server-side and are never returned in plaintext. The API only returns a masked version (e.g. `••••••4wAA`).

**Q: What are the limitations of the free tier?**

A: The free tier has a limited AI usage quota (both AI Chat and review analysis consume quota). Paid plans include higher quotas and larger storage.

---

## 6. Support

- **Product website**: https://factoriago.com
- **Editor**: https://editor.factoriago.com
- **Feedback**: Contact the Factoria.AI team via the FactoriaGo website
