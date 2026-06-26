/**
 * 将 Furcas CSV 数据导入飞书多维表格，并创建按责任人分组的看板视图。
 *
 * 用法:
 *   node scripts/import_to_bitable.mjs \
 *       --csv <path-to-csv> \
 *       --app <app_token> \
 *       --table <table_id> \
 *       --name <table-name> \
 *       [--batch-size 15]
 *
 * 前置条件:
 *   加密令牌存储在 OpenClaw 的 feishu-uat 目录下。
 *   路径规则: $XDG_DATA_HOME/openclaw-feishu-uat/ (Linux)
 *   或 $HOME/.local/share/openclaw-feishu-uat/
 *   也可通过 FEISHU_UAT_DIR 环境变量指定
 */

import { readFileSync, readdirSync } from "fs";
import { createDecipheriv } from "crypto";
import { homedir } from "os";
import { join } from "path";

// ---------- 参数 (通过环境变量传入) ----------
const APP_TOKEN = process.env.APP_TOKEN || "";
const TABLE_ID = process.env.TABLE_ID || "";
const CSV_PATH = process.env.CSV_PATH || "/workspace/furcas.csv";
const BATCH_SIZE = parseInt(process.env.BATCH_SIZE || "15", 10);
const TABLE_NAME = process.env.TABLE_NAME || "工单数据";

if (!APP_TOKEN || !TABLE_ID) {
  console.error("Error: 必须提供 --app 和 --table 参数，或设置 APP_TOKEN/TABLE_ID 环境变量");
  process.exit(1);
}

// ---------- 获取 UAT 目录 ----------
function getUatDir() {
  return process.env.FEISHU_UAT_DIR || join(
    process.env.XDG_DATA_HOME || join(homedir(), '.local', 'share'),
    'openclaw-feishu-uat'
  );
}

// ---------- 获取 Access Token ----------
function getAccessToken() {
  const uatDir = getUatDir();
  const masterKeyPath = join(uatDir, 'master.key');
  const masterKey = readFileSync(masterKeyPath);
  const files = readdirSync(uatDir).filter((f) => f.endsWith(".enc"));
  if (files.length === 0) {
    throw new Error(`未找到加密令牌文件 (${uatDir})`);
  }
  const encData = readFileSync(join(uatDir, files[0]));
  const iv = encData.subarray(0, 12);
  const tag = encData.subarray(12, 28);
  const ciphertext = encData.subarray(28);
  const decipher = createDecipheriv("aes-256-gcm", masterKey, iv);
  decipher.setAuthTag(tag);
  const plaintext = Buffer.concat([decipher.update(ciphertext), decipher.final()]).toString("utf8");
  return JSON.parse(plaintext).accessToken;
}

// ---------- 解析 CSV ----------
function parseCsv(path) {
  const text = readFileSync(path, "utf-8");
  const lines = text.split("\n").filter((l) => l.trim());
  const headers = lines[0].split(",").map((h) => h.replace(/^"|"$/g, ""));

  // 字段映射: CSV 列名 -> Bitable 字段名
  const FIELD_MAP = {
    "问题描述": "文本",
    "问题链接": "问题链接",
    "工单状态/修复情况": "工单状态|修复情况",
    "问题原因": "问题原因",
    "责任人": "责任人",
    "解决类别": "解决类别",
    "解决模块": "解决模块",
    "超时时间": "超时时间",
    "超时备注": "超时备注",
  };

  function parseLine(line) {
    const result = [];
    let current = "";
    let inQuotes = false;
    for (const ch of line) {
      if (ch === '"') { inQuotes = !inQuotes; continue; }
      if (ch === "," && !inQuotes) { result.push(current.trim()); current = ""; continue; }
      current += ch;
    }
    result.push(current.trim());
    return result;
  }

  const records = [];
  for (let i = 1; i < lines.length; i++) {
    const fields = parseLine(lines[i]);
    const row = {};
    headers.forEach((h, idx) => (row[h] = fields[idx] || ""));

    const bitableFields = {};
    for (const [csvKey, bitableKey] of Object.entries(FIELD_MAP)) {
      const val = (row[csvKey] || "").trim();
      if (bitableKey === "问题链接" && val) {
        bitableFields[bitableKey] = { link: val, text: "查看工单" };
      } else {
        bitableFields[bitableKey] = val;
      }
    }
    records.push({ fields: bitableFields });
  }
  return records;
}

// ---------- Feishu API ----------
const BASE = "https://open.feishu.cn/open-apis";
let token = null;
function headers() {
  if (!token) token = getAccessToken();
  return { Authorization: "Bearer " + token, "Content-Type": "application/json" };
}

async function api(method, path, body) {
  const resp = await fetch(BASE + path, {
    method,
    headers: headers(),
    body: body ? JSON.stringify(body) : undefined,
  });
  const data = await resp.json();
  if (data.code !== 0) throw new Error(`API ${method} ${path}: ${data.code} ${data.msg}`);
  return data;
}

