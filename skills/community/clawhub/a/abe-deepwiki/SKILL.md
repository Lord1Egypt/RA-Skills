---
name: deepwiki
description: Query GitHub repository documentation, wiki structure, and ask AI-powered questions via SkillBoss API Hub.
homepage: https://docs.devin.ai/work-with-devin/deepwiki-mcp
requires_env: [SKILLBOSS_API_KEY]
---

# DeepWiki

Use this skill to access documentation for public GitHub repositories via SkillBoss API Hub. You can retrieve repository wiki pages, get structure, and ask complex questions grounded in the repository's documentation. All requests are routed through SkillBoss API Hub using a single API key.

## Commands

### Ask Question
Ask any question about a GitHub repository and get an AI-powered, context-grounded response.
```bash
node ./scripts/deepwiki.js ask <owner/repo> "your question"
```

### Read Wiki Structure
Get a list of documentation topics for a GitHub repository.
```bash
node ./scripts/deepwiki.js structure <owner/repo>
```

### Read Wiki Contents
View documentation about a specific path in a GitHub repository's wiki.
```bash
node ./scripts/deepwiki.js contents <owner/repo> <path>
```

## Examples

**Ask about Devin's MCP usage:**
```bash
node ./scripts/deepwiki.js ask cognitionlabs/devin "How do I use MCP?"
```

**Get the structure for the React docs:**
```bash
node ./scripts/deepwiki.js structure facebook/react
```

## Setup

Set the following environment variable before running:

```bash
export SKILLBOSS_API_KEY=your_skillboss_api_key
```

## Notes
- Powered by SkillBoss API Hub (`https://api.heybossai.com/v1/pilot`).
- Web scraping fetches content from `https://deepwiki.com/<owner>/<repo>`.
- Works for public repositories only.
- The `ask` command uses SkillBoss API Hub's web scraping + LLM chat for AI-powered answers.
