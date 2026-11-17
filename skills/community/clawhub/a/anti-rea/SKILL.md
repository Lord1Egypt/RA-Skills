---
name: anti-rea
description: >-
  Integrate the antiRea npm library (@dannyphan190/anti-rea) into a host web application to meter dataset access per identity and detect automated abuse: per-identity record budgets that cap bulk extraction and cloning, slow per-identity harvesting, republication of derived data, enumeration walks, and coordinated bot cohorts such as scheduler-driven herds and reconnect storms - including, in shared rooms and communities, seat squatting and vote brigading. Version 2.8.0 adds the combined room guard and an evidence layer: config provenance hashes, verified-neutral identity facts, single-use step-up proofs and evidentiary roles. Version 2.8.1 adds a span gate to the two phase signals: a member counts toward a confirmed cohort only when its observed event span covers at least one full grid period. Version 2.9.0 adds the surface guard - field-level control of what enters and leaves the server - and documents the declared-cohort union budget pattern. Version 2.9.2 hardens Unicode token checks, retained state, late events and invalid-input handling without enabling enforcement. Version 2.9.3 adds the shadow decoy graph - decoy record sets with full referential consistency that survive offline reconstruction filtering - plus issued-at checks on the pagination and echo tokens, and host-supplied vocabularies for decoy documents. Version 3.0.0 adds tier-2 conversion for the C27 and C35 signals (opt-in soft step-down toward a 500-record floor and decoy first-touch taint with step-up), bulk capability keys that put dataset tails behind server-issued keys, and the opt-in FC-07 pin novel statistic. Version 2.9.1 adds the ownership probe (BOLA/IDOR sweeps across many owners), the early-minimal occupancy counter to the A1 squat, a machine-readable 402 step-up answer (no settlement), the preference declaration log that pairs with the value watermark, and three calibration utilities (volume rank, EMP-MIX threshold selection, hold-type session features). Use when a developer reports bulk scraping, one account quietly draining a dataset, coordinated account groups acting as one machine, or floods of fresh accounts. Every signal is advisory (enforcement: "none") - the host code decides the response, and step-up applies to new actions only.
license: MIT
compatibility: Requires Node.js >= 20 and the npm package @dannyphan190/anti-rea, wired server-side at the application layer. Examples are TypeScript; plain JavaScript works the same way.
metadata:
  version: "3.0.0"
  npm-package: "@dannyphan190/anti-rea"
  source-repository: "https://github.com/dankezo/antiRea"
---

# antiRea integration skill

You are wiring antiRea into a host application on behalf of a developer. antiRea is a server-side TypeScript library (Node >= 20, zero runtime dependencies) that meters dataset access per identity and measures coordinated automated abuse; the host application decides what to do with its output. This skill covers antiRea 3.0.0.

Install:

```bash
npm install @dannyphan190/anti-rea
```

Read the ground rules first - they override any pattern you find elsewhere. Then find the developer's symptom in the decision tree, wire the matching module exactly as its section shows, and finish with the post-integration verification checklist.

## Ground rules (read before writing any code)

1. **Every antiRea signal is advisory.** Every result object carries `enforcement: "none"`. antiRea measures and reports; **your host code** decides what happens. There is no module in this package that blocks, bans, or throttles anyone by itself.
2. **Never hard-block on advisory output.** The strongest legitimate reaction to a signal is a *step-up* (an extra verification challenge) for **new** actions, wired through `createVerificationGrace`. A signal is evidence, not a verdict about a person.
3. **Never apply consequences to people already inside.** For live rooms specifically: members already in the room are never kicked, muted, or down-ranked because a room-level signal fired. Signals gate **new joins only**.
4. **Defaults are lab-frozen, not suggestions.** Thresholds in the modules below were fixed before the lab ran and validated against pre-registered false-positive budgets. Do not "tune" them silently. If a host's traffic differs, say so in the integration notes and keep the defaults until the host has its own measurements.
5. **All lab numbers are simulation numbers.** They were measured on seeded synthetic populations, not on the host's real traffic. Present them that way in any summary you write for the developer.
6. **antiRea works at the application layer.** It sees joins, actions, and serves - not packets. Network-layer volumetric DDoS is out of scope: that layer belongs to the hosting/CDN provider (e.g. Cloudflare). Do not promise DDoS protection from this package.

## Decision tree: symptom -> shape -> module

| What the developer reports | Likely shape | Reach for | Section |
|---|---|---|---|
| "Our live room crashes / freezes when bots swarm in" | Join flood at the application layer (hundreds of fresh accounts joining at once, then doing nothing) | Meter + step up **new joins** under pressure: `createVerificationGrace` `guardStepUp` driven by your own join-rate check; feed joins to `createHerdPhaseSignal` for the fleet picture | A, B |
| "The karaoke seats are always full of silent accounts" | Seat squatting: fresh accounts take limited seats and hold them with zero activity | `createSeatOccupancySignal` (one instance per room; step up **new** seat claims via Section B while it flags) | C, B |
| "Bots keep rejoining / retrying on a fixed rhythm" | One scheduler driving a fleet: joins/retries phase-locked to a shared timer | `createHerdPhaseSignal` | A |
| "A whole group of accounts moves like one machine, but no single account misbehaves" | One scheduler driving a cohort: the group's timing points pile onto one spot of the phase plane | `createHerdTightnessSignal` (needs a reference stream from established users; cohort-level evidence, names nobody) | H |
| "Chat / emotes arrive in machine-locked bursts" | A fleet that joined normally but acts on one shared scheduler | `createActivityPhaseSignal` on ONE activity stream, evaluated scoped | D |
| "Songs keep getting skip-voted by brand-new accounts" | Vote brigading: fresh accounts voting together, song after song | `createVoteBrigadingSignal` (room state; step up new voters while it flags) | E |
| "Something is crawling all our rooms / member lists" | Room enumeration: one account joining room after room | `createRoomHopSignal` (step up the named identities) | F |
| "The realtime server keeps dying and reviving at night" | Reconnect storm: sources cycling connect/disconnect at sub-second cadence | `createReconnectStormSignal` on your socket connect/disconnect hooks; enforce backoff host-side | G |
| "Accounts cycle join -> leave -> join constantly" | Churn against presence/connection limits | `createHerdPhaseSignal` on the join stream (the cycle is a repeated event), plus host-side join-rate metering | A |
| "The room as a whole is under attack - floods, slow drips, cycling, seats held" | Combined room pressure across all four shapes at once | `createRoomGuard` (one instance per room; step up **new** joins via Section B while `recommendStepUpForNewJoins`) | I, B |
| "We need verdicts we can audit later" | Evidence hygiene: which config produced a verdict, what verification proves, who may ground a consequence | The evidence layer: `createConfigProvenance`, `classifyWebBotAuthVerdict`, `issueStepUpProof` / `createStepUpProofVerifier`, `auditEvidencePack` | J |
| "Our API leaked fields we never meant to publish (password hash, national id, bank account)" | Excessive data exposure: the data layer returns the whole record and the route ships it | `createSurfaceGuard` on responses (sensitive denylist + per-route allowlists) | K |
| "Attackers set fields we never offered - role, owner, admin flags" | Mass assignment on writes | `createSurfaceGuard` on requests (privileged denylist + per-route allowlists) | K |
| "One account is reading everyone's records one by one, slowly" | BOLA/IDOR enumeration: every request looks authorized; the sweep is visible only across owners | `createOwnershipProbe` (advisory; wire beside your authorization logic, never instead of it) | L |
| "Squats dodge the occupancy laws by chatting once or twice, right after joining" | The A1 shape: 1-2 early activities take a squat outside the zero-activity definition | `createOccupancyEarlyMinimalSignal` beside `createSeatOccupancySignal` (same room; step up new joins while it flags) | L, C |
| "Agents hit our step-up and just retry blindly" | The step-up consequence is illegible to machines: no manifest, no off-ramp | `createStepUp402Responder` as the step-up consequence (402 + manifest; no settlement) | L |
| "A competitor republished our data and disputes the preference we declared" | Provenance dispute: the declaration is stripped on republication, the watermark is not | `createDeclarationLog` (hash-chained, predates the copy) + `createValueWatermark` | L |
| "One account has been quietly taking our data for weeks" | Slow per-identity harvesting | `createShrinkSlopeSignal`; accumulate with `createCusumTripwire` / `createEvalueTripwire` | - |
| "Accounts poll the same pages like metronomes" | Machine-paced revisiting | `createWatchlistSignal` | - |
| "Something is enumerating our ids / endpoints" | Enumeration walk | `createDecoyTripwire` (plant decoys outside every menu/sitemap/listing) | - |
| "Our published totals appear on a competitor's site" | Republication of derived data | `createValueWatermark` | - |
| "Users pile up just under our known limit" | Calibration against a ceiling | `createBunchingMonitor` | - |

