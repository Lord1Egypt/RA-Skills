# ClawHub Publish / Install Notes

## Install CLI

```bash
npm i -g clawhub
```

## Login for publish

```bash
clawhub login
clawhub whoami
```

## Publish this skill

```bash
clawhub publish ./skills/employee-reminder-ops --slug employee-reminder-ops --name "Employee Reminder Ops" --version 1.0.0 --changelog "Initial release: Google Sheets reminder workflow, Telegram/Discord routing, scheduler notes"
```

## Install on a new machine

```bash
npm i -g clawhub
clawhub install employee-reminder-ops
```

## Upgrade

```bash
clawhub update employee-reminder-ops
```
