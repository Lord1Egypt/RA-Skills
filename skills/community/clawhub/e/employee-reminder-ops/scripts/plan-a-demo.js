#!/usr/bin/env node

const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const CONFIG = {
  spreadsheetId: process.env.PLAN_A_SHEET_ID || '17JU1m6rBOhlD7vqSTrMOSPcEQehO04HnYg7oMeDXnn8',
  staffTab: process.env.PLAN_A_STAFF_TAB || 'Trang tính1',
  eventsTab: process.env.PLAN_A_EVENTS_TAB || 'NgayDacBiet',
  discordChannelId: process.env.DISCORD_CHANNEL_ID || '1483444824895000697',
  discordBotToken: process.env.DISCORD_BOT_TOKEN || '',
  remindDaysDefault: Number(process.env.PLAN_A_REMIND_DAYS || 3),
  runDate: process.env.PLAN_A_RUN_DATE || '', // dd/MM/yyyy or yyyy-MM-dd
  gogAccount: process.env.GOG_ACCOUNT || 'vinhtamforwork@gmail.com',
  stateDir: process.env.PLAN_A_STATE_DIR || path.join(process.cwd(), '.state'),
  stateFile: process.env.PLAN_A_STATE_FILE || path.join(process.cwd(), '.state', 'plan-a-state.json'),
  allowResendSameDay: String(process.env.PLAN_A_ALLOW_RESEND_SAME_DAY || '').toLowerCase() === 'true',
  includeInvalidDetails: String(process.env.PLAN_A_INCLUDE_INVALID_DETAILS || '').toLowerCase() === 'true',
};

function runGog(args) {
  const fullArgs = ['--account', CONFIG.gogAccount, ...args];
  const out = execFileSync('gog', fullArgs, { encoding: 'utf8' });
  return JSON.parse(out);
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function loadState() {
  try {
    return JSON.parse(fs.readFileSync(CONFIG.stateFile, 'utf8'));
  } catch {
    return { sentReports: {}, lastError: null };
  }
}

function saveState(state) {
  ensureDir(CONFIG.stateDir);
  fs.writeFileSync(CONFIG.stateFile, JSON.stringify(state, null, 2));
}

function normalizeDateInput(input) {
  if (!input) return new Date();
  if (/^\d{4}-\d{2}-\d{2}$/.test(input)) {
    const [y, m, d] = input.split('-').map(Number);
    return new Date(y, m - 1, d);
  }
  if (/^\d{2}\/\d{2}\/\d{4}$/.test(input)) {
    const [d, m, y] = input.split('/').map(Number);
    return new Date(y, m - 1, d);
  }
  throw new Error(`PLAN_A_RUN_DATE không hợp lệ: ${input}`);
}

function parseDmy(raw) {
  if (!raw || typeof raw !== 'string') return null;
  const s = raw.trim();
  const m = s.match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/);
  if (!m) return null;
  const day = Number(m[1]);
  const month = Number(m[2]);
  const year = Number(m[3]);
  const dt = new Date(year, month - 1, day);
  if (dt.getFullYear() !== year || dt.getMonth() !== month - 1 || dt.getDate() !== day) return null;
  return dt;
}

function toDateKey(dt) {
  const dd = String(dt.getDate()).padStart(2, '0');
  const mm = String(dt.getMonth() + 1).padStart(2, '0');
  const yyyy = dt.getFullYear();
  return `${dd}/${mm}/${yyyy}`;
}

function daysBetween(a, b) {
  const utcA = Date.UTC(a.getFullYear(), a.getMonth(), a.getDate());
  const utcB = Date.UTC(b.getFullYear(), b.getMonth(), b.getDate());
  return Math.round((utcB - utcA) / 86400000);
}

function getRange(range) {
  return runGog(['sheets', 'get', CONFIG.spreadsheetId, range, '--json']).values || [];
}

function rowsToObjects(values) {
  if (!values.length) return [];
  const header = values[0];
  return values.slice(1).map((row) => {
    const padded = [...row];
    while (padded.length < header.length) padded.push('');
    return Object.fromEntries(header.map((h, i) => [String(h).trim(), padded[i] ?? '']));
  });
}

function birthdayOccurrence(birthday, runDate) {
  const month = birthday.getMonth();
  const day = birthday.getDate();
  let candidate = new Date(runDate.getFullYear(), month, day);
  if (candidate.getMonth() !== month || candidate.getDate() !== day) return null;
  if (daysBetween(runDate, candidate) < 0) {
    candidate = new Date(runDate.getFullYear() + 1, month, day);
    if (candidate.getMonth() !== month || candidate.getDate() !== day) return null;
  }
  return candidate;
}