### Honest note on the room guard's history (read this before wiring it)

A combined room-guard module (`createRoomGuard`) was designed for 2.7.3 and **deliberately not shipped in that version**: in its pre-registered lab pin, the frozen signal combination caught join floods (60 s), slow drips (31 min) and churn (30 s) with zero false alarms across four legitimate room cells - but it **missed the seat-squatting cell completely**, because squatting attacks occupancy, not join velocity. Under this project's release rule (no gate loosened after the numbers), the module was excluded rather than shipped half-blind. **Since 2.8.0 it exists** (Section I): the combination was re-registered as RECOMB-06 with the occupancy leg declared up front - the leg that had meanwhile passed its own pin and shipped standalone as `createSeatOccupancySignal` (Section C) - and passed all six frozen gates on fresh seeds, including the squat cell at +690 s against the 900 s gate taken from that leg's own pin. If you are working against a 2.7.3 or 2.7.4 install, `createRoomGuard` really is absent there; upgrade rather than improvising a substitute.

## Section A - `createHerdPhaseSignal` (new in 2.7.3)

Detects a fleet driven by **one shared scheduler**: identities whose repeated events (room joins, session starts, retries) lock onto the same 900-second grid **at the same offset**. The cohort statistic is the point: an identity locked to *its own* grid (a personal cron job, an independent bot) is common and is **not** flagged - only a shared offset confirms a herd.

```ts
import { createHerdPhaseSignal, HERD_PHASE_ROOM_COHORT_WINDOW_MS } from "@dannyphan190/anti-rea";

// One instance per room (or per surface). Do not mix unrelated
// populations into one instance - the cohort is the population
// you evaluate together.
const herd = createHerdPhaseSignal(); // all defaults are the lab-frozen law

// On every room join (or session start, or retry - pick ONE
// homogeneous event kind per instance and stay with it):
herd.observe({ identity: accountId, ts: Date.now() });

// Periodically (e.g. every 5 minutes), evaluate. For room joins,
// scope the cohort to identities first seen in the last 24 h -
// the scoping the roomguard pin validated:
const r = herd.evaluate({ cohortWindowMs: HERD_PHASE_ROOM_COHORT_WINDOW_MS });

if (r.confirmed) {
  // r.members names the fleet's identities - named ONLY because
  // the cohort confirmed. Treat this as evidence: feed your
  // accumulator, raise step-up for NEW joins, alert the operator.
  // Do NOT ban r.members on this output alone.
}
```

Contract details an agent must not get wrong:

- An identity needs **>= 8 events** before it is scored (`minEvents`). One-shot floods are invisible to this signal by construction - that shape belongs to metering, not here.
- `result.members` is **empty unless `result.confirmed` is true**. A large `result.memberCount` with `confirmed: false` means "many grid-locked identities, no shared scheduler" - the designed refusal, not a bug.
- `evaluate()` is a pure function of the fed state: same state, same result, byte for byte.
- The only lab-validated grid period is **900 s** (`periodSec` default). Changing it leaves the lab record behind.
- Malformed events never throw into your request path: a bad `ts` returns `{ status: "invalid_ts", counted: false }`. Bad *options* and a blank identity throw `HerdPhaseError` at setup/feed time - that is a programmer error, fix it, don't catch-and-ignore it in production paths.
- Memory is bounded (`maxIdentities` default 100,000, `maxEventsPerIdentity` default 4,096); watch `snapshot().counters` for evictions if your rooms are huge.

## Section B - Step up NEW joins under pressure (`createVerificationGrace`)

antiRea ships no combined room-pressure module in 2.7.3 (see the note above), but the reaction pattern for a join flood is standard and uses shipped pieces:

```ts
import { createVerificationGrace } from "@dannyphan190/anti-rea";

const grace = createVerificationGrace();

// When a visitor passes your step-up challenge (captcha, email
// code, ...), record it:
grace.recordVerified(accountId);

// At JOIN time, translate your own pressure reading (join rate
// vs this room's baseline, an accumulator score, ...) into an
// evidence level in YOUR units, and ask the grace module whether
// the step-up may be applied to this identity right now:
const verdict = grace.guardStepUp(accountId, evidenceLevel);
if (verdict.action === "step_up") {
  // Run your step-up challenge BEFORE completing the join.
  // "observe" means the identity is inside its post-verification
  // grace window - let the join through without re-challenging.
}
// Existing room members are never re-challenged by this pattern -
// it runs at join time only. Set `flagThreshold` (constructor
// option) to the evidence level that normally triggers step-up in
// your units; the module never invents an evidence scale.
```

Rules: the step-up applies to the **join attempt**, never retroactively to members; a failed or pending step-up delays a join, it does not ban the account; keep your room's normal (non-pressure) joins challenge-free - friction is for pressure moments only.

## Section C - `createSeatOccupancySignal` (new in 2.7.3)

