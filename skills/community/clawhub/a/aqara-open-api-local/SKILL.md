---
name: aqara-open-api-local
description: Route Aqara Open API requests across device, space, and automation skills with a relationship-first router, shared CLI contract, and structured handoff contract. Supports AQARA_OPEN_API_TOKEN and AQARA_ENDPOINT_URL through environment variables or AQARA CLI config.
author: aqara
metadata: {"clawdbot":{"emoji":"🏠","requires":{"bins":["node"],"env":["AQARA_ENDPOINT_URL","AQARA_OPEN_API_TOKEN"]}}}
---

# Aqara Open API Skill

This file is the single entry router for the Aqara Open Platform HTTP API skill package.

Read this file first. Use it to do four things:

1. Classify whether the user request lands in `device`, `space`, or `automation`.
2. Preserve the shared request envelope, credential rules, and non-guessing rules.
3. Build a structured handoff contract instead of forwarding raw user prose.
4. Decide whether the next step may use cache-first execution or must upgrade to stricter validation.

Child skills:

- `aqara-open-api-local/device/SKILL.md`
- `aqara-open-api-local/space/SKILL.md`
- `aqara-open-api-local/automation/SKILL.md`

## Quick Route Table

Use this table before reading any child skill in depth.

| User asks for | Final intent | Next file |
|---|---|---|
| list devices, count devices, read state, control a device | `device` | `aqara-open-api-local/device/SKILL.md` |
| list spaces, create or rename spaces, move devices between spaces | `space` | `aqara-open-api-local/space/SKILL.md` |
| create automation, inspect automation, update automation config, enable or disable automation, delete automation | `automation` | `aqara-open-api-local/automation/SKILL.md` |
| room-scoped device query such as "what lights are in the living room" | `device` | confirm room identity, then query devices from `data/devices.json` |
| room-related automation such as "turn on the light when someone is in the living room" | `automation` | resolve room and device evidence first, then enter `automation` |

## Language Policy

- user-facing explanations, routing notes, and clarification questions should use Chinese Simplified
- Open API request types, field names, file paths, enums, and code examples must keep exact English identifiers
- do not mix Chinese and English in one rule sentence unless an exact identifier must be quoted

## Package Model

Treat the three business entities as related, not isolated:

- `space` is the container and grouping scope for devices
- `device` is the concrete instance that can be queried, counted, and controlled
- `automation` is the orchestration layer that references rooms, devices, and device traits

Route by the final action target, not by keyword count alone.

Important relationship rule:

- for room-scoped device queries, `space` is the filter key and `device` is the answer source
- `GetSpacesRequest` confirms that a room exists or resolves `spaceId`; it does not answer which devices are inside the room
- the actual room-to-device result must come from `data/devices.json` by filtering devices whose room membership matches the resolved room

Examples:

- "what devices are in the living room" -> final intent is `device`
- "move all lights from the master bedroom to the second bedroom" -> final intent is `space`
- "create an automation that turns on the light when someone is in the living room" -> final intent is `automation`

## Shared Runtime Contract

Runtime configuration may come from:

- `AQARA_ENDPOINT_URL`
- `AQARA_OPEN_API_TOKEN`
- `aqara config`

Credential resolution order:

1. Use the current shell environment if `AQARA_ENDPOINT_URL` and `AQARA_OPEN_API_TOKEN` are already set.
2. Otherwise read the AQARA CLI config file from `~/.aqa/config.json`.
3. Use `aqara config set-endpoint <url>` and `aqara config set-token <token>` when the values are not already configured.

Hard credential rules:

- never guess or hardcode real credentials
- never print the real token in chat, logs, or generated files
- never write secrets into persistent shell startup files
- if the config file is missing or unreadable, stop and report the configuration problem without dumping file contents

## Shared API Contract

Global execution rules:

1. All execution should go through the `aqara` CLI instead of handwritten `curl`.
2. `aqara devices cache refresh` is the only allowed route for `GetAllDevicesWithSpaceRequest`.
3. Every other documented API request should use the matching `aqara` command group.
4. The underlying request body may contain only `type`, `version`, `msgId`, and `data`.
5. `version` must always be `"v1"`.
6. `type` is whitelist-only. Never guess nearby request names.
7. Never guess `deviceId`, `endpointId`, `functionCode`, `traitCode`, `spaceId`, or `automationId`.
8. Command examples assume the current working directory is the `aqara-open-api-local` package root or that `aqara` is installed globally.
9. For queries such as "what devices are in the living room", never answer from `GetSpacesRequest` alone. Resolve the room first, then filter `data/devices.json` to produce the device list.

Shared request envelope:

```json
{
  "type": "<RequestType>",
  "version": "v1",
  "msgId": "<unique-id>",
  "data": {}
}
```

CLI execution note:

- `aqara` encapsulates the request envelope and headers
- do not hand-build headers in normal skill execution

Request type whitelist:

