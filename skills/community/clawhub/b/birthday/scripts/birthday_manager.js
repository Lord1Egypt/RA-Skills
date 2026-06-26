#!/usr/bin/env node
/*
中文生日提醒管理脚本（Node.js 版本）。

功能：
- 从中国身份证提取公历生日
- 默认按农历保存，也支持按公历保存
- 为每条记录单独设置提前提醒天数
- 列出记录、查询下一个生日、检查当天是否需要提醒
*/

const fs = require("fs");
const path = require("path");
const childProcess = require("child_process");

const LUNAR_INFO = [
  0x04bd8, 0x04ae0, 0x0a570, 0x054d5, 0x0d260, 0x0d950, 0x16554, 0x056a0,
  0x09ad0, 0x055d2, 0x04ae0, 0x0a5b6, 0x0a4d0, 0x0d250, 0x1d255, 0x0b540,
  0x0d6a0, 0x0ada2, 0x095b0, 0x14977, 0x04970, 0x0a4b0, 0x0b4b5, 0x06a50,
  0x06d40, 0x1ab54, 0x02b60, 0x09570, 0x052f2, 0x04970, 0x06566, 0x0d4a0,
  0x0ea50, 0x06e95, 0x05ad0, 0x02b60, 0x186e3, 0x092e0, 0x1c8d7, 0x0c950,
  0x0d4a0, 0x1d8a6, 0x0b550, 0x056a0, 0x1a5b4, 0x025d0, 0x092d0, 0x0d2b2,
  0x0a950, 0x0b557, 0x06ca0, 0x0b550, 0x15355, 0x04da0, 0x0a5d0, 0x14573,
  0x052d0, 0x0a9a8, 0x0e950, 0x06aa0, 0x0aea6, 0x0ab50, 0x04b60, 0x0aae4,
  0x0a570, 0x05260, 0x0f263, 0x0d950, 0x05b57, 0x056a0, 0x096d0, 0x04dd5,
  0x04ad0, 0x0a4d0, 0x0d4d4, 0x0d250, 0x0d558, 0x0b540, 0x0b5a0, 0x195a6,
  0x095b0, 0x049b0, 0x0a974, 0x0a4b0, 0x0b27a, 0x06a50, 0x06d40, 0x0af46,
  0x0ab60, 0x09570, 0x04af5, 0x04970, 0x064b0, 0x074a3, 0x0ea50, 0x06b58,
  0x05ac0, 0x0ab60, 0x096d5, 0x092e0, 0x0c960, 0x0d954, 0x0d4a0, 0x0da50,
  0x07552, 0x056a0, 0x0abb7, 0x025d0, 0x092d0, 0x0cab5, 0x0a950, 0x0b4a0,
  0x0baa4, 0x0ad50, 0x055d9, 0x04ba0, 0x0a5b0, 0x15176, 0x052b0, 0x0a930,
  0x07954, 0x06aa0, 0x0ad50, 0x05b52, 0x04b60, 0x0a6e6, 0x0a4e0, 0x0d260,
  0x0ea65, 0x0d530, 0x05aa0, 0x076a3, 0x096d0, 0x04bd7, 0x04ad0, 0x0a4d0,
  0x1d0b6, 0x0d250, 0x0d520, 0x0dd45, 0x0b5a0, 0x056d0, 0x055b2, 0x049b0,
  0x0a577, 0x0a4b0, 0x0aa50, 0x1b255, 0x06d20, 0x0ada0,
];

