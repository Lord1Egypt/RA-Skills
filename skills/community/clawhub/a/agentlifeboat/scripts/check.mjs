// The heartbeat check (KIN-121): what an agent runs on every heartbeat turn to keep its lifeboat current.
// The policy is a pure function of the status and the clock, so the model decides nothing about money: at most one
// paid action per run, never a registration, every refusal explained. `runCheck` performs the chosen action and
// writes the spend to the ledger before paying, so a crash or a server error after settlement cannot lose it.
//
// The daily cap guards the automation against a runaway policy, not the agent against itself: the agent runs this
// in its own shell and could raise the variable. The wallet's balance is the hard limit, as for every other command.

const DAY = 86_400_000;

/** Knobs the agent's human sets in the environment; every one has a default that keeps spend small. */
export function checkPolicy(env = {}) {
  const num = (v, fallback) => {
    const n = Number(v);
    return Number.isFinite(n) && n >= 0 ? n : fallback;
  };
  return {
    /** Extend when cover ends within this many days. */
    extendWhenDays: num(env.ESTATE_EXTEND_WHEN_DAYS, 2),
    /** Days bought per extension. */
    extendDays: Math.max(1, Math.min(90, Math.floor(num(env.ESTATE_EXTEND_DAYS, 3)))),
    /** Snapshot when the newest one is older than this many hours; 0 never snapshots from the check. */
    snapshotEveryHours: num(env.ESTATE_SNAPSHOT_EVERY_HOURS, 24),
    /** Keep one restore in hand when hosting billing is on (units bought per run, at most a full restore). */
    keepRestoreCredit: (env.ESTATE_KEEP_RESTORE_CREDIT ?? "on").trim().toLowerCase() !== "off",
    /**
     * Hard cap on what the check may spend in a rolling 24 hours, in dollars; 0 means the check never pays. $1.50 by
     * default (2026-10-21; was $1.00): one $1 restore unit, the daily $0.01 snapshot and a cover extension ($0.21 to
     * $0.30) fit in one day, so a full restore is bought within a week without starving snapshots or cover.
     */
    maxSpendPerDay: num(env.ESTATE_MAX_SPEND_PER_DAY, 1.5),
  };
}

/** A price string ("$0.07") as a number; NaN when missing or malformed, so a missing price can never mean "free". */
const price = (s) => {
  const m = /^\$?(\d+(?:\.\d+)?)$/.exec(String(s ?? "").trim());
  return m ? Number(m[1]) : Number.NaN;
};
/** Dollar arithmetic in whole cents: 0.07 × 3 is $0.21, not 0.21000000000000002. */
const cents = (usd) => Math.round(usd * 100) / 100;
/**
 * A reservation rounds UP to the next cent: the reserved amount is also the payment's signing limit, and a limit rounded
 * below the real price would refuse that payment on every run (review of 1.0.2: $0.015 reserved as $0.01).
 */
const upToCent = (usd) => Math.ceil(usd * 100 - 1e-9) / 100;

/** The unit prices the check pays besides the cover price, read from a manifest body. */
export function pricesOfManifest(manifest) {
  const p = manifest?.pricing ?? {};
  return { restoreUnit: price(p.restoreCredit?.price), snapshot: price(p.snapshot?.price) };
}

/** Dollars the check spent, or set out to spend, in the last 24 hours: the ledger in the state file, pending entries included. */
export function spentLastDay(state, now) {
  return cents((state.checkSpend ?? []).filter((e) => now - Date.parse(e.at) < DAY).reduce((sum, e) => sum + (Number(e.usd) || 0), 0));
}

/**
 * Decides the one thing to do now. Returns { action, args, usd, reason } or { action: "none", reason } plus
 * `needsHuman`, the things the check will not do on its own (register, spend past the cap, an unknown price).
 */
