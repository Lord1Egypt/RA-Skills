# Validated Feishu cron delivery pattern

## Observed failure modes

### Failure mode 1: main + systemEvent

Pattern:
- `sessionTarget: main`
- `payload.kind: systemEvent`

Observed result:
- cron run can be `ok`
- `lastDeliveryStatus` remains `not-requested`
- user receives nothing in Feishu

Interpretation:
- this pattern wakes internal session flow
- it is not a reliable user-visible outbound delivery pattern

### Failure mode 2: isolated + announce + channel:last

Pattern:
- `sessionTarget: isolated`
- `payload.kind: agentTurn`
- `delivery.mode: announce`
- `delivery.channel: last`

Observed result in this environment:
- run enters delivery path
- Feishu outbound returns HTTP 400
- user may see internal/heartbeat-visible evidence but not a Feishu message

Interpretation:
- `last` route fallback is not reliable enough for production Feishu delivery here

## Validated success pattern

Pattern:
- `sessionTarget: isolated`
- `payload.kind: agentTurn`
- `delivery.mode: announce`
- `delivery.channel: feishu`
- `delivery.accountId: ACCOUNT_ID`
- `delivery.to: user:OPEN_ID`

Observed result:
- one-shot smoke test delivered successfully to Feishu when explicit route fields were provided
- recurring report delivery also succeeded after switching to explicit Feishu routing

## Operational rule

For proactive Feishu delivery with hard expectations:
- always use explicit Feishu routing
- treat `channel:last` as optional debugging convenience, not the final delivery path
- validate with at least one smoke test before promising delivery SLAs
