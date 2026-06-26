---
name: appian-missingdescr
description: Audit Appian application objects for missing descriptions. Given an application UUID, reports every object whose description field is empty or absent.
metadata:
  clawdbot:
    emoji: "🔎"
    requires:
      env:
        - APPIAN_PROC_URL
        - APPIAN_RUNNER
      binaries:
        - node
    primaryEnv: APPIAN_PROC_URL
---
# Appian Missing Descriptions

Reports every object in an Appian application that has an empty or absent description field, grouped by object type.

## Prerequisites

Both `APPIAN_PROC_URL` and `APPIAN_RUNNER` must be set in your environment before running.

## How to run

```bash
node $APPIAN_RUNNER missing-descr APPLICATION_UUID
```

Replace `APPLICATION_UUID` with the UUID the user provided.

## After running

Report the output verbatim — do not summarize or omit any lines.
