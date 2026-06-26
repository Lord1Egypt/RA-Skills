#!/usr/bin/env bun
// @bun

// src/db.ts
import { Database } from "bun:sqlite";
import { join } from "path";
import { mkdirSync, existsSync } from "fs";
import { homedir } from "os";
var DEFAULT_DB_DIR = join(homedir(), ".car-log");
var DEFAULT_DB_NAME = "car_log.db";
function getDbPath(customPath) {
  if (customPath)
    return customPath;
  if (process.env.CAR_LOG_DB)
    return process.env.CAR_LOG_DB;
  return join(DEFAULT_DB_DIR, DEFAULT_DB_NAME);
}
function createDatabase(dbPath) {
  const dir = dbPath.substring(0, dbPath.lastIndexOf("/"));
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }
  const db = new Database(dbPath);
  db.exec("PRAGMA journal_mode = WAL");
  db.exec("PRAGMA foreign_keys = ON");
  return db;
}
var CREATE_VEHICLES_TABLE = `
CREATE TABLE IF NOT EXISTS vehicles (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL UNIQUE,
  plate TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
  deleted INTEGER NOT NULL DEFAULT 0
);
`;
var CREATE_RECORDS_TABLE = `
CREATE TABLE IF NOT EXISTS records (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  vehicle_id INTEGER NOT NULL,
  record_type TEXT NOT NULL CHECK(record_type IN ('mileage', 'refuel', 'maintenance')),
  mileage REAL,
  datetime TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
  note TEXT,
  liters REAL,
  cost REAL,
  deleted INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL DEFAULT (datetime('now', 'localtime')),
  FOREIGN KEY (vehicle_id) REFERENCES vehicles(id)
);
`;
var CREATE_INDEXES = `
CREATE INDEX IF NOT EXISTS idx_records_vehicle_deleted ON records(vehicle_id, deleted);
CREATE INDEX IF NOT EXISTS idx_records_vehicle_type_datetime ON records(vehicle_id, record_type, datetime);
`;
function initDb(db) {
  db.exec(CREATE_VEHICLES_TABLE);
  db.exec(CREATE_RECORDS_TABLE);
  db.exec(CREATE_INDEXES);
}

// src/vehicle.ts
function addVehicle(db, name, plate) {
  const existing = db.query("SELECT id FROM vehicles WHERE name = ? AND deleted = 0").get(name);
  if (existing) {
    throw new Error(`\u8F66\u8F86\u540D\u79F0 "${name}" \u5DF2\u5B58\u5728 (ID: ${existing.id})`);
  }
  const softDeleted = db.query("SELECT id FROM vehicles WHERE name = ? AND deleted = 1").get(name);
  if (softDeleted) {
    db.query("UPDATE vehicles SET deleted = 0, plate = ?, created_at = datetime('now', 'localtime') WHERE id = ?").run(plate ?? null, softDeleted.id);
    return getVehicleById(db, softDeleted.id);
  }
  const result = db.query("INSERT INTO vehicles (name, plate) VALUES (?, ?) RETURNING id").get(name, plate ?? null);
  return getVehicleById(db, result.id);
}
function getVehicleById(db, id) {
  return db.query("SELECT * FROM vehicles WHERE id = ? AND deleted = 0").get(id);
}
function listVehicles(db) {
  return db.query(`
    SELECT v.*,
      (SELECT r.mileage FROM records r
       WHERE r.vehicle_id = v.id AND r.deleted = 0 AND r.mileage IS NOT NULL
       ORDER BY r.datetime DESC LIMIT 1) AS current_mileage
    FROM vehicles v
    WHERE v.deleted = 0
    ORDER BY v.created_at DESC
    `).all();
}
function deleteVehicle(db, vehicleId) {
  const vehicle = getVehicleById(db, vehicleId);
  if (!vehicle) {
    throw new Error(`\u8F66\u8F86\u4E0D\u5B58\u5728 (ID: ${vehicleId})`);
  }
  const tx = db.transaction(() => {
    db.query("UPDATE vehicles SET deleted = 1 WHERE id = ?").run(vehicleId);
    db.query("UPDATE records SET deleted = 1 WHERE vehicle_id = ?").run(vehicleId);
  });
  tx();
}

