/**
 * 飞书目标表解析与持久化 (target resolution)
 * ───────────────────────────────────────────────────────────────────────────
 * 解决"同步到哪张表"：用户给一个飞书链接(wiki/base) → 解析出 base+table
 *   → 校验字段 → 存到 ~/.opencli/boss-recruit/target.json。
 * 之后 feishu.mjs 读这份配置，并只写"该表实际存在"的字段（适配不同模板）。
 */
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import fs from 'node:fs';
import path from 'node:path';
import * as BASE from './feishu-base.mjs';
const pexec = promisify(execFile);

export const TARGET_FILE = path.join(process.env.HOME || '.', '.opencli', 'boss-recruit', 'target.json');

/** 我们会往人才表写的核心字段；缺这些会影响功能（但只写实际存在的）。 */
export const EXPECTED_FIELDS = ['姓名', '简历来源', '当前阶段', '简历附件'];

async function lark(args) {
  const { stdout } = await pexec('lark-cli', args, { maxBuffer: 64 * 1024 * 1024 });
  const i = stdout.indexOf('{');
  const j = i >= 0 ? JSON.parse(stdout.slice(i)) : null;
  if (j && j.ok === false) throw new Error(`lark-cli: ${JSON.stringify(j.error)}`);
  return j;
}

export function loadTarget() {
  try { return JSON.parse(fs.readFileSync(TARGET_FILE, 'utf8')); } catch { return null; }
}
export function saveTarget(obj) {
  fs.mkdirSync(path.dirname(TARGET_FILE), { recursive: true });
  fs.writeFileSync(TARGET_FILE, JSON.stringify(obj, null, 2));
  return obj;
}

/** 从飞书链接/token 解析出 { baseToken, tableHint }。支持 /wiki/、/base/、裸 base token。 */
export async function resolveBaseFromLink(link, identity = 'user') {
  const s = String(link).trim();
  const tableHint = (s.match(/[?&]table=(tbl[\w]+)/) || [])[1] || null;

  // /wiki/<token> → 解析 obj_token(bitable)
  if (/\/wiki\//.test(s) || /^[A-Za-z0-9]{20,}$/.test(s) && !s.startsWith('bas')) {
    if (/\/wiki\//.test(s)) {
      const r = await lark(['wiki', '+node-get', '--node-token', s, '--as', identity]);
      const d = r?.data || {};
      if (d.obj_type === 'bitable' && d.obj_token) return { baseToken: d.obj_token, tableHint, title: d.title };
      throw new Error(`该 wiki 节点不是多维表格(obj_type=${d.obj_type})`);
    }
  }
  // /base/<token>
  const m = s.match(/\/base\/([A-Za-z0-9]+)/);
  if (m) return { baseToken: m[1], tableHint };
  // 裸 base token（bascn.../其它 20+ 串）
  if (/^[A-Za-z0-9]{20,}$/.test(s)) return { baseToken: s, tableHint };
  throw new Error('无法识别的飞书链接/token，请给 /wiki/ 或 /base/ 链接');
}

/** 列出 base 内数据表。 */
export async function listTables(baseToken, identity = 'user') {
  const r = await lark(['base', '+table-list', '--base-token', baseToken, '--as', identity]);
  return r?.data?.tables || [];
}

/** 选人才表：优先 URL 里的 table 参数 → 名字含"人才/候选/talent" → 唯一表 → 否则需用户指定。 */
export function pickTalentTable(tables, tableHint) {
  if (tableHint) { const t = tables.find((x) => x.id === tableHint); if (t) return t; }
  const byName = tables.find((x) => /人才|候选|talent|candidate/i.test(x.name));
  if (byName) return byName;
  if (tables.length === 1) return tables[0];
  return null; // 歧义，调用方让用户从 tables 里选
}

/** 读字段，返回 { fieldNames[], attachmentField } 。附件字段按 type 优先、名字兜底。 */
export async function inspectFields(baseToken, tableId, identity = 'user') {
  const r = await lark(['base', '+field-list', '--base-token', baseToken, '--table-id', tableId, '--as', identity]);
  const fields = r?.data?.fields || [];
  const fieldNames = fields.map((f) => f.name);
  // 飞书附件字段 type=17；兜底用名字含"附件"
  const att = fields.find((f) => f.type === 17) || fields.find((f) => /附件/.test(f.name));
  return { fieldNames, attachmentField: att?.name || null };
}

/**
 * 一站式配置：给链接 → 解析 → 选表 → 校验字段 → 存盘。
 * 两种后端：
 *   - 有 opts.token(授权码) → base-api(BaseOpenSDK 等价)，强制 /base/ 链接，可分发
 *   - 无 token → lark-cli(用户 OAuth)，本机自用
 * 返回 { ok, target?, tables?(歧义时), missing?, backend }。
 */
export async function configureTarget(link, opts = {}) {
  const token = opts.token || null;

  // 授权码模式：只认 /base/ 链接（企业端 /wiki/ 不支持）
  if (token) {
    if (/\/wiki\//.test(String(link))) {
      return { ok: false, reason: 'wiki_not_supported' };
    }
    const m = String(link).match(/\/base\/([A-Za-z0-9]+)/);
    const baseToken = m ? m[1] : (/^[A-Za-z0-9]{20,}$/.test(String(link).trim()) ? String(link).trim() : null);
    if (!baseToken) return { ok: false, reason: 'need_base_link' };
    const tableHint = (String(link).match(/[?&]table=(tbl[\w]+)/) || [])[1] || opts.tableId || null;
    if (!tableHint) return { ok: false, reason: 'need_table_in_url' };
    // base-api 校验授权码 + 表，并取字段、表名
    await BASE.testConnection(baseToken, tableHint, token);
    const { fieldNames, attachmentField } = await BASE.listFields(baseToken, tableHint, token);
    const talentTableName = await BASE.getTableName(baseToken, tableHint, token);
    const missing = EXPECTED_FIELDS.filter((f) => f !== '简历附件' && !fieldNames.includes(f));
    const target = {
      backend: 'base-api', baseToken, talentTable: tableHint, talentTableName,
      personal_base_token: token, attachmentField: attachmentField || null,
      fields: fieldNames, configured_at: new Date().toISOString(),
    };
    saveTarget(target);
    return { ok: true, target, missing, hasAttachment: !!attachmentField, backend: 'base-api' };
  }

  // lark-cli 模式（用户 OAuth）
  const identity = opts.identity || 'user';
  const { baseToken, tableHint, title } = await resolveBaseFromLink(link, identity);
  const tables = await listTables(baseToken, identity);
  if (!tables.length) return { ok: false, reason: 'base 内无数据表', baseToken };

  let table = opts.tableId ? tables.find((t) => t.id === opts.tableId) : pickTalentTable(tables, tableHint);
  if (!table) return { ok: false, reason: 'ambiguous_table', baseToken, tables, title };

  const { fieldNames, attachmentField } = await inspectFields(baseToken, table.id, identity);
  const missing = EXPECTED_FIELDS.filter((f) => f !== '简历附件' && !fieldNames.includes(f));

  const target = {
    backend: 'lark-cli', baseToken, talentTable: table.id, talentTableName: table.name,
    attachmentField: attachmentField || null,
    fields: fieldNames, identity,
    title: title || null, configured_at: new Date().toISOString(),
  };
  saveTarget(target);
  return { ok: true, target, missing, hasAttachment: !!attachmentField, backend: 'lark-cli' };
}

export default { TARGET_FILE, EXPECTED_FIELDS, loadTarget, saveTarget, resolveBaseFromLink, listTables, pickTalentTable, inspectFields, configureTarget };
