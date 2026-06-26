# azure-devops — OpenClaw Skill

> Interact with Azure DevOps from OpenClaw. No MCP required — pure REST API via Node.js built-ins.

## What it does

- 📁 **Projects & Teams** — list projects, teams, and sprint iterations
- 🗂️ **Work Items** — list, get, create, update, query via WIQL, view current sprint
- 🔀 **Repos & PRs** — list repos, get repo details, browse pull requests
- 🚀 **Pipelines & Builds** — list pipelines, view runs, inspect builds
- 📖 **Wikis** — list wikis, read and write pages
- 🧪 **Test Plans** — list test plans and suites

## Requirements

- Node.js 18+
- An Azure DevOps organization
- A Personal Access Token (PAT)

## Setup

### 1. Create a PAT

Go to `https://dev.azure.com/<your-org>/_usersSettings/tokens` and create a token with these scopes:

- Work Items: Read & Write
- Code: Read
- Build: Read
- Release: Read
- Test Management: Read
- Wiki: Read & Write
- Project and Team: Read

### 2. Configure environment

```bash
export AZURE_DEVOPS_ORG=contoso
export AZURE_DEVOPS_PAT=your_pat_here
```

Or via `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "entries": {
      "azure-devops": {
        "enabled": true,
        "env": {
          "AZURE_DEVOPS_ORG": "contoso",
          "AZURE_DEVOPS_PAT": "your_pat_here"
        }
      }
    }
  }
}
```

### 3. Install

```bash
clawhub install azure-devops
```

Or manually:

```bash
cp -r azure-devops/ ~/.openclaw/skills/
```

No `npm install` needed — all scripts use Node.js built-in `https`.

## Usage Examples

```
List my ADO projects
Show work items in the Contoso project
Get current sprint for team "Backend" in project "Contoso"
Create a bug titled "Login page 500 error" in project "Contoso"
List repos in the Contoso project
Show open pull requests in repo "backend-api"
List pipelines in project "Contoso"
Get the wiki page /Architecture/Overview from the Contoso wiki
```

## Script Reference

| Script | Commands |
|---|---|
| `scripts/projects.js` | `list`, `get <project>` |
| `scripts/teams.js` | `list <project>`, `iterations <project> <team>` |
| `scripts/workitems.js` | `list`, `get`, `current-sprint`, `create`, `update`, `query` |
| `scripts/repos.js` | `list`, `get`, `prs`, `pr-detail` |
| `scripts/pipelines.js` | `list`, `runs` |
| `scripts/builds.js` | `list`, `get` |
| `scripts/wiki.js` | `list`, `get-page`, `create-page`, `update-page` |
| `scripts/testplans.js` | `list`, `suites` |

## Security

- All scripts use Node.js built-in `https` — no third-party dependencies
- Input is validated and sanitized before use in URLs
- Credentials are passed as HTTP headers to `dev.azure.com` only
- Security manifest is documented at the top of every script

## License

MIT
