# Distill Invocation Examples

## 1) Fix Mode recovery

```text
distill:
- task: Feishu pairing failure recovery
- result: confirmed expired pairing codes cannot be approved; user must re-trigger a new code
- scope: feishu / auth
- reusable: yes
- candidate_layers: multi
- signals:
  - fix-mode
  - stable failure mode discovered
  - other agents can reuse this
```

## 2) New cron/report workflow

```text
distill:
- task: Hupu forum monitoring cron
- result: built current-snapshot report flow + Feishu delivery + report style rules
- scope: hupu-monitor / cron / reporting / feishu
- reusable: yes
- candidate_layers: multi
- signals:
  - new cron/report workflow
  - output style locked in
  - repeated workflow
```

## 3) New agent/channel integration

```text
distill:
- task: information-digest-agent Feishu routing setup
- result: bound dedicated Feishu account and synced agent rename across config/routes/cron/path references
- scope: agent-config / feishu / routing
- reusable: yes
- candidate_layers: multi
- signals:
  - new integration
  - stable failure mode discovered
  - other agents can reuse this
```

## 4) Data dependency split

```text
distill:
- task: investment daily monitor prefetch split
- result: moved price fetching into a separate cron before the main report job
- scope: cron / reporting / investment
- reusable: yes
- candidate_layers: experience
- signals:
  - repeated workflow
  - stable failure mode discovered
```

## 5) Output style finalized

```text
distill:
- task: Feishu brief formatting for forum monitor
- result: replaced raw title dump with sub-500-char synthesized briefing
- scope: reporting / feishu
- reusable: yes
- candidate_layers: experience
- signals:
  - output style locked in
  - other agents can reuse this
```

## 6) Playbook compaction

```text
distill:
- task: rule/archive compaction into playbooks
- result: consolidated scattered operational knowledge into canonical playbooks and updated indexes
- scope: docs / workflow / knowledge-system
- reusable: yes
- candidate_layers: playbook
- signals:
  - repeated workflow
  - workflow changed
```

## 7) Memory tuning

```text
distill:
- task: QMD indexing latency tuning
- result: shortened update/embed intervals so new notes become searchable faster
- scope: memory / qmd
- reusable: yes
- candidate_layers: experience
- signals:
  - repeated workflow
  - stable failure mode discovered
```

## 8) No-op case

```text
distill:
- task: one-off website lookup
- result: found the answer and nothing reusable emerged
- scope: web
- reusable: no
- candidate_layers: no-op
```

## Usage note

If unsure, prefer `candidate_layers: multi` and let `experience-distiller` narrow it down.

When in doubt, err toward writing too little rather than turning noise into permanent knowledge.
