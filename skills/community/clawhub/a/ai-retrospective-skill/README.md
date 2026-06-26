[中文版](README.zh-CN.md) | **English**

# AI Retrospective Skill

A tool-agnostic post-session analysis framework for AI-assisted coding. Works with any AI coding assistant that has conversation context access.

After each AI-assisted development session, trigger a systematic review across **eight dimensions** to identify improvement opportunities and generate a structured retrospective report.

**Core goal: Make every AI coding session better than the last.**

## Why This Exists

Most developers use AI assistants reactively — they code, hit problems, move on. They rarely stop to ask: *"Could this session have gone better? What patterns keep wasting our time?"*

This skill turns that reflection into a structured, repeatable process. It analyzes the conversation between you and your AI assistant, finds concrete waste points, quantifies the impact, and produces actionable recommendations.

## The Eight Dimensions

| # | Dimension | What It Examines |
|---|-----------|-----------------|
| 1 | **AI Self-Reflection** | AI's mistakes, delayed reactions, missed judgments (analyzed first — highest priority) |
| 2 | **Verification Strategy** | Whether AI proactively defined verification criteria or passively waited for feedback |
| 3 | **Automation Opportunities** | Repetitive workflows that could be encapsulated into reusable automations |
| 4 | **Existing Automation Tuning** | Gaps in automations/skills/rules that were active during the session |
| 5 | **Tool Integration Opportunities** | Operations that need dedicated tools, plugins, or API connections |
| 6 | **Knowledge Persistence** | Preferences, conventions, and decisions worth persisting for future sessions |
| 7 | **Documentation Updates** | Project docs, standards, or architecture notes needing updates |
| 8 | **Workflow Efficiency** | Sequential steps that could be parallel, repeated labor, suboptimal tool choices |

## Supported AI Tools

This skill is designed to work with any AI coding assistant. It has been tested with:

| Tool | How to Install |
|------|---------------|
| **WorkBuddy** | Copy to `.workbuddy/skills/ai-retrospective/` |
| **Cursor** | Copy SKILL.md content to `.cursor/rules/` or reference in project instructions |
| **Claude Code** | Append to `CLAUDE.md` or use as a slash command reference |
| **GitHub Copilot** | Reference in `.github/copilot-instructions.md` |
| **Windsurf** | Reference in `.windsurfrules` or Cascade workflow |
| **Cline** | Reference in `.clinerules` or custom instructions |

The skill degrades gracefully — if your tool lacks certain capabilities (e.g., no file writing, no memory persistence), the analysis steps still work; only the output/persistence steps adapt.

## Quick Start

### 1. Install

```bash
# Clone into your project (or globally)
git clone https://github.com/AmosHC/ai-retrospective-skill.git

# Or just copy the files
cp -r ai-retrospective-skill/ your-project/.ai-retrospective/
```

### 2. Trigger

At the end of any AI-assisted coding session, say one of:
- "retrospective" / "retro"
- "review this session"

### 3. Get Your Report

The skill will:
1. Scan your conversation history and build an event timeline
2. Tag waste points (avoidable steps, delayed actions, duplicated work)
3. Analyze across all eight dimensions with specific event references
4. Generate a full report in the conversation AND save to file
5. Auto-persist knowledge items (if your tool supports it)
6. List pending actions for your confirmation

## Directory Structure

```
ai-retrospective-skill/
├── SKILL.md                              # Core skill definition and workflow
├── references/
│   └── analysis_dimensions.md            # Detailed criteria for all 8 dimensions
├── assets/
│   └── report_template.md                # Markdown template for reports
├── README.md                             # English documentation
├── README.zh-CN.md                       # Chinese documentation
└── LICENSE                               # MIT License
```

## How It Works

The skill is **pure LLM instruction-driven** — no scripts, no external dependencies, no API keys. It works entirely through structured prompts that guide the AI assistant through the analysis workflow.

The key insight: your AI assistant already has the complete conversation history in context. This skill simply provides a systematic framework for the AI to analyze that history and extract actionable insights.

### Workflow Overview

```
Session ends → Trigger word → Step 1: Extract events & tag waste
→ Step 2: Eight-dimension analysis → Step 3: Generate report file
→ Step 4: Display full analysis in chat → Step 5: Auto-persist knowledge
→ Step 6: List pending actions for confirmation
```

## Adaptation Guide

### For tool-specific installation

Each AI tool has its own convention for custom instructions. The core content lives in `SKILL.md` and `references/analysis_dimensions.md`. Adapt the packaging:

- **WorkBuddy**: Use as-is — the directory structure matches the Skills format
- **Cursor**: Create a `.cursor/rules/retrospective.md` combining SKILL.md + key parts of analysis_dimensions.md
- **Claude Code**: Append a "Retrospective" section to your `CLAUDE.md` with the workflow and dimension summaries
- **Other tools**: Wherever your tool reads custom instructions, include the SKILL.md content

### Customizing dimensions

The eight dimensions are designed to be comprehensive but not exhaustive. You can:
- Add domain-specific dimensions (e.g., "Security Review" for security-critical projects)
- Adjust priority weights for dimensions most relevant to your workflow
- Add new patterns to the self-check lists based on your experience

### Customizing the report

Edit `assets/report_template.md` to match your team's conventions. The template uses placeholder variables that the AI fills during report generation.

## Contributing

Issues and PRs are welcome. Some areas where contributions would be especially valuable:

- **New dimensions**: Domain-specific analysis dimensions with self-check lists
- **Pattern libraries**: Common waste patterns for specific languages/frameworks
- **Tool adapters**: Pre-built configurations for additional AI tools
- **Translations**: Localized versions of the analysis dimensions

## License

MIT — see [LICENSE](LICENSE) for details.
