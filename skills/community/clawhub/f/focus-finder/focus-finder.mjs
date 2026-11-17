// focus-finder: free focus blocks from calendar JSON on stdin. Read-only, no network.

/** @typedef {{ start: number, end: number }} Interval   // minutes since local midnight */
/** @typedef {{ start: number, end: number, minutes: number }} Gap */


function mergeIntervals(intervals){
    const values = Object.values(intervals);
    if (values.length === 0) return [];

    // 1. Sort by start time (shallow copy each interval to avoid mutating input)
    const sorted = values
        .map((item) => ({ ...item }))
        .sort((a, b) => a.start - b.start);

    // 2. Initialize merged list with the earliest interval
    /** @type {Interval[]} */
    const merged = [sorted[0]];

    // 3. Compare each interval against the last merged interval
    for (let i = 1; i < sorted.length; i++) {
        const current = sorted[i];
        const lastMerged = merged[merged.length - 1];

        // Check for overlap (use <= if touching intervals like [1, 4] and [4, 5] should merge)
        if (current.start <= lastMerged.end) {
        lastMerged.end = Math.max(lastMerged.end, current.end);
        } else {
        merged.push(current);
        }
    }

    return merged;
}
export const DEFAULTS = { dayStart: 9 * 60, dayEnd: 18 * 60, minMinutes: 45, timeZone: "America/Los_Angeles" };


/**
 * Pure interval math. No dates, no I/O.
 * @param {Interval[]} busy   any order, may overlap, may lie outside the window
 * @param {{dayStart:number, dayEnd:number, minMinutes:number}} opts
 * @returns {Gap[]}           sorted, each gap.minutes >= opts.minMinutes
 */
export function findGaps(busy, opts) {
  const { dayStart, dayEnd, minMinutes } = opts;

  const clipped = busy
    .map(({ start, end }) => ({
      start: Math.max(start, dayStart),
      end: Math.min(end, dayEnd),
    }))
    .filter(({ start, end }) => start < end)
    .sort((a, b) => a.start - b.start);

  const merged = [];
  for (const interval of clipped) {
    const last = merged[merged.length - 1];
    if (last && interval.start <= last.end) {
      last.end = Math.max(last.end, interval.end);
    } else {
      merged.push({ ...interval });
    }
  }

  const gaps = [];
  let cursor = dayStart;

  for (const { start, end } of merged) {
    if (start > cursor) {
      gaps.push({ start: cursor, end: start, minutes: start - cursor });
    }
    cursor = end;
  }

  if (cursor < dayEnd) {
    gaps.push({ start: cursor, end: dayEnd, minutes: dayEnd - cursor });
  }

  return gaps.filter(({ minutes }) => minutes >= minMinutes);
}

// ---- Below: assistant-written at the student's request ("Complete remaining part in M5", Nov 14). ----

const DAY_MINUTES = 24 * 60;
const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;
const LOCAL_RE = /^(\d{4}-\d{2}-\d{2})T(\d{2}):(\d{2})/;
const OFFSET_RE = /(Z|[+-]\d{2}:?\d{2})$/i;

/**
 * Wall-clock date and minute of an instant in a time zone (DST handled by Intl).
 * @param {Date} instant  @param {string} timeZone
 * @returns {{ date: string, minutes: number }}
 */
function localParts(instant, timeZone) {
  const fmt = new Intl.DateTimeFormat("en-US", {
    timeZone, hourCycle: "h23",
    year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit",
  });
  const p = Object.fromEntries(fmt.formatToParts(instant).map((x) => [x.type, x.value]));
  return { date: `${p.year}-${p.month}-${p.day}`, minutes: Number(p.hour) * 60 + Number(p.minute) };
}

/**
 * One event boundary → local date + minute, or null for all-day / unusable values.
 * Accepts Google's shape ({ dateTime } / { date }) or a plain ISO string.
 * A dateTime without an offset is read as wall-clock time in timeZone (not the machine's zone).
 * @param {unknown} boundary  @param {string} timeZone
 * @returns {{ date: string, minutes: number } | null}
 */
function boundaryParts(boundary, timeZone) {
  const iso = typeof boundary === "string" ? boundary
    : boundary && typeof boundary === "object" && typeof boundary.dateTime === "string" ? boundary.dateTime
    : null;
  if (!iso) return null; // all-day ({ date }) or malformed
  const m = LOCAL_RE.exec(iso);
  if (!m) return null; // date-only string = all-day
  if (!OFFSET_RE.test(iso)) return { date: m[1], minutes: Number(m[2]) * 60 + Number(m[3]) };
  const instant = new Date(iso);
  if (Number.isNaN(instant.getTime())) return null;
  return localParts(instant, timeZone);
}

