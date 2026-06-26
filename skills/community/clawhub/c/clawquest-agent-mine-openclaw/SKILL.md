---
slug: clawquest-agent-mine-openclaw
name: ClawQuest: Agent Mine - OpenClaw Managed Mining
owner: "@zhzai30 - zhzai30"
version: 1.0.10
description: Managed mining over public game APIs using X-Api-Code authentication.
metadata:
  openclaw:
    requires:
      env:
        - REQUEST_TIMEOUT_MS
    emoji: "⛏️"
    homepage: ""
---

# ClawQuest: Agent Mine - OpenClaw Managed Mining

This Skill exposes managed mining tools for OpenClaw session workflows.

## Agent rules OpenClaw

Automated agents (including OpenClaw workflows) must follow these constraints:

- **Tools only**: Interact with the game **only** through this Skill’s **tool** HTTP API — `POST /tool/:name` on the skill-openclaw service, using the tool names documented below (`set_api_code`, `check_mining_state`, `start_managed_mining_loop`, etc.). Do **not** call the upstream game **`/api/*`** endpoints directly from the agent, custom scripts, or curl unless this Skill explicitly documents that path as a supported tool (it does not for raw `/api/*`).
- **Do not modify source**: Do **not** edit, patch, or fork the `skill-openclaw` source tree, `package.json`, or runtime code to “fix” behaviour. Use documented environment variables and this `SKILL.md` only.
- **Report errors; do not self-heal in code**: If a tool fails or behaviour is unexpected, **report** the failure (HTTP status, response body, tool name, `cacheKey`, timestamps, logs). Do **not** rewrite Skill code, inject alternate HTTP clients, or bypass the tool layer as a workaround.

## API Contract

All mining and stamina APIs require `X-Api-Code`.

- `POST /api/startMining`
- `POST /api/checkMiningState`
- `POST /api/endMining`
- `POST /api/setAutoMining`
- `POST /api/buyStamina`
- `POST /api/getStamina`

(Internal round flow still uses `POST /api/setAutoMining`, `POST /api/startMining` and `POST /api/endMining` via the managed loop implementation; they are not exposed as Skill tools.)

Authentication:

- Header: `X-Api-Code: <apiCode>`

The Skill does not perform game client login. Users must provide `apiCode` generated in-game.

## State Codes

`check_mining_state` returns `apiState` and `miningState`. Numeric values map as follows.

**apiState**

| Value | Name        |
| ----- | ----------- |
| 0     | ApiInactive |
| 1     | ApiInUse    |
| 2     | ApiClosing  |
| 3     | ApiActive   |

**miningState**

| Value | Name                |
| ----- | ------------------- |
| 0     | MiningIdle          |
| 1     | MiningInProgress    |
| 2     | MiningRewardPending |

## Tools

### set_api_code

Persist an `apiCode` for later calls.

Inputs:

- `apiCode` (required)
- `cacheKey` (optional, default: `default`)

### get_api_code

Read the cached `apiCode`.

Inputs:

- `cacheKey` (optional, default: `default`)

### clear_api_code

Delete the cached `apiCode`.

Inputs:

- `cacheKey` (optional, default: `default`)

### check_mining_state

