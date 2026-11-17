# Client and Agent API reference

## Client commands

Run all commands from the Skill directory.

```bash
python3 scripts/famine_agent.py me
python3 scripts/famine_agent.py state
python3 scripts/famine_agent.py events --after-id 120
python3 scripts/famine_agent.py start --save-name "My Survival Log"
python3 scripts/famine_agent.py do --state-version VERSION --command-id ID
python3 scripts/famine_agent.py do --state-version VERSION --command-id ID --arguments '{"quantity":1}'
```

Optional global settings:

- `--api-base`: override `FAMINE_API_BASE_URL` for the current invocation. The default is `https://famine.aipmedia.cn`.
- `--timeout`: request timeout in seconds, default 20.
- `--state-file`: idempotency recovery file, default platform user-state directory.

`FAMINE_AGENT_TOKEN` is always read from the environment and must not be passed on the command line. `FAMINE_API_BASE_URL` is optional unless using a non-production server.

## Command types

The server can return:

- `TRAVEL`
- `WORLD_ACTION`
- `USE_ITEM`
- `EQUIP_ITEM`
- `BUILD`
- `BUILDING_ACTION`
- `COMBAT_ACTION`
- `NPC_INTERACTION`
- `SHOP_BUY`
- `SHOP_SELL`
- `POINT_STORE_EXCHANGE`
- `MARKET_CREATE`
- `MARKET_BUY`
- `MARKET_CANCEL`

Only execute a command present in the latest `availableCommands` array.

## Arguments

Each command contains an `arguments` object. Values such as these describe required input:

```json
{
  "quantity": { "type": "integer", "min": 1, "max": 5 },
  "unitPrice": { "type": "integer", "min": 1, "max": 1000000 }
}
```

Supply only actual values to `--arguments`:

```json
{ "quantity": 2, "unitPrice": 15 }
```

Other fields such as `energyCost`, `durationHours`, `cost`, and `requirements` are informational and must not be sent back unless the command explicitly describes them as integer input specifications.

## Errors

- `401`: Token is missing, expired, revoked, or lacks a scope. Stop and ask the user to create or configure a valid Token.
- `404`: The Token does not own the requested game. Run `me` and `state`; never try another game ID.
- `409`: State changed, an argument is invalid, or the command is no longer legal. Run `state` and decide again.
- `429`: Rate limit reached. Wait until the next minute before continuing.
- Network timeout: repeat the exact same `do` invocation. The client reuses the pending idempotency key.

Do not work around rejected commands by calling internal browser endpoints.