const MIN_YEAR = 1900;
const MAX_YEAR = 2099;
const BASE_SOLAR_MS = Date.UTC(1900, 0, 31);
const MS_PER_DAY = 24 * 60 * 60 * 1000;
const DEFAULT_DATA_FILE = path.resolve(__dirname, "..", "data", "birthdays.json");
const DEFAULT_NOTIFICATION_CONFIG = path.resolve(__dirname, "..", "data", "notification.json");
const DEFAULT_NOTIFICATION_TEMPLATE = {
  channels: [
    { type: "agent", enabled: true },
    {
      type: "email",
      enabled: false,
      host: "${BIRTHDAY_SMTP_HOST}",
      port: "${BIRTHDAY_SMTP_PORT}",
      username: "${BIRTHDAY_SMTP_USERNAME}",
      password: "${BIRTHDAY_SMTP_PASSWORD}",
      from: "${BIRTHDAY_EMAIL_FROM}",
      to: ["${BIRTHDAY_EMAIL_TO}"],
      use_tls: true,
      subject: "生日提醒"
    }
  ]
};

function usage() {
  console.log(`用法:
  node birthday_manager.js [--data-file 文件路径] [--notification-config 配置路径] add 姓名 值 [--calendar lunar|solar] [--leap-month] [--remind-before 天数]
  node birthday_manager.js [--data-file 文件路径] [--notification-config 配置路径] add-idcard 姓名 身份证号 [--calendar lunar|solar] [--remind-before 天数]
  node birthday_manager.js [--data-file 文件路径] [--notification-config 配置路径] add-manual 姓名 --calendar lunar|solar --month 月 --day 日 [--year 年] [--leap-month] [--remind-before 天数]
  node birthday_manager.js [--data-file 文件路径] [--notification-config 配置路径] list [--upcoming] [--days 天数] [--today YYYY-MM-DD]
  node birthday_manager.js [--data-file 文件路径] [--notification-config 配置路径] next [--today YYYY-MM-DD]
  node birthday_manager.js [--data-file 文件路径] [--notification-config 配置路径] check [--today YYYY-MM-DD]
  node birthday_manager.js [--data-file 文件路径] [--notification-config 配置路径] remove 姓名`);
}

function fail(message) {
  console.error(message);
  process.exit(1);
}

function ensureSupportedYear(year) {
  if (year < MIN_YEAR || year > MAX_YEAR) {
    throw new Error(`年份 ${year} 超出支持范围，当前仅支持 ${MIN_YEAR}-${MAX_YEAR}。`);
  }
}

function leapMonth(year) {
  return LUNAR_INFO[year - MIN_YEAR] & 0xf;
}

function leapDays(year) {
  if (leapMonth(year)) {
    return (LUNAR_INFO[year - MIN_YEAR] & 0x10000) ? 30 : 29;
  }
  return 0;
}

function monthDays(year, month) {
  return (LUNAR_INFO[year - MIN_YEAR] & (0x10000 >> month)) ? 30 : 29;
}

function lunarYearDays(year) {
  let total = 348;
  let bit = 0x8000;
  const info = LUNAR_INFO[year - MIN_YEAR];
  while (bit > 0x8) {
    if (info & bit) {
      total += 1;
    }
    bit >>= 1;
  }
  return total + leapDays(year);
}

function utcDate(year, month, day) {
  return new Date(Date.UTC(year, month - 1, day));
}

function formatDate(dateObj) {
  return dateObj.toISOString().slice(0, 10);
}

function addDays(dateObj, days) {
  return new Date(dateObj.getTime() + days * MS_PER_DAY);
}

function diffDays(later, earlier) {
  return Math.round((later.getTime() - earlier.getTime()) / MS_PER_DAY);
}

function solarToLunar(dateObj) {
  ensureSupportedYear(dateObj.getUTCFullYear());
  let offset = diffDays(dateObj, new Date(BASE_SOLAR_MS));
  let lunarYear = MIN_YEAR;

  while (lunarYear <= MAX_YEAR && offset >= lunarYearDays(lunarYear)) {
    offset -= lunarYearDays(lunarYear);
    lunarYear += 1;
  }

  if (lunarYear > MAX_YEAR) {
    throw new Error("公历日期超出农历换算范围。");
  }

  const leap = leapMonth(lunarYear);
  let lunarMonth = 1;
  let isLeap = false;

  while (lunarMonth <= 12) {
    let days;
    if (leap && lunarMonth === leap + 1 && !isLeap) {
      lunarMonth -= 1;
      isLeap = true;
      days = leapDays(lunarYear);
    } else {
      days = monthDays(lunarYear, lunarMonth);
    }

    if (offset < days) {
      break;
    }

    offset -= days;
    if (isLeap && lunarMonth === leap) {
      isLeap = false;
    }
    lunarMonth += 1;
  }

  return {
    year: lunarYear,
    month: lunarMonth,
    day: offset + 1,
    isLeap,
  };
}