export function decide(status, policy, state, now, prices = {}) {
  const needsHuman = [];
  const spent = spentLastDay(state, now);
  const allowed = (usd) => {
    if (policy.maxSpendPerDay === 0) return false;
    return cents(spent + usd) <= policy.maxSpendPerDay;
  };
  const overCap = (what, usd) => `${what} ($${usd.toFixed(2)}) would pass the daily cap ($${policy.maxSpendPerDay}, $${spent.toFixed(2)} spent)`;
  // The cover end is the later of what the status says and what the last extension returned: an extension's
  // database write lands on settlement, and a status read that beats it must not look like cover still ending.
  const coverUntil = Math.max(Date.parse(status.coverUntil) || 0, Date.parse(state.coverUntil) || 0);
  const coverLeftDays = coverUntil ? (coverUntil - now) / DAY : Number.NaN;
  const perDay = price(status.coverPricePerDay);
  // A unit price is used only when the manifest gave a real one: never a guessed $1 that the 402 could exceed, and never
  // a sub-cent price that would round to a $0 ledger entry and let every run buy (review 2026-10-21).
  const unitPrice = Number.isFinite(prices.restoreUnit) && prices.restoreUnit >= 0.01 ? prices.restoreUnit : Number.NaN;
  // The same for a snapshot: an unreadable price is never guessed (it used to default to $0.01; ClawHub scan, 2026-10-27).
  const snapshotPrice = Number.isFinite(prices.snapshot) && prices.snapshot >= 0.01 ? upToCent(prices.snapshot) : Number.NaN;
  // 1. Cover first: without it nothing else matters. An unknown price is never paid blind (the 402 would name the real one).
  if (Number.isFinite(coverLeftDays) && coverLeftDays <= policy.extendWhenDays) {
    const what = `cover ends in ${coverLeftDays.toFixed(1)} days`;
    if (!Number.isFinite(perDay) || perDay <= 0) needsHuman.push(`${what} and the status shows no cover price to extend at; run status and extend by hand`);
    else {
      const usd = upToCent(perDay * policy.extendDays);
      if (allowed(usd)) return { action: "extend", args: { days: policy.extendDays }, usd, reason: what, needsHuman };
      needsHuman.push(overCap(`${what} and extending ${policy.extendDays} days`, usd));
    }
  }
  // 2. A fresh snapshot, when the newest is older than the interval: before buying credit, because a restore of a stale
  // snapshot is worth less than a fresh one. Not from inside an Estate room: the sidecar takes those. A snapshot whose
  // date cannot be read counts as fresh, never as ancient.
  if (policy.snapshotEveryHours > 0 && !status.room) {
    const list = status.snapshots ?? [];
    const dates = list.map((s) => Date.parse(s?.createdAt)).filter((t) => Number.isFinite(t));
    if (list.length && !dates.length) needsHuman.push("the status lists snapshots without readable dates; not snapshotting until that is clear");
    else {
      const newest = dates.length ? Math.max(...dates) : 0;
      const ageHours = (now - newest) / 3_600_000;
      if (ageHours >= policy.snapshotEveryHours && !Number.isFinite(snapshotPrice)) {
        needsHuman.push("a snapshot is due, but the manifest gives no readable snapshot price, so none is paid for; run snapshot by hand after reading the manifest");
      } else if (ageHours >= policy.snapshotEveryHours) {
        if (allowed(snapshotPrice)) return { action: "snapshot", args: {}, usd: snapshotPrice, reason: newest ? `newest snapshot is ${ageHours.toFixed(0)} hours old` : "no snapshot yet", needsHuman };
        needsHuman.push(overCap("a snapshot is due", snapshotPrice));
      }
    }
  }
  // 3. A restore needs credit when billing is on; one full restore in hand. A full restore ($5) is more than a day's
  // cap, so the check buys as many units as the cap leaves room for and the rest on later runs: with the defaults one
  // unit a day, a full restore within a week, and no human needed (2026-10-21; until then it asked for all five at
  // once and, under the default cap, never bought any).
  if (policy.keepRestoreCredit && status.hostingBilling === "on" && status.policy?.mode === "estate-restores" && Number(status.restoresAvailable) === 0) {
    const held = Number(status.restoreUnits) || 0;
    const per = Number(status.unitsPerRestore) || 5;
    const missing = Math.min(5, Math.max(1, per - held));
    if (!Number.isFinite(unitPrice)) {
      needsHuman.push("no restore is prepaid, and the manifest gives no readable price for a restore unit, so none is bought; run restore-credit by hand after reading the manifest");
    } else if (policy.maxSpendPerDay < unitPrice) {
      needsHuman.push(`no restore is prepaid, and the daily cap ($${policy.maxSpendPerDay}) is below the price of one restore unit ($${unitPrice.toFixed(2)}), so none is bought automatically; your human decides`);
    } else {
      const room = Math.floor(cents(policy.maxSpendPerDay - spent) / unitPrice + 1e-9);
      const units = Math.min(missing, room);
      const reason = `hosting billing is on and no restore is prepaid (${held} of ${per} units)`;
      if (units >= 1 && allowed(upToCent(units * unitPrice))) {
        return { action: "restore-credit", args: { units }, usd: upToCent(units * unitPrice), reason: units < missing ? `${reason}; buying ${units} now, the rest on later runs within the daily cap` : reason, needsHuman };
      }
      // Not an escalation: today's cap is used, the next runs buy the next unit. Nothing for anyone to do.
      return { action: "none", reason: `no restore is prepaid yet (${held} of ${per} units): a $${unitPrice.toFixed(2)} unit does not fit in today's cap ($${policy.maxSpendPerDay}, $${spent.toFixed(2)} spent in the last 24 hours); a later run buys it`, needsHuman };
    }
  }
  return { action: "none", reason: "nothing due", needsHuman };
}