// src/utils.ts
function parseDatetime(input) {
  if (!input || input.trim() === "") {
    return formatNow();
  }
  const trimmed = input.trim();
  if (/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/.test(trimmed)) {
    return trimmed;
  }
  if (/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}/.test(trimmed)) {
    return trimmed.replace("T", " ").substring(0, 19);
  }
  if (/^\d{4}-\d{2}-\d{2}$/.test(trimmed)) {
    return trimmed + " 00:00:00";
  }
  throw new Error(`Invalid datetime format: "${input}". Expected YYYY-MM-DD or YYYY-MM-DD HH:MM:SS.`);
}
function formatNow() {
  const now = new Date;
  return formatDate(now);
}
function formatDate(d) {
  const pad = (n) => n.toString().padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ` + `${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`;
}
function formatCurrency(amount) {
  return `\xA5${amount.toFixed(2)}`;
}
function formatDuration(days) {
  if (days < 1)
    return "\u4E0D\u52301\u5929";
  if (days < 30)
    return `${Math.floor(days)}\u5929`;
  if (days < 365) {
    const months2 = Math.floor(days / 30);
    const remainDays = Math.floor(days % 30);
    return remainDays > 0 ? `${months2}\u4E2A\u6708${remainDays}\u5929` : `${months2}\u4E2A\u6708`;
  }
  const years = Math.floor(days / 365);
  const months = Math.floor(days % 365 / 30);
  return months > 0 ? `${years}\u5E74${months}\u4E2A\u6708` : `${years}\u5E74`;
}
function formatMileage(km) {
  if (km === null)
    return "-";
  return `${km.toLocaleString("zh-CN")} km`;
}
function displayWidth(s) {
  let w = 0;
  for (const ch of s) {
    const code = ch.codePointAt(0);
    if (code >= 19968 && code <= 40959 || code >= 12288 && code <= 12351 || code >= 65280 && code <= 65519) {
      w += 2;
    } else {
      w += 1;
    }
  }
  return w;
}
function padToWidth(s, w, alignRight = false) {
  const cur = displayWidth(s);
  if (cur > w) {
    let result = "";
    let resultWidth = 0;
    for (const ch of s) {
      const chWidth = displayWidth(ch);
      if (resultWidth + chWidth > w - 1)
        break;
      result += ch;
      resultWidth += chWidth;
    }
    return result + "\u2026";
  }
  const padding = w - cur;
  const space = " ".repeat(padding);
  return alignRight ? space + s : s + space;
}
function table(headers, rows, options) {
  const maxWidth = options?.maxWidth ?? 50;
  const widths = headers.map((h, i) => {
    const maxData = rows.reduce((max, row) => {
      const cell = String(row[i] ?? "-");
      return Math.max(max, displayWidth(cell));
    }, 0);
    return Math.min(Math.max(displayWidth(h), maxData), maxWidth);
  });
  const divider = widths.map((w) => "-".repeat(w + 2)).join("+");
  const lines = [];
  lines.push(divider);
  lines.push("| " + headers.map((h, i) => padToWidth(h, widths[i])).join(" | ") + " |");
  lines.push(divider);
  for (const row of rows) {
    const cells = row.map((cell, i) => {
      const str = cell === null ? "-" : String(cell);
      const alignRight = typeof cell === "number";
      return padToWidth(str, widths[i], alignRight);
    });
    lines.push("| " + cells.join(" | ") + " |");
  }
  lines.push(divider);
  return lines.join(`
`);
}

// src/mileage.ts
function validateMileage(db, vehicleId, mileage, datetime) {
  const datetimeValue = datetime ? parseDatetime(datetime) : undefined;
  if (datetimeValue) {
    const rowBefore = db.query(`SELECT MAX(mileage) as max_mileage FROM records
         WHERE vehicle_id = ? AND deleted = 0 AND mileage IS NOT NULL
         AND datetime < ?`).get(vehicleId, datetimeValue);
    const maxBefore = rowBefore?.max_mileage;
    if (maxBefore !== null && maxBefore !== undefined && mileage < maxBefore) {
      throw new Error(`\u91CC\u7A0B\u6821\u9A8C\u5931\u8D25\uFF1A\u65B0\u8BB0\u5F55\u91CC\u7A0B ${mileage.toLocaleString("zh-CN")} km ` + `\u5C0F\u4E8E\u8FC7\u53BB\u7684\u6700\u5927\u91CC\u7A0B ${maxBefore.toLocaleString("zh-CN")} km\u3002\u8BF7\u68C0\u67E5\u6570\u636E\u3002`);
    }
    const rowAfter = db.query(`SELECT MIN(mileage) as min_mileage FROM records
         WHERE vehicle_id = ? AND deleted = 0 AND mileage IS NOT NULL
         AND datetime > ?`).get(vehicleId, datetimeValue);
    const minAfter = rowAfter?.min_mileage;
    if (minAfter !== null && minAfter !== undefined && mileage > minAfter) {
      throw new Error(`\u91CC\u7A0B\u6821\u9A8C\u5931\u8D25\uFF1A\u65B0\u8BB0\u5F55\u91CC\u7A0B ${mileage.toLocaleString("zh-CN")} km ` + `\u5927\u4E8E\u672A\u6765\u7684\u6700\u5C0F\u91CC\u7A0B ${minAfter.toLocaleString("zh-CN")} km\u3002\u8BF7\u68C0\u67E5\u6570\u636E\u3002`);
    }
  } else {
    const row = db.query(`SELECT MAX(mileage) as max_mileage FROM records
         WHERE vehicle_id = ? AND deleted = 0 AND mileage IS NOT NULL`).get(vehicleId);
    const currentMax = row?.max_mileage;
    if (currentMax !== null && currentMax !== undefined && mileage < currentMax) {
      throw new Error(`\u91CC\u7A0B\u6821\u9A8C\u5931\u8D25\uFF1A\u65B0\u8BB0\u5F55\u91CC\u7A0B ${mileage.toLocaleString("zh-CN")} km ` + `\u5C0F\u4E8E\u5F53\u524D\u6700\u5927\u91CC\u7A0B ${currentMax.toLocaleString("zh-CN")} km\u3002\u8BF7\u68C0\u67E5\u6570\u636E\u3002`);
    }
  }
}
function addMileageRecord(db, input) {
  const vehicleExists = db.query("SELECT id FROM vehicles WHERE id = ? AND deleted = 0").get(input.vehicle_id);
  if (!vehicleExists) {
    throw new Error(`\u8F66\u8F86\u4E0D\u5B58\u5728 (ID: ${input.vehicle_id})`);
  }
  validateMileage(db, input.vehicle_id, input.mileage, input.datetime);
  const datetime = parseDatetime(input.datetime);
  const result = db.query(`INSERT INTO records (vehicle_id, record_type, mileage, datetime, note)
       VALUES (?, 'mileage', ?, ?, ?)
       RETURNING id`).get(input.vehicle_id, input.mileage, datetime, input.note ?? null);
  return getRecordById(db, result.id);
}
function listMileageRecords(db, vehicleId) {
  return db.query(`SELECT * FROM records
       WHERE vehicle_id = ? AND record_type = 'mileage' AND deleted = 0
       ORDER BY datetime DESC`).all(vehicleId);
}
function deleteRecord(db, recordId) {
  const record = getRecordById(db, recordId);
  if (!record) {
    throw new Error(`\u8BB0\u5F55\u4E0D\u5B58\u5728 (ID: ${recordId})`);
  }
  db.query("UPDATE records SET deleted = 1 WHERE id = ?").run(recordId);
}
function getRecordById(db, id) {
  return db.query("SELECT * FROM records WHERE id = ? AND deleted = 0").get(id);
}

// src/refuel.ts
function addRefuelRecord(db, input) {
  const vehicleExists = db.query("SELECT id FROM vehicles WHERE id = ? AND deleted = 0").get(input.vehicle_id);
  if (!vehicleExists) {
    throw new Error(`\u8F66\u8F86\u4E0D\u5B58\u5728 (ID: ${input.vehicle_id})`);
  }
  validateMileage(db, input.vehicle_id, input.mileage, input.datetime);
  const datetime = parseDatetime(input.datetime);
  const result = db.query(`INSERT INTO records (vehicle_id, record_type, mileage, datetime, note, liters, cost)
       VALUES (?, 'refuel', ?, ?, ?, ?, ?)
       RETURNING id`).get(input.vehicle_id, input.mileage, datetime, input.note ?? null, input.liters, input.cost);
  return getRecordById2(db, result.id);
}
function listRefuelRecords(db, vehicleId) {
  return db.query(`SELECT * FROM records
       WHERE vehicle_id = ? AND record_type = 'refuel' AND deleted = 0
       ORDER BY datetime DESC`).all(vehicleId);
}
function deleteRecord2(db, recordId) {
  const record = getRecordById2(db, recordId);
  if (!record) {
    throw new Error(`\u8BB0\u5F55\u4E0D\u5B58\u5728 (ID: ${recordId})`);
  }
  db.query("UPDATE records SET deleted = 1 WHERE id = ?").run(recordId);
}
function getRecordById2(db, id) {
  return db.query("SELECT * FROM records WHERE id = ? AND deleted = 0").get(id);
}
function calculateConsumption(db, vehicleId) {
  const records = db.query(`SELECT * FROM records
       WHERE vehicle_id = ? AND record_type = 'refuel' AND deleted = 0
       ORDER BY datetime ASC`).all(vehicleId);
  if (records.length < 2)
    return [];
  const results = [];
  for (let i = 0;i < records.length - 1; i++) {
    const prev = records[i];
    const curr = records[i + 1];
    if (prev.mileage === null || curr.mileage === null)
      continue;
    if (prev.liters === null || prev.liters <= 0)
      continue;
    if (prev.cost === null || curr.liters === null || curr.liters <= 0)
      continue;
    const distance = curr.mileage - prev.mileage;
    if (distance <= 0)
      continue;
    const prevPricePerLiter = prev.cost / prev.liters;
    const cost = prev.liters * prevPricePerLiter;
    results.push({
      from_datetime: prev.datetime,
      to_datetime: curr.datetime,
      from_mileage: prev.mileage,
      to_mileage: curr.mileage,
      distance,
      liters: prev.liters,
      cost,
      l_per_100km: prev.liters / distance * 100,
      cost_per_km: cost / distance
    });
  }
  return results;
}

// src/maintenance.ts
function addMaintenanceRecord(db, input) {
  const vehicleExists = db.query("SELECT id FROM vehicles WHERE id = ? AND deleted = 0").get(input.vehicle_id);
  if (!vehicleExists) {
    throw new Error(`\u8F66\u8F86\u4E0D\u5B58\u5728 (ID: ${input.vehicle_id})`);
  }
  validateMileage(db, input.vehicle_id, input.mileage, input.datetime);
  const datetime = parseDatetime(input.datetime);
  const result = db.query(`INSERT INTO records (vehicle_id, record_type, mileage, datetime, note, cost)
       VALUES (?, 'maintenance', ?, ?, ?, ?)
       RETURNING id`).get(input.vehicle_id, input.mileage, datetime, input.note ?? null, input.cost ?? null);
  return getRecordById3(db, result.id);
}
function listMaintenanceRecords(db, vehicleId) {
  return db.query(`SELECT * FROM records
       WHERE vehicle_id = ? AND record_type = 'maintenance' AND deleted = 0
       ORDER BY datetime DESC`).all(vehicleId);
}
function deleteRecord3(db, recordId) {
  const record = getRecordById3(db, recordId);
  if (!record) {
    throw new Error(`\u8BB0\u5F55\u4E0D\u5B58\u5728 (ID: ${recordId})`);
  }
  db.query("UPDATE records SET deleted = 1 WHERE id = ?").run(recordId);
}
function getRecordById3(db, id) {
  return db.query("SELECT * FROM records WHERE id = ? AND deleted = 0").get(id);
}
function getMaintenanceInterval(db, vehicleId) {
  const latest = db.query(`SELECT * FROM records
       WHERE vehicle_id = ? AND deleted = 0 AND mileage IS NOT NULL
       ORDER BY datetime DESC, id DESC LIMIT 1`).get(vehicleId);
  if (!latest || latest.mileage === null)
    return null;
  const lastMaintenance = db.query(`SELECT * FROM records
       WHERE vehicle_id = ? AND record_type = 'maintenance' AND deleted = 0
         AND datetime <= ?
       ORDER BY datetime DESC LIMIT 1`).get(vehicleId, latest.datetime);
  if (!lastMaintenance || lastMaintenance.mileage === null)
    return null;
  const daysSince = daysBetween(lastMaintenance.datetime, latest.datetime);
  const distanceSince = latest.mileage - lastMaintenance.mileage;
  return {
    last_maintenance_datetime: lastMaintenance.datetime,
    last_maintenance_mileage: lastMaintenance.mileage,
    days_since: daysSince,
    distance_since: distanceSince,
    current_datetime: latest.datetime,
    current_mileage: latest.mileage
  };
}
function daysBetween(from, to) {
  const fromMs = new Date(from.replace(" ", "T")).getTime();
  const toMs = new Date(to.replace(" ", "T")).getTime();
  return Math.floor((toMs - fromMs) / (1000 * 60 * 60 * 24));
}

// src/stats.ts
function getCurrentMileage(db, vehicleId) {
  const row = db.query(`SELECT mileage FROM records
       WHERE vehicle_id = ? AND deleted = 0 AND mileage IS NOT NULL
       ORDER BY datetime DESC, id DESC LIMIT 1`).get(vehicleId);
  return row?.mileage ?? null;
}
function getExpenses(db, vehicleId, year, month) {
  let dateFilter = "";
  const params = [vehicleId];
  if (year !== undefined) {
    dateFilter += " AND strftime('%Y', datetime) = ?";
    params.push(year.toString());
  }
  if (month !== undefined) {
    dateFilter += " AND strftime('%m', datetime) = ?";
    params.push(month.toString().padStart(2, "0"));
  }
  const refuelRow = db.query(`SELECT COALESCE(SUM(cost), 0) as total FROM records
       WHERE vehicle_id = ? AND record_type = 'refuel' AND deleted = 0 AND cost IS NOT NULL
       ${dateFilter}`).get(...params);
  const maintenanceRow = db.query(`SELECT COALESCE(SUM(cost), 0) as total FROM records
       WHERE vehicle_id = ? AND record_type = 'maintenance' AND deleted = 0 AND cost IS NOT NULL
       ${dateFilter}`).get(...params);
  const refuelCost = refuelRow?.total ?? 0;
  const maintenanceCost = maintenanceRow?.total ?? 0;
  return {
    refuel_cost: refuelCost,
    maintenance_cost: maintenanceCost,
    total_cost: refuelCost + maintenanceCost
  };
}
function deleteAllRecords(db, vehicleId, recordType) {
  if (recordType) {
    const result = db.query(`UPDATE records SET deleted = 1
         WHERE vehicle_id = ? AND record_type = ? AND deleted = 0`).run(vehicleId, recordType);
    return result.changes;
  } else {
    const result = db.query(`UPDATE records SET deleted = 1
         WHERE vehicle_id = ? AND deleted = 0`).run(vehicleId);
    return result.changes;
  }
}
function getLastRefuel(db, vehicleId) {
  return db.query("SELECT mileage, datetime FROM records WHERE vehicle_id = ? AND record_type = 'refuel' AND deleted = 0 ORDER BY datetime DESC LIMIT 1").get(vehicleId);
}
function getLastMaintenance(db, vehicleId) {
  return db.query("SELECT mileage, datetime FROM records WHERE vehicle_id = ? AND record_type = 'maintenance' AND deleted = 0 ORDER BY datetime DESC LIMIT 1").get(vehicleId);
}

// src/index.ts
var customDbPath;
var db;
function getDb() {
  if (!db) {
    const path = getDbPath(customDbPath);
    db = createDatabase(path);
    initDb(db);
  }
  return db;
}
function setDbPath(path) {
  customDbPath = path;
  db = undefined;
}
function printUsage() {
  console.log(`
\u6C7D\u8F66\u91CC\u7A0B\u7BA1\u7406\u5DE5\u5177 (carlog)

\u7528\u6CD5:
  carlog [--db PATH] <command> [subcommand] [options]

\u5168\u5C40\u9009\u9879:
  --db PATH              \u81EA\u5B9A\u4E49\u6570\u636E\u5E93\u8DEF\u5F84

\u547D\u4EE4:
  car                    \u8F66\u8F86\u7BA1\u7406
    add --name NAME [--plate PLATE]   \u6DFB\u52A0\u8F66\u8F86
    list                             \u5217\u51FA\u6240\u6709\u8F66\u8F86
    delete <ID>                      \u5220\u9664\u8F66\u8F86(\u53CA\u5176\u6240\u6709\u8BB0\u5F55)

  mileage                \u91CC\u7A0B\u8BB0\u5F55
    add --car ID --mileage KM [--datetime DT] [--note NOTE]   \u6DFB\u52A0\u91CC\u7A0B\u8BB0\u5F55
    list --car ID                \u5217\u51FA\u91CC\u7A0B\u8BB0\u5F55
    delete <ID>                      \u5220\u9664\u8BB0\u5F55

  refuel                 \u52A0\u6CB9\u8BB0\u5F55
    add --car ID --liters L --cost C --mileage KM [--datetime DT] [--note NOTE]   \u6DFB\u52A0\u52A0\u6CB9\u8BB0\u5F55
    list --car ID                \u5217\u51FA\u52A0\u6CB9\u8BB0\u5F55
    delete <ID>                      \u5220\u9664\u8BB0\u5F55
    consumption --car ID         \u67E5\u770B\u6CB9\u8017\u7EDF\u8BA1

  maintenance            \u4FDD\u517B\u8BB0\u5F55
    add --car ID --mileage KM [--cost C] [--datetime DT] [--note NOTE]   \u6DFB\u52A0\u4FDD\u517B\u8BB0\u5F55
    list --car ID                \u5217\u51FA\u4FDD\u517B\u8BB0\u5F55
    delete <ID>                      \u5220\u9664\u8BB0\u5F55
    since --car ID               \u8DDD\u4E0A\u6B21\u4FDD\u517B\u7684\u65F6\u95F4\u548C\u91CC\u7A0B

  stats                  \u7EDF\u8BA1
    expenses --car ID [--year Y] [--month M]   \u67E5\u770B\u82B1\u8D39\u7EDF\u8BA1
    current-mileage --car ID                   \u67E5\u770B\u5F53\u524D\u91CC\u7A0B

  delete-all --car ID [--type TYPE]            \u6279\u91CF\u5220\u9664\u8BB0\u5F55
`);
}
function parseArgs(argv) {
  const args = {};
  const positional = [];
  for (let i = 0;i < argv.length; i++) {
    const arg = argv[i];
    if (arg === "--db" && argv[i + 1]) {
      customDbPath = argv[++i];
    } else if (arg.startsWith("--")) {
      const key = arg.slice(2);
      if (argv[i + 1] && !argv[i + 1].startsWith("--")) {
        args[key] = argv[++i];
      } else {
        args[key] = "true";
      }
    } else {
      positional.push(arg);
    }
  }
  return {
    command: positional[0] ?? "",
    subcommand: positional[1] ?? "",
    args,
    positional: positional.slice(2)
  };
}
function runCli(argv) {
  if (argv.length === 0) {
    printUsage();
    return { success: true, exitCode: 0 };
  }
  const parsed = parseArgs(argv);
  try {
    switch (parsed.command) {
      case "car":
        handleVehicle(parsed.subcommand, parsed.args, parsed.positional);
        break;
      case "mileage":
        handleMileage(parsed.subcommand, parsed.args, parsed.positional);
        break;
      case "refuel":
        handleRefuel(parsed.subcommand, parsed.args, parsed.positional);
        break;
      case "maintenance":
        handleMaintenance(parsed.subcommand, parsed.args, parsed.positional);
        break;
      case "stats":
        handleStats(parsed.subcommand, parsed.args);
        break;
      case "delete-all":
        handleDeleteAll(parsed.args);
        break;
      default:
        console.error(`\u672A\u77E5\u547D\u4EE4: ${parsed.command}`);
        printUsage();
        return { success: false, exitCode: 1, error: `\u672A\u77E5\u547D\u4EE4: ${parsed.command}` };
    }
    return { success: true, exitCode: 0 };
  } catch (err) {
    const errorMsg = err instanceof Error ? err.message : String(err);
    console.error(`\x1B[31m\u9519\u8BEF: ${errorMsg}\x1B[0m`);
    return { success: false, exitCode: 1, error: errorMsg };
  }
}
function main() {
  const result = runCli(process.argv.slice(2));
  process.exit(result.exitCode);
}
function handleVehicle(subcommand, args, positional) {
  const database = getDb();
  switch (subcommand) {
    case "add": {
      const name = args["name"];
      if (!name)
        throw new Error("\u8BF7\u63D0\u4F9B --name \u53C2\u6570");
      const vehicle = addVehicle(database, name, args["plate"]);
      console.log(`\x1B[32m\u8F66\u8F86\u5DF2\u6DFB\u52A0: ${vehicle.name}${vehicle.plate ? ` (${vehicle.plate})` : ""} (ID: ${vehicle.id})\x1B[0m`);
      break;
    }
    case "list": {
      const vehicles = listVehicles(database);
      if (vehicles.length === 0) {
        console.log("\u6682\u65E0\u8F66\u8F86\u8BB0\u5F55");
        return;
      }
      console.log(table(["ID", "\u540D\u79F0", "\u8F66\u724C", "\u5F53\u524D\u91CC\u7A0B", "\u521B\u5EFA\u65F6\u95F4"], vehicles.map((v) => [
        v.id,
        v.name,
        v.plate ?? "-",
        formatMileage(v.current_mileage),
        v.created_at
      ])));
      break;
    }
    case "delete": {
      const id = parseInt(positional[0] ?? "");
      if (isNaN(id))
        throw new Error("\u8BF7\u63D0\u4F9B\u8F66\u8F86 ID");
      deleteVehicle(database, id);
      console.log(`\x1B[32m\u8F66\u8F86\u5DF2\u5220\u9664 (ID: ${id})\x1B[0m`);
      break;
    }
    default:
      console.error(`\u672A\u77E5\u5B50\u547D\u4EE4: car ${subcommand}`);
      console.log("\u53EF\u7528\u5B50\u547D\u4EE4: add, list, delete");
  }
}
function handleMileage(subcommand, args, positional) {
  const database = getDb();
  switch (subcommand) {
    case "add": {
      const vehicleId = parseInt(args["car"]);
      const mileage = parseFloat(args["mileage"]);
      if (isNaN(vehicleId))
        throw new Error("\u8BF7\u63D0\u4F9B --car \u53C2\u6570(\u8F66\u8F86ID)");
      if (isNaN(mileage))
        throw new Error("\u8BF7\u63D0\u4F9B --mileage \u53C2\u6570(\u91CC\u7A0B\u6570)");
      const record = addMileageRecord(database, {
        vehicle_id: vehicleId,
        mileage,
        datetime: args["datetime"],
        note: args["note"]
      });
      console.log(`\u2705 \u91CC\u7A0B\u8BB0\u5F55\u5DF2\u4FDD\u5B58`);
      const lastRefuel = getLastRefuel(database, vehicleId);
      if (lastRefuel) {
        const distance = mileage - lastRefuel.mileage;
        const refuelDate = new Date(lastRefuel.datetime);
        const currentDate = new Date(record.datetime);
        const daysSince = Math.floor((currentDate.getTime() - refuelDate.getTime()) / (1000 * 60 * 60 * 24));
        console.log(`\uD83D\uDCCA \u8DDD\u79BB\u4E0A\u6B21\u52A0\u6CB9: ${formatDuration(daysSince)}, \u884C\u9A76 ${distance.toLocaleString("zh-CN")} km`);
      }
      const lastMaintenance = getLastMaintenance(database, vehicleId);
      if (lastMaintenance) {
        const distance = mileage - lastMaintenance.mileage;
        const maintenanceDate = new Date(lastMaintenance.datetime);
        const currentDate = new Date(record.datetime);
        const daysSince = Math.floor((currentDate.getTime() - maintenanceDate.getTime()) / (1000 * 60 * 60 * 24));
        console.log(`\uD83D\uDD27 \u8DDD\u79BB\u4E0A\u6B21\u4FDD\u517B: ${formatDuration(daysSince)}, \u884C\u9A76 ${distance.toLocaleString("zh-CN")} km`);
      }
      break;
    }
    case "list": {
      const vehicleId = parseInt(args["car"]);
      if (isNaN(vehicleId))
        throw new Error("\u8BF7\u63D0\u4F9B --car \u53C2\u6570(\u8F66\u8F86ID)");
      const records = listMileageRecords(database, vehicleId);
      if (records.length === 0) {
        console.log("\u6682\u65E0\u91CC\u7A0B\u8BB0\u5F55");
        return;
      }
      console.log(table(["ID", "\u91CC\u7A0B(km)", "\u65F6\u95F4", "\u5907\u6CE8"], records.map((r) => [
        r.id,
        r.mileage?.toLocaleString("zh-CN") ?? "-",
        r.datetime,
        r.note ?? "-"
      ])));
      break;
    }
    case "delete": {
      const id = parseInt(positional[0] ?? "");
      if (isNaN(id))
        throw new Error("\u8BF7\u63D0\u4F9B\u8BB0\u5F55 ID");
      deleteRecord(database, id);
      console.log(`\x1B[32m\u8BB0\u5F55\u5DF2\u5220\u9664 (ID: ${id})\x1B[0m`);
      break;
    }
    default:
      console.error(`\u672A\u77E5\u5B50\u547D\u4EE4: mileage ${subcommand}`);
      console.log("\u53EF\u7528\u5B50\u547D\u4EE4: add, list, delete");
  }
}
function handleRefuel(subcommand, args, positional) {
  const database = getDb();
  switch (subcommand) {
    case "add": {
      const vehicleId = parseInt(args["car"]);
      const liters = parseFloat(args["liters"]);
      const cost = parseFloat(args["cost"]);
      const mileage = parseFloat(args["mileage"]);
      if (isNaN(vehicleId))
        throw new Error("\u8BF7\u63D0\u4F9B --car \u53C2\u6570(\u8F66\u8F86ID)");
      if (isNaN(liters))
        throw new Error("\u8BF7\u63D0\u4F9B --liters \u53C2\u6570(\u52A0\u6CB9\u5347\u6570)");
      if (isNaN(cost))
        throw new Error("\u8BF7\u63D0\u4F9B --cost \u53C2\u6570(\u82B1\u8D39\u91D1\u989D)");
      if (isNaN(mileage))
        throw new Error("\u8BF7\u63D0\u4F9B --mileage \u53C2\u6570(\u5F53\u524D\u91CC\u7A0B)");
      const record = addRefuelRecord(database, {
        vehicle_id: vehicleId,
        liters,
        cost,
        mileage,
        datetime: args["datetime"],
        note: args["note"]
      });
      console.log(`\u2705 \u52A0\u6CB9\u8BB0\u5F55\u5DF2\u4FDD\u5B58: ${liters}L / ${formatCurrency(cost)}`);
      const previousRefuel = database.query("SELECT mileage, liters, cost FROM records WHERE vehicle_id = ? AND record_type = 'refuel' AND deleted = 0 ORDER BY datetime DESC LIMIT 1 OFFSET 1").get(vehicleId);
      if (previousRefuel) {
        const distance = mileage - previousRefuel.mileage;
        const prevPricePerLiter = previousRefuel.cost / previousRefuel.liters;
        const lPer100km = liters / distance * 100;
        const costPerKm = liters * prevPricePerLiter / distance;
        console.log(`\uD83D\uDCCA \u8DDD\u79BB\u4E0A\u6B21\u52A0\u6CB9\u884C\u9A76: ${distance.toLocaleString("zh-CN")} km`);
        console.log(`\u26FD \u6CB9\u8017: ${lPer100km.toFixed(2)} L/100km`);
        console.log(`\uD83D\uDCB0 \u6BCF\u516C\u91CC\u6210\u672C: ${costPerKm.toFixed(3)} \u5143/km`);
        const lastMaintenance = getLastMaintenance(database, vehicleId);
        if (lastMaintenance) {
          const distanceSinceMaintenance = mileage - lastMaintenance.mileage;
          const maintenanceDate = new Date(lastMaintenance.datetime);
          const currentDate = new Date(record.datetime);
          const daysSinceMaintenance = Math.floor((currentDate.getTime() - maintenanceDate.getTime()) / (1000 * 60 * 60 * 24));
          console.log(`\uD83D\uDD27 \u8DDD\u79BB\u4E0A\u6B21\u4FDD\u517B: ${formatDuration(daysSinceMaintenance)}, \u884C\u9A76 ${distanceSinceMaintenance.toLocaleString("zh-CN")} km`);
        }
      } else {
        console.log("\uD83D\uDCCA \u8FD9\u662F\u7B2C\u4E00\u6B21\u52A0\u6CB9\u8BB0\u5F55\uFF0C\u4E0B\u6B21\u52A0\u6CB9\u540E\u53EF\u8BA1\u7B97\u6CB9\u8017");
      }
      break;
    }
    case "list": {
      const vehicleId = parseInt(args["car"]);
      if (isNaN(vehicleId))
        throw new Error("\u8BF7\u63D0\u4F9B --car \u53C2\u6570(\u8F66\u8F86ID)");
      const records = listRefuelRecords(database, vehicleId);
      if (records.length === 0) {
        console.log("\u6682\u65E0\u52A0\u6CB9\u8BB0\u5F55");
        return;
      }
      console.log(table(["ID", "\u91CC\u7A0B(km)", "\u5347\u6570(L)", "\u82B1\u8D39(\u5143)", "\u65F6\u95F4", "\u5907\u6CE8"], records.map((r) => [
        r.id,
        r.mileage?.toLocaleString("zh-CN") ?? "-",
        r.liters ?? "-",
        r.cost ? r.cost.toFixed(2) : "-",
        r.datetime,
        r.note ?? "-"
      ])));
      break;
    }
    case "delete": {
      const id = parseInt(positional[0] ?? "");
      if (isNaN(id))
        throw new Error("\u8BF7\u63D0\u4F9B\u8BB0\u5F55 ID");
      deleteRecord2(database, id);
      console.log(`\x1B[32m\u8BB0\u5F55\u5DF2\u5220\u9664 (ID: ${id})\x1B[0m`);
      break;
    }
    case "consumption": {
      const vehicleId = parseInt(args["car"]);
      if (isNaN(vehicleId))
        throw new Error("\u8BF7\u63D0\u4F9B --car \u53C2\u6570(\u8F66\u8F86ID)");
      const results = calculateConsumption(database, vehicleId);
      if (results.length === 0) {
        console.log("\u81F3\u5C11\u9700\u89812\u6761\u52A0\u6CB9\u8BB0\u5F55\u624D\u80FD\u8BA1\u7B97\u6CB9\u8017");
        return;
      }
      console.log(table(["\u65F6\u6BB5", "\u91CC\u7A0B\u8303\u56F4(km)", "\u884C\u9A76\u91CC\u7A0B(km)", "\u52A0\u6CB9\u91CF(L)", "\u82B1\u8D39(\u5143)", "L/100km", "\u5143/km"], results.map((r) => [
        `${r.from_datetime} -> ${r.to_datetime}`,
        `${r.from_mileage.toLocaleString("zh-CN")} -> ${r.to_mileage.toLocaleString("zh-CN")}`,
        r.distance.toLocaleString("zh-CN"),
        r.liters.toFixed(1),
        formatCurrency(r.cost),
        r.l_per_100km.toFixed(2),
        r.cost_per_km.toFixed(3)
      ])));
      const totalDistance = results.reduce((sum, r) => sum + r.distance, 0);
      const totalLiters = results.reduce((sum, r) => sum + r.liters, 0);
      const totalCost = results.reduce((sum, r) => sum + r.cost, 0);
      if (totalDistance > 0) {
        console.log(`
\u7EFC\u5408\u5E73\u5747:`);
        console.log(`  \u5E73\u5747\u6CB9\u8017: ${(totalLiters / totalDistance * 100).toFixed(2)} L/100km`);
        console.log(`  \u5E73\u5747\u6BCF\u516C\u91CC: ${(totalCost / totalDistance).toFixed(3)} \u5143/km`);
      }
      break;
    }
    default:
      console.error(`\u672A\u77E5\u5B50\u547D\u4EE4: refuel ${subcommand}`);
      console.log("\u53EF\u7528\u5B50\u547D\u4EE4: add, list, delete, consumption");
  }
}
function handleMaintenance(subcommand, args, positional) {
  const database = getDb();
  switch (subcommand) {
    case "add": {
      const vehicleId = parseInt(args["car"]);
      const mileage = parseFloat(args["mileage"]);
      const cost = args["cost"] ? parseFloat(args["cost"]) : undefined;
      if (isNaN(vehicleId))
        throw new Error("\u8BF7\u63D0\u4F9B --car \u53C2\u6570(\u8F66\u8F86ID)");
      if (isNaN(mileage))
        throw new Error("\u8BF7\u63D0\u4F9B --mileage \u53C2\u6570(\u91CC\u7A0B\u6570)");
      const record = addMaintenanceRecord(database, {
        vehicle_id: vehicleId,
        mileage,
        cost: isNaN(cost) ? undefined : cost,
        datetime: args["datetime"],
        note: args["note"]
      });
      console.log(`\x1B[32m\u4FDD\u517B\u8BB0\u5F55\u5DF2\u6DFB\u52A0: ${mileage.toLocaleString("zh-CN")} km (ID: ${record.id}, \u65F6\u95F4: ${record.datetime})\x1B[0m`);
      break;
    }
    case "list": {
      const vehicleId = parseInt(args["car"]);
      if (isNaN(vehicleId))
        throw new Error("\u8BF7\u63D0\u4F9B --car \u53C2\u6570(\u8F66\u8F86ID)");
      const records = listMaintenanceRecords(database, vehicleId);
      if (records.length === 0) {
        console.log("\u6682\u65E0\u4FDD\u517B\u8BB0\u5F55");
        return;
      }
      console.log(table(["ID", "\u91CC\u7A0B(km)", "\u82B1\u8D39(\u5143)", "\u65F6\u95F4", "\u5907\u6CE8"], records.map((r) => [
        r.id,
        r.mileage?.toLocaleString("zh-CN") ?? "-",
        r.cost ? r.cost.toFixed(2) : "-",
        r.datetime,
        r.note ?? "-"
      ])));
      break;
    }
    case "delete": {
      const id = parseInt(positional[0] ?? "");
      if (isNaN(id))
        throw new Error("\u8BF7\u63D0\u4F9B\u8BB0\u5F55 ID");
      deleteRecord3(database, id);
      console.log(`\x1B[32m\u8BB0\u5F55\u5DF2\u5220\u9664 (ID: ${id})\x1B[0m`);
      break;
    }
    case "since": {
      const vehicleId = parseInt(args["car"]);
      if (isNaN(vehicleId))
        throw new Error("\u8BF7\u63D0\u4F9B --car \u53C2\u6570(\u8F66\u8F86ID)");
      const interval = getMaintenanceInterval(database, vehicleId);
      if (!interval) {
        console.log("\u6682\u65E0\u4FDD\u517B\u8BB0\u5F55\u6216\u65E0\u6CD5\u8BA1\u7B97\u95F4\u9694");
        return;
      }
      console.log(`\u4E0A\u6B21\u4FDD\u517B\u65F6\u95F4: ${interval.last_maintenance_datetime}`);
      console.log(`\u4E0A\u6B21\u4FDD\u517B\u91CC\u7A0B: ${interval.last_maintenance_mileage.toLocaleString("zh-CN")} km`);
      console.log(`\u8DDD\u4ECA: ${formatDuration(interval.days_since)}`);
      console.log(`\u5DF2\u884C\u9A76: ${interval.distance_since.toLocaleString("zh-CN")} km`);
      console.log(`\u5F53\u524D\u91CC\u7A0B: ${interval.current_mileage.toLocaleString("zh-CN")} km (${interval.current_datetime})`);
      break;
    }
    default:
      console.error(`\u672A\u77E5\u5B50\u547D\u4EE4: maintenance ${subcommand}`);
      console.log("\u53EF\u7528\u5B50\u547D\u4EE4: add, list, delete, since");
  }
}
function handleStats(subcommand, args) {
  const database = getDb();
  switch (subcommand) {
    case "expenses": {
      const vehicleId = parseInt(args["car"]);
      if (isNaN(vehicleId))
        throw new Error("\u8BF7\u63D0\u4F9B --car \u53C2\u6570(\u8F66\u8F86ID)");
      const year = args["year"] ? parseInt(args["year"]) : undefined;
      const month = args["month"] ? parseInt(args["month"]) : undefined;
      let period = "\u5168\u90E8\u65F6\u95F4";
      if (year && month) {
        period = `${year}\u5E74${month}\u6708`;
      } else if (year) {
        period = `${year}\u5E74`;
      }
      const summary = getExpenses(database, vehicleId, year, month);
      console.log(`
\u82B1\u8D39\u7EDF\u8BA1 (${period}):`);
      console.log(table(["\u7C7B\u522B", "\u82B1\u8D39"], [
        ["\u52A0\u6CB9\u82B1\u8D39", formatCurrency(summary.refuel_cost)],
        ["\u4FDD\u517B\u82B1\u8D39", formatCurrency(summary.maintenance_cost)],
        ["\u603B\u8BA1", formatCurrency(summary.total_cost)]
      ]));
      break;
    }
    case "current-mileage": {
      const vehicleId = parseInt(args["car"]);
      if (isNaN(vehicleId))
        throw new Error("\u8BF7\u63D0\u4F9B --car \u53C2\u6570(\u8F66\u8F86ID)");
      const mileage = getCurrentMileage(database, vehicleId);
      if (mileage === null) {
        console.log("\u8BE5\u8F66\u8F86\u6682\u65E0\u91CC\u7A0B\u8BB0\u5F55");
        return;
      }
      console.log(`\u5F53\u524D\u91CC\u7A0B: ${mileage.toLocaleString("zh-CN")} km`);
      break;
    }
    default:
      console.error(`\u672A\u77E5\u5B50\u547D\u4EE4: stats ${subcommand}`);
      console.log("\u53EF\u7528\u5B50\u547D\u4EE4: expenses, current-mileage");
  }
}
function handleDeleteAll(args) {
  const database = getDb();
  const vehicleId = parseInt(args["car"]);
  if (isNaN(vehicleId))
    throw new Error("\u8BF7\u63D0\u4F9B --car \u53C2\u6570(\u8F66\u8F86ID)");
  const recordType = args["type"];
  const typeLabel = recordType ? { mileage: "\u91CC\u7A0B", refuel: "\u52A0\u6CB9", maintenance: "\u4FDD\u517B" }[recordType] ?? recordType : "\u5168\u90E8";
  const vehicle = getVehicleById(database, vehicleId);
  if (!vehicle)
    throw new Error(`\u8F66\u8F86\u4E0D\u5B58\u5728 (ID: ${vehicleId})`);
  const count = deleteAllRecords(database, vehicleId, recordType);
  if (count === 0) {
    console.log("\u6CA1\u6709\u9700\u8981\u5220\u9664\u7684\u8BB0\u5F55");
    return;
  }
  console.log(`\x1B[32m\u5DF2\u5220\u9664 ${count} \u6761${typeLabel}\u8BB0\u5F55 (\u8F66\u8F86: ${vehicle.name})\x1B[0m`);
}
main();
export {
  setDbPath,
  runCli,
  getDb
};