function lunarToSolar(lunar) {
  ensureSupportedYear(lunar.year);
  let offset = 0;

  for (let year = MIN_YEAR; year < lunar.year; year += 1) {
    offset += lunarYearDays(year);
  }

  const leap = leapMonth(lunar.year);
  for (let month = 1; month < lunar.month; month += 1) {
    offset += monthDays(lunar.year, month);
    if (leap === month) {
      offset += leapDays(lunar.year);
    }
  }

  if (lunar.isLeap) {
    if (leap !== lunar.month) {
      throw new Error(`${lunar.year} 年农历 ${lunar.month} 月不是闰月。`);
    }
    offset += monthDays(lunar.year, lunar.month);
  }

  const maxDays = lunar.isLeap ? leapDays(lunar.year) : monthDays(lunar.year, lunar.month);
  if (lunar.day < 1 || lunar.day > maxDays) {
    throw new Error("农历日期不合法。");
  }

  offset += lunar.day - 1;
  return new Date(BASE_SOLAR_MS + offset * MS_PER_DAY);
}

function maskIdcard(idcard) {
  if (idcard.length < 8) {
    return "*".repeat(idcard.length);
  }
  return `${idcard.slice(0, 6)}${"*".repeat(idcard.length - 10)}${idcard.slice(-4)}`;
}

function parseIdcardBirthday(idcard) {
  const raw = idcard.trim().toUpperCase();
  if (raw.length === 18) {
    const digits = raw.slice(0, 17);
    if (!/^\d+$/.test(digits) || !/^(?:\d|X)$/.test(raw.slice(-1))) {
      throw new Error("18 位身份证号码格式不合法。");
    }
    const birthday = raw.slice(6, 14);
    return utcDate(Number(birthday.slice(0, 4)), Number(birthday.slice(4, 6)), Number(birthday.slice(6, 8)));
  }
  if (raw.length === 15) {
    if (!/^\d+$/.test(raw)) {
      throw new Error("15 位身份证号码格式不合法。");
    }
    const birthday = raw.slice(6, 12);
    return utcDate(Number(`19${birthday.slice(0, 2)}`), Number(birthday.slice(2, 4)), Number(birthday.slice(4, 6)));
  }
  throw new Error("仅支持 15 位或 18 位中国身份证号码。");
}

function isIdcardValue(value) {
  const raw = value.trim().toUpperCase();
  return /^\d{15}$/.test(raw) || /^\d{17}[\dX]$/.test(raw);
}

function parseBirthdayValue(value, calendarHint, leapMonth) {
  let raw = value.trim();
  let calendar = calendarHint;
  for (const [prefix, detected] of [
    ["公历:", "solar"],
    ["solar:", "solar"],
    ["阳历:", "solar"],
    ["农历:", "lunar"],
    ["lunar:", "lunar"],
  ]) {
    if (raw.toLowerCase().startsWith(prefix.toLowerCase())) {
      raw = raw.slice(prefix.length).trim();
      calendar = detected;
      break;
    }
  }

  calendar = calendar || "lunar";
  let normalized = raw.replaceAll("/", "-").replaceAll(".", "-");
  let localLeap = leapMonth;
  if (normalized.startsWith("闰")) {
    localLeap = true;
    normalized = normalized.slice(1);
  }

  const parts = normalized.split("-").filter(Boolean).map((part) => Number(part));
  if (parts.length !== 2 && parts.length !== 3) {
    throw new Error("生日格式不正确。请使用 YYYY-MM-DD、MM-DD、农历:8-15 或 公历:1990-03-14。");
  }

  let year = null;
  let month;
  let day;
  if (parts.length === 3) {
    [year, month, day] = parts;
  } else {
    [month, day] = parts;
  }

  if (calendar === "solar") {
    utcDate(year || 2000, month, day);
    return { source: "manual", calendar: "solar", month, day, year, leap_month: false };
  }

  const targetYear = year || new Date().getUTCFullYear();
  lunarToSolar({ year: targetYear, month, day, isLeap: localLeap });
  return { source: "manual", calendar: "lunar", month, day, year, leap_month: localLeap };
}

