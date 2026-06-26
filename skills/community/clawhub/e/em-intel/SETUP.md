# em-intel Setup Guide

Step-by-step instructions for generating the API tokens em-intel needs.

## 1. Code Platform

### GitLab (default)

1. Go to <https://gitlab.com/-/user_settings/personal_access_tokens>
2. Click **Add new token**
3. Name: `em-intel` (or similar)
4. Scope: **`read_api`**
5. Click **Create personal access token** and copy the value

```env
EM_CODE_PROVIDER=gitlab
GITLAB_URL=https://gitlab.com
GITLAB_TOKEN=glpat-xxxxxxxxxxxxxxxxxxxx
GITLAB_GROUP=your-org/your-group
```

> `GITLAB_GROUP` is the full path shown in the URL when you visit your group page.

### GitHub (alternative)

1. Go to <https://github.com/settings/tokens/new>
2. Name: `em-intel`
3. Scopes: **`repo`**, **`read:org`**
4. Click **Generate token** and copy the value

```env
EM_CODE_PROVIDER=github
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
GITHUB_ORG=your-org
GITHUB_REPO=your-repo
```

## 2. Ticket System

### Jira (default)

1. Go to <https://id.atlassian.com/manage-profile/security/api-tokens>
2. Click **Create API token**
3. Label: `em-intel`
4. Copy the token

```env
EM_TICKET_PROVIDER=jira
JIRA_URL=https://your-site.atlassian.net
JIRA_EMAIL=you@company.com
JIRA_TOKEN=your-api-token
JIRA_PROJECTS=PROJ1,PROJ2
```

> **Important**: `JIRA_EMAIL` must match your Atlassian account email exactly.
> `JIRA_PROJECTS` is a comma-separated list of Jira project keys.

### GitHub Issues (alternative)

Uses the same `GITHUB_TOKEN` from the code platform setup above.

```env
EM_TICKET_PROVIDER=github_issues
```

## 3. Delivery Channel (optional)

Default is `print` (stdout). Configure one of:

### Email (SMTP)

```env
EM_DELIVERY=email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=you@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_TO=recipient@example.com
```

> For Gmail, use an [App Password](https://myaccount.google.com/apppasswords), not your regular password.

### Slack

```env
EM_DELIVERY=slack
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/T.../B.../xxx
```

### Telegram

```env
EM_DELIVERY=telegram
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
TELEGRAM_CHAT_ID=-100123456789
```

## 4. Tuning (optional)

```env
EM_QUIET_ENGINEER_DAYS=10    # Days of silence = "quiet"
EM_STALE_EPIC_DAYS=14        # Days without update = "stale"
EM_LOOKBACK_DAYS=30          # Default lookback for ticket queries
```

## 5. Verify

```bash
python3 em_intel.py doctor
```

This checks all env vars are set and tests each API connection.

If you don't have credentials yet, try dry-run mode:

```bash
python3 em_intel.py morning-brief --dry-run
```
