---
name: aqara-open-api-local-automation
description: Create, inspect, update, enable, disable, rename, and delete Aqara Open API automations with a schema-first, cache-first generation workflow and explicit capability-escalation rules through the AQARA CLI. Supports AQARA_OPEN_API_TOKEN and AQARA_ENDPOINT_URL through environment variables or AQARA CLI config.
version: 2.0.0
author: aqara
metadata: {"clawdbot":{"emoji":"⚙️","requires":{"bins":["node"],"env":["AQARA_ENDPOINT_URL","AQARA_OPEN_API_TOKEN"]}}}
---

# Aqara Open API Automation Skill

Read these in order:

1. `aqara-open-api-local/SKILL.md`
2. this file
3. only if needed, `aqara-open-api-local/references/automation_config.md`

This file is intentionally short. It should let the agent create or operate automation quickly without re-reading the whole package.

## Use This File

Stay in this file when the final action target is `automation`:

- create automation from natural language
- create manual-trigger automation from natural language
- generate `CreateAutomationRequest.data.config`
- inspect automation details
- rename, update, enable, disable, or delete automation

## Do Not Stay Here

Resolve room or device evidence here only as far as automation needs it. If the final action target changes, leave:

- device state or device control only -> `aqara-open-api-local/device/SKILL.md`
- room creation, rename, or device reassignment -> `aqara-open-api-local/space/SKILL.md`

## Required Inputs

Reuse the parent handoff contract:

- `resolvedSpace`
- `resolvedDevices`
- `resolvedAutomation`
- `ambiguityState`
- `operationContext`
- `capabilityValidationMode`
- `branchingIntent`

Important rules:

- default creation mode is `cache_first_generate`
- upgrade to `query_capabilities_required` only when the parent rules require it
- do not rediscover room or device scope from scratch if the parent already resolved it
- automation creation may use only already retrieved evidence: `resolvedSpace`, `resolvedDevices`, `data/devices.json`, and any room results already fetched in the current turn
- if the requested room or device is absent from the retrieved evidence, stop and ask instead of inventing fallback scope

## Default Creation SOP

Use this exact order for creation:

1. Write an intent card: trigger, optional condition, action, room scope, split need. Manual trigger is allowed when the user explicitly wants one-tap, shortcut, scene, or panel style execution.
2. Load room and device evidence from `data/devices.json`.
3. Verify that every requested room and device already exists in the retrieved evidence, and that the requested room contains the devices needed by the automation.
4. Build a capability table from real cache tuples: `deviceId`, `endpointId`, `functionCode`, `traitCode`.
5. Write `metadata.scope` first when reusable device-property starter sources are needed. For pure manual-trigger automations, `metadata.scope` may be omitted or set to an empty array.
6. Write `automations[]` next.
7. Check the result against `automation-instance-v0.schema.json`.
8. Validate the `config` with `aqara automations validate`, then submit it with `aqara automations create`.

If any step cannot be completed safely, stop and ask or upgrade validation mode.

CLI shortcut for the safe default path:

- use `aqara automations generate motion-light --room "<roomName>"` when the request is the common occupied-on / unoccupied-off light automation
- use `aqara automations generate manual-scene --room "<roomName>" --value <true|false>` when the request is a generic manual On/Off scene
- use `aqara automations generate manual-scene-off --room "<roomName>"` when the request is a manual one-tap off scene for a room
- use `aqara automations create-from-intent motion-light --room "<roomName>"` when the cache evidence is already sufficient and the user wants direct creation
- use `aqara automations create-from-intent manual-scene --room "<roomName>" --value <true|false>` when the user wants immediate creation of a manual On/Off scene
- use `aqara automations create-from-intent manual-scene-off --room "<roomName>"` when the user wants immediate creation of a manual off scene
- if multiple motion sensors or light targets are possible, add `--sensor` and `--light` instead of guessing

## Shape-First Rules

The generated `config` must follow the same shape family as:

- `aqara-open-api-local/references/stand.automation-instance.json`
- `aqara-open-api-local/references/automation-instance-v0.schema.json`
- `aqara-open-api-local/references/manual-instance.json`

Minimal legal `config` skeleton:

```json
{
  "metadata": {
    "name": "Automation pack name",
    "description": "Optional description",
    "scope": []
  },
  "automations": [
    {
      "name": "Branch name",
      "starters": [],
      "actions": []
    }
  ]
}
```

Create wrapper:

```json
{
  "type": "CreateAutomationRequest",
  "version": "v1",
  "msgId": "msg-123",
  "data": {
    "definitionType": "SCRIPT_JSON",
    "config": {}
  }
}
```

## Hard Rules

1. Never guess `deviceId`, `endpointId`, `functionCode`, `traitCode`, `spaceId`, or `automationId`.
2. `functionCode` and `traitCode` are different fields. Never swap them.
3. The automation JSON belongs inside `data.config`, not directly inside top-level `data`.
4. Every automation branch must contain `name`, `starters`, and `actions`.
5. Use `metadata.scope` plus `data.ref` for reusable starter sources when the trigger depends on device properties.
6. Do not invent traits that are absent from `data/devices.json`.
7. Do not use `operator`, `fieldCode`, or `property.state.source.targets`.
8. Do not use `device.command.call` in the default schema-first path.
9. If room membership evidence is stale after a space mutation, stop before create until the cache is refreshed.
10. If enum or event values are uncertain, ask instead of guessing.
11. Never create automation from a room name or device phrase that is not present in the already retrieved space or device evidence.
12. If the requested room exists but currently contains zero devices in the retrieved evidence, stop and clarify. Do not search nearby rooms, parent rooms, or similarly named rooms.
13. If the requested scenario needs target devices in a room but that room has no eligible devices, stop and clarify. Do not silently move the automation to another room.
14. If the user gives a thematic scene name such as "Chinese New Year" but the referenced room or devices are missing, ask the user to choose from existing rooms or refresh evidence. Do not loop on room guessing.