function ensureDataFile(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  if (!fs.existsSync(filePath)) {
    fs.writeFileSync(filePath, JSON.stringify({ records: [] }, null, 2), "utf8");
  }
}

function ensureNotificationConfig(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  if (!fs.existsSync(filePath)) {
    fs.writeFileSync(filePath, `${JSON.stringify(DEFAULT_NOTIFICATION_TEMPLATE, null, 2)}\n`, "utf8");
  }
}

function resolveConfigValue(value) {
  if (typeof value === "string") {
    const match = /^\$\{([A-Z0-9_]+)\}$/.exec(value);
    if (match) {
      return process.env[match[1]] || "";
    }
    return value;
  }
  if (Array.isArray(value)) {
    return value.map((item) => resolveConfigValue(item));
  }
  if (value && typeof value === "object") {
    return Object.fromEntries(Object.entries(value).map(([key, item]) => [key, resolveConfigValue(item)]));
  }
  return value;
}

function loadData(filePath) {
  ensureDataFile(filePath);
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

function saveData(filePath, data) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, `${JSON.stringify(data, null, 2)}\n`, "utf8");
}

function findRecord(records, name) {
  return records.find((record) => record.name === name);
}

function birthdayStorageText(record) {
  const prefix = record.calendar === "lunar" ? "农历" : "公历";
  const leap = record.leap_month ? "闰" : "";
  const year = record.year ? `${record.year}年` : "";
  return `${prefix} ${year}${leap}${record.month}月${record.day}日`;
}

function parseToday(raw) {
  if (!raw) {
    const now = new Date();
    return utcDate(now.getUTCFullYear(), now.getUTCMonth() + 1, now.getUTCDate());
  }
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(raw);
  if (!match) {
    throw new Error("日期格式必须是 YYYY-MM-DD。");
  }
  return utcDate(Number(match[1]), Number(match[2]), Number(match[3]));
}

function resolveNextSolarBirthday(record, today) {
  if (record.calendar === "solar") {
    let current = utcDate(today.getUTCFullYear(), record.month, record.day);
    if (current.getTime() < today.getTime()) {
      current = utcDate(today.getUTCFullYear() + 1, record.month, record.day);
    }
    return current;
  }

  for (const targetYear of [today.getUTCFullYear(), today.getUTCFullYear() + 1]) {
    const leapRequested = Boolean(record.leap_month);
    const candidates = leapRequested ? [true, false] : [false];

    let converted = null;
    for (const isLeap of candidates) {
      try {
        converted = lunarToSolar({
          year: targetYear,
          month: record.month,
          day: record.day,
          isLeap,
        });
        break;
      } catch (error) {
        converted = null;
      }
    }
    if (converted && converted.getTime() >= today.getTime()) {
      return converted;
    }
  }

  throw new Error(`无法为 ${record.name} 计算下一次生日。`);
}

function computeTurningAge(record, solarBirthday) {
  if (!record.year) {
    return null;
  }
  return solarBirthday.getUTCFullYear() - Number(record.year);
}

