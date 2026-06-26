# DraftMachine Skill

A Claude Code skill that helps agents install and use [DraftMachine](https://github.com/johnkennedy/DraftMachine) — a CLI tool for Gmail mail merge via drafts.

## What it does

When a user asks to send personalized batch emails or do a mail merge to Gmail, this skill guides the agent through:

1. Checking / installing DraftMachine (`pip install draftmachine`)
2. Setting up Gmail OAuth credentials (one-time GCP setup)
3. Writing a CSV recipient list and Jinja2 Markdown template
4. Running `--preview` to validate before touching the API
5. Creating all Gmail drafts in one shot

Drafts land in the user's Gmail Drafts folder for review — nothing is sent automatically.

## Install

```bash
npx skills add johnkennedy/DraftMachineSkill
```

Or install the `.skill` file directly in Claude Code by dragging it into the chat.

## Requirements

- Python 3.8+
- A Gmail account
- A Google Cloud project with the Gmail API enabled (the skill walks you through this)

## Links

- [DraftMachine on PyPI](https://pypi.org/project/draftmachine/)
- [DraftMachine source](https://github.com/johnkennedy/DraftMachine)