Query API activation status and mining state. Returns `apiState` and `miningState` (see [State Codes](#state-codes)).

Inputs:

- `apiCode` (optional, falls back to cache)
- `cacheKey` (optional, default: `default`)

### buy_stamina

Buy stamina using diamonds.

Inputs:

- `apiCode` (optional, falls back to cache)
- `cacheKey` (optional, default: `default`)

### get_stamina

Get stamina and diamonds.

Inputs:

- `apiCode` (optional, falls back to cache)
- `cacheKey` (optional, default: `default`)

### start_managed_mining_loop

Start managed loop execution.

Flow:

1. `start_mining` — abort on error
2. wait for `estimatedEndAt`
3. loop `end_mining` — retry on error, round complete on success
4. record reward
5. wait round interval and continue

Inputs:

- `apiCode` (optional, falls back to cache)
- `cacheKey` (optional, default: `default`)
- `lang` (optional)
- `pollingIntervalMilliseconds` (optional)
- `roundIntervalMilliseconds` (optional)
- `maxConsecutiveErrorCount` (optional)
- `autoBuyStamina` (optional)
- `autoBuyStaminaMaxFailures` (optional)
- `forceRestart` (optional)

### start_mining_session

Same as `start_managed_mining_loop` with OpenClaw session binding and event stream.

### get_mining_session_events

Read incremental session events.

Inputs:

- `sinceEventId` (optional, default: `0`)

### get_mining_quick_status

Read lightweight managed loop status.

### get_managed_mining_status

Read full managed loop status.

### stop_managed_mining_loop

Request safe stop for running managed loop.

## Deprecated Tools

- `start_auto_mining` (deprecated)
- `stop_auto_mining` (deprecated)

## Suggested Call Order

1. `set_api_code` (one-time setup)
2. `start_mining_session`
3. (optional) call `get_mining_quick_status` or `get_mining_session_events` on demand — do **not** set up automatic periodic polling by default
4. call `stop_managed_mining_loop` when needed

## Error Codes

All API responses include a `code` field. `0` means success; non-zero values indicate an error.

### Common Errors

| Code | Name                | Description                                                       |
| ---- | ------------------- | ----------------------------------------------------------------- |
| 400  | InvalidParams       | Invalid or missing parameters (e.g. empty `X-Api-Code` header)    |
| 401  | AuthFailed          | Authentication failed (invalid `apiCode`)                         |
| 500  | InternalServerError | Server internal error                                             |
| 1010 | NotEnoughResources  | Insufficient resources (diamonds not enough for stamina purchase) |

### Mining Errors

| Code | Name                  | Description                                                                                                          |
| ---- | --------------------- | -------------------------------------------------------------------------------------------------------------------- |
| 2003 | InsufficientResources | Insufficient stamina to start mining                                                                                 |
| 2008 | DiamondNotEnought     | Insufficient diamonds                                                                                                |
| 2009 | MiningStateConflict   | Mining state conflict (e.g. calling `startMining` while already in progress, or `endMining` when not mining via API) |
| 2014 | MiningApiNotActive    | API mining feature not activated for this player                                                                     |
| 2018 | MiningNotFinished     | Mining not finished yet (current time has not reached `estimatedEndAt`)                                              |

## Environment Variables

| Variable                                     | Description                                                                |
| -------------------------------------------- | -------------------------------------------------------------------------- |
| `GAME_API_BASE_URL`                          | Optional API base URL override (default: `https://api.km.cocweb3.com`)     |
| `REQUEST_TIMEOUT_MS`                         | Request timeout in milliseconds (default: `8000`)                          |
| `MANAGED_MINING_POLL_INTERVAL_MS`            | Default polling interval in milliseconds (default: `1000`)                 |
| `MANAGED_MINING_ROUND_INTERVAL_MS`           | Default round interval in milliseconds (default: `2000`)                   |
| `MANAGED_MINING_MAX_CONSECUTIVE_ERROR_COUNT` | Consecutive error stop threshold (default: `10`)                           |
| `MANAGED_MINING_AUTO_BUY_STAMINA`            | Enable auto-buy on stamina insufficient: `1` or `true`                     |
| `MANAGED_MINING_AUTO_BUY_MAX_FAILURES`       | Consecutive auto-buy failures stop threshold (default: `3`)                |
| `MINING_SESSION_MAX_EVENTS`                  | Ring buffer size for events (default: `200`)                               |
| `API_CODE_STORE_PATH`                        | Path for cached apiCode store (default: `./data/api-code-store.json`)      |
| `ORE_TYPE_NAME_MAP_PATH`                     | Path for ore type display name map (default: `./config/ore-type-map.json`) |
