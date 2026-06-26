---
name: aqara-open-api-local-device
description: Query, count, interpret, and control Aqara Open API devices with a cache-first workflow and structured room-aware filtering through the AQARA CLI. Supports AQARA_OPEN_API_TOKEN and AQARA_ENDPOINT_URL through environment variables or AQARA CLI config.
author: aqara
metadata: {"clawdbot":{"emoji":"💡","requires":{"bins":["node"],"env":["AQARA_ENDPOINT_URL","AQARA_OPEN_API_TOKEN"]}}}
---

# Aqara Open API Device Skill

Read the parent router first:

- `aqara-open-api-local/SKILL.md`

This file should feel simple. Use it only for device query, device interpretation, and device control.

## Use This File

Stay in this file when the final action target is `device`:

- list devices
- filter devices by room, type, online status, or display name
- count or group devices
- explain device state from cache
- control a device through `ExecuteTraitRequest`
- refresh the device cache

## Do Not Stay Here

Resolve device evidence here, then leave when the final action target is not `device`:

- move devices to another room -> hand off to `aqara-open-api-local/space/SKILL.md`
- create or update automation from resolved room or device context -> hand off to `aqara-open-api-local/automation/SKILL.md`

## Required Inputs

Reuse the parent handoff contract instead of guessing again:

- `resolvedSpace`
- `resolvedDevices`
- `ambiguityState`
- `operationContext`

If `resolvedSpace.name` already exists, start from that scoped room filter.

Room-scoped device query rule:

- when the user asks "what devices are in a specific space", do not answer from the space list alone
- `GetSpacesRequest` may confirm the room name or `spaceId`, but the actual device result must come from filtering `aqara-open-api-local/data/devices.json`
- if the room exists in space metadata but no device currently maps to that room in cache, answer that no devices were found in current device evidence instead of pretending the query itself failed

## Device Evidence Model

Primary evidence source:

- `aqara-open-api-local/data/devices.json`

What this cache contains:

- the `data` array returned by `GetAllDevicesWithSpaceRequest`
- one logical device object per `deviceId`
- room membership, online status, endpoint layout, and trait values from the last successful refresh

Refresh command:

```bash
aqara devices cache refresh
```

Cache rules:

1. Read `data/devices.json` before any listing, filtering, counting, or state lookup.
2. If the file is missing, empty, or invalid, run the refresh script and then read the file again.
3. If the user explicitly asks to refresh, run the script even if the file exists.
4. Do not call `GetAllDevicesWithSpaceRequest` directly with HTTP tools. Use `aqara devices cache refresh`.

## Mini SOP

Follow this order:

1. Confirm the final action target is still `device`.
2. Load `data/devices.json`. Refresh it if missing or invalid.
3. If `resolvedSpace` exists, treat it as a filter key and reverse lookup devices from `data/devices.json`.
4. Narrow by exact device name or `deviceTypesList`.
5. If the task is state explanation, separate device level from endpoint or trait level.
6. If the task is control, copy real `deviceId`, `endpointId`, `functionCode`, and `traitCode` from cache. The CLI may auto-resolve `endpointId` and `functionCode` when the target `traitCode` is unique.
7. If multiple devices still match, ask before answering or controlling.

## Device Query Rules

- prefer local filtering over extra API calls
- use exact cache fields for `deviceId`, `space.name`, `deviceTypesList`, `endpoints`, `functionCode`, and `traitCode`
- treat device type and display name as different concepts
- do not answer from partial scans, memory, or example payloads
- if the cache may be stale, say so unless you refresh first
- for room-scoped device queries, use `space` only to resolve the room identity; use the device cache to answer the actual device list

Room-aware matching order:

1. parent `resolvedDevices`
2. parent `resolvedSpace`
3. exact device name
4. room plus device name
5. device type
6. explicit user clarification

## State Interpretation Rules

When explaining state, split the answer into these layers:

- device level: identity, online state, and room membership
- endpoint level: which endpoint owns the relevant function or trait
- trait level: observed values such as `OnOff`, brightness, color temperature, or sensor readings

Do not invent trait values that are missing from cache.

## Control Rules

Use `ExecuteTraitRequest` only after copying real identifiers from cache.

Payload item shape:

```json
{
  "deviceId": "<deviceId>",
  "endpointId": 2,
  "functionCode": "Output",
  "traitCode": "OnOff",
  "value": true
}
```

Control rules:

- `endpointId` must be numeric
- `value` must match the target trait type
- response `data` contains failed items only; an empty array means success
- if the user wants post-control confirmation, refresh the cache or explicitly say the answer is based on the latest cached snapshot

## Reliability And Clarification Rules

Ask for clarification when:

- multiple devices match the same phrase
- room scope is still ambiguous after filtering
- a room-scoped query depends on stale cache after a recent space mutation

Answer directly instead of asking when:

- the room is already resolved and cache filtering returns zero devices; report that current device evidence contains no devices for that room

Reliability rules:

- if `operationContext.cacheFreshness` is `stale`, refresh before room-sensitive answers when possible
- if refresh is unavailable because bash cannot run, stop and report the limitation
- never treat cache data as guaranteed real-time state

## Request Catalog

### Refresh all devices

```bash
aqara devices cache refresh
```

### Get device types — `GetDeviceTypeInfosRequest`

```bash
aqara devices types --json
```

### Control device — `ExecuteTraitRequest`

```bash
aqara devices execute "<deviceIdOrName>" \
  --trait-code OnOff \
  --value true \
  --json
```

If the trait tuple is ambiguous on the device, add `--function-code` and `--endpoint-id`.

## Reference Index

- `aqara-open-api-local/SKILL.md` — parent router and shared contract
- `aqara-open-api-local/data/devices.json` — device cache
- `aqara-open-api-local/docs/commands.md` — CLI command catalog
- `aqara-open-api-local/assets/device-space-examples.md` — device and room examples
