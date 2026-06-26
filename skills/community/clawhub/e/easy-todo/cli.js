#!/usr/bin/env node
// openclawd TODO skill — cli.js
// Plain Node.js, zero dependencies. Copy this file alongside SKILL.md.
//
// Usage: node cli.js <command> [options]
// The todos.md file is created next to this script on first run.

"use strict";

const fs   = require("fs");
const path = require("path");

// ─── Store path ───────────────────────────────────────────────────────────────

const TODOS_FILE = process.env.TODOS_FILE
  || path.join(__dirname, "todos.md");

// ─── Date helpers ─────────────────────────────────────────────────────────────

function todayISO() {
  return new Date().toISOString().slice(0, 10);
}

function addDays(dateISO, n) {
  const d = new Date(dateISO);
  d.setUTCDate(d.getUTCDate() + n);
  return d.toISOString().slice(0, 10);
}

function nextMonday(from) {
  const d = new Date(from);
  const day = d.getUTCDay();
  d.setUTCDate(d.getUTCDate() + (day === 1 ? 7 : (8 - day) % 7 || 7));
  return d.toISOString().slice(0, 10);
}

// weekdays: array of UTC day numbers (0=Sun … 6=Sat), must be non-empty.
// Returns the next date strictly after `from` that falls on one of those days.
function nextWeekdayOccurrence(from, weekdays) {
  const d = new Date(from);
  for (let i = 1; i <= 7; i++) {
    d.setUTCDate(d.getUTCDate() + 1);
    if (weekdays.includes(d.getUTCDay())) return d.toISOString().slice(0, 10);
  }
  throw new Error("nextWeekdayOccurrence: no match (weekdays list empty?)");
}

const DAY_ABBR  = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"];
const DAY_FULL  = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"];
const DAY_SHORT = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"];

// Parse a comma-separated day string like "mon,wed,fri" or "1,3,5" into
// a sorted array of day numbers (0–6). Throws on unrecognised input.
function parseWeekdays(str) {
  const days = str.split(",").map(s => s.trim().toLowerCase()).filter(Boolean);
  const nums = days.map(s => {
    const n = parseInt(s, 10);
    if (!isNaN(n) && n >= 0 && n <= 6) return n;
    const abbr = DAY_ABBR.indexOf(s.slice(0, 3));
    if (abbr !== -1) return abbr;
    const full = DAY_FULL.indexOf(s);
    if (full !== -1) return full;
    throw new Error(`Unrecognised day "${s}". Use: sun mon tue wed thu fri sat (or 0–6)`);
  });
  if (!nums.length) throw new Error("--days requires at least one day");
  return [...new Set(nums)].sort((a, b) => a - b);
}

function fmtWeekdays(weekdays) {
  return weekdays.map(n => DAY_SHORT[n]).join(", ");
}

function nextFirstOfMonth(from) {
  const d = new Date(from);
  d.setUTCDate(1);
  d.setUTCMonth(d.getUTCMonth() + 1);
  return d.toISOString().slice(0, 10);
}

function nextLastOfMonth(from) {
  const d = new Date(from);
  d.setUTCDate(1);
  d.setUTCMonth(d.getUTCMonth() + 2);
  d.setUTCDate(d.getUTCDate() - 1);
  return d.toISOString().slice(0, 10);
}

function nextDueDate(frequency, after, weekdays) {
  switch (frequency) {
    case "daily":         return addDays(after, 1);
    case "weekly":        return nextMonday(after);
    case "monthly-first": return nextFirstOfMonth(after);
    case "monthly-last":  return nextLastOfMonth(after);
    case "weekdays":      return nextWeekdayOccurrence(after, weekdays || []);
    default: throw new Error(`Unknown frequency: ${frequency}`);
  }
}

// ─── Store read / write ───────────────────────────────────────────────────────

