# Aqara Open API — Automation CLI Examples

This document only demonstrates an automated CLI encapsulation example. Automated intent decomposition and `data.config` construction should primarily follow the guidelines in `aqara-open-api-local/automation/SKILL.md`. Explanations and reasoning suggestions should be in Chinese, while field names and code examples should remain in their original English form.

These examples cover the automation lifecycle at the CLI request level.

For automation JSON authoring patterns, do not learn from these CLI invocations alone. Build `data.config` by following:

- `automation_config.md`
- `assets/automation_examples.md`

All examples assume `AQARA_ENDPOINT_URL` and `AQARA_OPEN_API_TOKEN` are available for the current command chain.

If either value is missing, configure the CLI first with `aqara config` or export the environment variables for the current shell. Do not write secrets into persistent shell profile files.

```bash
export AQARA_OPEN_API_TOKEN="your-bearer-token"
export AQARA_ENDPOINT_URL="https://aiot-open-3rd.aqara.cn/open/api"
```

## Query And Inspect

### List Automations

```bash
aqara automations list --definition-type SCRIPT_JSON --page-num 1 --page-size 50 --json
```

### List Automations (page 2)

```bash
aqara automations list --page-num 2 --page-size 20 --order-by "createTime desc" --json
```

### Get Automation Capabilities

OpenAPI note:

- `QueryAutomationCapabilitiesRequest.data` is not required by the schema
- if you send `data`, it must be an object
- do not copy the OpenAPI example that shows `data: ""`, because that example conflicts with the schema type

```bash
aqara automations capabilities --data-json "{}" --json
```

### Get Automation Details

```bash
aqara automations get auto_abc123 --json
```

## Create And Update

### Create Automation Request Wrapper

Use this only as the CLI submission example. The `config` object itself should be built from the dedicated automation JSON references.

Validate first:

```bash
aqara automations validate --config-file ./validated-config.json --json
```

```bash
aqara automations create --config-file ./validated-config.json --definition-type SCRIPT_JSON --json
```

Hard reminder:

- `data` must include `definitionType: "SCRIPT_JSON"` and `config`
- top-level `name` is optional; if omitted, the server can use `config.metadata.name`
- do not put `name`, `starters`, `condition`, or `actions` directly under `data`
- capability query must happen before authoring the final `config`

Successful create responses return the new `automationId` string in `data`.

### Update Automation Name Or Single Status

```bash
# Rename
aqara automations rename auto_abc123 --name "Night Mode" --json

# Disable
aqara automations disable auto_abc123 --json
```

For `name` or `enabled` updates, carry the current automation `definitionType`. The OpenAPI allows `SCRIPT_JSON`, `SCRIPT_TEXT`, or `WHEN_IF_THEN` for this path.

If `updateMask` contains `name`, the `name` value must not be empty or whitespace only.

### Update Automation Config

Use when triggers, conditions, actions, or scope change:

```bash
aqara automations update auto_abc123 --config-file ./validated-config.json --json
```

## Enable, Disable, And Delete

### Batch Enable/Disable Automations

```bash
# Enable multiple
aqara automations enable auto_abc123 auto_def456 --json

# Disable single
aqara automations disable auto_abc123 --json
```

The response may be partial success. Check `data.successIds` and `data.failedItems` before reporting the outcome.

### Delete Automations

```bash
# Single
aqara automations delete auto_abc123 --json

# Batch
aqara automations delete auto_abc123 auto_def456 --json
```

Delete responses may also be partial success. Check `data.successIds` and `data.failedItems`.
