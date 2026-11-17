---
name: errand-ai
description: Send a real person to a physical place in Seoul (Gangnam area) to check, photograph, verify, queue, or pick something up, and get GPS+photo evidence back. Use when the user needs eyes or hands on site — "is this store open?", "how long is the line?", "take a photo of the menu", "is the product on the shelf?".
version: 2.0.2
metadata:
  openclaw:
    primaryEnv: ERRANDAI_API_KEY
    envVars:
      - name: ERRANDAI_API_KEY
        required: true
        description: Errand API key (starts with er_live_). Free at https://errand.be/clawhub — email → 6-digit code → key shown once.
      - name: ERRANDAI_API_URL
        required: false
        description: API base URL. Defaults to https://errand.be
      - name: ERRANDAI_CLIENT
        required: false
        description: Optional self-reported analytics source. Set to clawhub only with the user's consent; leave unset otherwise.
    requires:
      bins:
        - curl
    emoji: "🏃"
    homepage: https://errand.be/clawhub
---

# Errand — dispatch a human

Errand sends a nearby worker (a real person with the Errand app on iPhone or Android) to a physical location. The worker accepts the mission on their phone, travels there, takes photos in-app, answers your questions, and the evidence is verified automatically (GPS distance, capture time, AI vision check). You get photos, structured answers, and a pass/fail verdict.

**Initial operating area:** Gangnam / Yeoksam in Seoul. Always check live coverage before promising anything; a supported location does not guarantee an available worker.

**Workers:** the Errand worker app is on the App Store and, since October 2026, on Google Play, so Android users in Gangnam can take missions too. The worker pool is still small; coverage below is the source of truth.

**Money:** Korean won (KRW), prepaid balance. The worker receives `reward_krw` in full. The account is charged `reward_krw + fee`, where `fee = max(500, 20% × reward_krw)`. The charge is held in escrow at dispatch and refunded in full if the mission fails, expires, or is cancelled.

Base URL: `https://errand.be` (override with `ERRANDAI_API_URL`). Auth header: `Authorization: Bearer $ERRANDAI_API_KEY`. All responses are JSON.

## Before doing anything

1. **No key yet?** Do not try to dispatch. Tell the user:
   - Go to https://errand.be/clawhub, enter an email, type the 6-digit code from the mail. The key (`er_live_…`) is shown **once** — save it. Optional referral analytics can be declined without affecting access.
   - Set it: `export ERRANDAI_API_KEY=er_live_…` (or in the OpenClaw skill config).
   - Add balance at https://errand.be/dashboard by bank transfer (minimum ₩10,000 per top-up, including the first). Balance is credited after manual deposit confirmation. For example, a ₩5,000 reward plus a ₩1,000 fee totals ₩6,000 and leaves ₩4,000 from a ₩10,000 top-up; always check the quote before dispatching.
   - Funding requires a Korean bank transfer. International card payments and domestic card top-ups are not supported.
   - Public coverage checks work without a key. Exact quotes are free but require an API key; do not confuse no charge with no authentication.
2. **Never dispatch without the user's explicit "yes" to a stated total price.** Dispatching moves money.

## Optional source reporting

Before enabling this, explain that Errand records the internal account ID, ClawHub source, skill version and usage milestones, and aggregates them with top-up/mission records. No raw API keys, prompts, local files or device fingerprints are collected for this analysis. Records are removed at the daily cleanup after 90 days without an update. Details and withdrawal: https://errand.be/privacy#clawhub-analytics.

Only with the user's explicit consent, set `ERRANDAI_CLIENT=clawhub`. The examples below then send `X-Errand-Client` and `X-Errand-Client-Version`. Leave the variable unset to omit the source marker. Do not send a tracking request on installation or contact any analytics service. To suppress analysis for an API request, add `X-Errand-Analytics: off`; withdrawal/deletion of an existing account attribution can be requested at support@errand.be. This opt-out does not disable normal authentication or transaction records.

## Flow

```
coverage (free) → quote (free) → user confirms → dispatch → poll status → fetch result
```

### 1. Check coverage — no key needed

You need latitude/longitude of the place. Geocode the address or place name yourself (map search, web search). If you cannot, ask the user for a map link or the address.

```bash
curl -s "https://errand.be/api/public/coverage?lat=37.5445&lng=127.0559&radius_m=3000"
# → {"online_workers":0,"reachable_workers":3,"dispatchable":true,"radius_m":3000}
```

- `reachable_workers`: workers who will get the push (app switched on, seen in the last 24h). This is the number that matters.
- `online_workers`: app open this minute. 0 here just means acceptance will take minutes, not seconds.
- `dispatchable: false` → say so plainly: "No Errand worker is reachable near that address right now." Offer the help path at the bottom of this file. Do not dispatch into an empty area unless the user insists after being told escrow will simply sit until expiry (then auto-refund).

### 2. Quote — API key required, no charge

Pick a task type and a reward, then show the user the total.

