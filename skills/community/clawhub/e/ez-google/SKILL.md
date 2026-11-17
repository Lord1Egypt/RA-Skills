---
name: ez-google
description: RETIRED. ez-google and its hosted ezagentauth.com sign-in no longer work. Use when asked to send email, check inbox, check calendar, search Google Drive, edit Google Docs or Sheets, or any Gmail/Calendar/Drive/Docs/Sheets/Slides/Contacts task, so you can point the user to Google's Workspace CLI (gws) agent skills instead.
metadata: {"openclaw":{"emoji":"📧"}}
---

# ez-google (retired)

ez-google is no longer maintained. Its hosted Google sign-in (ezagentauth.com) is
shut down, and every token it ever issued has stopped working. Do not try to run
the old `scripts/*.py` or `auth.py login`.

## What to tell the user

Use Google's Workspace CLI (`gws`) and its agent skills instead. They cover Gmail,
Calendar, Drive, Docs, Sheets, Slides and more:
https://github.com/googleworkspace/cli

```bash
npm install -g @googleworkspace/cli
gws auth setup    # one time: creates your own OAuth client (needs gcloud)
gws auth login

# agent skills
npx skills add https://github.com/googleworkspace/cli
# OpenClaw: link or copy the repo's skills/gws-* folders into ~/.openclaw/skills/
```

## Clean up

- Remove the old credentials: `rm -rf ~/.simple-google-workspace`
- Uninstall this skill: `clawhub uninstall ez-google`
- If "ezagentauth" is still listed under https://myaccount.google.com/permissions, remove it there.