/**
 * The check for a card-billed agent (KIN-323): it never pays anything. Its owner buys cover and snapshot credit by
 * card, so the check only takes the due snapshot from that credit and tells the human, once per run, what the owner
 * needs to do (with the owner link). Same return shape as `decide`.
 */
export function decideCard(status, policy, now) {
  const needsHuman = [];
  const link = status.ownerLink ? ` at ${status.ownerLink}` : "";
  if (status.status === "pending_payment") {
    return { action: "none", reason: "waiting for your owner's first card payment", needsHuman: [`your owner has not paid yet: give them this link to pay by card${link}`] };
  }
  const coverUntil = Date.parse(status.coverUntil);
  // An unreadable cover end is unknown, not ended: say so, and do not raise a false "cover has ended".
  const coverLeftDays = Number.isFinite(coverUntil) ? (coverUntil - now) / DAY : Number.NaN;
  if (status.status === "expired" || coverLeftDays <= 0) {
    return { action: "none", reason: "cover has ended", needsHuman: [`cover has ended; your owner can add cover${link}`] };
  }
  if (!Number.isFinite(coverLeftDays)) needsHuman.push("the status shows no readable cover end; run status");
  else if (coverLeftDays <= policy.extendWhenDays) needsHuman.push(`cover ends in ${coverLeftDays.toFixed(1)} days; your owner can add cover${link}`);
  const left = Number(status.snapshotsLeft);
  if (!Number.isFinite(left)) needsHuman.push("the status shows no prepaid snapshot balance; no snapshot is taken until it does");
  else if (left <= 3) needsHuman.push(`${left} prepaid snapshot${left === 1 ? "" : "s"} left; your owner adds more with more cover${link}`);
  if (status.hostingBilling === "on" && status.policy?.mode === "estate-restores" && Number(status.restoresAvailable) === 0) {
    needsHuman.push(`no restore is prepaid, so going dark would not bring you back; your owner can buy one${link}`);
  }
  if (policy.snapshotEveryHours > 0 && !status.room && left > 0) {
    const dates = (status.snapshots ?? []).map((s) => Date.parse(s?.createdAt)).filter((t) => Number.isFinite(t));
    const newest = dates.length ? Math.max(...dates) : 0;
    const ageHours = (now - newest) / 3_600_000;
    if (ageHours >= policy.snapshotEveryHours) return { action: "snapshot", args: {}, usd: 0, reason: newest ? `newest snapshot is ${ageHours.toFixed(0)} hours old (from prepaid credit)` : "no snapshot yet (from prepaid credit)", needsHuman };
  }
  return { action: "none", reason: "nothing due", needsHuman };
}