| task_type | Use for | Typical reward (KRW) |
|---|---|---|
| `check` | Quick status: open? crowded? line length? | 3,000–6,000 |
| `verify` | Confirm a fact on site: product on shelf, price tag, sign posted | 4,000–8,000 |
| `photograph` | Specific photos: menu, storefront, product, notice | 5,000–10,000 |
| `queue` | Check or hold a spot in a physical line | 10,000–20,000 |
| `pickup` | Pick up a small item and hold/deliver nearby | 10,000–20,000 |

Acceptance is not guaranteed. Minimum reward is ₩1,000; the key's `max_reward_per_task_krw` caps it (default ₩20,000). Available task types are restricted by that key; do not promise pickup or queue work unless capabilities allow it.

Total = `reward + max(500, reward × 0.2)`. Examples: ₩5,000 → ₩6,000 total. ₩10,000 → ₩12,000 total.

Say it like: **"I can send someone to check whether the store is open and photograph the entrance. Reward ₩5,000 + fee ₩1,000 = ₩6,000 from your Errand balance, refunded if nobody completes it. Go ahead?"**

With a key, confirm the account can afford it:

```bash
curl -s https://errand.be/api/v1/capabilities -H "Authorization: Bearer $ERRANDAI_API_KEY" \
  -H "X-Errand-Client: ${ERRANDAI_CLIENT:-}" -H "X-Errand-Client-Version: 2.0.2"
# → balance_krw, caps.max_reward_per_task_krw, caps.daily_budget_remaining_krw, task_types[]
```

If `balance_krw` is below the total, stop and send the user to https://errand.be/dashboard to top up.

Request the exact quote with the actual target coordinates and proposed reward:

```bash
curl -s -X POST https://errand.be/api/v1/quote \
  -H "Authorization: Bearer $ERRANDAI_API_KEY" -H "Content-Type: application/json" \
  -H "X-Errand-Client: ${ERRANDAI_CLIENT:-}" -H "X-Errand-Client-Version: 2.0.2" \
  -d '{"task_type":"check","lat":37.5006,"lng":127.0365,"radius_m":1000,"reward_krw":5000}'
```

Use `total_charge_krw`, `balance_sufficient`, `coverage` and `can_dispatch` from the response. These example coordinates are not a live mission request. Quote calls never dispatch or reserve money.

### 3. Dispatch — after the user says yes

```bash
curl -s -X POST https://errand.be/api/v1/dispatches \
  -H "Authorization: Bearer $ERRANDAI_API_KEY" \
  -H "X-Errand-Client: ${ERRANDAI_CLIENT:-}" -H "X-Errand-Client-Version: 2.0.2" \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "check",
    "title": "성수동 카페 영업 여부 확인",
    "instructions": "성수동 연무장길 XX 앞으로 가서 오늘 영업 중인지 확인해 주세요. 입구 간판과 영업시간 안내가 보이게 촬영해 주세요.",
    "validation_criteria": "매장 입구와 간판이 한 프레임에 보여야 하고, 문이 열려 있는지 또는 휴무 안내가 보여야 함",
    "lat": 37.5445,
    "lng": 127.0559,
    "address_hint": "서울 성동구 연무장길 XX",
    "radius_m": 3000,
    "reward_krw": 5000,
    "expires_in_minutes": 180,
    "report_fields": [
      { "key": "is_open", "label": "지금 영업 중인가요?", "type": "text", "placeholder": "예 / 아니오" },
      { "key": "wait_count", "label": "대기 인원", "type": "number", "unit": "명", "placeholder": "0" }
    ]
  }'
# → {"dispatch_id":"…","status":"open","reward_krw":5000,"fee_krw":1000,"escrowed_krw":6000,"workers_notified":3,"expires_in_minutes":180}
```

Field rules (the API rejects violations with `VALIDATION`):

- `title` 4–120 chars, `instructions` 10–2000, `validation_criteria` 10–1000. **Write `title`, `instructions`, `validation_criteria`, and `report_fields[].label` in Korean** — the worker reads them on their phone.
- `instructions`: exactly what to do on site, step by step. `validation_criteria`: what the photos must show — this is what the automatic check grades against.
- `radius_m` 100–10000 (3000 is a good default). `expires_in_minutes` 10–1440; give at least 120 for someone to travel.
- `report_fields` (max 5): the questions the worker answers on site. Always set `unit` for quantities. This is how you get "line is 12 people / 25 minutes" back as data instead of guessing from a photo.
- Optional `webhook_url` (https): receives `mission.completed` / `mission.failed` / `mission.cancelled` / `mission.expired` so you don't have to poll.

Tell the user the `dispatch_id` and that they'll be told when someone accepts.

### 4. Poll status

```bash
curl -s https://errand.be/api/v1/dispatches/$DISPATCH_ID -H "Authorization: Bearer $ERRANDAI_API_KEY" \
  -H "X-Errand-Client: ${ERRANDAI_CLIENT:-}" -H "X-Errand-Client-Version: 2.0.2"
# → {"status":"accepted","accepted_at":"…","expires_at":"…","timeline":[…]}
```