function buildSummary(record, today) {
  const nextBirthday = resolveNextSolarBirthday(record, today);
  const remindBefore = Number(record.remind_before_days ?? 1);
  const remindDate = addDays(nextBirthday, -remindBefore);
  return {
    name: record.name,
    storage: birthdayStorageText(record),
    next_birthday: formatDate(nextBirthday),
    days_until_birthday: diffDays(nextBirthday, today),
    remind_before_days: remindBefore,
    next_remind_date: formatDate(remindDate),
    days_until_remind: diffDays(remindDate, today),
    turning_age: computeTurningAge(record, nextBirthday),
  };
}

function loadNotificationChannels(filePath) {
  ensureNotificationConfig(filePath);
  const data = resolveConfigValue(JSON.parse(fs.readFileSync(filePath, "utf8")));
  const channels = data.channels && data.channels.length ? data.channels : [{ type: "agent" }];
  const enabled = channels.filter((channel) => channel.enabled !== false);
  return enabled.length ? enabled : [{ type: "agent" }];
}

function emitOpenclawSchedulerHint(dataFile, notificationConfig) {
  const cwd = process.cwd().toLowerCase();
  if (!cwd.includes("openclaw") && !process.env.CODEX_HOME) {
    return;
  }
  const payload = {
    name: "生日提醒检查",
    prompt: `运行 node ${path.resolve(__filename)} --data-file ${dataFile} --notification-config ${notificationConfig} check，并处理输出中的提醒结果。`,
    rrule: "FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR,SA,SU;BYHOUR=9;BYMINUTE=0",
    cwds: path.resolve(__dirname, ".."),
    status: "ACTIVE",
  };
  console.log(`OPENCLAW_AUTOMATION_SUGGESTION ${JSON.stringify(payload)}`);
}

function dispatchNotifications(matches, configPath) {
  if (!matches.length) {
    return;
  }
  const channels = loadNotificationChannels(configPath);
  const message = matches.map((item) => {
    const ageText = item.turning_age !== null ? `，这次过 ${item.turning_age} 岁` : "";
    return (
      `生日提醒：${item.name}（${item.storage}）将在 ${item.next_birthday} 过生日，` +
      `今天需要提醒，已提前 ${item.remind_before_days} 天设置${ageText}。`
    );
  }).join("\n");

  for (const channel of channels) {
    const type = channel.type || "agent";
    if (type === "agent") {
      console.log(`AGENT_NOTIFICATION\n${message}`);
      continue;
    }
    if (type === "stdout") {
      console.log(message);
      continue;
    }
    if (type === "email") {
      const recipients = (channel.to || []).filter(Boolean);
      const sender = channel.from || channel.username || "birthday-reminder@localhost";
      if (!recipients.length) {
        console.log("通知失败：email 渠道缺少 to 配置。");
        continue;
      }
      const sendmailPath = childProcess.spawnSync("which", ["sendmail"], { encoding: "utf8" }).stdout.trim();
      if (!sendmailPath) {
        console.log("通知失败：当前环境未安装 sendmail，无法通过 JS 发送 email。");
        continue;
      }
      const mail = [
        `Subject: ${channel.subject || "生日提醒"}`,
        `From: ${sender}`,
        `To: ${recipients.join(", ")}`,
        "Content-Type: text/plain; charset=utf-8",
        "",
        message,
      ].join("\n");
      const sent = childProcess.spawnSync(sendmailPath, ["-t"], { input: mail, encoding: "utf8" });
      if (sent.status !== 0) {
        console.log(`通知失败：email 渠道发送异常，原因：${sent.stderr || "sendmail 返回非 0"}`);
      }
      continue;
    }
    if (type === "webhook") {
      console.log(`通知配置已命中 webhook 渠道：${channel.url}`);
    }
  }
}

