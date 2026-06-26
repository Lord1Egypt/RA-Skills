# Publish a CLI

Only do this when the user explicitly asks to publish or share their CLI.

## Step 1: Push to GitHub

```bash
cd ~/.cli/<app>-cli
git init
git add -A
git commit -m "feat: <app>-cli - manage <app> via CLI"
gh repo create <app>-cli --public --source . --push
```

## Step 2: Register on api2cli.dev

```bash
curl -X POST https://api2cli.dev/api/publish-cli \
  -H "Content-Type: application/json" \
  -d '{"githubUrl": "<github-user>/<app>-cli"}'
```

The registry auto-detects from the repo:
- Repo description, stars, topics
- package.json name and version
- README.md auth type
- SKILL.md name and description
- Category (social, finance, devtools, marketing, etc.)

## After publishing

Anyone can install the CLI and skill with one command:

```bash
npx api2cli install <github-user>/<app>-cli
```

This clones the repo, builds, links to PATH, and symlinks the skill to their agent.

## Checklist before publishing

- All resources implemented and tested
- `skills/<app>-cli/SKILL.md` updated with actual resource commands (no placeholders)
- `README.md` updated with actual resources and GitHub repo path
- `<app>-cli auth test` works with a valid token
