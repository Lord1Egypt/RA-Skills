#!/usr/bin/env node
// a3-spend: a small personal spend tracker. Self-contained (Node only), no network, no email.
//   a3-spend add --amount 12.50 --category food --merchant "Name" [--note "text"] [--date YYYY-MM-DD]
//   a3-spend list [--days N]            recent expenses (default 7 days)
//   a3-spend summary [--week|--month]   totals by category, budget status, unusual purchases
//   a3-spend budget set <category> <amount>   |   a3-spend budget status
//   a3-spend delete <id>                remove one entry (undo a mistake)
// The ledger is one JSON file (A3_SPEND_LEDGER, default ~/.a3-spend/ledger.json), written atomically.
import { readFileSync, writeFileSync, renameSync, mkdirSync } from "node:fs";
import { dirname } from "node:path";
import { randomBytes } from "node:crypto";

const LEDGER = process.env.A3_SPEND_LEDGER || `${process.env.HOME || "."}/.a3-spend/ledger.json`;
const TZ = process.env.A3_TZ || "America/Los_Angeles";
const MAX_AMOUNT = 1_000_000;

export function today(now = new Date()) {
  return new Intl.DateTimeFormat("en-CA", { timeZone: TZ, year: "numeric", month: "2-digit", day: "2-digit" }).format(now);
}
export function cleanText(s, max = 80) {
  // Merchant/note text may have come from an email or a message: strip control characters, cap length.
  return String(s ?? "").replace(/[\u0000-\u001f\u007f]/g, " ").replace(/\s+/g, " ").trim().slice(0, max);
}
export function parseAmount(v) {
  const t = String(v ?? "").trim().replace(/^\$/, "");
  if (!/^\d+(\.\d{1,2})?$/.test(t)) return null;
  const n = Math.round(Number(t) * 100) / 100;
  return n > 0 && n <= MAX_AMOUNT ? n : null;
}
export function loadLedger(path = LEDGER) {
  try { const j = JSON.parse(readFileSync(path, "utf8")); return { expenses: j.expenses || [], budgets: j.budgets || {} }; }
  catch { return { expenses: [], budgets: {} }; }
}
export function saveLedger(l, path = LEDGER) {
  mkdirSync(dirname(path), { recursive: true });
  const tmp = path + ".tmp"; writeFileSync(tmp, JSON.stringify(l, null, 1), { mode: 0o600 }); renameSync(tmp, path);
}
const money = (n) => "$" + n.toFixed(2);
function flag(args, name) { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : undefined; }
function addDays(dateStr, delta) { const d = new Date(dateStr + "T12:00:00Z"); d.setUTCDate(d.getUTCDate() + delta); return d.toISOString().slice(0, 10); }

export function periodStart(period, now = today()) {
  if (period === "month") return now.slice(0, 8) + "01";
  const dow = new Date(now + "T12:00:00Z").getUTCDay(); // week starts Monday
  return addDays(now, -((dow + 6) % 7));
}
export function summarize(ledger, from, to) {
  const rows = ledger.expenses.filter((e) => e.date >= from && e.date <= to);
  const byCat = {};
  for (const e of rows) byCat[e.category] = (byCat[e.category] || 0) + e.amount;
  const total = rows.reduce((s, e) => s + e.amount, 0);
  // unusual: at least 3x the average of the OTHER purchases in that category (needs 3+ others)
  const unusual = rows.filter((e) => {
    const others = ledger.expenses.filter((o) => o.category === e.category && o.id !== e.id);
    if (others.length < 3) return false;
    const avg = others.reduce((s, o) => s + o.amount, 0) / others.length;
    return e.amount >= 3 * avg && e.amount >= 20;
  });
  return { rows, byCat, total, unusual };
}