Population-only room state for capacity-limited rooms: the share of seats held by accounts created < 24 h before joining that have shown **zero activity** since joining. It names no identity - a flag means "this room's seats are being held", never "this person is a bot". Two lab-frozen profiles: FAST (defaults) for burst squats, DRIP for slow seat-taking; run two instances if you want both.

```ts
import { createSeatOccupancySignal, SEAT_OCCUPANCY_DRIP_PROFILE } from "@dannyphan190/anti-rea";

// ONE instance per room; capacity is the room's real seat count.
const seats = createSeatOccupancySignal({ capacity: room.capacity });
const seatsDrip = createSeatOccupancySignal({ capacity: room.capacity, ...SEAT_OCCUPANCY_DRIP_PROFILE });

// Feed the room's seat lifecycle. accountCreatedTs whenever you
// have it; without it, first observation stands in.
seats.observe({ type: "join", identity: accountId, ts: Date.now(), accountCreatedTs });
seats.observe({ type: "activity", identity: accountId, ts: Date.now() }); // chat, emote, sing, react - any real activity
seats.observe({ type: "leave", identity: accountId, ts: Date.now() });

const r = seats.evaluate();
if (r.flagged) {
  // Room state, not a verdict on anyone seated: step up NEW seat
  // claims (Section B pattern), alert the operator. NEVER eject
  // current occupants because this fired.
}
```

Contract details: a first-time listener who never chats is normal - the lab's silent-audience cell (60% of seat sessions silent) peaked at 0.1333 against the 0.50 FAST line. The DRIP line (0.34 for a full hour) is closer to unusual-but-legit rooms; check `currentRatio` in the result before acting on a DRIP flag. If your app never emits an activity type, everyone looks idle - feed at least one real activity kind.

Field note (real site, inspected 2026-11-06): on wetube cine, joining a room auto-assigns a free seat and empty seats are backfilled with house bots that yield the moment a human picks their seat. If your app does anything similar, feed the signal the real seat lifecycle (join / activity / leave) for human accounts - house bots are your own population, not occupants.

## Section D - `createActivityPhaseSignal` (new in 2.7.3)

The herd-phase law (Section A) over an **activity** stream - for fleets that join like everyone else but chat/emote/react on one shared scheduler. Same options, same thresholds, same naming rule as `createHerdPhaseSignal`; only the factory name, the `kind` field and the notice differ.

```ts
import { createActivityPhaseSignal, ACTIVITY_PHASE_ROOM_COHORT_WINDOW_MS } from "@dannyphan190/anti-rea";

const actPhase = createActivityPhaseSignal();
// Feed ONE activity kind per instance (chat sends, say):
chatBus.on("message", (m) => actPhase.observe({ identity: m.accountId, ts: m.ts }));

// Evaluate SCOPED - this is part of the law, not a style choice:
const r = actPhase.evaluate({ cohortWindowMs: ACTIVITY_PHASE_ROOM_COHORT_WINDOW_MS });
```

Contract details an agent must not get wrong: **unscoped evaluation over the whole user base was measured NOT to confirm even a real shared herd** (the legitimate background dilutes R_cohort) - a silent unscoped result means "wrong evaluation", not "no fleet". A room reacting together to the same film moment is safe: that cell measured zero members, because content moments are not on a fixed 900 s grid. Everything in Section A's contract list applies unchanged.

One more dilution limit, measured in the 2.7.3 integration benchmark on a busy room stream: even the SCOPED read confirms only when the herd dominates the >= 8-event scored population. On a busy chat stream, legitimate chatters cross the 8-event floor in large numbers, R_cohort can peak well under the 0.80 bar (0.531 in the benchmark) and never confirm - while the member list still names exactly the herd (25/25, zero legitimate). On chat-like streams, treat `members` plus the R_cohort trend as the usable telemetry below confirmation; do not expect the join stream's clean confirmations there (legitimate users rarely reach 8 joins, so the join stream's scored population stays nearly pure).

## Section E - `createVoteBrigadingSignal` (new in 2.7.3)

Population-only room state for vote-driven rooms (skip votes, queue votes): evidence accumulates across 60-second windows and flags only when at least **two** windows contribute - one mass skip by first-time visitors (a streamer raid hating one song) measured a bigger single spike than a brigade makes, and cannot flag by construction.

```ts
import { createVoteBrigadingSignal } from "@dannyphan190/anti-rea";

const votes = createVoteBrigadingSignal(); // one instance per room
onSkipVote((v) => votes.observe({ identity: v.accountId, ts: v.ts, accountCreatedTs: v.accountCreatedTs }));

const r = votes.evaluate();
if (r.flagged) {
  // Step up NEW voters (Section B pattern) or weight votes from
  // accounts < 24 h old at zero until it clears. Do not cancel
  // the current song retroactively and never name voters - the
  // result contains no identities.
}
```

