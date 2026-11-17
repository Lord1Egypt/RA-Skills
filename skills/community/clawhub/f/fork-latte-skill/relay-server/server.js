// 报名中转服务
// 接收报名信息并写入飞书多维表格。飞书凭证只存在于服务端环境变量，绝不下发客户端。
// 两种写入模式：
//   MODE=lark_cli    —— 调用本机已授权的 lark-cli（适合本地快速验证）
//   MODE=feishu_api  —— 调用飞书开放平台 API（生产，需自建应用，可部署到任意服务器/Serverless）
// 重复提交处理：
//   GET  /api/signup/exists?wechat=XXX  → 查询该微信号是否已有记录（同一人 = 微信号相同）
//   POST /api/signup  body 可带 overwrite:true + record_id → 覆盖（更新）已有记录；否则新增

import http from 'node:http';
import { writeFile, unlink } from 'node:fs/promises';
import { spawn } from 'node:child_process';

const PORT = process.env.PORT || 3000;
const MODE = (process.env.MODE || 'feishu_api').toLowerCase();
const API_KEY = process.env.API_KEY || '';           // 可选：启用后客户端需在 header x-api-key 携带
const BASE_TOKEN = process.env.FEISHU_BASE_TOKEN || '';
const TABLE_ID = process.env.FEISHU_TABLE_ID || '';
const APP_ID = process.env.FEISHU_APP_ID || '';
const APP_SECRET = process.env.FEISHU_APP_SECRET || '';
const FEISHU_DOMAIN = process.env.FEISHU_DOMAIN || 'https://open.feishu.cn';

function send(res, code, obj) {
  res.writeHead(code, { 'Content-Type': 'application/json; charset=utf-8' });
  res.end(JSON.stringify(obj));
}

function normalizeExp(v) {
  if (!v) return null;
  const s = String(v).trim().toLowerCase();
  if (['有', '创过业', '是', 'yes', 'y', '有经验'].includes(s)) return '有';
  if (['无', '没', '没有', '否', 'no', 'n', '无经验'].includes(s)) return '无';
  return null;
}

// 从单元格取值里提取单选文本（lark_cli 返回 ["有"]，feishu_api 返回 [{text:"有"}]）
function expText(cell) {
  if (Array.isArray(cell)) {
    const x = cell[0];
    return x && (x.text || x) ? (x.text || x) : null;
  }
  return cell;
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let data = '';
    req.on('data', c => (data += c));
    req.on('end', () => {
      try { resolve(data ? JSON.parse(data) : {}); }
      catch (e) { reject(new Error('body not json')); }
    });
    req.on('error', reject);
  });
}

let _token = null, _expire = 0;
async function getTenantToken() {
  if (_token && Date.now() < _expire) return _token;
  const r = await fetch(`${FEISHU_DOMAIN}/open-apis/auth/v3/tenant_access_token/internal`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ app_id: APP_ID, app_secret: APP_SECRET }),
  });
  const j = await r.json();
  if (j.code !== 0) throw new Error('tenant_token: ' + JSON.stringify(j));
  _token = j.tenant_access_token;
  _expire = Date.now() + (j.expire - 60) * 1000;
  return _token;
}

function runLarkCli(args) {
  return new Promise((resolve, reject) => {
    const proc = spawn('lark-cli', args, { shell: true });
    let o = '', e = '';
    proc.stdout.on('data', d => (o += d));
    proc.stderr.on('data', d => (e += d));
    proc.on('close', c => (c === 0 ? resolve(o) : reject(new Error('lark-cli exit ' + c + ': ' + e))));
  });
}

// 构造写入字段（两种模式的单选字段形状不同）
function buildFields(name, job, wechat, exp) {
  if (MODE === 'lark_cli') {
    // lark-cli 单选字段用数组包裹
    return { 名字: name, 职业: job, 微信号: wechat, 有无创业经验: [exp] };
  }
  // feishu_api：单选字段（SingleSelect）写入时值必须是纯字符串，不能是 {text:...}
  return { 名字: name, 职业: job, 微信号: wechat, 有无创业经验: exp };
}

// 查重：返回第一个微信号匹配的记录 { record_id, fields:{名字,职业,微信号,有无创业经验} } 或 null
async function findExisting(wechat) {
  if (MODE === 'lark_cli') {
    // 用 record-list 直接读表（不走搜索索引，避免亚秒级延迟），客户端按微信号过滤
    const out = await runLarkCli([
      'base', '+record-list', '--base-token', BASE_TOKEN, '--table-id', TABLE_ID,
      '--format', 'json', '--limit', '200',
    ]);
    const j = JSON.parse(out);
    if (!j.ok) throw new Error('lark-cli search: ' + JSON.stringify(j.error || j));
    const rows = (j.data && j.data.data) || [];
    const cols = (j.data && j.data.fields) || [];
    const ids = (j.data && j.data.record_id_list) || [];
    const wi = cols.indexOf('微信号');
    for (let i = 0; i < rows.length; i++) {
      if (wi >= 0 && rows[i][wi] === wechat) {
        const f = {};
        cols.forEach((k, idx) => { f[k] = rows[i][idx]; });
        return {
          record_id: ids[i],
          fields: {
            名字: f['名字'], 职业: f['职业'], 微信号: f['微信号'],
            有无创业经验: expText(f['有无创业经验']),
          },
        };
      }
    }
    return null;
  }
  // feishu_api
  const token = await getTenantToken();
  const r = await fetch(
    `${FEISHU_DOMAIN}/open-apis/bitable/v1/apps/${BASE_TOKEN}/tables/${TABLE_ID}/records?page_size=500`,
    { headers: { Authorization: 'Bearer ' + token } }
  );
  const j = await r.json();
  if (j.code !== 0) throw new Error('feishu_list: ' + JSON.stringify(j));
  const items = (j.data && j.data.items) || [];
  for (const it of items) {
    const f = it.fields || {};
    if (f['微信号'] === wechat) {
      return {
        record_id: it.record_id,
        fields: {
          名字: f['名字'], 职业: f['职业'], 微信号: f['微信号'],
          有无创业经验: expText(f['有无创业经验']),
        },
      };
    }
  }
  return null;
}

