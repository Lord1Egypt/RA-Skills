# Install or Upgrade `fotor-skills`

Use this guide when the user asks how to install or upgrade the skill, or when the update checker reports that a newer version is available.

## Goal

Keep the upgrade reminder short, explicit, and non-pushy:

- Tell the user that a newer version exists
- Briefly mention the main highlights if available
- Give the correct upgrade command for the detected install source
- Leave the decision to upgrade to the user
- Do not auto-upgrade unless the user explicitly asks

## First: Identify the Install Source

Use the install source already detected by the update checker.

Supported install sources:

- `clawhub`
- `skills-github`

## If Installed via ClawHub

### Install

```bash
clawhub install fotor-skills
```

### Upgrade

```bash
clawhub update fotor-skills
```

### What to say

Use a short reminder like:

> `fotor-skills` has a newer version available. If you want, you can upgrade with `clawhub update fotor-skills`.

If highlights are available, add one short clause with the main changes. Do not dump the full changelog.

## If Installed via GitHub / `npx skills`

### Install

```bash
npx skills add https://github.com/fotor-ai/fotor-skills.git --skill fotor-skills --copy -y
```

### Upgrade

```bash
npx skills update
```

### What to say

Use a short reminder like:

> `fotor-skills` has a newer version available. If you want, you can upgrade with `npx skills update`.

If highlights are available, add one short clause with the main changes. Do not dump the full changelog.

## Reminder Style Rules

- Keep the reminder to one short sentence or two short lines
- Do not turn the conversation into a release note dump
- Do not pressure the user to upgrade
- Do not auto-upgrade unless the user explicitly asks
- After reminding, continue or return to the user’s main task whenever appropriate