const STORE_START = "<!-- STORE_JSON";
const STORE_END   = "STORE_JSON -->";
const EMPTY_STORE = { tasks: [], recurringTasks: [] };

function readStore() {
  if (!fs.existsSync(TODOS_FILE)) return { ...EMPTY_STORE, tasks: [], recurringTasks: [] };
  const content = fs.readFileSync(TODOS_FILE, "utf8");
  const s = content.indexOf(STORE_START);
  const e = content.indexOf(STORE_END);
  if (s === -1 || e === -1) return { ...EMPTY_STORE };
  try {
    return JSON.parse(content.slice(s + STORE_START.length, e).trim());
  } catch {
    return { ...EMPTY_STORE };
  }
}

function writeStore(store) {
  const json = JSON.stringify(store, null, 2);
  fs.writeFileSync(TODOS_FILE, renderMarkdown(store, json), "utf8");
}

// ─── Markdown renderer ────────────────────────────────────────────────────────

function esc(s) { return String(s).replace(/\|/g, "\\|"); }

function renderMarkdown(store, json) {
  const now = new Date().toISOString().slice(0, 16).replace("T", " ") + " UTC";
  const active    = store.tasks.filter(t => t.status === "active").sort(byDuePriority);
  const completed = store.tasks.filter(t => t.status === "completed")
                               .sort((a, b) => (b.completedAt || "").localeCompare(a.completedAt || ""));

  const lines = [
    `# TODO List\n`,
    `_Last updated: ${now}_\n`,
    `${STORE_START}\n${json}\n${STORE_END}\n`,
    `## 📋 Active Tasks\n`,
  ];

  if (active.length === 0) {
    lines.push("_No active tasks._\n");
  } else {
    lines.push("| ID | Task | Due | Priority | Tags |");
    lines.push("|----|------|-----|----------|------|");
    active.forEach(t => {
      const notes = t.notes ? `<br><sub>${esc(t.notes)}</sub>` : "";
      lines.push(`| ${t.id} | ${esc(t.title)}${notes} | ${t.dueDate || "—"} | ${t.priority} | ${(t.tags||[]).join(", ") || "—"} |`);
    });
    lines.push("");
  }

  lines.push(`## 🔁 Recurring Tasks\n`);
  if (store.recurringTasks.length === 0) {
    lines.push("_No recurring tasks._\n");
  } else {
    lines.push("| ID | Task | Frequency | Next Due | Priority |");
    lines.push("|----|------|-----------|----------|----------|");
    store.recurringTasks.forEach(t => {
      const freq = t.frequency === "weekdays"
        ? `weekdays: ${fmtWeekdays(t.weekdays || [])}`
        : t.frequency;
      lines.push(`| ${t.id} | ${esc(t.title)} | ${freq} | ${t.nextDueDate} | ${t.priority} |`);
    });
    lines.push("");
  }

  lines.push(`## ✅ Completed Tasks\n`);
  if (completed.length === 0) {
    lines.push("_No completed tasks yet._\n");
  } else {
    lines.push("| ID | Task | Completed | Due |");
    lines.push("|----|------|-----------|-----|");
    completed.forEach(t =>
      lines.push(`| ${t.id} | ${esc(t.title)} | ${(t.completedAt||"").slice(0,10) || "—"} | ${t.dueDate || "—"} |`)
    );
    lines.push("");
  }

  return lines.join("\n");
}

const PRIO = { high: 0, medium: 1, low: 2 };
function byDuePriority(a, b) {
  if (a.dueDate && b.dueDate) { const d = a.dueDate.localeCompare(b.dueDate); if (d) return d; }
  else if (a.dueDate) return -1;
  else if (b.dueDate) return  1;
  return (PRIO[a.priority] ?? 1) - (PRIO[b.priority] ?? 1);
}

// ─── ID helpers ───────────────────────────────────────────────────────────────

