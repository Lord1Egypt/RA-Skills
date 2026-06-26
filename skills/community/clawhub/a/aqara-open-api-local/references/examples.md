# Aqara Open API Example Index

This file is an intent-based index.

Do not read every example file by default. Start from the parent skill and then follow the smallest reference path that matches the task.

## Read Order

1. `aqara-open-api-local/SKILL.md`
2. the target child skill
3. only then open one of the references below if more detail is needed

## Device And Space Tasks

Use these for device discovery, device state, device control, and room management:

- `aqara-open-api-local/assets/device-space-examples.md`

## Automation Tasks

### Automation routing and execution workflow

Use this first for automation intent handling:

- `aqara-open-api-local/automation/SKILL.md`

### Automation HTTP lifecycle

Use this when the task is about list, detail, update, enable or disable, delete, or request wrapping:

- `aqara-open-api-local/references/automation-http-examples.md`

### Automation shape boundary

Use these when the task is about what the generated `config` is allowed to look like:

- `aqara-open-api-local/references/automation-instance-v0.schema.json`
- `aqara-open-api-local/references/stand.automation-instance.json`

### Automation field detail

Use this only when the child skill still needs field-level semantics after the workflow is already clear:

- `aqara-open-api-local/references/automation_config.md`

### Automation pattern JSON

Pick the smallest matching sample instead of reading every sample:

- motion to light: `aqara-open-api-local/references/coldstart-living-room-motion-light.automation-instance.json`
- motion to light and air conditioner: `aqara-open-api-local/references/study-room-motion-light-ac.automation-instance.json`
- threshold emergency automation: `aqara-open-api-local/references/kitchen-gas-safety.automation-instance.json`

## Important Boundaries

- do not use `automation-http-examples.md` as the primary source for `data.config`
- do not use `automation_config.md` as a stronger authority than `automation-instance-v0.schema.json`
- for default generation, the child skill workflow and schema shape come before long-form examples