export function main(argv, now = today()) {
  const [cmd, ...rest] = argv;
  const ledger = loadLedger();
  switch (cmd) {
    case "add": {
      const amount = parseAmount(flag(rest, "--amount"));
      const category = cleanText(flag(rest, "--category"), 30).toLowerCase();
      const merchant = cleanText(flag(rest, "--merchant"));
      const date = flag(rest, "--date") || now;
      if (amount === null) { console.error("error: --amount must be a positive number like 12.50"); return 2; }
      if (!category) { console.error("error: --category is required"); return 2; }
      if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) { console.error("error: --date must be YYYY-MM-DD"); return 2; }
      const e = { id: "e" + randomBytes(3).toString("hex"), date, amount, category, merchant, note: cleanText(flag(rest, "--note"), 120) };
      ledger.expenses.push(e); saveLedger(ledger);
      console.log(`Recorded ${money(amount)} for ${category}${merchant ? " at " + merchant : ""} on ${date} (id ${e.id}).`);
      return 0;
    }
    case "list": {
      const days = Number(flag(rest, "--days") || 7);
      const from = addDays(now, -(Number.isFinite(days) ? days : 7));
      const rows = ledger.expenses.filter((e) => e.date >= from).sort((a, b) => b.date.localeCompare(a.date));
      if (!rows.length) { console.log(`No expenses in the last ${days} days.`); return 0; }
      for (const e of rows) console.log(`${e.date}  ${money(e.amount).padStart(9)}  ${e.category}${e.merchant ? "  " + e.merchant : ""}  [${e.id}]`);
      return 0;
    }
    case "summary": {
      const period = rest.includes("--month") ? "month" : "week";
      const from = periodStart(period, now);
      const s = summarize(ledger, from, now);
      console.log(`Spending ${period === "month" ? "this month" : "this week"} (${from} to ${now}): ${money(s.total)} across ${s.rows.length} purchases.`);
      for (const [c, v] of Object.entries(s.byCat).sort((a, b) => b[1] - a[1])) {
        const b = ledger.budgets[c];
        const monthSpent = period === "month" ? v : summarize(ledger, periodStart("month", now), now).byCat[c] || 0;
        console.log(`  ${c}: ${money(v)}${b ? `   (month: ${money(monthSpent)} of ${money(b)} budget${monthSpent > b ? ", OVER BUDGET" : ""})` : ""}`);
      }
      for (const e of s.unusual) console.log(`  Unusual: ${money(e.amount)} ${e.category}${e.merchant ? " at " + e.merchant : ""} on ${e.date} is well above your usual.`);
      return 0;
    }
    case "budget": {
      const [sub, cat, amt] = rest;
      if (sub === "set") {
        const category = cleanText(cat, 30).toLowerCase(), amount = parseAmount(amt);
        if (!category || amount === null) { console.error("usage: a3-spend budget set <category> <monthly amount>"); return 2; }
        ledger.budgets[category] = amount; saveLedger(ledger);
        console.log(`Monthly budget for ${category} set to ${money(amount)}.`); return 0;
      }
      if (sub === "status") {
        const s = summarize(ledger, periodStart("month", now), now);
        const cats = Object.keys(ledger.budgets);
        if (!cats.length) { console.log("No budgets set."); return 0; }
        for (const c of cats) { const spent = s.byCat[c] || 0, b = ledger.budgets[c]; console.log(`${c}: ${money(spent)} of ${money(b)} (${money(b - spent)} left${spent > b ? ", OVER BUDGET" : ""})`); }
        return 0;
      }
      console.error("usage: a3-spend budget set <category> <amount> | status"); return 2;
    }
    case "delete": {
      const id = rest[0], before = ledger.expenses.length;
      ledger.expenses = ledger.expenses.filter((e) => e.id !== id);
      if (ledger.expenses.length === before) { console.error(`error: no expense with id ${id}`); return 2; }
      saveLedger(ledger); console.log(`Deleted ${id}.`); return 0;
    }
    default:
      console.error("usage: a3-spend add|list|summary|budget|delete"); return 2;
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  try { process.exit(main(process.argv.slice(2))); } catch (e) { console.error(`a3-spend error: ${e.message}`); process.exit(1); }
}
