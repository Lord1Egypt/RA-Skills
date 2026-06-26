---
name: aqara-open-api-local-space
description: List, create, update, and manage Aqara Open API spaces with structured room resolution, real ID lookup, and cache freshness guardrails through the AQARA CLI. Supports AQARA_OPEN_API_TOKEN and AQARA_ENDPOINT_URL through environment variables or AQARA CLI config.
author: aqara
metadata: {"clawdbot":{"emoji":"🗂️","requires":{"bins":["node"],"env":["AQARA_ENDPOINT_URL","AQARA_OPEN_API_TOKEN"]}}}
---

# Aqara Open API Space Skill

Read the parent router first:

- `aqara-open-api-local/SKILL.md`

This file handles room and space mutation. It should not be used as a general device query skill.

Important boundary:

- if the user asks which devices are inside a room, this file may help resolve the room identity only
- the actual room-to-device answer must come from `aqara-open-api-local/device/SKILL.md` by filtering `aqara-open-api-local/data/devices.json`

## Use This File

Stay in this file when the final action target is `space`:

- list spaces
- create a space
- rename or update a space
- move devices between spaces
- associate devices to a space

## Do Not Stay Here

Resolve room context here, then leave when the final action target changes:

- room-scoped device query -> hand off to `aqara-open-api-local/device/SKILL.md`
- room-related automation creation or update -> hand off to `aqara-open-api-local/automation/SKILL.md`

## Required Inputs

Reuse the parent handoff contract:

- `resolvedSpace`
- `resolvedDevices`
- `ambiguityState`
- `operationContext`

If `resolvedSpace.spaceId` already exists, reuse it after confirming the user still means the same room.

## Evidence Model

Room and device work use two evidence paths:

- `GetSpacesRequest` for real space metadata such as `spaceId` and room name
- `aqara-open-api-local/data/devices.json` for the current device-to-room membership snapshot

Important rule:

- space metadata is realtime through `GetSpacesRequest`
- device room membership becomes stale after a successful space mutation until `data/devices.json` is refreshed

## Mini SOP

Follow this order:

1. Confirm the final action target is still `space`.
2. Resolve the target room with `GetSpacesRequest` when needed.
3. Resolve affected `deviceIds` from `data/devices.json`.
4. Confirm destructive scope before broad mutations.
5. Execute the space request with real identifiers only.
6. If the mutation changes room membership, refresh `data/devices.json` or mark cache freshness as stale before any follow-up automation or room-scoped device work.

## Space Rules

- the only valid request type for listing spaces is `GetSpacesRequest`
- never guess alternatives such as `GetAllSpacesRequest` or `QuerySpaceListRequest`
- never guess `spaceId` or `deviceIds`
- do not infer automation updates automatically from a space mutation

Relationship rules:

1. resolve the target space first
2. resolve affected devices from real data
3. only then build the mutation request

## Destructive Change Gate

Confirm scope before any broad mutation:

- moving multiple devices between spaces
- reassigning all devices of one type in a room
- renaming a room that was identified ambiguously

Clarify these points before execution:

- source room
- target room
- affected device scope
- whether the user wants all matches or only a subset

## Cache Freshness Guardrails

After `AssociateDevicesToSpaceRequest` or any room mutation that changes membership:

- `data/devices.json` should be treated as stale
- if the next task is room-scoped device work, refresh the cache first when possible
- if the next task is automation generation, refresh the cache first or stop and state that room membership evidence is stale
- if refresh cannot run because the CLI is unavailable, stop instead of pretending the cache is fresh

## Reliability And Clarification Rules

Ask for clarification when:

- more than one space matches the same phrase
- the source or target room is unclear
- the device set is still ambiguous after room filtering

Recovery rules:

- if space update fails, re-check `spaceId`, payload shape, and mutation scope
- if device membership is inconsistent after mutation, refresh `data/devices.json` once before proceeding

## Request Catalog

### List spaces — `GetSpacesRequest`

```bash
aqara spaces list --json
```

### Create space — `CreateSpaceRequest`

```bash
aqara spaces create --name "Living Room" --spatial-marking living_room --json
```

### Update space — `UpdateSpaceRequest`

```bash
aqara spaces update --space-id "<spaceId>" --name "New Room Name" --json
```

### Associate devices to space — `AssociateDevicesToSpaceRequest`

```bash
aqara spaces associate --space-id "<spaceId>" --device-id "<deviceId1>" --device-id "<deviceId2>" --json
```

## Reference Index

- `aqara-open-api-local/SKILL.md` — parent router and shared contract
- `aqara-open-api-local/device/SKILL.md` — room-scoped device filtering
- `aqara-open-api-local/automation/SKILL.md` — automation work after room resolution
- `aqara-open-api-local/data/devices.json` — device membership snapshot
- `aqara-open-api-local/docs/commands.md` — CLI command catalog