function nextId(store, prefix) {
  const all = prefix === "T" ? store.tasks : store.recurringTasks;
  const max = all.reduce((m, t) => { const n = parseInt(t.id.slice(1)); return isNaN(n) ? m : Math.max(m, n); }, 0);
  return `${prefix}${max + 1}`;
}

// ─── Task finders ─────────────────────────────────────────────────────────────

function findActive(store, ref) {
  return store.tasks.find(t => t.status === "active" && t.id === ref)
      || store.tasks.find(t => t.status === "active" && t.title.toLowerCase() === ref.toLowerCase())
      || store.tasks.find(t => t.status === "active" && t.title.toLowerCase().includes(ref.toLowerCase()));
}

// ─── Briefing formatters ──────────────────────────────────────────────────────

function fmtTask(t) {
  const due  = t.dueDate   ? ` (due ${t.dueDate})`   : "";
  const prio = t.priority !== "medium" ? ` [${t.priority}]` : "";
  return `• ${t.id} — ${t.title}${prio}${due}`;
}

// ─── Commands ─────────────────────────────────────────────────────────────────

function cmdAdd(pos, flags) {
  const title = pos[0] || flags["title"];
  if (!title) return die('task title required:  node cli.js add "<title>"');

  const store = readStore();
  const task = {
    id:        nextId(store, "T"),
    title,
    notes:     flags["notes"]    || undefined,
    dueDate:   flags["due"]      || undefined,
    priority:  flags["priority"] || "medium",
    status:    "active",
    createdAt: new Date().toISOString(),
    tags:      flags["tags"] ? flags["tags"].split(",").map(s => s.trim()) : [],
  };
  store.tasks.push(task);
  writeStore(store);

  const due  = task.dueDate   ? ` (due ${task.dueDate})`        : "";
  const prio = task.priority !== "medium" ? ` [${task.priority}]` : "";
  console.log(`Added ${task.id}: ${task.title}${due}${prio}`);
}

function cmdComplete(pos) {
  const ref = pos[0]; if (!ref) return die("provide task ID or title");
  const store = readStore();
  const task = findActive(store, ref);
  if (!task) return die(`no active task matching "${ref}"`);
  task.status      = "completed";
  task.completedAt = new Date().toISOString();
  writeStore(store);
  console.log(`Done: ${task.id} — ${task.title}`);
}

function cmdCancel(pos) {
  const ref = pos[0]; if (!ref) return die("provide task ID or title");
  const store = readStore();
  const task = findActive(store, ref);
  if (!task) return die(`no active task matching "${ref}"`);
  task.status = "cancelled";
  writeStore(store);
  console.log(`Cancelled: ${task.id} — ${task.title}`);
}

function cmdList(flags) {
  const store = readStore();

  if (flags["recurring"]) {
    const r = store.recurringTasks;
    if (!r.length) { console.log("No recurring tasks."); return; }
    r.forEach(t => {
      const freq = t.frequency === "weekdays"
        ? `weekdays: ${fmtWeekdays(t.weekdays || [])}`
        : t.frequency;
      console.log(`${t.id}: ${t.title} [${freq}] — next due: ${t.nextDueDate}`);
    });
    return;
  }

  if (flags["completed"]) {
    const done = store.tasks.filter(t => t.status === "completed");
    if (!done.length) { console.log("No completed tasks."); return; }
    done.slice(0, 30).forEach(t => console.log(`${t.id}: ${t.title} — completed ${(t.completedAt||"").slice(0,10)}`));
    return;
  }

  const today = todayISO();

  if (flags["today"]) {
    cmdMaterialize(true);
    const tasks = readStore().tasks.filter(t => t.status === "active" && (!t.dueDate || t.dueDate <= today));
    if (!tasks.length) { console.log("Nothing due today."); return; }
    tasks.sort(byDuePriority).forEach(t => console.log(fmtTask(t)));
    return;
  }

  if (flags["upcoming"]) {
    const days   = parseInt(flags["days"] || "7", 10);
    const future = addDays(today, days);
    const tasks  = store.tasks.filter(t => t.status === "active" && t.dueDate && t.dueDate > today && t.dueDate <= future);
    if (!tasks.length) { console.log(`No tasks due in the next ${days} days.`); return; }
    tasks.sort(byDuePriority).forEach(t => console.log(fmtTask(t)));
    return;
  }

  const active = store.tasks.filter(t => t.status === "active");
  if (!active.length) { console.log("No active tasks."); return; }
  active.sort(byDuePriority).forEach(t => console.log(fmtTask(t)));
}

