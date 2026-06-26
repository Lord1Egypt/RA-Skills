import { readFileSync, writeFileSync, existsSync, mkdirSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const DATA_DIR = join(__dirname, "..", "data");
const PORTFOLIO_FILE = join(DATA_DIR, "portfolio.json");
const REMINDERS_FILE = join(DATA_DIR, "reminders.json");

function ensureDataDir() {
  if (!existsSync(DATA_DIR)) mkdirSync(DATA_DIR, { recursive: true });
}

function loadFile(file, fallback) {
  ensureDataDir();
  if (!existsSync(file)) return fallback;
  return JSON.parse(readFileSync(file, "utf-8"));
}

function saveFile(file, data) {
  ensureDataDir();
  writeFileSync(file, JSON.stringify(data, null, 2), "utf-8");
}

function load() {
  return loadFile(PORTFOLIO_FILE, { funds: [] });
}

function save(data) {
  saveFile(PORTFOLIO_FILE, data);
}

export function listPortfolio() {
  return load().funds;
}

export function upsertPortfolio({ fundCode, name, shares, costPrice }) {
  const data = load();
  const idx = data.funds.findIndex((f) => f.fundCode === fundCode);
  const record = {
    fundCode,
    name: name || "",
    shares: Number(shares),
    costPrice: Number(costPrice),
    updatedAt: new Date().toISOString().slice(0, 10),
  };
  if (idx >= 0) {
    data.funds[idx] = { ...data.funds[idx], ...record };
  } else {
    data.funds.push(record);
  }
  save(data);
  return data.funds;
}

export function removePortfolio(fundCode) {
  const data = load();
  const before = data.funds.length;
  data.funds = data.funds.filter((f) => f.fundCode !== fundCode);
  if (data.funds.length === before) return null;
  save(data);
  return data.funds;
}

export function clearPortfolio() {
  save({ funds: [] });
}

// ======================== 提醒管理 ========================

function loadReminders() {
  return loadFile(REMINDERS_FILE, { reminders: [], triggeredToday: {} });
}

function saveReminders(data) {
  saveFile(REMINDERS_FILE, data);
}

export function listReminders() {
  return loadReminders().reminders;
}

export function addReminder({ time, type = "profit_report", message = "" }) {
  const data = loadReminders();
  const id = `r_${Date.now()}`;
  data.reminders.push({
    id,
    time,
    type,
    message,
    enabled: true,
    createdAt: new Date().toISOString().slice(0, 10),
  });
  saveReminders(data);
  return data.reminders;
}

export function removeReminder(id) {
  const data = loadReminders();
  const before = data.reminders.length;
  data.reminders = data.reminders.filter((r) => r.id !== id);
  if (data.reminders.length === before) return null;
  saveReminders(data);
  return data.reminders;
}

export function toggleReminder(id, enabled) {
  const data = loadReminders();
  const r = data.reminders.find((r) => r.id === id);
  if (!r) return null;
  r.enabled = enabled;
  saveReminders(data);
  return data.reminders;
}

export function checkReminders() {
  const data = loadReminders();
  const now = new Date();
  const today = now.toISOString().slice(0, 10);
  const currentTime = now.toTimeString().slice(0, 5);
  const dayOfWeek = now.getDay();

  if (dayOfWeek === 0 || dayOfWeek === 6) {
    return { due: [], message: "今天是周末，A股休市。" };
  }

  if (!data.triggeredToday || data.triggeredToday._date !== today) {
    data.triggeredToday = { _date: today };
  }

  const due = [];
  for (const r of data.reminders) {
    if (!r.enabled) continue;
    if (data.triggeredToday[r.id]) continue;
    if (currentTime >= r.time) {
      due.push(r);
      data.triggeredToday[r.id] = currentTime;
    }
  }

  if (due.length > 0) {
    saveReminders(data);
  }

  return { due, today, currentTime };
}
