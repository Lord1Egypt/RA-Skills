# Distill Invocation Template

Use this lightweight block after an important task finishes:

```text
distill:
- task: <task name>
- result: <what was completed / fixed / configured>
- scope: <feishu | cron | memory | agent-config | browser | reporting | general>
- reusable: <yes | no | maybe>
- candidate_layers: <daily-log | experience | playbook | skill | multi>
```

## Recommended richer form

```text
distill:
- task: information-digest-agent Hupu monitor setup
- result: built Hupu full-snapshot monitor + Feishu DM delivery + stable report format
- scope: hupu-monitor / cron / reporting / feishu
- reusable: yes
- candidate_layers: multi
- signals:
  - repeated workflow
  - output style locked in
  - new channel integration
  - stable failure mode discovered
```

## Candidate layers
- `daily-log` → dated fact / evidence
- `experience` → action-level reusable lesson
- `playbook` → workflow-level canon
- `skill` → reusable capability package
- `multi` → spans more than one layer