function cmdAddRecurring(pos, flags) {
  const title = pos[0] || flags["title"];
  if (!title) return die('title required:  node cli.js add-recurring "<title>" --frequency ...');

  // --days implies --frequency weekdays
  let frequency = flags["frequency"];
  let weekdays;

  if (flags["days"]) {
    try { weekdays = parseWeekdays(String(flags["days"])); } catch (e) { return die(e.message); }
    if (frequency && frequency !== "weekdays")
      return die('--days cannot be combined with --frequency other than "weekdays"');
    frequency = "weekdays";
  }

  const valid = ["daily", "weekly", "monthly-first", "monthly-last", "weekdays"];
  if (!frequency || !valid.includes(frequency))
    return die(`--frequency required: ${valid.join(" | ")}\n  Or use --days mon,wed,fri for specific weekdays`);

  if (frequency === "weekdays" && !weekdays)
    return die('--days is required when using --frequency weekdays\n  Example: --days mon,wed,fri');

  const store = readStore();
  const today = todayISO();
  const task = {
    id:          nextId(store, "R"),
    title,
    notes:       flags["notes"]    || undefined,
    frequency,
    weekdays,                          // defined only for "weekdays" frequency
    priority:    flags["priority"] || "medium",
    tags:        flags["tags"] ? flags["tags"].split(",").map(s => s.trim()) : [],
    createdAt:   new Date().toISOString(),
    nextDueDate: nextDueDate(frequency, today, weekdays),
  };
  store.recurringTasks.push(task);
  writeStore(store);

  const freqStr = frequency === "weekdays"
    ? `weekdays: ${fmtWeekdays(weekdays)}`
    : frequency;
  console.log(`Added recurring ${task.id}: ${task.title} [${freqStr}] — next due: ${task.nextDueDate}`);
}

function cmdMaterialize(silent) {
  const store  = readStore();
  const today  = todayISO();
  const created = [];

  for (const r of store.recurringTasks) {
    if (r.nextDueDate <= today) {
      const already = store.tasks.some(t =>
        t.status === "active" && t.title === r.title && t.dueDate === r.nextDueDate
      );
      if (!already) {
        const task = {
          id:        nextId(store, "T"),
          title:     r.title,
          notes:     `(recurring: ${r.id})`,
          dueDate:   r.nextDueDate,
          priority:  r.priority,
          status:    "active",
          createdAt: new Date().toISOString(),
          tags:      [...(r.tags || []), "recurring"],
        };
        store.tasks.push(task);
        created.push(task);
      }
      r.lastTriggeredDate = r.nextDueDate;
      r.nextDueDate       = nextDueDate(r.frequency, r.nextDueDate, r.weekdays);
    }
  }

  if (created.length) writeStore(store);

  if (!silent) {
    if (!created.length) console.log("No recurring tasks to materialize.");
    else { console.log(`Materialized ${created.length} recurring task(s):`); created.forEach(t => console.log(` • ${t.id}: ${t.title} (due ${t.dueDate})`)); }
  }
}