function buildRecordFromInput(name, value, calendar, remindBefore, leapMonth) {
  if (isIdcardValue(value)) {
    const solarBirthday = parseIdcardBirthday(value);
    const targetCalendar = calendar || "lunar";
    if (targetCalendar === "lunar") {
      const lunar = solarToLunar(solarBirthday);
      return {
        name,
        calendar: "lunar",
        month: lunar.month,
        day: lunar.day,
        year: lunar.year,
        leap_month: lunar.isLeap,
        remind_before_days: remindBefore,
        source: "idcard",
        idcard_masked: maskIdcard(value),
        solar_birthday: formatDate(solarBirthday),
        created_at: new Date().toISOString().slice(0, 19),
      };
    }
    return {
      name,
      calendar: "solar",
      month: solarBirthday.getUTCMonth() + 1,
      day: solarBirthday.getUTCDate(),
      year: solarBirthday.getUTCFullYear(),
      leap_month: false,
      remind_before_days: remindBefore,
      source: "idcard",
      idcard_masked: maskIdcard(value),
      solar_birthday: formatDate(solarBirthday),
      created_at: new Date().toISOString().slice(0, 19),
    };
  }

  const parsed = parseBirthdayValue(value, calendar, leapMonth);
  return {
    ...parsed,
    name,
    remind_before_days: remindBefore,
    created_at: new Date().toISOString().slice(0, 19),
  };
}

function upsertRecord(filePath, record) {
  const data = loadData(filePath);
  const records = data.records || [];
  const firstAdd = records.length === 0;
  const existing = findRecord(records, record.name);
  if (existing) {
    Object.assign(existing, record);
    data.records = records;
    saveData(filePath, data);
    return { created: false, first_add: false };
  } else {
    records.push(record);
  }
  data.records = records;
  saveData(filePath, data);
  return { created: true, first_add: firstAdd };
}

function parseOptions(args) {
  const options = {};
  const positional = [];
  for (let i = 0; i < args.length; i += 1) {
    const token = args[i];
    if (!token.startsWith("--")) {
      positional.push(token);
      continue;
    }
    const key = token.slice(2);
    if (key === "upcoming" || key === "leap-month") {
      options[key] = true;
      continue;
    }
    i += 1;
    if (i >= args.length) {
      fail(`缺少参数值：--${key}`);
    }
    options[key] = args[i];
  }
  return { options, positional };
}

function addAuto(filePath, notificationConfig, positional, options) {
  if (positional.length < 3) {
    usage();
    process.exit(1);
  }
  const name = positional[1];
  const value = positional[2];
  const remindBefore = Number(options["remind-before"] ?? 1);
  if (remindBefore < 0) {
    fail("提前提醒天数不能小于 0。");
  }
  const record = buildRecordFromInput(name, value, options.calendar, remindBefore, Boolean(options["leap-month"]));
  const result = upsertRecord(filePath, record);
  console.log(`已保存：${name}，${birthdayStorageText(record)}，提前 ${remindBefore} 天提醒。`);
  if (result.first_add) {
    emitOpenclawSchedulerHint(filePath, notificationConfig);
  }
}

function addIdcard(filePath, notificationConfig, positional, options) {
  addAuto(filePath, notificationConfig, ["add", positional[1], positional[2]], options);
}

function addManual(filePath, notificationConfig, positional, options) {
  if (positional.length < 2) {
    usage();
    process.exit(1);
  }
  const name = positional[1];
  const calendar = options.calendar || "lunar";
  const month = Number(options.month);
  const day = Number(options.day);
  const year = options.year ? Number(options.year) : null;
  const remindBefore = Number(options["remind-before"] ?? 1);
  const leapMonth = Boolean(options["leap-month"]);

  if (!month || !day) {
    fail("手动添加时必须提供 --month 和 --day。");
  }
  if (remindBefore < 0) {
    fail("提前提醒天数不能小于 0。");
  }

  const prefix = calendar === "solar" ? "公历:" : "农历:";
  const leap = leapMonth && calendar === "lunar" ? "闰" : "";
  const value = `${prefix}${leap}${year ? `${year}-` : ""}${month}-${day}`;
  addAuto(filePath, notificationConfig, ["add", name, value], options);
}