async function importBatch(records) {
  return api("POST", `/bitable/v1/apps/${APP_TOKEN}/tables/${TABLE_ID}/records/batch_create`, { records });
}

async function listTableIds() {
  const data = await api("GET", `/bitable/v1/apps/${APP_TOKEN}/tables?page_size=100`);
  return data.data.items;
}

async function createTable(tableName, fields) {
  const body = {
    table: {
      name: tableName,
      default_view_name: "全部",
      fields: fields.map((f) => ({
        field_name: f.name,
        type: f.type,
        property: f.property || undefined,
      })),
    },
  };
  // Filter out undefined property
  body.table.fields = body.table.fields.map((f) => {
    if (f.property === undefined) delete f.property;
    return f;
  });
  const data = await api("POST", `/bitable/v1/apps/${APP_TOKEN}/tables`, body);
  return data.data.table_id;
}

async function listViews() {
  const data = await api("GET", `/bitable/v1/apps/${APP_TOKEN}/tables/${TABLE_ID}/views?page_size=100`);
  return data.data.items;
}

async function createKanbanView(viewName) {
  const data = await api("POST", `/bitable/v1/apps/${APP_TOKEN}/tables/${TABLE_ID}/views`, {
    view_name: viewName,
    view_type: "kanban",
  });
  return data.data;
}

async function checkTable() {
  try {
    const tables = await listTableIds();
    return tables.find((t) => t.name === TABLE_NAME);
  } catch {
    return null;
  }
}

// ---------- 获取责任人字段（用于看板） ----------
async function getResponsibleFieldId() {
  const data = await api("GET", `/bitable/v1/apps/${APP_TOKEN}/tables/${TABLE_ID}/fields?page_size=100`);
  const field = data.data.items.find((f) => f.field_name === "责任人");
  return field ? field.field_id : null;
}

