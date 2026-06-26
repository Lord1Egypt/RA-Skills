# Auth and CLI Matrix

## Auth by Surface

| Surface | Typical auth | Notes |
|--------|---------------|-------|
| Jira, Confluence, GraphQL | API token + email, OAuth 2.0, or Forge auth | Good default for tenant automation |
| Bitbucket | Access token, app password, or OAuth 2.0 | Different host and scopes from Jira/Confluence |
| Trello | Key + token | Usually passed as query params |
| Cloud Admin | Admin API key | Org-wide and higher risk |
| Compass | API token, OAuth 2.0, or Forge | Often combined with GraphQL |
| Statuspage | API token in `Authorization: OAuth ...` | Page-scoped workflows |
| Opsgenie | API key | Region-specific base URL |

## Official Atlassian CLI: `acli`

Current official command tree includes:
- `acli admin`
- `acli jira`
- `acli rovodev`

Install on macOS:
```bash
brew tap atlassian/homebrew-acli
brew install acli
acli --version
```

Alternative binary install:
```bash
curl -LO "https://acli.atlassian.com/darwin/latest/acli_darwin_arm64/acli"
chmod +x ./acli
./acli --help
```

Jira auth with API token:
```bash
acli jira auth login --web
```

Admin auth with API key:
```bash
acli admin auth login --email "<email>" --token < admin-api-key.txt
```

Useful official examples:
```bash
acli jira workitem view KEY-123 --fields summary,comment
acli jira workitem create --summary "New Task" --project "TEAM" --type "Task"
acli admin user activate --email "user@example.com"
```

Important limitation:
- Official docs currently expose Jira, Admin, and Rovo Dev command groups only.
- Treat missing Confluence, Bitbucket, Trello, Statuspage, and Opsgenie CLI support as API-first territory.

## Official Atlassian CLI: `forge`

Use `forge` for building and deploying Forge apps, especially for Jira, Confluence, and Compass extensions.

Install and login:
```bash
npm i -g @forge/cli@latest
forge login
```

Common flow:
```bash
forge create
forge deploy
forge install
forge tunnel
```

## Partner CLI Family

If the user explicitly wants a non-first-party CLI, Appfire ACLI is the broadest documented partner family. Marketplace and partner docs cover Jira, Confluence, Bitbucket, Bamboo, and related products, but treat it as a separate trust boundary because it is vendor software rather than an Atlassian first-party CLI.

## Official Docs

- Atlassian CLI commands: https://developer.atlassian.com/cloud/acli/reference/commands/
- Atlassian CLI getting started: https://developer.atlassian.com/cloud/acli/guides/how-to-get-started/
- Atlassian CLI install: https://developer.atlassian.com/cloud/acli/guides/install-macos/
- Forge CLI: https://developer.atlassian.com/platform/forge/cli-reference/
