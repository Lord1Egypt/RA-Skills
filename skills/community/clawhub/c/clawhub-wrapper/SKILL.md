---
name: clawhub
version: "1.0.1"
description: "Download and install skills from ClawHub (https://clawhub.ai). Use when user wants to browse, search, or download skills from the ClawHub skill registry."
---

# ClawHub Skill

Download and install skills from ClawHub - a fast skill registry for AI agents.

## Commands

### Search Skills

Search for skills by keyword:

```bash
{baseDir}/clawhub-search.sh "<keyword>"
```

This searches the ClawHub registry and displays matching skills with their slug, name, summary, and download count.

### Download and Install Skill

Download and install a skill by slug or ClawHub URL:

```bash
# By slug
{baseDir}/clawhub-download.sh <slug>

# By ClawHub URL (e.g., https://clawhub.ai/steipete/github)
{baseDir}/clawhub-download.sh https://clawhub.ai/owner/slug
```

This will:
1. Download the skill package from ClawHub
2. Extract it to `~/.agents/skills/clawhub-skills/<slug>/`
3. Display the installed skill information

### List Skills

Browse available skills (sorted by downloads):

```bash
{baseDir}/clawhub-search.sh
```

## API Endpoints

ClawHub uses the following API endpoints:

- **List/Search Skills**: `https://wry-manatee-359.convex.site/api/v1/skills`
- **Download Skill**: `https://wry-manatee-359.convex.site/api/v1/download?slug=<slug>`

## Examples

User says: "I want to download the github skill from clawhub"
→ Use `clawhub-download.sh github`

User says: "Search for weather related skills on clawhub"
→ Use `clawhub-search.sh "weather"`

User says: "Install https://clawhub.ai/steipete/summarize"
→ Use `clawhub-download.sh https://clawhub.ai/steipete/summarize`

User says: "What skills are popular on clawhub?"
→ Use `clawhub-search.sh` to list top skills by downloads