// ---------- Main ----------
async function main() {
  console.log(`=== Furcas 数据导入 ===`);
  console.log(`CSV: ${CSV_PATH}`);
  console.log(`Bitable: ${APP_TOKEN} / ${TABLE_ID}`);

  // 0. 校验目标表名
  console.log(`\n[0/6] 校验目标表名...`);
  try {
    const tables = await listTableIds();
    const tableInfo = tables.find((t) => t.table_id === TABLE_ID);
    if (tableInfo) {
      const actualName = tableInfo.name;
      if (actualName !== TABLE_NAME) {
        console.log(`  ⚠️ 表名不匹配: 期望="${TABLE_NAME}", 实际="${actualName}"`);
        console.log(`  ⚠️ 请确认 APP_TOKEN/TABLE_ID 是否正确！继续导入但数据可能被写入错误的表`);
      } else {
        console.log(`  ✅ 表名匹配: "${actualName}"`);
      }
    } else {
      console.log(`  ⚠️ 未找到 Table ID "${TABLE_ID}" 对应的表，请检查参数`);
    }
  } catch (e) {
    console.log(`  ⚠️ 校验失败: ${e.message}，跳过校验`);
  }

  // 1. 解析 CSV
  console.log(`\n[1/6] 解析 CSV...`);
  const records = parseCsv(CSV_PATH);
  console.log(`  读取 ${records.length} 条记录`);

  // 2. 清空已有数据
  console.log(`\n[2/6] 清空现有数据...`);
  const listData = await api("GET", `/bitable/v1/apps/${APP_TOKEN}/tables/${TABLE_ID}/records?page_size=500`);
  const items = listData.data?.items || [];
  if (items.length > 0) {
    const ids = items.map((r) => r.record_id);
    // ⚠️ API 参数名是 record_ids，不是 records
    await api("POST", `/bitable/v1/apps/${APP_TOKEN}/tables/${TABLE_ID}/records/batch_delete`, {
      record_ids: ids,
    });
    console.log(`  已删除 ${ids.length} 条旧记录`);
  } else {
    console.log(`  表为空，无需清理`);
  }

  // 3. 分批次导入
  console.log(`\n[3/6] 导入数据 (每批 ${BATCH_SIZE} 条)...`);
  let success = 0;
  for (let i = 0; i < records.length; i += BATCH_SIZE) {
    const batch = records.slice(i, i + BATCH_SIZE);
    await importBatch(batch);
    success += batch.length;
    const pct = ((success / records.length) * 100).toFixed(0);
    console.log(`  批 ${Math.floor(i / BATCH_SIZE) + 1}: ${batch.length} 条 ✅ (${pct}%)`);
    await new Promise((r) => setTimeout(r, 300));
  }

  // 4. 创建按责任人分组的看板视图
  console.log(`\n[4/6] 创建看板视图...`);
  const views = await listViews();
  let kanbanId = null;
  const existingKanban = views.find((v) => v.view_type === "kanban");
  if (existingKanban) {
    kanbanId = existingKanban.view_id;
    console.log(`  看板视图已存在: "${existingKanban.view_name}" (ID: ${kanbanId})`);
  } else {
    const kanban = await createKanbanView("按责任人分组");
    kanbanId = kanban.view_id;
    console.log(`  已创建看板视图: "${kanban.view_name}" (ID: ${kanbanId})`);
  }

  // 设置看板按"责任人"字段分组
  const respField = await getResponsibleFieldId();
  if (respField) {
    const kanbanMeta = await api("GET", `/bitable/v1/apps/${APP_TOKEN}/tables/${TABLE_ID}/views/${kanbanId}`);
    const currentProperty = kanbanMeta.data?.property || {};
    if (currentProperty.kanban_field_id !== respField) {
      await api("PATCH", `/bitable/v1/apps/${APP_TOKEN}/tables/${TABLE_ID}/views/${kanbanId}`, {
        property: { kanban_field_id: respField },
      });
      console.log(`  看板已按"责任人"字段分组 ✅`);
    } else {
      console.log(`  看板已按"责任人"分组，无需修改`);
    }
  } else {
    console.log(`  ⚠️ 未找到"责任人"字段，无法设置看板分组`);
  }

  // 5. 验证
  console.log(`\n[5/6] 验证...`);
  const verifyData = await api("GET", `/bitable/v1/apps/${APP_TOKEN}/tables/${TABLE_ID}/records?page_size=500`);
  const verified = verifyData.data.items.length;
  if (verified !== records.length) {
    console.log(`  ⚠️ 不一致: 导入${records.length}条, 实际${verified}条`);
  } else {
    console.log(`  CSV: ${records.length} 条, Bitable: ${verified} 条 → ✅ 完美匹配`);
  }

  // 5b. 校验超时备注字段是否成功导入
  console.log(`\n[5b/6] 校验超时备注...`);
  let csvWithRemark = 0, csvWithOvertime = 0;
  for (const rec of records) {
    if (rec.fields["超时备注"]) csvWithRemark++;
    if (rec.fields["超时时间"]) csvWithOvertime++;
  }
  console.log(`  CSV中有超时时间: ${csvWithOvertime}条, 有超时备注: ${csvWithRemark}条`);
  if (csvWithRemark > 0) {
    let bitableWithRemark = 0;
    for (const rec of verifyData.data.items) {
      if (rec.fields["超时备注"]) bitableWithRemark++;
    }
    console.log(`  Bitable中有超时备注: ${bitableWithRemark}条`);
    if (bitableWithRemark < csvWithRemark) {
      console.log(`  ⚠️ 超时备注字段可能未完全导入! CSV ${csvWithRemark}条, Bitable ${bitableWithRemark}条`);
      console.log(`  ⚠️ 建议检查是否缺少字段映射, 或字段在表中不存在`);
    } else {
      console.log(`  ✅ 超时备注字段导入完整`);
    }
  } else {
    console.log(`  ⚠️ CSV中未发现超时备注数据, 跳过校验`);
  }

  // 6. 去重（防止清空失败导致的数据重复）
  console.log(`\n[6/6] 去重检查...`);
  const allData = await api("GET", `/bitable/v1/apps/${APP_TOKEN}/tables/${TABLE_ID}/records?page_size=500`);
  const allRecs = allData.data.items;
  const ticketMap = {};
  for (const rec of allRecs) {
    const linkField = rec.fields?.问题链接;
    if (linkField?.link) {
      const match = linkField.link.match(/id=(\d+)/);
      if (match) {
        const tid = match[1];
        if (!ticketMap[tid]) ticketMap[tid] = [];
        ticketMap[tid].push(rec.record_id);
      }
    }
  }
  let dupCount = 0;
  for (const [, ids] of Object.entries(ticketMap)) {
    if (ids.length > 1) {
      const dupes = ids.slice(1);
      dupCount += dupes.length;
      // Delete duplicates one by one
      for (const rid of dupes) {
        await api("DELETE", `/bitable/v1/apps/${APP_TOKEN}/tables/${TABLE_ID}/records/${rid}`);
        await new Promise((r) => setTimeout(r, 50));
      }
    }
  }
  if (dupCount > 0) {
    console.log(`  删除了 ${dupCount} 条重复记录 ✅`);
    // 验证最终数量
    const finalData = await api("GET", `/bitable/v1/apps/${APP_TOKEN}/tables/${TABLE_ID}/records?page_size=500`);
    console.log(`  最终: ${finalData.data.items.length} 条唯一工单`);
  } else {
    console.log(`  无重复记录 ✅`);
  }

  console.log(`\n=== 导入完成 ===`);
}

main().catch((e) => {
  console.error("FATAL:", e.message);
  process.exit(1);
});