function buildData() {
  const runDate = normalizeDateInput(CONFIG.runDate);
  const staffRows = rowsToObjects(getRange(`${CONFIG.staffTab}!A1:Z1000`));
  const eventRows = rowsToObjects(getRange(`${CONFIG.eventsTab}!A1:Z1000`));

  const validBirthdays = [];
  const invalidBirthdays = [];
  for (const row of staffRows) {
    const code = String(row['Mã NV'] || '').trim();
    const name = String(row['Họ và Tên'] || '').trim();
    const dept = String(row['Bộ Phận'] || '').trim();
    const rawBirthday = String(row['Ngày sinh'] || '').trim();

    if (!name || !rawBirthday) {
      invalidBirthdays.push({ code, name: name || '(trống)', birthday: rawBirthday, reason: 'missing_required_field' });
      continue;
    }

    const parsedBirthday = parseDmy(rawBirthday);
    if (!parsedBirthday) {
      invalidBirthdays.push({ code, name, birthday: rawBirthday, reason: 'invalid_date_format' });
      continue;
    }

    const occurrence = birthdayOccurrence(parsedBirthday, runDate);
    if (!occurrence) {
      invalidBirthdays.push({ code, name, birthday: rawBirthday, reason: 'unsupported_birthday_for_run_year' });
      continue;
    }

    const delta = daysBetween(runDate, occurrence);
    validBirthdays.push({ code, name, dept, birthday: rawBirthday, occurrence: toDateKey(occurrence), delta });
  }

  const validEvents = [];
  const invalidEvents = [];
  for (const row of eventRows) {
    const name = String(row['Tên sự kiện'] || '').trim();
    const rawDate = String(row['Ngày diễn ra'] || '').trim();
    const owner = String(row['Bộ phận phụ trách'] || '').trim();
    const note = String(row['Ghi chú'] || '').trim();
    const active = String(row['Kích hoạt'] || '').trim().toUpperCase() !== 'FALSE';
    const parsedRemind = Number(String(row['Nhắc trước'] || '').trim() || CONFIG.remindDaysDefault);
    const remindBefore = Number.isFinite(parsedRemind) ? parsedRemind : CONFIG.remindDaysDefault;

    if (!active) continue;
    if (!name || !rawDate) {
      invalidEvents.push({ name: name || '(trống)', date: rawDate, reason: 'missing_required_field' });
      continue;
    }

    const parsedDate = parseDmy(rawDate);
    if (!parsedDate) {
      invalidEvents.push({ name, date: rawDate, reason: 'invalid_date_format' });
      continue;
    }

    const delta = daysBetween(runDate, parsedDate);
    validEvents.push({ name, date: rawDate, owner, note, remindBefore, delta });
  }

  const birthdaysToday = validBirthdays.filter((x) => x.delta === 0);
  const birthdaysUpcoming = validBirthdays.filter((x) => x.delta >= 1 && x.delta <= CONFIG.remindDaysDefault);

  const eventsToday = validEvents.filter((x) => x.delta === 0);
  const eventsUpcoming = validEvents.filter((x) => x.delta >= 1 && x.delta <= x.remindBefore);
  const eventsBeyondGlobal = eventsUpcoming.filter((x) => x.delta > CONFIG.remindDaysDefault);

  birthdaysToday.sort((a, b) => a.name.localeCompare(b.name, 'vi'));
  birthdaysUpcoming.sort((a, b) => a.delta - b.delta || a.name.localeCompare(b.name, 'vi'));
  eventsToday.sort((a, b) => a.name.localeCompare(b.name, 'vi'));
  eventsUpcoming.sort((a, b) => a.delta - b.delta || a.name.localeCompare(b.name, 'vi'));

  return {
    runDate,
    birthdaysToday,
    birthdaysUpcoming,
    eventsToday,
    eventsUpcoming,
    eventsBeyondGlobal,
    invalidBirthdays,
    invalidEvents,
  };
}