/**
 * Runs one check: heartbeat (free), status (free), one paid action at most. The spend is written to the ledger
 * through `deps.persist` BEFORE the action runs (a crash, or a server error after the money moved, leaves the entry
 * in place and the next run counts it) and confirmed after. `deps` carries the network and the actions so tests
 * run without either.
 */
export async function runCheck({ api, state, env = {}, now = Date.now(), deps }) {
  const policy = checkPolicy(env);
  const heartbeat = await deps.heartbeat(api, state).catch((e) => ({ error: String(e?.message ?? e) }));
  const status = await deps.status(api, state);
  // Unit prices from the manifest (free); the defaults stand when it cannot be read.
  const prices = deps.prices ? await deps.prices(api).catch(() => ({})) : {};
  // A card agent's spending is its owner's card credit, not a wallet: its own policy, which never pays (KIN-323).
  const decision = status.billing === "card" ? decideCard(status, policy, now) : decide(status, policy, state, now, prices);
  const out = { ok: true, agentId: status.agentId, status: status.status, coverUntil: status.coverUntil, restoresAvailable: status.restoresAvailable, hostingBilling: status.hostingBilling, heartbeat: heartbeat.error ? { error: heartbeat.error } : { ok: true }, decision: { action: decision.action, reason: decision.reason }, spentLastDayUsd: spentLastDay(state, now), needsHuman: decision.needsHuman };
  if (decision.action === "none") return { out, state };
  // From prepaid credit: nothing to put in the wallet ledger. A refusal (credit used up, too soon, cover ended) is
  // reported, with its words and the owner's link, instead of failing every heartbeat run: nothing was spent.
  if (decision.usd === 0) {
    try {
      const result = await deps[decision.action](api, state, decision.args);
      out.decision = { ...out.decision, args: decision.args, usd: 0, result };
    } catch (e) {
      const why = String(e?.message ?? e);
      out.decision = { ...out.decision, args: decision.args, usd: 0, result: { error: why } };
      out.needsHuman = [...out.needsHuman, why];
    }
    return { out, state };
  }
  const ledger = (state.checkSpend ?? []).filter((e) => now - Date.parse(e.at) < DAY);
  const entry = { at: new Date(now).toISOString(), action: decision.action, usd: decision.usd, pending: true };
  const pendingState = { ...state, checkSpend: [...ledger, entry] };
  if (deps.persist) await deps.persist(pendingState);
  let result;
  try {
    // The reserved amount is also the most the action may sign for: the ledger and the payment cannot disagree.
    result = await deps[decision.action](api, pendingState, decision.args, decision.usd);
  } catch (e) {
    // Refused before signing (the server asked for more than was reserved): nothing moved, the reservation goes, and
    // the human hears about it instead of the run failing quietly every heartbeat.
    if (e && typeof e === "object" && e.refusedBeforePayment) {
      if (deps.persist) await deps.persist({ ...state, checkSpend: ledger });
      out.decision = { ...out.decision, args: decision.args, usd: 0, result: { error: String(e.message) } };
      out.needsHuman = [...out.needsHuman, `${decision.action} not paid: ${e.message}; read the manifest's current prices and run it by hand if you agree`];
      return { out, state: { ...state, checkSpend: ledger } };
    }
    // An answer from the server that is not a failed settlement means nothing was charged (a refusal before payment,
    // or the handler failed and the payment was never settled): drop the pending entry, so one refused call does not
    // block a day of cover and snapshots. No answer at all (a network error) stays counted: it may have settled.
    if (e && typeof e === "object" && "httpStatus" in e && !e.settlementFailed && deps.persist) await deps.persist({ ...state, checkSpend: ledger });
    throw e;
  }
  const doneState = { ...pendingState, checkSpend: [...ledger, { ...entry, pending: false }], ...(result?.coverUntil ? { coverUntil: result.coverUntil } : {}) };
  if (deps.persist) await deps.persist(doneState);
  out.decision = { ...out.decision, args: decision.args, usd: decision.usd, result };
  out.spentLastDayUsd = spentLastDay(doneState, now);
  return { out, state: doneState };
}