Contract details: measured scope is **vote-skip only** - queue stuffing was registered but not measured; do not claim it. Brigades voting from aged accounts are out of scope by construction (newness is the score's main leg).

Field note (real site, inspected 2026-11-06): wetube cine's skip rule is "30% of the people present ends the song", counted over real people only - house bots are excluded from the denominator - with one vote per account per video and click-again-to-withdraw. Real thresholds on this class of site are commonly a share of the real humans present, not a fixed count; the signal's job is unchanged: watch HOW the votes arrive (many brand-new accounts across several windows), not the threshold arithmetic itself.

## Section F - `createRoomHopSignal` (new in 2.7.3)

Per-identity enumeration shape: flags an identity joining **16+ distinct rooms in any trailing hour** (legit surfers measured at most 11). It carries a self-disarm: if more than 25% of tracked identities would flag, the result names nobody and reports `disarmed: true`. A disarm usually means "the platform changed or the feed is wrong" - but it can also engage during a genuine concentrated attack while the legitimate background is thin (at night, say): the 2.7.3 integration benchmark saw names emitted first, then the disarm flipping on as the evening background thinned. So: never act on names while `disarmed` (there are none), but DO alert a human when `disarmed: true` arrives with `flaggedCount > 0` - that combination is a population-level attack signal, not noise.

```ts
import { createRoomHopSignal } from "@dannyphan190/anti-rea";

const hops = createRoomHopSignal();
onRoomJoin((j) => hops.observe({ identity: j.accountId, room: j.roomId, ts: j.ts }));

const r = hops.evaluate();
if (!r.disarmed) {
  for (const id of r.flagged) {
    // Step-up friction for THIS identity (Section B pattern).
    // Never an automatic ban: breadth is evidence, not proof.
  }
}
```

Contract details: never key this by IP - carrier NAT makes shared IPs meaningless; the verdict is per-identity breadth over its own joins. If your platform's discovery UI encourages much heavier surfing than the lab populations, re-derive `threshold` from your own legit maximum with margin.

## Section G - `createReconnectStormSignal` (new in 2.7.3)

Per-source reconnect abuse over your socket layer's app-level connect/disconnect hooks: flags a source with **40+ connects in 10 minutes whose sessions median under 5 seconds**. Flaky phones (13) and train commuters (21) measured well under the rate leg. Same 25% self-disarm as Section F - a bad deploy that makes every client flap SHOULD disarm it; that is the platform telling on itself. The same disarm can also cover a genuine concentrated storm at night: in the 2.7.3 integration benchmark the raw law flagged 20/20 storm sources, but `disarmed` stayed true for the storm's whole duration (at 22:45 almost nobody legitimate is connecting, so the flagged share sits over 25%) and the named list stayed empty. Wire your alerting on `disarmed: true` WITH `flaggedCount > 0`, not only on named flags - a host that reads only `flagged` is blind exactly during a concentrated night storm.

```ts
import { createReconnectStormSignal } from "@dannyphan190/anti-rea";

const storms = createReconnectStormSignal();
io.on("connection", (socket) => {
  const source = socket.data.sessionKey; // session/account key - NOT socket.handshake.address
  storms.observe({ source, kind: "connect", ts: Date.now() });
  socket.on("disconnect", () => storms.observe({ source, kind: "disconnect", ts: Date.now() }));
});

const r = storms.evaluate();
if (!r.disarmed) {
  for (const src of r.flagged) {
    // Enforce reconnect backoff / step-up for this source.
    // Friction, never punishment of the source's user.
  }
}
```

Contract details: **never use an IP as the source key**. Known blind spot, stated plainly: a storm spread thin across many sources (each under 40/10 min) flags nobody - there is deliberately no population gate, because legitimate rush-hour commutes reach 417 connects/10 min in aggregate. Distributed storms belong to socket-layer rate limits, not this signal.

Field note (real site, inspected 2026-11-06): wetube cine's own room rules give a dropped connection up to **2 minutes** to reconnect before the seat is lost. Hosts commonly hold a seat through a grace window like this, so legitimate reconnects legitimately cluster inside it - that is exactly the flaky-client population the rate leg was calibrated to stay clear of.

## Section H - `createHerdTightnessSignal` (new in 2.7.4)

The companion statistic to Section A, one level up: where herd-phase asks whether a fleet's members share one timer *offset*, herd-tightness asks whether a whole cohort's timing points pile onto **one spot** of the phase plane - the shape one scheduler leaves on a group all at once. Each identity with >= 8 events becomes one point (its mean phase vector on the 900 s grid); the module measures how spread out the cohort's cloud of points is (the longest minimum-spanning-tree edge, d0max), standardised against a **reference population you feed it** - your established, known-legitimate users. A shared-scheduler herd reads tight (lab: 0.26-0.28 against the frozen bar 0.81); ordinary users (1.09-1.36) and an office-hours group behind one NAT (1.39-1.72) read spread.

```ts
import { createHerdTightnessSignal } from "@dannyphan190/anti-rea";

const tightness = createHerdTightnessSignal(); // defaults are the lab-frozen law

// Feed your established legitimate population as the reference
// (long-lived accounts, known-good traffic - the standardisation
// baseline), and the population under watch as the cohort. One
// homogeneous stream each: session starts OR room joins.
tightness.observeReference({ identity: establishedAccountId, ts });
tightness.observe({ identity: accountId, ts });

const r = tightness.evaluate();
if (r.status === "scored" && r.tight) {
  // Cohort-level evidence that this group is driven by one
  // scheduler. Feed it to your accumulator / human review.
  // r names NO identity - there is nobody to step up from this
  // signal alone; pair it with Section A to find the members.
}
```

Contract details: **the output never names an identity** - tightness is a property of a cloud, and any wiring that turns it into a per-account action is a misuse. Without a scored reference population the module returns `status: "uncalibrated"` with `tight: null` - wire your alerting to treat that as "not wired yet", never as "not tight". A herd whose bots each keep their **own** timer offset reads spread and is not flagged (that shape is Section A's cohort leg); the two signals are companions, not substitutes. Evaluate is O(n^2) in scored identities - this is a small-cohort instrument (the lab clouds were 9-16 points), not a fleet-wide scan.

## Section I - `createRoomGuard` (new in 2.8.0)

The combined room-pressure guard: one instance per room, fed the same `join` / `leave` / `activity` events as Section C, evaluating pressure on 30-second ticks across four frozen paths - burst, sustained, churn (join velocity against the room's own trailing baseline, new-account concentration, post-join inactivity, fast-leave cycling) plus the occupancy leg of Section C under its FAST and DRIP laws. RECOMB-06 lab record (seeded simulation, 20,161 ticks per cell): pressure never fired on five legitimate cells (including a karaoke audience with 60% of seat sessions silent); flood +60 s, drip +32.5 min, churn +30 s, squat +690 s via occupancy alone, squat-drip warned 5,100 s before the last seat was taken.

```ts
import { createRoomGuard } from "@dannyphan190/anti-rea";

const guard = createRoomGuard({ capacity: room.capacity }); // one per room
guard.observe({ type: "join", identity: accountId, ts, accountCreatedTs });
guard.observe({ type: "activity", identity: accountId, ts });
guard.observe({ type: "leave", identity: accountId, ts });

const r = guard.evaluate();
if (r.recommendStepUpForNewJoins) {
  // Pressure is high at the latest tick: step up NEW joins only
  // (Section B). Members already seated are never this module's
  // business - it names nobody. r.paths shows which path fired;
  // r.firstFlagTs / r.firstPathTs are the audit history.
}
```

Contract details: `flagged` is history (pressure has been high at some tick); the live recommendation is `pressureHighNow` / `recommendStepUpForNewJoins` at the latest tick - do not latch a step-up forever off a stale `flagged`. The path constants are the lab-frozen law (exported as `ROOM_GUARD_LAW`); they are not options. Known hole, declared: a squatter who emits even 1-2 activity events escapes the occupancy leg's zero-activity definition (hole A1) - the guard does not claim that shape. Prefer the guard when the room faces mixed shapes; keep Section C wired separately only if you also need its standalone ratio readout.

## Section J - The evidence layer (new in 2.8.0)

Four small exact modules that pin down what verdicts mean. Wire them around the signals, not instead of them:

- **Config provenance (CS-02).** At construction, pin each signal instance's effective config: `createConfigProvenance({ kind, version, defaults, options })` returns a SHA-256 `hash`. Attach that hash to every evaluation you log or forward - an evidence item that cannot name the exact detector configuration that produced it cannot be audited later.
- **Verified-neutral facts (BS-01).** Classify identity-verification outcomes with `classifyWebBotAuthVerdict(verdict)` (and `classifyHostVerificationFact` for FCrDNS / range checks). The law: verified moves suspicion by exactly 0, every ambiguous outcome is `unverified` with delta 0, and only a `spoofed` fact (proven forgery) carries evidence. Never treat a verified fact as innocence or an unverified one as guilt, and never key enforcement on a verdict's `detail` string yourself - the classifier exists so you do not have to.
- **Step-up proofs (CAP-01).** When an identity passes a step-up, remember it with `issueStepUpProof` (Ed25519; binds the identity, the stepping-up signal's CS-02 hash, and your challenge config's hash; single-use nonce; lifetime at most 3,600 s) and check presentations with `createStepUpProofVerifier` - the consume hook is required at construction, because single-use is part of the shape. A config change invalidates outstanding proofs by construction (the `cfg` binding stops matching).
- **Evidentiary roles (KT-01).** Before composing signals into any consequence, run the pack through `auditEvidencePack`: unknown channels and mis-claimed roles are invalid, and a pack whose fired items are all CORROBORATING is **ineligible** - corroboration supports, it never grounds. `decorateSignalResult(result, { configHash })` attaches role, config hash and fired state to a signal result in the pinned format. The tier rules ship as data (`ENFORCEMENT_TIER_EVIDENCE_RULES`): tier 3 is forbidden for inferred evidence at any composition.

## Section K - `createSurfaceGuard` (new in 2.9.0)

Field-level control of the payload boundary, in both directions. Budgets cap how MUCH an identity takes; the surface guard caps WHAT a single response carries and what a single request may set - the failure behind the Spoutible and eHUST leaks (profile/search responses shipping password hashes, national ids and bank accounts) and behind mass assignment (GitHub 2012, Rocket.Chat, Langflow).

```ts
import { createSurfaceGuard } from "@dannyphan190/anti-rea";

const surface = createSurfaceGuard({
  mode: "advisory", // default - report only, never touches the payload
  routes: {
    "GET /api/users/:id": { responseFields: ["id", "name", "email", "avatarUrl"] },
    "PATCH /api/users/:id": { requestFields: ["name", "email", "bio"] },
  },
  onViolation: (e) => log.warn("surface", e),
});

// before sending a response / after building the payload object:
const out = surface.inspectResponse("GET /api/users/:id", payload);
// before binding a write body to your model:
const inc = surface.inspectRequest("PATCH /api/users/:id", req.body);
```

The law of the module:

- Two layers. A built-in DENYLIST of field-name patterns (sensitive outbound, privileged inbound) needs no configuration and catches over-broad payloads on undeclared routes. A per-route SCHEMA allowlist flags anything undeclared; a field the host declared is exempt from the denylist (a login response legitimately returns a token).
- Field names are normalized before matching (case and `_`/`-` removed), so renaming games do not slip past.
- Consequences are the host's choice and never escalate themselves: `advisory` reports, `strip` returns a sanitized copy, `block` marks the inspection not-ok. Start in advisory, read your own traffic's violations, declare schemas for the noisy routes, and only then consider strip.
- Traversal is capped (`maxScanNodes`, default 10,000) and reports `truncated` rather than scanning hostile payloads forever.
- It reads field NAMES, not values or ownership: a declared field holding another user's data still passes. BOLA/ownership stays your authorization logic - wire the guard beside it, never instead of it.
- Lab record (pre-registered, seeded synthetic corpora): 0 false positives on 2,000 legitimate responses and 2,000 requests; 1,194/1,194 injected sensitive fields and 918/918 injected privileged fields caught.

**Declared-cohort union budget (pattern, 2.9.0).** When several accounts belong to one principal you know about, do not give each its own record budget and stop there: give the cohort ONE `createRecordBudget` keyed by the cohort id, checked and consumed beside the per-identity budget, so rotation inside a declared cohort stops diluting the cap (measured: a declared herd halts at exactly 150 of 500; undeclared, the same herd takes everything - declaration-gating is the law, never invent a cohort from inferred evidence). Runnable wiring and verification: `examples/declared-cohort-budget` in the repo. Single-process only; scaled hosts use the disclosure ledger's `reserveDisclosure`.

## Section L - The 2.9.1 lab graduates (audited in 2.9.2) (ownership, the A1 counter, the 402 answer, provenance, calibration utilities)

Seven modules that had each passed a pre-registered lab pin and were waiting on a build order. All advisory (`enforcement: "none"`), all additive.

### `createOwnershipProbe` - the sweep across owners (WALL-03)

Budgets cap how much one identity takes; the surface guard caps what a payload carries; the ownership probe watches WHOSE objects an identity touches. One account reading 200 records of 180 different owners is enumeration even when every request is authorized-looking and the volume is small.

```ts
import { createOwnershipProbe } from "@dannyphan190/anti-rea";

const probe = createOwnershipProbe({ onEvidence: (e) => log.warn("ownership", e) });
// on each object read, after your authorization check:
const verdict = probe.touch({ identity, objectId, ownerId, route, publicRoute: false, ts });
```

- A window flags when counted touches >= `minEvents` (20) AND distinct owners >= `minDistinctOwners` (10) AND owners / touches >= `minRatio` (0.5). Dual windows (1 h and 6 h) share one incremental state; public routes are excluded from numerator and denominator; unknown owners count in the denominator only; below the floor the answer is `insufficient_history`, never a flag.
- It reads access patterns, not authorization: it cannot tell a sweep from a support agent with a legitimate queue. Advisory evidence for review and step-up decisions - never wire it as an authorization check.
- Lab record: sweeps flagged 500/500 in both windows; 0 false positives on 2,000 legitimate sessions; the historical ingest timing is not a portable performance promise. See docs/audit-2.9.2.json for this audit machine and measured medians.

### `createOccupancyEarlyMinimalSignal` - the A1 counter (A1-COUNTER-D2)

Attack A1 beat the shipped occupancy laws with 1-2 early activities: any activity took the squat outside the zero-activity estimand. This sibling signal counts a session only while its identity is new (created < 24 h before join), it holds 1-2 activities so far, and EVERY activity sits within 300 s of join - the exact shape of the dodge, and of almost no legitimate newcomer.

```ts
import { createOccupancyEarlyMinimalSignal } from "@dannyphan190/anti-rea";

// Example host-declared room capacity; replace with your room capacity.
const early = createOccupancyEarlyMinimalSignal({ capacity: 100, onEvidence: (e) => log.warn("early-minimal", e) });
early.observe({ type: "join", identity, ts, accountCreatedTs });
early.observe({ type: "activity", identity, ts });
const state = early.evaluate({ asOfTs: ts }); // per-law results: fast 0.50/600 s, drip 0.34/3,600 s
```

- Wire it BESIDE `createSeatOccupancySignal`, not instead of it: the shipped laws own the zero-activity case, this one owns the 1-2-early-activity case. Step up NEW joins while either flags (Section B).
- Read the stated limits before acting on it: the lab lurker gate passed with exactly ONE session of headroom (peak 0.3333 vs the 0.34 drip bar), so treat a drip-only flag as weak evidence; first activities delayed into the (300 s, ~630 s) band evade both laws by design; 3 quick activities evade by construction.
- Lab record (PASS-lab, two byte-identical runs): fast squats flagged +690 s, 300 s-delay +960 s, drip +1,440 s; legitimate twins and the new-lurker cell unflagged.

### `createStepUp402Responder` - a step-up machines can read (RECOMB-09)

When step-up fires, answer with a manifest instead of a wall: HTTP 402 in x402 style, `X-Payment-Required` header, and a body carrying the price (a signal price - there is NO settlement and no payment processing), the session token, and pay / appeal / continue-free next steps.

```ts
import { createStepUp402Responder, checkAssertion } from "@dannyphan190/anti-rea";

const answer = createStepUp402Responder({ priceUsd: 0.001, manifestUrl, facilitator, payUrl, appealUrl, continueFreeUrl });
// only AFTER a step-up trigger fires for this session:
const res = answer.respond(sessionId, issuedToken); // { status: 402, headers, body }
// on the next request:
const ok = checkAssertion(req.headers["x-step-up-assertion"], issuedToken);
```

- Never call `respond()` for an identity that has not triggered step-up - the lab control arm (no trigger, no 402) is the FP gate.
- Lab record: cooperative agents retreated in 94.5% of sessions and presented a valid assertion in 94.0%; 0 legitimate dead-ends across 200 browser and 200 API sessions. Agents that ignore the manifest are unaffected - the shape informs, it does not block.

### `createDeclarationLog` - provenance for declared preferences (RECOMB-10)

Robots `Content-Signal`, RSL and aipref declarations live on the host and are stripped the moment data is republished; the C39 value watermark survives republication but says nothing about what you declared, or when. The declaration log is the missing half: an append-only, hash-chained, host-side record that a declaration existed BEFORE a given copy appeared.

```ts
import { createDeclarationLog, importDeclarationLog } from "@dannyphan190/anti-rea";

const decl = createDeclarationLog();
decl.append({ form: "robots-content-signal", declaration: "search=yes, ai-input=no, ai-train=no", timestamp: Date.now() });
decl.verify();        // { ok, checked, firstBadIndex }
decl.predates(copyTs); // was a declaration in force before this copy?
const archive = decl.export(); // JSON; importDeclarationLog re-verifies and refuses a broken chain
```

- The log proves ordering and integrity only - not that any crawler complied, and not legal recognition of the claim. Pair it with `createValueWatermark`: watermark for the copy, log for the declaration.
- Lab record: the declaration arm matched watermark-only at 18/18 gated transform cells with 0 mis-attributions; chain verified 200/200.

### Calibration utilities (pure functions, no state)

- `applyVolumeRankRule` (RECOMB-04) - rank cells by two-component EB05 score; flag an identity when >= 2 of its rare cells land in the top 5%, reported per volume stratum (frozen boundaries 63.2 / 632.5). Lab at gated kappa 100/300/1000: MID-stratum walker detection 0.85-0.90, legit FP <= 0.007. Kappa 30 is descriptive, not covered by that FP bound. Detection was measured in the MID stratum only - no production threshold is claimed.
- `selectEmpMixThreshold` (RECOMB-05) - choose a clustering threshold from a 50/50 mixed calibration set (null permutations + flat empirical forests): the largest grid point whose mixed FMR stays <= target (default 1%). Lab (R14 branch-C frame): held h = 0.36 across 0-30% calibration contamination where the null-only set flipped at 10%.
- `computeHoldTypeFeatures` + `createHoldTypeScorer` (RECOMB-02, Step 0) - five session-timing features and the frozen signed-z composite S_R2 against a host-supplied human reference. Step 0 measured feature separation ONLY: this ships computation, not a detection claim; thresholds are the host's (the lab used the outer-5% tail of the human distribution).

## Section M - 2.9.2 audit and host handling

- Ownership windows use a monotone event-time watermark. Late arrivals are counted in the correct live windows. Capacity loss is explicit `truncated` telemetry, suppressing incomplete flags; identity-cap gaps also suppress newly admitted histories until the missing window expires.
- D2, seat occupancy and room guard bound open sessions and retained activity timestamps. Saturation suppresses flags and recommendations; investigate the feed and start a fresh observation epoch deliberately. D2 exposes reset; older room signals require a fresh instance.
- Invalid hold-type sessions return finite neutral features and scores with `valid: false`; inspect `invalidReasons` rather than treating missing data as human evidence.
- Assertions compare exact UTF-16 token units with bounded lengths. The declaration log checks export format/version and refuses capacity overflow; external count/head anchors are needed to detect tail truncation.
- Volume-rank's historical FP bound belongs to generator-component lab strata. It does not transfer to the SDK's volume-derived regrouping. The audit reproduced 1/115 HIGH false flags at kappa 1000 in that regrouping.
- E-value histories are never silently evicted or restarted. Capacity and invalid-input errors are telemetry failures to catch and report, not authorization decisions.
- D2 defaults remain unchanged: a registered FAST-only candidate lost the minority attack cell and was not shipped. RECOMB-03 remains excluded after a fresh independent pair experiment showed heavy legitimate persona harm. These are synthetic measurements, not production calibration.
- Historical quantitative claims in Section L retain their original scope. The release audit marks missing generator dependencies as NOT VERIFIED; it does not upgrade them into newly verified measurements.

## Section N - 2.9.3: the shadow decoy graph, issued-at checks, decoy vocabularies

- **Shadow decoy graph (`generateShadowDecoyGraph` / `verifyShadowGraphClosure`).** Standalone decoy records fall to offline referential-integrity filtering (unresolvable references, asymmetric chain links, counts that do not match). The shadow graph is a decoy SET built closed and internally consistent - authors, series, chained records whose references resolve, counts match and timestamps never run backwards - so a reconstruction absorbs it as real. Lab record (BLA-02, pre-registered frozen gates, seed family 20301xxx): a fixpoint integrity filter removed 100% of standalone decoys (720/720) and 0% of shadow decoys (0/720) over 12 instances; the decoy-free control lost 0 of 24,000 real records. Placement is the host's contract: shadow entities are reachable only through enumeration surfaces, never linked from a real record. The generator takes NO real-data input (nothing about the real population leaks), and it does NOT claim resistance to statistical fingerprinting - the shadow distributions are deliberately unfitted. `verifyShadowGraphClosure` re-checks the invariants after any host-side transformation.
- **Issued-at checks (LPG-07).** `verifyCursor`, `verifyCursorV2` and `verifyEchoId` now reject a token whose `iat` is more than 60 s in the future (`not_yet_valid`) and treat a non-numeric `iat` as `malformed` - before 2.9.3 only `exp` was checked. A future `iat` means a host clock or minting error; the 60 s skew matches the step-up proof and the Web Bot Auth verifier.
- **Web Bot Auth robustness (SLC-05).** `verify()` returns the structured `no_signature_headers` verdict for a null or non-object request instead of throwing.
- **Decoy vocabularies (RSH-01).** `createDecoyMirage` accepts host `fieldNames` / `featureNames` (at least 4 distinct names each). The built-in lists are constants of this public source and fingerprint default documents with certainty; wire the host's own dialect. The shadow graph generator likewise takes a host `categories` vocabulary.
- **Measured and NOT shipped:** IA-02 parameter jitter (deployment-level budget jitter in [130, 170]) was killed at its frozen false-positive gate: legitimate power users were newly blocked at 1.38-5.14% against a 1% ceiling - the same population that killed IA-01 edge-hugging. A different band is a new registration, not a retune.

## Section O - 3.0.0: tier-2 conversion, bulk capability keys, the pin statistic, queue stuffing, UAS forms

- **Tier-2 conversion (`createTier2Conversion`, opt-in, default observe).** The C27+C35 enforcement layer under the locked decisions of 2026-11-04 (1A/2A/5A). A persistent C27 flag (>= 2 distinct evidence epochs) with independent corroboration from a different detector family steps the identity's record budget down toward the 500-record floor - never below the floor, never a hard block. First C35 decoy touch = taint + step-up immediately, with the V-C taint expiry (the ledger clears 90 days after the last touch) and retroactive void built in. The alpha-wealth fleet FP budget ships with the layer: tier-ups spend from a fleet ledger and exhaustion falls back to observe-only automatically. Strata enter by host declaration only. Evidence basis: FC-03R PREMISE-CONFIRMED (farm age-aligned statistic, ages 1-12) plus the lab pin; the C35 leg is lab-only - the farm has no decoy surface and no C35 farm claim is made, and there is no theta claim for ages 31-90.
- **Bulk capability keys (`createBulkAccessKeyAuthority`, GATEKEY-01).** Bulk access (novel records past the 150-record free zone, any tail record, any novel export) requires a server-issued key; issuance is the metered event. Anonymous channel: <= 1 key/24h/identity AND a fleet pool of 6 keys/24h (with a step-up-proof fast lane that buys queue position, never pool expansion); account channel <= 6/24h; verified channel (host allowlist + Web Bot Auth) <= 60/24h. Each key unlocks one non-contiguous 150-record slice of a seeded epoch permutation, records served under a key carry that key's C39 watermark variant, and shared keys manufacture fork evidence (lineage revoked, re-issuance step-up-gated). Lab record (GATEKEY-01 Step-0, PASS-LAB): ordinary and heavy strata served in full with 0 denials, and a 200-identity rotation farm needed 12 days to complete the tail. Scope limit: the economics cover the tail, exports and beyond-free-zone serving only - the head stays keyless by design.
- **FC-07 pin novel statistic (`fitPinNovelStatistic` / `scorePinNovelStatistic`, OPT-IN).** Novel-only per-identity exposure counts with per-stratum C-LAW thresholds and the strict flag rule (novel > tau); small strata fall back to the pooled threshold, reported. Farm calibration window: ordinary FP 0/36, heavy FP 0/18, slow attacker 2/2, bulk shapes 4/4. Verdict PASS-LAB-WITH-COST: review-team-shaped traffic crosses 100% against the 25% cost line. Holdout validation on the 16-22/11 traces is pending - the statistic ships opt-in with the default unchanged; do not present it as field-validated.
- **Queue-stuffing axis (`createQueueStuffingSignal`).** The vote-brigading law transplanted verbatim to the queue-submission stream, sharing the accumulator core with `createVoteBrigadingSignal` (whose behavior is unchanged). Lab record (PASS-LAB, CAND-273-4 stuffing registration): legitimate and raid-queue cells never flag in 7 evenings (peak A = 3, under the threshold of 12); a stuff-burst flags at the second burst's window close (A = 15). Constants are harness-fitted and uncalibrated for real traffic; aged-account stuffing is invisible by construction.
- **UAS family, restricted forms (advisory-only).** `analyzeHeaderCoherence` ships only the fixed V1 form (the V0 table flags on a single signal - a measured defect); the proxy false-positive class is disclosed (75.15% behind header-stripping proxies). `classifyUserAgent` ships the named-bot catalogue minus the generic tokens (the generics flag real in-app webview users 8/8 in the trap corpus and are excluded), plus the empty-UA rule; browser corpus FP 0/36. `createFakeEndpoints` is an opt-in decoy pack (default OFF): scanner-probed paths serve fake-200 bodies on GET/HEAD only, and the fake /.env credential is a canary-echo token, not a dumb bait string. `asset-referrer-profile` now stores a supplied referer as its origin only (WART-1 fixed: opaque origins store actual null).
- **Self-disarm denominator fix (273-5 / 273-6).** `createRoomHopSignal` and `createReconnectStormSignal` now compute their 25% self-disarm share over the cumulative tracked population, matching their frozen CAND-273-5/-6 pins, instead of identities active in a trailing window - the windowed denominator let both disarm mid-attack. Re-measured on the fixed build: 20/20 attackers named on time under periodic evaluation with zero disarms, and the FP cells unchanged (room-hop max 6/11 vs threshold 16; reconnect maxima 2/13/21 vs 40). `createReconnectStormSignal` also reports the true `maxConnectsObserved` (549 in the pin; an early return had understated it at 40). Counting laws, thresholds and APIs are unchanged.
- **Measured and NOT shipped in 3.0.0:** MGH-01..03 (PASS-LAB in restricted forms, entered after the 3.0 scope froze), IA-03 / IA-04 (unmeasured), SIS-01..03 as standalone detectors (unmeasured; SIS-01 survives only as the bulk-key fork semantics), LPG-06 (frozen design only), and the API evidence pack (tier-2 decision 3B, later version). Suite: 1056 tests / 1054 pass / 0 fail / 2 skipped; release gate 17/17. The MCP wrapper stays 2.8.2 and pins SDK 2.8.1; it is not part of this release.

## Safe defaults (do not retune silently)

| Module | Option | Default | Why |
|---|---|---|---|
| `createHerdPhaseSignal` | `periodSec` | 900 | Only lab-validated scheduler grid |
| | `memberThreshold` (tau_R) | 0.90 | Frozen in the measured gap (legit p99 0.6495, herd p05 0.9616 in the lab) |
| | `cohortThreshold` (tau_C) | 0.80 | Frozen between the shared (~0.98) and independent (~0.10) regimes |
| | `minEvents` | 8 | Lab scoring floor |
| | `minMembers` | 10 | Lab confirmation floor |
| | `cohortWindowMs` (evaluate) | 86,400,000 (24 h) for room joins | Scoping validated by the roomguard pin |
| `createSeatOccupancySignal` | `threshold` / `sustainMs` | 0.50 / 600,000 (FAST) | Frozen in the CAND-273-1 pin (legit peak 0.1333, squat flagged 660 s) |
| | DRIP profile | 0.34 / 3,600,000 | Frozen in the CAND-273-2 pin; narrower margin - check `currentRatio` before acting |
| `createActivityPhaseSignal` | (all) | Same as herd-phase | The law is inherited, not re-tuned; scoping is mandatory (Section D) |
| `createVoteBrigadingSignal` | `threshold` / `minWindows` | 12 / 2 | Frozen in the CAND-273-4 pin; the 2-window rule is what a one-off raid cannot pass |
| `createRoomHopSignal` | `threshold` / `windowMs` | 16 / 3,600,000 | Frozen in the CAND-273-5 pin (heavy legit max 11/hour) |
| | `disarmShare` | 0.25 | C35-pattern insurance; lowering it mutes the signal, raising it risks mass flags |
| `createReconnectStormSignal` | `minConnects` / `maxMedianDurationMs` | 40 / 5,000 | Frozen in the CAND-273-6 pin (legit max 21/10 min) |
| `createHerdTightnessSignal` | `periodSec` | 900 | Only lab-validated scheduler grid |
| | `tightnessBar` | 0.805436 | Frozen C148 calibration midpoint (herd bootstrap max 0.645, legit bootstrap min 0.965); recalibrate only against your own reference population, with the recalibration recorded |
| | `minEvents` / `minIdentities` | 8 / 8 | Lab scoring floor / lab cloud floor (below 8 scored identities the lab voided the reading) |
| `createRoomGuard` | (path constants) | `ROOM_GUARD_LAW` | Frozen in the RECOMB-06 pin; the paths are not options - only `capacity` (required), `tickMs` (30,000), `newnessWindowMs` (24 h) and `maxSessions` (100,000) are options |
| `createSurfaceGuard` | `mode` | `advisory` | The tiering law: observe first; strip/block only by the host's explicit choice after reading advisory output on real traffic |
| `createOwnershipProbe` | `minEvents` / `minDistinctOwners` / `minRatio` | 20 / 10 / 0.5 (per window) | Frozen in the WALL-03 pin (FP 0/2,000 legit); the floor is what keeps small readers at `insufficient_history` |
| `createOccupancyEarlyMinimalSignal` | FAST / DRIP profiles | 0.50 / 600,000 ms; 0.34 / 3,600,000 ms | Frozen in the A1-COUNTER-D2 pin, mirroring the shipped occupancy geometry; the drip bar's lurker headroom measured exactly one session - do not lower it |
| | `earlyWindowMs` / newness | 300,000 / 86,400,000 (24 h) | The 300 s edge is the largest known delay that evades the shipped laws; widening it re-opens the lurker FP the pin closed |
| `createStepUp402Responder` | `priceUsd` | host-set (lab 0.001) | A signal price only - no settlement exists in the module; never present it as a real charge |
| `selectEmpMixThreshold` | `targetFmr` | 0.01 | Frozen in the RECOMB-05 registration (branch-C selection law) |
| `applyVolumeRankRule` | `topFrac` | 0.05 | Frozen R2-rank5 construction; the 10% variant is descriptive only |
| | `maxScanNodes` | 10,000 | Cost bound against hostile payloads; past the cap the result is `truncated`, never silently complete |

## Never do this

- Never ban, kick, or shadow-limit an account or a room member **solely** because an advisory signal fired - including a confirmed herd-phase cohort.
- Never re-challenge or eject **existing room members** when a room-level signal fires. New joins only.
- Never lower `memberThreshold` / `cohortThreshold` / `minMembers` to "catch more" - you are spending a false-positive budget that was measured for you; the lab's legitimate groups (office-hours fleets, sale bursts) sit closer to the line than intuition suggests.
- Never feed mixed event kinds (joins + chats + clicks) into one herd-phase instance; phases only mean something on one homogeneous stream.
- Never evaluate `createActivityPhaseSignal` (or herd-phase over a huge base) over an unscoped whole-platform population and report its silence as coverage - unscoped dilution is measured, and scoped evaluation is part of the law.
- Never use an IP address as the identity/source key for room-hop or reconnect-storm - carrier NAT shares IPs across strangers; both signals are per-identity by design.
- Never act on a room-hop or reconnect-storm result when `disarmed` is true - the disarm means the platform or the feed changed shape; investigate first.
- Never eject or punish current room occupants because a population signal (seat-occupancy, vote-brigading) flagged the room - those outputs name no one and accuse no one.
- Never present lab numbers as real-traffic performance in a summary, README, or sales copy.
- Never claim this package stops network DDoS. It does not see packets.
- Never invent APIs. If a function is not in `dist/index.d.ts`, it does not exist.
- Never treat a BS-01 `verified` fact as innocence or an `unverified` one as guilt - both carry an evidence delta of exactly 0 by law; only `spoofed` is evidence.
- Never verify a CAP-01 proof with a verifier built without a real single-use nonce store - a `consumeNonce` that always returns true deletes the replay protection the shape exists for.
- Never ground a consequence on a pack `auditEvidencePack` reports ineligible (corroborating-only) or invalid (unknown channel, mis-claimed role).

## Post-integration verification checklist

Run through this before reporting the integration done:

- [ ] `npm run build` (or the host's build) passes with the new wiring; no antiRea import reaches the default request path unless intended - signals are opt-in.
- [ ] A synthetic shared-grid herd (12 joins per identity on a 900 s grid, ~30 s jitter, 12+ identities) fed to `createHerdPhaseSignal` in a test returns `confirmed: true` and names the members.
- [ ] The same herd with a **different random offset per identity** returns `confirmed: false` and `members: []`.
- [ ] Ordinary traffic shapes (steady joins, a 50-user raid after a link drop, a scheduled showtime join) produce **no** confirmation and **no** step-ups beyond your intended pressure rule.
- [ ] Step-up (Section B) triggers only on join attempts during pressure, and a member already in the room can keep watching/chatting uninterrupted while it is active.
- [ ] A synthetic squat (16+ fresh silent joins into a 30-seat room, no activity) fed to `createSeatOccupancySignal` in a test flags after the 600 s sustain, and the same stream with the joiners chatting does not.
- [ ] Room-hop / reconnect-storm wiring keys on identity/session keys (never IPs), and your code checks `disarmed` before reading `flagged`.
- [ ] `snapshot()` counters on each instance show no unexpected `invalidTs` growth (that means your timestamps are malformed somewhere upstream).
- [ ] A synthetic squat (30 fresh silent joins into a 30-seat room) fed to `createRoomGuard` in a test flags via the occupancy path, `recommendStepUpForNewJoins` is true while they sit and false after they leave, and the same stream with the joiners chatting does not flag (hole A1, expected).
- [ ] Your summary to the developer states plainly: which signals are wired, that all are advisory (`enforcement: "none"`), what enforcement the *host code* performs, and which package version the wiring targets (`createRoomGuard` and the evidence layer exist since 2.8.0; the surface guard exists since 2.9.0; the ownership probe, early-minimal occupancy, the 402 responder, the declaration log and the calibration utilities exist since 2.9.1; the shadow decoy graph exists since 2.9.3; tier-2 conversion, bulk capability keys, the queue-stuffing signal and the UAS restricted forms exist since 3.0.0, and the FC-07 pin statistic is opt-in since 3.0.0).

- [ ] The host targets audited package 3.0.0 and handles truncated, saturated and invalid telemetry without inventing enforcement.