function listRecords(filePath, options) {
  const data = loadData(filePath);
  const records = data.records || [];
  if (!records.length) {
    console.log("暂无生日记录。");
    return;
  }
  const today = parseToday(options.today);
  const items = records.map((record) => buildSummary(record, today)).sort((a, b) => a.days_until_birthday - b.days_until_birthday);
  const days = Number(options.days ?? 30);
  for (const item of items) {
    if (options.upcoming && item.days_until_birthday > days) {
      continue;
    }
    const ageText = item.turning_age !== null ? `，即将 ${item.turning_age} 岁` : "";
    console.log(
      `${item.name} | ${item.storage} | 下次公历生日 ${item.next_birthday} | ` +
      `还有 ${item.days_until_birthday} 天${ageText} | 提醒日 ${item.next_remind_date}`
    );
  }
}

function showNext(filePath, options) {
  const data = loadData(filePath);
  const records = data.records || [];
  if (!records.length) {
    console.log("暂无生日记录。");
    return;
  }
  const today = parseToday(options.today);
  const item = records.map((record) => buildSummary(record, today)).sort((a, b) => a.days_until_birthday - b.days_until_birthday)[0];
  console.log(
    `最近生日：${item.name}，${item.storage}，下次公历生日 ${item.next_birthday}，还有 ${item.days_until_birthday} 天。`
  );
}

function checkReminders(filePath, notificationConfig, options) {
  const data = loadData(filePath);
  const records = data.records || [];
  if (!records.length) {
    return;
  }
  const today = parseToday(options.today);
  const items = records
    .map((record) => buildSummary(record, today))
    .filter((item) => item.days_until_remind === 0)
    .sort((a, b) => a.next_birthday.localeCompare(b.next_birthday));

  dispatchNotifications(items, notificationConfig);
}

function removeRecord(filePath, positional) {
  if (positional.length < 2) {
    usage();
    process.exit(1);
  }
  const name = positional[1];
  const data = loadData(filePath);
  const records = data.records || [];
  const filtered = records.filter((record) => record.name !== name);
  if (filtered.length === records.length) {
    console.log(`未找到记录：${name}`);
    return;
  }
  data.records = filtered;
  saveData(filePath, data);
  console.log(`已删除：${name}`);
}

function main() {
  const rawArgs = process.argv.slice(2);
  if (!rawArgs.length || rawArgs.includes("--help") || rawArgs.includes("-h")) {
    usage();
    return;
  }

  let dataFile = DEFAULT_DATA_FILE;
  let notificationConfig = DEFAULT_NOTIFICATION_CONFIG;
  const args = [];
  for (let i = 0; i < rawArgs.length; i += 1) {
    if (rawArgs[i] === "--data-file") {
      i += 1;
      if (i >= rawArgs.length) {
        fail("缺少参数值：--data-file");
      }
      dataFile = path.resolve(rawArgs[i]);
      continue;
    }
    if (rawArgs[i] === "--notification-config") {
      i += 1;
      if (i >= rawArgs.length) {
        fail("缺少参数值：--notification-config");
      }
      notificationConfig = path.resolve(rawArgs[i]);
      continue;
    }
    args.push(rawArgs[i]);
  }

  const { options, positional } = parseOptions(args);
  const command = positional[0];
  if (!command) {
    usage();
    process.exit(1);
  }

  switch (command) {
    case "add":
      addAuto(dataFile, notificationConfig, positional, options);
      break;
    case "add-idcard":
      addIdcard(dataFile, notificationConfig, positional, options);
      break;
    case "add-manual":
      addManual(dataFile, notificationConfig, positional, options);
      break;
    case "list":
      listRecords(dataFile, options);
      break;
    case "next":
      showNext(dataFile, options);
      break;
    case "check":
      checkReminders(dataFile, notificationConfig, options);
      break;
    case "remove":
      removeRecord(dataFile, positional);
      break;
    default:
      usage();
      process.exit(1);
  }
}

try {
  main();
} catch (error) {
  fail(error instanceof Error ? error.message : String(error));
}
