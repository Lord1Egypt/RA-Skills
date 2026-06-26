---
name: exa
description: "Manage Exa AI via CLI - search, contents, answer, context. Use when user mentions 'exa', 'web search', 'find similar pages', 'ai answer', or wants to interact with the Exa API."
category: web-search
---

# exa-cli

## Setup

If `exa-cli` is not installed, install it from GitHub:
```bash
npx api2cli install Melvynx/exa-cli
```

If `exa-cli` is not found, install and build it:
```bash
bun --version || curl -fsSL https://bun.sh/install | bash
npx api2cli bundle exa
npx api2cli link exa
```

`api2cli link` adds `~/.local/bin` to PATH automatically. The CLI is available in the next command.

Always use `--json` flag when calling commands programmatically.

## Authentication

```bash
exa-cli auth set "your-token"
exa-cli auth test
```

## Resources

### search

| Command | Description |
|---------|-------------|
| `exa-cli search query --query "latest AI research" --json` | Search web with natural language query |
| `exa-cli search query --query "best React frameworks" --type neural --num-results 5 --json` | Neural search with custom result count |
| `exa-cli search query --query "SpaceX news" --type keyword --json` | Keyword-based search |
| `exa-cli search query --query "AI trends" --start-date 2024-01-01 --json` | Search with date filter |
| `exa-cli search query --query "research" --category news --json` | Search by category |
| `exa-cli search query --query "frameworks" --include-domains github.com,stackoverflow.com --json` | Include specific domains |
| `exa-cli search query --query "news" --exclude-domains twitter.com --json` | Exclude specific domains |
| `exa-cli search query --query "topic" --text --json` | Include page text in results |
| `exa-cli search query --query "topic" --summary --json` | Include AI summary for each result |
| `exa-cli search query --query "topic" --highlights --json` | Include text highlights |
| `exa-cli search find-similar --url "https://example.com" --json` | Find similar pages to URL |
| `exa-cli search find-similar --url "https://example.com" --num-results 5 --text --json` | Find similar with text content |

### contents

| Command | Description |
|---------|-------------|
| `exa-cli contents get --urls "https://example.com" --json` | Get page contents for URL |
| `exa-cli contents get --urls "https://a.com,https://b.com" --json` | Get contents for multiple URLs |
| `exa-cli contents get --urls "https://example.com" --text --json` | Get contents with full page text |
| `exa-cli contents get --urls "https://example.com" --summary --json` | Get contents with AI summary |
| `exa-cli contents get --urls "https://example.com" --highlights --json` | Get contents with text highlights |

### answer

| Command | Description |
|---------|-------------|
| `exa-cli answer query --query "What is the latest valuation of SpaceX?" --json` | Get AI answer with web citations |
| `exa-cli answer query --query "Who won the 2024 election?" --text --json` | Answer with source text included |
| `exa-cli answer query --query "Explain quantum computing" --stream --json` | Stream answer response |

### context

| Command | Description |
|---------|-------------|
| `exa-cli context get --query "how to use React hooks" --json` | Get web context for query |
| `exa-cli context get --query "Python async await patterns" --tokens-num 8000 --json` | Get context with token limit |

## Global Flags

All commands support: `--json`, `--format <text|json|csv|yaml>`, `--verbose`, `--no-color`, `--no-header`
