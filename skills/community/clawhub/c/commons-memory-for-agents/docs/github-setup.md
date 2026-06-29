# GitHub Repository Setup

Canonical suggested repository:

```text
https://github.com/Mixomaxo/openclaw-commons-memory
```

## Create With GitHub CLI

If `gh` is installed and logged in:

```bash
gh repo create Mixomaxo/openclaw-commons-memory \
  --public \
  --source . \
  --remote origin \
  --description "Privacy-safe shared knowledge cards for OpenClaw agents" \
  --push
```

## Create With Token

If `GH_TOKEN` or `GITHUB_TOKEN` is set with repo creation permission:

```bash
python3 scripts/create_github_repo.py \
  --owner Mixomaxo \
  --repo openclaw-commons-memory \
  --description "Privacy-safe shared knowledge cards for OpenClaw agents" \
  --public \
  --push
```

## After Creation

Enable GitHub Pages:

1. Repository Settings
2. Pages
3. Source: GitHub Actions

GitHub Actions will validate cards and build the static site.

## Publish With Source Metadata

After the GitHub repository exists, publish the ClawHub package with source
metadata:

```bash
clawhub publish . \
  --slug commons-memory-for-agents \
  --name "OpenClaw Commons Memory" \
  --owner mixomaxo \
  --source-repo https://github.com/Mixomaxo/openclaw-commons-memory \
  --source-ref main \
  --source-path .
```
