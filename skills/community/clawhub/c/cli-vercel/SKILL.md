---
name: vercel
description: "Deploy and manage Vercel projects via CLI - deploy, env, domains, logs, teams. Use when user mentions 'vercel', 'deploy', 'vercel project', or wants to interact with Vercel."
category: devtools
install_command: "npm i -g vercel"
---

# vercel

## Setup

```bash
npm i -g vercel
```

Verify installation:
```bash
vercel --version
```

Always use `--json` flag when calling commands programmatically.

## Authentication

```bash
vercel login
```

## Resources

### Deploy

| Command | Description |
|---------|-------------|
| `vercel` | Deploy current project to preview |
| `vercel --prod` | Deploy current project to production |
| `vercel deploy --prod` | Deploy to production (explicit) |
| `vercel ls` | List all deployments |
| `vercel inspect <url>` | Show details of a deployment |
| `vercel promote <url>` | Promote a deployment to production |
| `vercel rollback` | Rollback to previous deployment |
| `vercel redeploy <url>` | Redeploy an existing deployment |

### Environment Variables

| Command | Description |
|---------|-------------|
| `vercel env ls` | List all environment variables |
| `vercel env add <name>` | Add a new environment variable |
| `vercel env rm <name>` | Remove an environment variable |
| `vercel env pull .env.local` | Pull env vars to a local file |

### Domains

| Command | Description |
|---------|-------------|
| `vercel domains ls` | List all domains |
| `vercel domains add <domain>` | Add a domain |
| `vercel domains rm <domain>` | Remove a domain |
| `vercel domains inspect <domain>` | Show domain details and DNS records |

### Projects

| Command | Description |
|---------|-------------|
| `vercel project ls` | List all projects |
| `vercel project add <name>` | Create a new project |
| `vercel project rm <name>` | Remove a project |
| `vercel link` | Link current directory to a project |

### Logs

| Command | Description |
|---------|-------------|
| `vercel logs <url>` | View realtime logs for a deployment |
| `vercel logs <url> --follow` | Stream logs in realtime |

### Teams

| Command | Description |
|---------|-------------|
| `vercel teams ls` | List all teams |
| `vercel teams switch` | Switch to a different team |

### Local Development

| Command | Description |
|---------|-------------|
| `vercel dev` | Start local development server |
| `vercel build` | Build project locally |

## Global Flags

| Flag | Description |
|------|-------------|
| `--json` | Output result as JSON |
| `--token <token>` | Login token |
| `--scope <team>` | Set scope to a team |
| `--yes` | Skip confirmation prompts |
| `--cwd <path>` | Set working directory |
| `--debug` | Enable debug output |