/**
 * Turn calendar event JSON into busy intervals for one day.
 * Rules: all-day events are ignored (holidays, "WFH", reminders don't block time); cancelled events and
 * events marked free (transparency "transparent") are ignored; events crossing midnight are clipped to
 * the day; malformed events are skipped (calendar data is untrusted input).
 * @param {unknown} raw        parsed stdin: an array of events, or { events: [...] } / { items: [...] }
 * @param {string} date        "YYYY-MM-DD" in timeZone
 * @param {string} timeZone
 * @returns {Interval[]}
 */
export function toBusyIntervals(raw, date, timeZone) {
  const list = Array.isArray(raw) ? raw
    : raw && typeof raw === "object" && Array.isArray(raw.events) ? raw.events
    : raw && typeof raw === "object" && Array.isArray(raw.items) ? raw.items
    : [];
  /** @type {Interval[]} */
  const busy = [];
  for (const ev of list) {
    if (!ev || typeof ev !== "object") continue;
    if (ev.status === "cancelled" || ev.transparency === "transparent") continue;
    const s = boundaryParts(ev.start, timeZone);
    const e = boundaryParts(ev.end, timeZone);
    if (!s || !e) continue;
    if (s.date > date || e.date < date) continue; // ISO dates compare correctly as strings
    const start = s.date < date ? 0 : s.minutes;
    const end = e.date > date ? DAY_MINUTES : e.minutes;
    if (end > start) busy.push({ start, end });
  }
  return busy;
}

/** @param {number} m  @returns {string} "HH:MM" */
export function formatMinutes(m) {
  const h = Math.floor(m / 60);
  return `${String(h).padStart(2, "0")}:${String(m % 60).padStart(2, "0")}`;
}

/** Today's date in timeZone. @param {string} timeZone @param {Date} [now] */
export function todayIn(timeZone, now = new Date()) {
  return localParts(now, timeZone).date;
}

function fail(message) {
  process.stderr.write(`focus-finder: ${message}\n`);
  process.exit(2);
}

// CLI: node focus-finder.mjs [--date YYYY-MM-DD] [--min 45] [--json]   (calendar JSON on stdin)
// Exit 0 ok, 2 bad usage / bad JSON. Output contains times only, never event titles.
if (import.meta.main) {
  const { parseArgs } = await import("node:util");
  let values;
  try {
    ({ values } = parseArgs({
      options: { date: { type: "string" }, min: { type: "string" }, json: { type: "boolean" }, help: { type: "boolean" } },
      strict: true, allowPositionals: false,
    }));
  } catch (err) {
    fail(`${err.message} (usage: focus-finder.mjs [--date YYYY-MM-DD] [--min N] [--json] < events.json)`);
  }
  if (values.help) {
    process.stdout.write("usage: <calendar JSON> | node focus-finder.mjs [--date YYYY-MM-DD] [--min N] [--json]\n");
    process.exit(0);
  }
  const tz = DEFAULTS.timeZone;
  const date = values.date ?? todayIn(tz);
  if (!DATE_RE.test(date) || Number.isNaN(Date.parse(`${date}T00:00:00Z`))) fail("--date must be YYYY-MM-DD");
  const minMinutes = values.min === undefined ? DEFAULTS.minMinutes : Number(values.min);
  if (!Number.isInteger(minMinutes) || minMinutes < 1 || minMinutes > DEFAULTS.dayEnd - DEFAULTS.dayStart) {
    fail(`--min must be a whole number from 1 to ${DEFAULTS.dayEnd - DEFAULTS.dayStart}`);
  }
  if (process.stdin.isTTY) fail("pipe calendar JSON on stdin (for example: gog calendar events --today --json | ...)");

  let text = "";
  for await (const chunk of process.stdin) text += chunk;
  let raw;
  try {
    raw = JSON.parse(text);
  } catch {
    fail("stdin is not valid JSON");
  }

  const gaps = findGaps(toBusyIntervals(raw, date, tz), { ...DEFAULTS, minMinutes });
  if (values.json) {
    const out = gaps.map((g) => ({ start: formatMinutes(g.start), end: formatMinutes(g.end), minutes: g.minutes }));
    process.stdout.write(`${JSON.stringify({ date, timeZone: tz, minMinutes, gaps: out })}\n`);
  } else {
    const window = `${formatMinutes(DEFAULTS.dayStart)}–${formatMinutes(DEFAULTS.dayEnd)}`;
    process.stdout.write(`Focus blocks on ${date} (${tz}, ${window}, at least ${minMinutes} min):\n`);
    if (gaps.length === 0) process.stdout.write(`No focus blocks of ${minMinutes}+ minutes.\n`);
    for (const g of gaps) process.stdout.write(`${formatMinutes(g.start)}–${formatMinutes(g.end)} (${g.minutes} min)\n`);
  }
}