## Evidence Gate

Before generating any automation config, pass this gate:

- the requested `space` must already exist in `resolvedSpace`, `resolvedDevices`, `data/devices.json`, or previously fetched room results in the same turn
- every referenced `device` must already exist in the retrieved evidence
- every starter source and action target must remain inside the user-requested scope unless the user explicitly asked for cross-space behavior
- if the requested room has no devices, or has devices but none that satisfy the requested trigger or action, stop and ask

If the evidence gate fails, do not continue generation, do not retry with guessed rooms, and do not rewrite the user intent to fit a different room.

## When To Upgrade Capability Validation

Upgrade to `QueryAutomationCapabilitiesRequest` before finalizing the config when:

- the needed starter, condition, or action trait is missing from cache
- the request depends on uncertain enum or event values
- the action is unusual, high risk, or not covered by the package's safe defaults
- the request is cross-space and source or target mapping is still ambiguous
- the user explicitly asks for live capability confirmation

If upgraded, use capability results to confirm the final trait mapping before create or config update.

## Safe Defaults For Cache-First Creation

These safe defaults are allowed in the default path because they are consistent across the provided schema and sample files:

- `manual` starter means the automation is user-triggered and does not need a device-event source
- `OccupancySensing.Occupancy = true` means occupied
- `OccupancySensing.Occupancy = false` means unoccupied
- `Contact.ContactSensorState = true` means open
- `Contact.ContactSensorState = false` means closed
- `Output.OnOff = true` means on
- `Output.OnOff = false` means off
- `WindowCovering.TargetPositionPercentage = 100` means fully open
- `WindowCovering.TargetPositionPercentage = 0` means fully closed

## Split Rules

Split one user request into multiple automation branches when:

- on and off behaviors need different actions
- one starter drives multiple outcomes with different conditions
- one room needs separate arrival and departure logic

If `branchingIntent.needsSplit` is already true, keep that split plan instead of collapsing branches.

## Validation Checklist

Before create or config update, verify:

- the root has `metadata` and `automations`
- `metadata.name` is non-empty
- every scope item is `type: "device.property"` when `metadata.scope` is present
- every `manual` starter includes a non-empty `name`
- every referenced room and device comes from already retrieved evidence
- every source and action target copies real cache identifiers
- the requested room actually contains the referenced target devices
- every branch has non-empty `name`, `starters`, and `actions`
- every comparator field is schema-allowed
- `operator` and `fieldCode` are absent
- all endpoint identifiers are numeric
- the JSON is placed under `data.config`

CLI note:

- `aqara automations validate`, `create`, and `update` support `starters.type = "manual"`
- pure manual-trigger automations may omit `metadata.scope` when no `data.ref` starter source is used
- `aqara automations generate motion-light` generates a cache-backed config without mutating the server
- `aqara automations generate manual-scene` generates a cache-backed manual On/Off scene without mutating the server
- `aqara automations generate manual-scene-off` generates a cache-backed manual off scene without mutating the server
- `aqara automations create-from-intent motion-light` generates, validates, and submits in one step
- `aqara automations create-from-intent manual-scene` generates, validates, and submits a manual On/Off scene in one step
- `aqara automations create-from-intent manual-scene-off` generates, validates, and submits a manual off scene in one step
- `aqara automations create` and `aqara automations update` run the same schema-first validation before submission
- use `aqara automations validate` when you want to inspect validation failures before mutating the server

## Existing Automation Operations

For non-create work, use the documented routes below.

### List automations — `GetAutomationListRequest`

```bash
aqara automations list --page-num 1 --page-size 200 --order-by "createTime desc" --json
```

### Get details — `GetAutomationDetailsRequest`

```bash
aqara automations get "<automationId>" --json
```

### Update name or config — `UpdateAutomationRequest`

Always load current details before config update.

```bash
aqara automations update "<automationId>" --config-file ./validated-config.json --json
```

### Enable or disable — `UpdateAutomationStatusRequest`

```bash
aqara automations enable "<id1>" --json
```

### Delete — `DeleteAutomationRequest`

```bash
aqara automations delete "<automationId1>" "<automationId2>" --json
```

## Reliability And Clarification Rules

Ask for clarification when:

- multiple devices match the target phrase
- room scope is ambiguous
- the requested room is not present in the retrieved evidence
- the requested room exists but has zero devices in the retrieved evidence
- the requested room has devices but none can satisfy the requested trigger or action
- the request is cross-space but source or target is still unresolved
- the requested action trait does not exist in cache
- a button or enum event value is uncertain

Reliability rules:

- after create, offer an optional detail read-back if the user wants verification
- before update, load existing automation details first
- if the cache is stale after a space mutation, refresh before generation or stop
- never fall back to a different room just because the requested room has no matching devices
- when evidence is missing, ask for clarification or refresh evidence; do not continue generation in a retry loop

## Reference Index

- `aqara-open-api-local/SKILL.md` — parent router and shared contract
- `aqara-open-api-local/references/automation_config.md` — detailed field semantics and reference boundary notes
- `aqara-open-api-local/references/stand.automation-instance.json` — canonical shape example
- `aqara-open-api-local/references/manual-instance.json` — manual trigger example
- `aqara-open-api-local/references/automation-instance-v0.schema.json` — shape constraints
- `aqara-open-api-local/references/coldstart-living-room-motion-light.automation-instance.json` — motion to light pattern
- `aqara-open-api-local/references/study-room-motion-light-ac.automation-instance.json` — motion to light and AC pattern
- `aqara-open-api-local/references/kitchen-gas-safety.automation-instance.json` — threshold emergency pattern
