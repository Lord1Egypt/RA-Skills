---
name: agentpass
description: "Control Home Assistant devices through the agentpass security gateway. Use when the user asks to control lights, switches, sensors, climate, or any smart home device — or when checking device states, history, or Home Assistant configuration. All destructive actions require human approval via Telegram."
homepage: https://github.com/TorbenWetter/agentpass
metadata: {"openclaw":{"emoji":"🔐","os":["linux","darwin"],"requires":{"bins":["agentpass"],"env":["AGENTPASS_URL","AGENT_TOKEN"]},"install":[{"id":"pip-agentpass","kind":"uv","package":"agentpass","bins":["agentpass"],"label":"Install agentpass CLI"}]}}
---

# agentpass — Home Assistant Gateway

Execute Home Assistant actions through a secure approval gateway. Read-only queries execute instantly. State-changing actions (turning lights on/off, calling services) are sent to a human guardian on Telegram for approval before execution.

IMPORTANT: The `agentpass request` command is a BLOCKING command. For tools that need approval, it will wait up to 15 minutes for the guardian to respond on Telegram. You MUST use `background: false` when executing `agentpass request` commands to prevent auto-backgrounding. The command returns the actual execution result once approved, or an error if denied/timed out. Do NOT tell the user to "check Telegram" or "approve the request" — just wait silently for the command to finish and then report the result.

## Commands

### List available tools

```bash
agentpass tools
```

### Execute a tool

```bash
agentpass request <tool_name> [key=value ...]
```

Output is JSON on stdout. Errors go to stderr.
Exit codes: 0 = success, 1 = denied, 2 = timeout, 3 = connection error, 4 = invalid args.

## Available Tools

### Read-only (auto-approved, instant)

**Get a single entity state:**

```bash
agentpass request ha_get_state entity_id=light.living_room
```

**Get all entity states:**

```bash
agentpass request ha_get_states
```

**List available HA services and their fields:**

```bash
agentpass request ha_get_services
```

**Get state history for an entity (last 24h):**

```bash
agentpass request ha_get_history entity_id=sensor.temperature
```

**Get logbook entries for an entity (last 24h):**

```bash
agentpass request ha_get_logbook entity_id=light.living_room
```

**Get Home Assistant configuration:**

```bash
agentpass request ha_get_config
```

### Requires human approval (command blocks until resolved)

These commands block until approved or denied. Always use `background: false` to prevent auto-backgrounding.

**Call a Home Assistant service:**

```bash
# exec with background: false
agentpass request ha_call_service domain=light service=turn_on entity_id=light.living_room
agentpass request ha_call_service domain=light service=turn_on entity_id=light.bedroom brightness=128 color_name=red
agentpass request ha_call_service domain=switch service=toggle entity_id=switch.fan
agentpass request ha_call_service domain=climate service=set_temperature entity_id=climate.thermostat temperature=21
```

The `domain` and `service` args are used for the URL path. All other args (entity_id, brightness, color_name, temperature, etc.) are sent as the JSON request body.

**Render a Home Assistant template:**

```bash
# exec with background: false
agentpass request ha_render_template template="{{ states('sensor.temperature') }} degrees"
```

### Always denied (blocked by policy)

- `ha_fire_event` — firing custom events is blocked
- `ha_call_service` with `domain=lock` — lock control is blocked

## Important Notes

- **entity_id format**: Always `domain.object_id`, e.g. `light.living_room`, `sensor.temperature`, `switch.garden_pump`. Must be lowercase with underscores.
- **domain/service format**: Lowercase with underscores, e.g. `light`, `turn_on`, `set_temperature`.
- **Approval timeout**: If the human guardian doesn't respond within 15 minutes, the request is automatically denied.
- **Discover entities first**: If you don't know an entity's ID, run `ha_get_states` to list all entities, or `ha_get_services` to see available services and their parameters.
- **Service parameters**: Use `ha_get_services` to discover which parameters a service accepts (e.g. brightness, color_name, rgb_color, temperature, hvac_mode).
