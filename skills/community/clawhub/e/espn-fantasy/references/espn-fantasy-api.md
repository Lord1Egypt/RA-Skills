# ESPN Fantasy Football API

After login you have `espn_s2` + `SWID`. Use them as cookies. This is far more reliable
than clicking the web UI.

## Auth

Send both cookies on every request:

```
Cookie: espn_s2=<value>; SWID=<value>
```

Key identifiers you'll need (get from the user or discover via the fan API below):
`leagueId`, `season` (year), `teamId` (your team), `scoringPeriodId` (week).

## Discover leagues / team id

```
GET https://fan.api.espn.com/apis/v2/fans/{SWID}?includeView=preferences
```
or the site endpoint. Your `teamId` also shows in the league settings.

## Read API (base)

```
https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{season}/segments/0/leagues/{leagueId}
```

Useful `?view=` values (comma-separated):

- `mSettings` — league size, roster slots, scoring
- `mTeam` — all teams (find yours by owner `SWID`)
- `mRoster` — rostered players per team
- `mMatchup` / `mScoreboard` — current-week matchups & scores
- `mStandings` — records
- `mTransactions2` — recent adds/drops
- `kona_player_info` — player pool (with `X-Fantasy-Filter` header for paging)

Players endpoint (skinnable via `X-Fantasy-Filter`):

```
GET .../seasons/{season}/segments/0/leagues/{leagueId}?view=kona_player_info
Header: x-fantasy-filter: {"players":{"limit":200,"sortPercOwned":{"sortAsc":false}}}
```

## Write API — setting a lineup

```
POST https://lm-api-writes.fantasy.espn.com/apis/v3/games/ffl/seasons/{season}/segments/0/leagues/{leagueId}/transactions/
Headers: Cookie: espn_s2=...; SWID=...   Content-Type: application/json
         x-fantasy-source: kona
```

Lineup body (move a player from bench slot 20 into a starting slot 0):

```json
{"transactions":[{
  "type":"LINEUP",
  "memberId":"{SWID}",
  "scoringPeriodId": <week>,
  "executionType":"EXECUTE",
  "items":[{"playerId": <id>, "type":"LINEUP", "fromLineupSlotId": 20, "toLineupSlotId": 0}]
}]}
```

- `fromLineupSlotId: 20` = bench; `toLineupSlotId` = target slot id (0=QB, 2=RB, 4=WR, 6=TE,
  16=D/ST, 17=K, 23=FLEX, ...). Slot ids come from `mSettings`.
- Adds/drops reuse the same `transactions/` endpoint with type `FREEAGENT` and
  `items` of type `ADD`/`DROP`.

> ⚠️ Verify against a real league before trusting: these write shapes are from ESPN's
> private API and change occasionally. Do a benign read first to confirm slot ids and
> `playerId`s, and test a no-op lineup move.

## Practical tips

- Always read `mSettings` + `mRoster` first to confirm leagueId/teamId/slot ids.
- A write returns the applied transaction; a 401/403 means the session/`espn_s2` is stale
  → re-run the login skill.
- Rate-limit reads; ESPN is not a firehose. Cache within a session.

## WRITE API — VERIFIED 2026-10-01

**Endpoint:** `POST https://lm-api-writes.fantasy.espn.com/apis/v3/games/ffl/seasons/{season}/segments/0/leagues/{leagueId}/transactions/?platformVersion={build}`
**Headers (all required):** `Cookie: espn_s2=..; SWID=..`, `Content-Type: application/json`,
`x-fantasy-source: kona`, **`x-fantasy-platform: espn-fantasy-web`**, `Referer: https://fantasy.espn.com/`

**BODY = ONE bare transaction object** (NOT `{"transactions":[...]}`, and **NO `memberId`**):
```json
{"isLeagueManager":false,"teamId":3,"type":"FREEAGENT","scoringPeriodId":4,"executionType":"EXECUTE",
 "items":[{"playerId":ADD_ID,"type":"ADD","toTeamId":3},
          {"playerId":DROP_ID,"type":"DROP","fromTeamId":3}]}
```
- **Lineup:** `"type":"LINEUP"`, items `[{"playerId":ID,"type":"LINEUP","fromLineupSlotId":A,"toLineupSlotId":B}]`
- **Add alone fails if roster is full** (`FAILED_ROSTERLIMIT`) — pair ADD with a DROP.
- 200 response = the applied transaction (with `"isPending":false`).

⚠️ **Gotcha that cost hours:** wrapping in `{"transactions":[...]}` and/or including `memberId`
→ **400 `{"messages":["Invalid Input."]}`**. Keep it bare, no memberId. (`x-fantasy-platform`
was also the missing header in early attempts.)

**Quick Lineup (auto-set optimal lineup):**
`POST .../leagues/{id}/teams/{teamId}/recommendations?lineupScoringPeriodId={wk}&recommendationTypeId=LINEUP&restOfWeek=true&platformVersion={build}`
with body `{}` — ESPN computes + **applies** the optimal lineup server-side. Verified working.

**Discovery trick:** to learn any write payload, open the action in the headed browser and log
`page.on('request')` for `lm-api-writes`. (This is how the format above was found.)

## Propose a trade (VERIFIED 2026-10-01)

Same bare-object shape on `/transactions/`, `type: "TRADE_PROPOSAL"`:
```json
{"isLeagueManager":false,"teamId":3,"type":"TRADE_PROPOSAL","scoringPeriodId":4,"executionType":"EXECUTE",
 "items":[{"playerId":4360761,"type":"TRADE","fromTeamId":3,"toTeamId":2},
          {"playerId":4569987,"type":"TRADE","fromTeamId":2,"toTeamId":3}]}
```
- One `TRADE` item per player, with `fromTeamId`/`toTeamId` on each.
- Responds 200 with `"isPending":true` and an `expirationDate` (~2 days). Offer is sent to the other team.
- (`type:"TRADE"`, `executionType:"PROPOSAL"`, or an extra `toTeamId` all 400 → use exactly the above.)
- Accept/reject an incoming offer: same endpoint, likely `type:"TRADE_ACCEPT"` with a `transactionId` (not yet verified).

## Lineup moves — type is "ROSTER" (NOT "LINEUP")  (verified 2026-10-01)

```json
{"isLeagueManager":false,"teamId":3,"type":"ROSTER","scoringPeriodId":4,"executionType":"EXECUTE",
 "items":[{"playerId":4685382,"type":"LINEUP","fromLineupSlotId":2,"toLineupSlotId":20}]}
```
- Top-level `type` = **"ROSTER"**; each item's `type` = "LINEUP" with from/to slot ids.
- `type:"LINEUP"` at the top level → 400 Invalid Input. Multi-item ROSTER transactions also 400'd;
  send **one move per call** (outgoing players to bench first, then incoming).