- `GetAllDevicesWithSpaceRequest`
- `GetDeviceTypeInfosRequest`
- `ExecuteTraitRequest`
- `GetSpacesRequest`
- `CreateSpaceRequest`
- `UpdateSpaceRequest`
- `AssociateDevicesToSpaceRequest`
- `QueryAutomationCapabilitiesRequest`
- `CreateAutomationRequest`
- `UpdateAutomationRequest`
- `UpdateAutomationStatusRequest`
- `GetAutomationListRequest`
- `GetAutomationDetailsRequest`
- `DeleteAutomationRequest`

## Capability Validation Strategy

This package uses two validation modes for automation work:

- `cache_first_generate`: default path for creation. Use resolved room and device context plus `data/devices.json` to build an automation-instance style `config`.
- `query_capabilities_required`: stricter path for risky or ambiguous automation work. Upgrade to `QueryAutomationCapabilitiesRequest` before finalizing the config.

Upgrade from `cache_first_generate` to `query_capabilities_required` when any of the following is true:

- the needed starter, condition, or action trait cannot be copied safely from `data/devices.json`
- the request depends on uncertain enum or event values
- the request is cross-space and the source or target mapping is still ambiguous
- the action is high risk, unusual, or not covered by the package's safe defaults
- the user explicitly asks for capability confirmation

Important rule:

- `data/devices.json` is the default creation evidence source
- `QueryAutomationCapabilitiesRequest` is the escalation path, not the default first step

## Handoff Contract

Before entering a child skill, build this structured handoff contract in reasoning. These are semantic routing fields only, not new Open API request fields.

### Required handoff fields

```json
{
  "finalIntentType": "device | space | automation",
  "resolvedSpace": {
    "name": "<spaceName or null>",
    "spaceId": "<spaceId or null>",
    "resolutionSource": "route | get_spaces | device_cache | unresolved"
  },
  "resolvedDevices": [
    {
      "deviceId": "<deviceId>",
      "deviceName": "<display name>",
      "spaceName": "<space name or null>",
      "spaceId": "<spaceId or null>",
      "matchReason": "exact_name | room_plus_name | type_match | parent_context"
    }
  ],
  "resolvedAutomation": {
    "automationId": "<automationId or null>"
  },
  "ambiguityState": {
    "status": "none | room | device | automation | event_enum",
    "questionNeeded": true
  },
  "operationContext": {
    "operation": "query | control | create | update | rename | status | delete",
    "cacheFreshness": "fresh | stale | unknown",
    "detailsLoaded": false
  },
  "capabilityValidationMode": "cache_first_generate | query_capabilities_required",
  "branchingIntent": {
    "needsSplit": false,
    "reason": "<optional reason>"
  }
}
```

### Handoff rules

- do not hand off the raw user sentence alone
- if room scope is already resolved, pass it as `resolvedSpace` instead of forcing the child skill to rediscover it
- if several candidate devices remain, preserve them in `resolvedDevices` and ask for clarification before mutation
- if the request is an automation update, pass whether current automation details have already been loaded
- if a preceding space mutation may have changed room membership, mark `cacheFreshness` as `stale`

## Router SOP

Follow this order. Do not skip steps.

1. Parse which entities are mentioned: `space`, `device`, `automation`.
2. Classify the final action target.
3. Resolve the anchor entity first: room-first, device-first, or automation-first.
4. If the task is a room-scoped device query, use `GetSpacesRequest` only to confirm the room identity when needed, then use `data/devices.json` to reverse lookup the devices in that room.
5. Build the handoff contract.
6. If ambiguity remains, ask before entering a mutating child workflow.
7. Enter the child skill whose domain matches `finalIntentType`.

## Shared Recovery And Reliability Rules

Response code reminders:

- `code: 0` means success
- `400` usually means invalid request data
- `1001` usually means token expired or invalid
- `2030` usually means device not found

Recovery rules:

- device not found during device or space work: refresh `data/devices.json` once, then re-resolve the device
- invalid space update: re-check `spaceId`, mutation scope, and device membership
- invalid automation request: move to the automation child skill, re-check schema shape, and upgrade validation mode if needed
- network timeout: retry once, then report the failure
- space mutation before automation generation: refresh `data/devices.json` or mark `cacheFreshness: "stale"` and stop before create

Platform note:

- the package uses `aqara devices cache refresh` for the full device cache
- if Node.js or the CLI entry cannot run in the current runtime, stop and explain that the CLI path is unavailable instead of inventing ad hoc shell replacements

## Forbidden Behavior

Never do any of the following:

- call Aqara APIs directly with `curl` when an `aqara` command exists
- guess request types or identifiers
- use stale prose memory or trait glossaries as authority for live state
- use `data/devices.json` as if it were an unconditional automation capability whitelist
- place automation `name`, `starters`, `condition`, or `actions` directly under top-level `data`
- describe impossible state such as "light is off and brightness is 100%"

## Reference Index

- `aqara-open-api-local/device/SKILL.md` — device cache-first query and control
- `aqara-open-api-local/space/SKILL.md` — space listing and mutation
- `aqara-open-api-local/automation/SKILL.md` — automation creation and CRUD
- `aqara-open-api-local/docs/commands.md` — CLI command catalog
- `aqara-open-api-local/data/devices.json` — device cache
- `aqara-open-api-local/references/examples.md` — intent-based example index
- `aqara-open-api-local/references/automation-http-examples.md` — automation HTTP lifecycle examples