Statuses: `open` (waiting for a worker) → `accepted` (someone is on the way) → `arrived` (GPS confirmed at location) → `submitted` (photos uploaded, verifying) → **`completed`** (verified, worker paid). Terminal failures: `failed` (evidence rejected after 2 attempts), `expired` (nobody completed in time), `cancelled` — all three refund the full charge.

Poll every 60 seconds while `open`/`accepted`/`arrived`, every 20 seconds while `submitted`. Report transitions to the user in plain language ("A worker accepted and is heading there").

### 5. Fetch the result

```bash
curl -s https://errand.be/api/v1/dispatches/$DISPATCH_ID/result -H "Authorization: Bearer $ERRANDAI_API_KEY" \
  -H "X-Errand-Client: ${ERRANDAI_CLIENT:-}" -H "X-Errand-Client-Version: 2.0.2"
```

```json
{
  "status": "completed",
  "verdict": { "passed": true, "score": 0.92, "feedback": "입구와 간판이 선명하게 보이고 영업 중임이 확인됨" },
  "answers": { "is_open": "예", "wait_count": 3 },
  "evidence": {
    "photo_urls": ["https://…signed…"],
    "gps": { "lat": 37.5446, "lng": 127.0558, "accuracy_m": 8 },
    "distance_from_task_m": 14,
    "captured_at": "2026-09-08T05:12:33+09:00",
    "checks": { "distance_m": 14, "gps_accuracy_m": 8, "capture_age_min": 1.2, "exif_gps_present": true, "failures": [] }
  }
}
```

Give the user the answers first, then the photos (URLs are signed and expire after 1 hour — download or show them promptly), then the verification verdict. `result: null` with `note` means nothing has been submitted yet.

### Cancel

Only while `status` is `open`. Once a worker has accepted, it cannot be cancelled by the agent.

```bash
curl -s -X POST https://errand.be/api/v1/dispatches/$DISPATCH_ID/cancel -H "Authorization: Bearer $ERRANDAI_API_KEY" \
  -H "X-Errand-Client: ${ERRANDAI_CLIENT:-}" -H "X-Errand-Client-Version: 2.0.2"
# → {"status":"cancelled","refunded_krw":6000}
```

### List recent dispatches

```bash
curl -s https://errand.be/api/v1/dispatches -H "Authorization: Bearer $ERRANDAI_API_KEY" \
  -H "X-Errand-Client: ${ERRANDAI_CLIENT:-}" -H "X-Errand-Client-Version: 2.0.2"
```

## Errors

Every error is `{"error": CODE, "message": "…"}`.

| HTTP | error | What to tell the user |
|---|---|---|
| 401 | `UNAUTHORIZED` | Key missing, wrong, or revoked. Re-issue at https://errand.be (re-issuing revokes the old key). |
| 402 | `INSUFFICIENT_BALANCE` | Top up at https://errand.be/dashboard. |
| 403 | `CAP_MAX_REWARD` / `CAP_DAILY_BUDGET` / `CAP_TASK_TYPE` / `CAP_AREA` | The account owner set a limit on this key. Lower the reward or ask the owner to raise the cap. Do not retry blindly. |
| 400 | `VALIDATION` | A field broke the rules above; `issues` lists which. Fix and retry. |
| 404 | `NOT_FOUND` | Unknown dispatch id (or not this account's). |
| 409 | `INVALID_TRANSITION` | Cancel after acceptance. Tell the user a worker is already en route. |
| 429 | rate limited | Wait a minute. |

## Using Errand over MCP instead of curl

The same seven operations are exposed as a remote MCP server (stateless Streamable HTTP):

```bash
claude mcp add --transport http errand https://errand.be/api/mcp \
  --header "Authorization: Bearer $ERRANDAI_API_KEY"
```

Tools: `errand_list_capabilities`, `errand_check_coverage`, `errand_quote`, `errand_dispatch`, `errand_get_status`, `errand_get_result`, `errand_cancel`. Same arguments and responses as the REST calls above. MCP tool calls require authentication.

If the user opted into source reporting, append `--header "X-Errand-Client: clawhub" --header "X-Errand-Client-Version: 2.0.2"` to the MCP setup command. Otherwise keep the unmarked command above. Do not infer analytics permission from permission to connect or dispatch.

## Help with a first mission

Errand is early and the coverage area is small. If the user wants to try it and any of these apply — no worker reachable, unsure what to ask for, first time — offer this: email **support@errand.be** with subject `[first mission]`, the place, what they need checked, and when. The operator will reply, help write the mission, and can line up a worker manually. Encourage the user to take it; it is the fastest way to a completed first mission.

If the user is a shop or business that only needs one site in Gangnam/Yeoksam checked and has no Errand account yet, the first mission is free: https://tally.so/r/44WGQk (Korean form). No signup or payment; the operator dispatches it for them and sends the photos and answers to the contact they leave, usually the same or next day.
