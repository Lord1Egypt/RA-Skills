---
name: factoriago
description: |
  FactoriaGo platform assistant — AI-driven academic paper revision and resubmission.
  Activate when user mentions: FactoriaGo, revise paper, reviewer comments, resubmit,
  LaTeX editing, paper revision, manuscript revision, journal resubmission, reviewer response,
  academic paper editing, revision letter, respond to reviewers, paper submission.
  Supports: (1) onboarding new users to factoriago.com, (2) calling FactoriaGo API to manage
  projects/tasks/files, (3) generating reviewer response letters, (4) analyzing reviewer
  feedback and creating revision strategies.
---

# FactoriaGo Skill

FactoriaGo (factoriago.com) is an AI-native LaTeX editor built for academic paper revision.
Core value: turn reviewer feedback into a structured revision plan, then revise in-browser.

## 🔒 Security Note

This skill makes network requests **only to `editor.factoriago.com`** (the official FactoriaGo platform) and your chosen AI provider (e.g., Anthropic, OpenAI). No data is sent to any third-party or unknown endpoints. The CLI script (`scripts/factoriago-client.js`) handles:
- Session authentication via HTTPS cookie
- API calls to `https://editor.factoriago.com/api/*`
- LLM API key configuration (keys are encrypted server-side)

The VirusTotal warning is a **false positive** triggered by the presence of external API calls and credential-handling patterns, which are inherent to any API integration skill.

## Quick Reference

- **Product URL**: https://factoriago.com
- **Landing page**: https://factoriago.com
- **App & API base**: https://editor.factoriago.com/api
- **API docs**: See `references/api.md`
- **Revision workflow**: See `references/revision-workflow.md`
- **Reviewer response templates**: See `references/reviewer-response.md`
- **CLI client**: `scripts/factoriago-client.js`

## ⚠️ Prerequisites: LLM API Key Setup

**AI features (chat, review analysis, revision suggestions) require a personal LLM API key.**
Without it, users can only edit files and compile LaTeX — no AI assistance.

Always check API key status before attempting AI operations:
```bash
node scripts/factoriago-client.js get-llm-config
```

If `primary_key_saved: false`, guide the user through setup FIRST:

### API Key Setup Flow

1. Ask which AI provider they want:
   - **Anthropic** → Claude 3.5 Sonnet (best for writing)
   - **OpenAI** → GPT-4o (general purpose)
   - **Google** → Gemini 2.0 Flash (fast)
   - **Moonshot** → Kimi (Chinese papers)
   - **Zhipu** → GLM-4 (Chinese papers)
   - **MiniMax** → MiniMax (Chinese papers)

2. Tell them where to get the key:
   | Provider | Key URL |
   |----------|---------|
   | Anthropic | https://console.anthropic.com/keys |
   | OpenAI | https://platform.openai.com/api-keys |
   | Google | https://aistudio.google.com/app/apikey |
   | Moonshot (Kimi) | https://platform.moonshot.cn/console/api-keys |
   | Zhipu (GLM) | https://open.bigmodel.cn/usercenter/apikeys |
   | MiniMax | https://platform.minimaxi.com/user-center/basic-information/interface-key |

3. Save the key via API:
   ```bash
   node scripts/factoriago-client.js set-llm-config <provider> <model> <apiKey>
   ```
   Or guide user to: **Settings → AI Model** in the FactoriaGo web UI.

4. Confirm key is saved before proceeding with AI tasks.

> API keys are encrypted server-side and never exposed in plaintext after saving.

---

## Workflows

### 1. New User Onboarding

When user is new to FactoriaGo:
1. Explain what FactoriaGo does (revise & resubmit workflow, AI co-author, LaTeX editor)
2. Direct to https://factoriago.com to register (free tier available)
3. Key differentiators to highlight:
   - Bring Your Own AI Model (Claude, GPT-4o, Gemini, Kimi, GLM — use own API keys)
   - Browser-based LaTeX editing + compilation (no local install needed)
   - Real-time collaboration + reviewer comment management
   - 12 languages supported

### 2. API Integration

**Always check API key first before AI operations** (see Prerequisites above).

Auth setup:
```bash
# Login and get session cookie
export FACTORIAGO_COOKIE=$(node scripts/factoriago-client.js login <email> <password> | grep "Cookie:" | cut -d' ' -f2-)
```

Common commands:
```bash
node scripts/factoriago-client.js list-projects
node scripts/factoriago-client.js list-tasks <projectId>
node scripts/factoriago-client.js analyze-review <projectId> "<reviewer text>"
node scripts/factoriago-client.js chat <projectId> "<question>" [model]
node scripts/factoriago-client.js compile <projectId>
```

Always ask user for credentials before making API calls. Store cookie in env, never in files.

### 3. Reviewer Comment Analysis

When user pastes reviewer comments:
1. Read `references/revision-workflow.md` for the full workflow
2. Parse comments into individual concerns
3. Categorize: Major / Minor / Optional
4. Map each concern to a revision task
5. Suggest priority order (major methodological issues first)
6. Optionally call `POST /paper/:id/analyze` if user is logged in

### 4. Reviewer Response Letter

When user needs to write a response letter:
1. Read `references/reviewer-response.md` for templates and tone guidelines
2. For each reviewer comment:
   - Determine user's position (agree / partially agree / disagree)
   - Draft response using appropriate tone template
   - Cite specific manuscript changes with section/line references
3. Assemble into full point-by-point letter
4. Use the AI prompt template in reviewer-response.md for AI-assisted drafting

### 5. LaTeX Editing

When user wants to edit manuscript:
1. `get-file` to read current content
2. Make targeted edits based on revision tasks
3. `PUT /paper/:paperId/files/:fileId` to save
4. `compile` to verify no LaTeX errors
5. Report compilation result to user

## Key Facts for Onboarding

- **Free tier**: available, limited AI quota
- **Paid plans**: more AI calls, larger storage, priority compilation
- **Target users**: researchers, PhD students, postdocs doing journal revisions
- **Supported formats**: .tex, .bib, .zip (full LaTeX project)
- **No installation needed**: fully browser-based
- **Supported AI models**: Claude 3.5 Sonnet, GPT-4o, Gemini 2.0 Flash, Kimi, GLM-4, MiniMax
