# Automation Config Reference

This file is a detailed reference for automation JSON fields.

It is not the first file to read.

Read order:

1. `aqara-open-api-local/SKILL.md`
2. `aqara-open-api-local/automation/SKILL.md`
3. this file only when field-level detail is still needed

## Precedence Rules

Use these sources in this order:

1. `aqara-open-api-local/automation/SKILL.md` for the default execution workflow
2. `automation-instance-v0.schema.json` for the default shape boundary
3. `stand.automation-instance.json` and sample JSON files for known-good patterns
4. this file for detailed field semantics and extension notes

If this file conflicts with `automation-instance-v0.schema.json`, the schema wins for the default generation path.

## Default Schema-First Subset

The current default generation path should stay within this subset:

- root: `metadata`, optional `capability_gaps`, `automations`
- starters: `property.event`, `time.schedule`
- conditions: `property.state`, `and`, `time.between`
- actions: `device.trait.write`, `delay`
- starter source reuse: `metadata.scope` plus `data.ref`
- inline condition source: `device.property` or `data.ref` when schema allows it

Do not generate anything outside that subset unless the current workflow explicitly upgrades to an extension path.

## Canonical Root Shape

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

## Datasource Rules

### `device.property`

Use this for inline condition sources or one-off references:

```json
{
  "type": "device.property",
  "deviceId": "device001",
  "endpointId": 1,
  "functionCode": "Output",
  "traitCode": "OnOff"
}
```

### `data.ref`

Use this for reusable starter sources stored in `metadata.scope`:

```json
{
  "type": "data.ref",
  "from": "/metadata/scope",
  "select": {
    "by": "name",
    "value": "livingRoomMotion"
  }
}
```

Default rule:

- in the schema-first path, prefer `data.ref` for reusable `property.event` sources
- keep starter reuse aligned with `stand.automation-instance.json` and sample JSON patterns

## Supported Default Nodes

### `property.event`

Use for occupancy, contact, threshold, or other supported event-like starters.

Allowed comparator fields in the default path:

- `is`
- `isNot`
- `greaterThan`
- `greaterThanOrEqual`
- `greaterThanOrEqualTo`
- `lessThan`
- `lessThanOrEqual`
- `lessThanOrEqualTo`
- `in`
- optional `for`
- optional `suppressFor`

### `time.schedule`

Use for schedule starters.

Default-safe `at` format:

- 24-hour time such as `"08:00"` or `"22:30"`

Important note:

- the schema requires `at`
- treat `cron` as advanced detail that should be used only if the current validator and workflow confirm it is acceptable

### `property.state`

Use for current state checks in conditions.

Default-safe sources:

- inline `device.property`
- `data.ref` only when the schema permits that exact shape

### `and`

Use to combine time and device-state conditions.

### `time.between`

Use for time windows such as:

```json
{ "type": "time.between", "after": "18:00", "before": "06:00" }
```

### `device.trait.write`

Use for all default actions.

```json
{
  "type": "device.trait.write",
  "functionCode": "Output",
  "traitCode": "OnOff",
  "targets": [
    { "deviceId": "light001", "endpointIds": [1] }
  ],
  "value": true
}
```

Rules:

- `targets` must use real `deviceId` and numeric `endpointIds`
- batch multiple targets only when they truly share the same `functionCode`, `traitCode`, and `value`

### `delay`

Use for simple pauses between actions:

```json
{ "type": "delay", "for": "20sec" }
```

## Extension-Only Shapes

The following shapes appear in broader documentation history, but they are not part of the default schema-first generation contract:

- `manual`
- `or`
- `not`
- `device.command.call`
- `time.schedule.timezone`
- non-24-hour `at` formats such as `"7:30 am"` or solar expressions

Treat these as extension-only:

- do not generate them by default
- do not use them unless the active workflow explicitly allows them
- if needed, upgrade capability validation and confirm that the target runtime accepts them

## Known Bad Patterns

Never generate these fields in the default path:

- `operator`
- `fieldCode`
- `property.state.source.targets`

These patterns are historical mistakes, not valid shortcuts.

## Value Guidance

Common safe defaults:

- `OccupancySensing.Occupancy = true` means occupied
- `OccupancySensing.Occupancy = false` means unoccupied
- `Contact.ContactSensorState = true` means open
- `Contact.ContactSensorState = false` means closed
- `Output.OnOff = true` means on
- `Output.OnOff = false` means off

If the request depends on a less certain enum or command value, stop and ask or upgrade capability validation.

## Duration Guidance

Valid examples:

- `"5sec"`
- `"30sec"`
- `"5min"`
- `"1hour"`
- `"1hour10min20sec"`

## Capability Query Boundary

`QueryAutomationCapabilitiesRequest` is not the default first step anymore.

Use it when:

- the cache does not expose enough trait evidence
- the action is risky or uncommon
- enum or event values are uncertain
- the user explicitly requests live capability confirmation

## Suggested Pattern Files

Use these files as known-good examples after the workflow is already clear:

- `aqara-open-api-local/references/stand.automation-instance.json`
- `aqara-open-api-local/references/coldstart-living-room-motion-light.automation-instance.json`
- `aqara-open-api-local/references/study-room-motion-light-ac.automation-instance.json`
- `aqara-open-api-local/references/kitchen-gas-safety.automation-instance.json`