function cmdBriefing(pos) {
  cmdMaterialize(true);
  const store = readStore();
  const today = todayISO();
  const type  = pos[0];

  const active  = store.tasks.filter(t => t.status === "active");
  const overdue = active.filter(t => t.dueDate && t.dueDate < today).sort(byDuePriority);
  const dueToday = active.filter(t => !t.dueDate || t.dueDate === today).sort(byDuePriority);
  const upcoming = active.filter(t => t.dueDate && t.dueDate > today && t.dueDate <= addDays(today, 7)).sort(byDuePriority);

  if (type === "morning") {
    const out = ["🌅 Good morning! Here is your TODO overview:\n"];
    if (overdue.length)  { out.push(`⚠️  Overdue (${overdue.length}):`);             overdue.forEach(t  => out.push(fmtTask(t))); out.push(""); }
    if (dueToday.length) { out.push(`📋 Due today (${dueToday.length}):`);           dueToday.forEach(t => out.push(fmtTask(t))); out.push(""); }
    else                   out.push("✨ Nothing due today — you are on top of things!\n");
    if (upcoming.length) { out.push(`📅 Coming up in the next 7 days (${upcoming.length}):`); upcoming.forEach(t => out.push(fmtTask(t))); }
    if (!overdue.length && !dueToday.length && !upcoming.length) out.push("🎉 No upcoming tasks.");
    console.log(out.join("\n"));
    return;
  }

  if (type === "evening") {
    const stillOpen = [...overdue, ...dueToday];
    const out = ["🌇 Evening check-in — still open today:\n"];
    if (!stillOpen.length) { console.log("🎉 All done for today — great work!"); return; }
    if (overdue.length)  { out.push(`⚠️  Overdue (${overdue.length}):`);  overdue.forEach(t  => out.push(fmtTask(t))); out.push(""); }
    if (dueToday.length) { out.push(`📋 Due today (${dueToday.length}):`); dueToday.forEach(t => out.push(fmtTask(t))); out.push(""); }
    out.push(`_${stillOpen.length} task${stillOpen.length !== 1 ? "s" : ""} left — you can do it! 💪_`);
    console.log(out.join("\n"));
    return;
  }

  die("specify morning or evening:  node cli.js briefing morning|evening");
}

function cmdHelp() {
  console.log(`
openclawd TODO skill

Commands:
  add "<title>" [--due YYYY-MM-DD] [--priority high|medium|low] [--notes "..."] [--tags a,b]
  complete <id-or-title>
  cancel   <id-or-title>
  list [--today] [--upcoming [--days N]] [--completed] [--recurring]
  add-recurring "<title>" --frequency daily|weekly|monthly-first|monthly-last|weekdays
                          --days mon,wed,fri   (sets frequency=weekdays; accepts full names, abbreviations, or 0–6)
  briefing morning|evening
  materialize
  help

Environment:
  TODOS_FILE   path to todos.md  (default: same directory as cli.js)
`.trim());
}

// ─── Arg parser ───────────────────────────────────────────────────────────────

function parseArgs(argv) {
  const args = argv.slice(2);
  const command    = args[0] || "help";
  const positional = [];
  const flags      = {};
  for (let i = 1; i < args.length; i++) {
    const a = args[i];
    if (a.startsWith("--")) {
      const key  = a.slice(2);
      const next = args[i + 1];
      if (next && !next.startsWith("--")) { flags[key] = next; i++; }
      else flags[key] = true;
    } else {
      positional.push(a);
    }
  }
  return { command, positional, flags };
}

function die(msg) { console.error(`error: ${msg}`); process.exit(1); }

// ─── Main ─────────────────────────────────────────────────────────────────────

const { command, positional, flags } = parseArgs(process.argv);

switch (command) {
  case "add":           cmdAdd(positional, flags);      break;
  case "complete":      cmdComplete(positional);        break;
  case "cancel":        cmdCancel(positional);          break;
  case "list":          cmdList(flags);                 break;
  case "add-recurring": cmdAddRecurring(positional, flags); break;
  case "briefing":      cmdBriefing(positional);        break;
  case "materialize":   cmdMaterialize(false);          break;
  case "help":
  default:              cmdHelp();                      break;
}