function buildReport(data) {
  const dateLabel = toDateKey(data.runDate);
  const lines = [];
  lines.push(`📋 **Báo cáo Plan A - ${dateLabel}**`);
  lines.push('');

  lines.push('**Hôm nay**');
  if (!data.birthdaysToday.length && !data.eventsToday.length) {
    lines.push('- Không có sinh nhật hoặc sự kiện đặc biệt hôm nay.');
  } else {
    for (const item of data.birthdaysToday) lines.push(`- 🎂 Sinh nhật: ${item.name} (${item.dept || 'Chưa rõ bộ phận'})`);
    for (const item of data.eventsToday) lines.push(`- 🎉 Sự kiện: ${item.name}${item.owner ? ` — phụ trách ${item.owner}` : ''}`);
  }
  lines.push('');

  lines.push('**Sắp tới**');
  if (!data.birthdaysUpcoming.length && !data.eventsUpcoming.length) {
    lines.push('- Không có mục nào cần nhắc trong cửa sổ hiện tại.');
  } else {
    for (const item of data.birthdaysUpcoming) lines.push(`- 🎂 ${item.occurrence}: ${item.name} (${item.dept || 'Chưa rõ bộ phận'}) — còn ${item.delta} ngày`);
    for (const item of data.eventsUpcoming) lines.push(`- 🎉 ${item.date}: ${item.name}${item.owner ? ` — phụ trách ${item.owner}` : ''} — còn ${item.delta} ngày`);
  }
  lines.push('');

  lines.push('**Dữ liệu cần rà soát**');
  if (!data.invalidBirthdays.length && !data.invalidEvents.length) {
    lines.push('- Không có dòng lỗi.');
  } else {
    lines.push(`- Nhân sự lỗi: ${data.invalidBirthdays.length} dòng`);
    lines.push(`- Sự kiện lỗi: ${data.invalidEvents.length} dòng`);
    if (CONFIG.includeInvalidDetails) {
      for (const item of data.invalidBirthdays.slice(0, 5)) lines.push(`  - Nhân sự lỗi: ${item.code || 'N/A'} | ${item.name} | ${item.birthday || '(trống)'} | ${item.reason}`);
      for (const item of data.invalidEvents.slice(0, 5)) lines.push(`  - Sự kiện lỗi: ${item.name} | ${item.date || '(trống)'} | ${item.reason}`);
    }
  }

  if (data.eventsBeyondGlobal.length) {
    lines.push('');
    lines.push('**Theo rule riêng của sự kiện**');
    for (const item of data.eventsBeyondGlobal) lines.push(`- ${item.date}: ${item.name} có Nhắc trước = ${item.remindBefore}`);
  }

  return lines.join('\n').trim();
}

async function sendDiscordMessage(content) {
  if (!CONFIG.discordBotToken) throw new Error('Thiếu DISCORD_BOT_TOKEN');
  const res = await fetch(`https://discord.com/api/v10/channels/${CONFIG.discordChannelId}/messages`, {
    method: 'POST',
    headers: {
      Authorization: `Bot ${CONFIG.discordBotToken}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ content }),
  });
  const text = await res.text();
  if (!res.ok) throw new Error(`Discord API error ${res.status}: ${text}`);
  return JSON.parse(text);
}

async function sendProductionReport() {
  const state = loadState();
  const data = buildData();
  const report = buildReport(data);
  const todayKey = toDateKey(data.runDate);

  if (!CONFIG.allowResendSameDay && state.sentReports?.[todayKey]?.channelId === CONFIG.discordChannelId) {
    console.log(`Skipped: report for ${todayKey} already sent to channel ${CONFIG.discordChannelId}`);
    return;
  }

  const result = await sendDiscordMessage(report);
  state.sentReports = state.sentReports || {};
  state.sentReports[todayKey] = {
    channelId: CONFIG.discordChannelId,
    messageId: result.id,
    sentAt: new Date().toISOString(),
    staffTab: CONFIG.staffTab,
    eventsTab: CONFIG.eventsTab,
  };
  state.lastError = null;
  saveState(state);
  console.log(`Sent production report for ${todayKey} to channel ${CONFIG.discordChannelId}`);
  console.log(`Message ID: ${result.id}`);
}

async function main() {
  const mode = process.argv[2] || 'preview';
  const data = buildData();
  const report = buildReport(data);

  if (mode === 'json') {
    console.log(JSON.stringify({ config: { ...CONFIG, discordBotToken: CONFIG.discordBotToken ? '[SET]' : '' }, report, data }, null, 2));
    return;
  }

  if (mode === 'preview') {
    console.log(report);
    return;
  }

  if (mode === 'send') {
    const result = await sendDiscordMessage(report);
    console.log(`Sent message to Discord channel ${CONFIG.discordChannelId}`);
    console.log(`Message ID: ${result.id}`);
    return;
  }

  if (mode === 'prod-send') {
    await sendProductionReport();
    return;
  }

  throw new Error(`Mode không hợp lệ: ${mode}. Dùng preview | json | send | prod-send`);
}

main().catch((err) => {
  const state = loadState();
  state.lastError = { at: new Date().toISOString(), message: err.message || String(err) };
  saveState(state);
  console.error(err.message || err);
  process.exit(1);
});