async function writeViaFeishuApi(fields, recordId) {
  const token = await getTenantToken();
  const url = recordId
    ? `${FEISHU_DOMAIN}/open-apis/bitable/v1/apps/${BASE_TOKEN}/tables/${TABLE_ID}/records/${recordId}`
    : `${FEISHU_DOMAIN}/open-apis/bitable/v1/apps/${BASE_TOKEN}/tables/${TABLE_ID}/records`;
  const method = recordId ? 'PUT' : 'POST';
  const r = await fetch(url, {
    method,
    headers: { 'Content-Type': 'application/json', Authorization: 'Bearer ' + token },
    body: JSON.stringify({ fields }),
  });
  const j = await r.json();
  if (j.code !== 0) throw new Error('feishu_write: ' + JSON.stringify(j));
  // 飞书创建/更新记录返回结构：data.record.record_id（兼容旧版 data.record_id）
  return recordId || (j.data && j.data.record && j.data.record.record_id) || j.data.record_id;
}

async function writeViaLarkCli(fields, recordId) {
  // recordId 存在 → 更新（upsert）；否则 → 新建（batch-create）
  const payload = recordId ? fields : { create_records: [fields] };
  const f = 'signup-rec-' + Date.now() + '-' + Math.floor(Math.random() * 1e6) + '.json';
  await writeFile(f, JSON.stringify(payload)); // UTF-8 无 BOM
  try {
    const args = recordId
      ? ['base', '+record-upsert', '--base-token', BASE_TOKEN, '--table-id', TABLE_ID, '--record-id', recordId, '--json', '@./' + f]
      : ['base', '+record-batch-create', '--base-token', BASE_TOKEN, '--table-id', TABLE_ID, '--json', '@./' + f];
    return await new Promise((resolve, reject) => {
      const proc = spawn('lark-cli', args, { shell: true });
      let out = '', err = '';
      proc.stdout.on('data', d => (out += d));
      proc.stderr.on('data', d => (err += d));
      proc.on('close', code => {
        if (code !== 0) return reject(new Error('lark-cli exit ' + code + ': ' + err));
        if (recordId) return resolve(recordId);
        try {
          const j = JSON.parse(out);
          if (!j.ok) return reject(new Error('lark-cli not ok: ' + out));
          resolve((j.data && j.data.record_id_list && j.data.record_id_list[0]) || 'ok');
        } catch (e) { reject(new Error('parse lark-cli out: ' + out)); }
      });
    });
  } finally {
    try { await unlink(f); } catch {}
  }
}

async function writeRecord(name, job, wechat, exp, recordId) {
  const fields = buildFields(name, job, wechat, exp);
  return MODE === 'lark_cli'
    ? writeViaLarkCli(fields, recordId || null)
    : writeViaFeishuApi(fields, recordId || null);
}

const server = http.createServer(async (req, res) => {
  // API_KEY 校验（GET/POST 统一）
  if (API_KEY && req.headers['x-api-key'] !== API_KEY) {
    return send(res, 401, { ok: false, error: 'unauthorized' });
  }
  let url;
  try { url = new URL(req.url, 'http://localhost'); } catch { return send(res, 400, { ok: false, error: 'bad url' }); }

  try {
    // 查重接口
    if (req.method === 'GET' && url.pathname === '/api/signup/exists') {
      const wechat = (url.searchParams.get('wechat') || '').trim();
      if (!wechat) return send(res, 400, { ok: false, error: 'wechat 必填' });
      const found = await findExisting(wechat);
      if (!found) return send(res, 200, { ok: true, exists: false });
      return send(res, 200, { ok: true, exists: true, record_id: found.record_id, fields: found.fields });
    }

    // 报名接口
    if (req.method === 'POST' && url.pathname === '/api/signup') {
      const b = await readBody(req);
      const name = String(b.name || b.名字 || '').trim();
      const job = String(b.job || b.职业 || '').trim();
      const wechat = String(b.wechat || b.微信号 || '').trim();
      const exp = normalizeExp(b.experience || b.有无创业经验);
      if (!name || !wechat) return send(res, 400, { ok: false, error: '名字和微信号必填' });
      if (!exp) return send(res, 400, { ok: false, error: '有无创业经验须为 有/无' });

      const overwrite = b.overwrite === true || b.overwrite === 'true' || b.overwrite === 1 || b.overwrite === '1';
      const recordId = b.record_id || b.record_id_ || null;

      const rid = await writeRecord(name, job, wechat, exp, overwrite ? recordId : null);
      return send(res, 200, { ok: true, record_id: rid, overwritten: !!(overwrite && recordId) });
    }

    return send(res, 404, { ok: false, error: 'not found' });
  } catch (e) {
    return send(res, 500, { ok: false, error: String(e.message || e) });
  }
});

server.listen(PORT, () => console.log(`signup relay listening on :${PORT} (mode=${MODE})`));
