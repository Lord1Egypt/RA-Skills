#!/usr/bin/env node
'use strict';

// Search doctors via OceanBus DoctorDataSvc (P2P)
//
// Usage:
//   node scripts/search-doctors.js search --city "北京" --depts "乳腺外科" [--keyword "许"]
//   node scripts/search-doctors.js list-depts
//   node scripts/search-doctors.js list-cities

const fs = require('fs');
const path = require('path');
const os = require('os');
const config = require('../config/api.js');

// Lazy-load oceanbus — allows help/version without npm install
let _createOceanBus = null;
function requireOceanBus() {
  if (!_createOceanBus) {
    _createOceanBus = require('oceanbus').createOceanBus;
  }
  return _createOceanBus;
}

const DATA_DIR = path.join(os.homedir(), '.oceanbus-referral');
const CRED_FILE = path.join(DATA_DIR, 'credentials.json');
const CONFIG_FILE = path.join(DATA_DIR, 'config.json');

const POLL_TIMEOUT_MS = 15000;
const POLL_INTERVAL_MS = 800;

function ensureDir() { fs.mkdirSync(DATA_DIR, { recursive: true }); }

function loadCredentials() {
  if (!fs.existsSync(CRED_FILE)) return null;
  try { return JSON.parse(fs.readFileSync(CRED_FILE, 'utf-8')); } catch (_) { return null; }
}

function saveCredentials(agentId, apiKey, openid) {
  ensureDir();
  fs.writeFileSync(CRED_FILE, JSON.stringify({ agent_id: agentId, api_key: apiKey, openid }, null, 2));
}

function loadConfig() {
  if (!fs.existsSync(CONFIG_FILE)) return { doctor_data_openid: '' };
  try { return JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8')); } catch (_) { return { doctor_data_openid: '' }; }
}

function saveConfigKey(key, value) {
  const cfg = loadConfig();
  cfg[key] = value;
  ensureDir();
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(cfg, null, 2));
}

// ── Doctor Data Service discovery ───────────────────────────────────────────

async function discoverDoctorData(ob, creds) {
  // 1. Yellow Pages discover (tags from skill config)
  try {
    const key = await ob.createServiceKey();
    ob.l1.yellowPages.setIdentity(creds.openid, key.signer, key.publicKey);
    const r = await ob.l1.yellowPages.discover(config.doctorDataTags, 5);
    if (r.data && r.data.entries && r.data.entries.length > 0) {
      const openid = r.data.entries[0].openid;
      saveConfigKey('doctor_data_openid', openid);
      return openid;
    }
  } catch (_) { /* YP may be unavailable */ }

  // 2. Local cache (~/.oceanbus-referral/config.json)
  const cfg = loadConfig();
  if (cfg.doctor_data_openid) return cfg.doctor_data_openid;

  // 3. Skill default (config/api.js — bootstrap for new users)
  if (config.doctorDataOpenid) return config.doctorDataOpenid;

  return null;
}

// ── Search ──────────────────────────────────────────────────────────────────

async function cmdSearch(opts) {
  const { city, depts, keyword } = opts;
  if (!city) { console.error('缺少参数: --city'); process.exit(1); }
  if (!depts || depts.length === 0) { console.error('缺少参数: --depts (逗号分隔)'); process.exit(1); }

  const ob = await getOceanBus();
  const creds = loadCredentials();

  const svcOpenid = await discoverDoctorData(ob, creds);
  if (!svcOpenid) {
    console.error('无法找到 DoctorDataSvc。请确保服务已部署且 Yellow Pages 可达。');
    console.error('也可以手动设置: 在 ~/.oceanbus-referral/config.json 中设置 doctor_data_openid');
    await ob.destroy();
    process.exit(1);
  }

  const request = { action: 'search', city, depts };
  if (keyword) request.keyword = keyword;

  // Set up listener BEFORE sending request
  let resolved = false;

  ob.startListening(async (msg) => {
    if (resolved) return;
    try {
      const result = JSON.parse(msg.content);
      // Response can arrive from a different OpenID than what YP returned
      if (result.results !== undefined || result.error) {
        resolved = true;
        formatOutput(result, opts);
        await ob.destroy();
        return;
      }
    } catch (_) { /* not a JSON response */ }
  });

  await sleep(300);

  try {
    await ob.sendJson(svcOpenid, request);
  } catch (e) {
    console.error('发送查询失败: ' + e.message);
    await ob.destroy();
    process.exit(1);
  }

  // Wait for response with timeout
  const deadline = Date.now() + POLL_TIMEOUT_MS;
  while (!resolved && Date.now() < deadline) {
    await sleep(300);
  }

  if (!resolved) {
    console.error('查询超时（' + POLL_TIMEOUT_MS / 1000 + ' 秒）。请稍后重试。');
    await ob.destroy();
    process.exit(1);
  }
}

// ── List ────────────────────────────────────────────────────────────────────

async function cmdList(action) {
  const ob = await getOceanBus();
  const creds = loadCredentials();
  const svcOpenid = await discoverDoctorData(ob, creds);
  if (!svcOpenid) {
    console.error('无法找到 DoctorDataSvc。');
    await ob.destroy();
    process.exit(1);
  }

  // Set up listener first
  let resolved = false;

  ob.startListening(async (msg) => {
    if (resolved) return;
    try {
      const result = JSON.parse(msg.content);
      const key = action === 'list_depts' ? 'depts' : 'cities';
      if (result[key]) {
        resolved = true;
        console.log(result[key].join('\n'));
        await ob.destroy();
        return;
      }
    } catch (_) {}
  });

  await sleep(300);

  try {
    await ob.sendJson(svcOpenid, { action });
  } catch (e) {
    console.error('发送失败: ' + e.message);
    await ob.destroy();
    process.exit(1);
  }

  const deadline = Date.now() + POLL_TIMEOUT_MS;
  while (!resolved && Date.now() < deadline) {
    await sleep(300);
  }

  if (!resolved) {
    console.error('查询超时。');
    await ob.destroy();
    process.exit(1);
  }
}

// ── Helpers ─────────────────────────────────────────────────────────────────

async function getOceanBus() {
  const createOceanBus = requireOceanBus();
  const creds = loadCredentials();
  let identity = undefined;

  if (creds) {
    identity = { agent_id: creds.agent_id, api_key: creds.api_key };
  }

  const ob = await createOceanBus({
    keyStore: { type: 'memory' },
    identity,
  });

  // Auto-register if no credentials
  if (!creds) {
    const reg = await ob.register();
    const openid = await ob.getOpenId();
    saveCredentials(reg.agent_id, reg.api_key, openid);
  }

  return ob;
}

function formatOutput(result, opts) {
  if (result.error) {
    console.error('查询失败: ' + result.error);
    return;
  }

  const label = opts.keyword
    ? `专家推荐 — ${opts.city} ${opts.depts.join(', ')} 关键词: ${opts.keyword}`
    : `专家推荐 — ${opts.city} ${opts.depts.join(', ')}`;

  console.log(label);
  console.log('共 ' + result.total + ' 位专家' + (result.truncated ? ' (仅显示前' + result.returned + '位)' : ''));
  console.log('');

  for (const d of (result.results || [])) {
    const fee = d.fee_low !== undefined && d.fee_high !== undefined
      ? d.fee_low + '-' + d.fee_high
      : (d.fee_low || d.fee_high || '—');
    const bilingual = d.bilingual ? ' 🌐' : '';
    const schedule = d.schedule ? ' · ' + d.schedule : '';

    console.log('### ' + d.name + ' — ' + d.title + ' (' + d.dept + ')');
    const mainHosp = d.main_hospital && d.main_hospital !== d.hospital
      ? ' | 原单位: ' + d.main_hospital : '';
    console.log('- 出诊: ' + d.hospital + mainHosp + (d.title.startsWith('主任') ? ' 🔴' : d.title.startsWith('副主任') ? ' 🟠' : ''));
    console.log('- 擅长: ' + (d.skill_short || '—'));
    console.log('- 挂号费: ¥' + fee + bilingual + schedule);
    console.log('');
  }

  if (result.truncated) {
    console.log('⚠️ 共 ' + result.total + ' 位，仅显示前 ' + MAX_RESULTS_DISPLAY + ' 位。请尝试缩小范围。');
  }
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

const MAX_RESULTS_DISPLAY = 30;

// ── Main ────────────────────────────────────────────────────────────────────

async function main() {
  const args = process.argv.slice(2);
  const cmd = args[0];

  if (!cmd || cmd === 'help') {
    console.log('专家推荐 — OceanBus DoctorDataSvc 查询');
    console.log('');
    console.log('命令:');
    console.log('  node scripts/search-doctors.js search --city <城市> --depts <科室> [--keyword <关键词>]');
    console.log('  node scripts/search-doctors.js list-depts');
    console.log('  node scripts/search-doctors.js list-cities');
    console.log('');
    console.log('示例:');
    console.log('  node scripts/search-doctors.js search --city "北京" --depts "乳腺外科"');
    console.log('  node scripts/search-doctors.js search --city "北京" --depts "呼吸科,胸外科" --keyword "许"');
    return;
  }

  try {
    switch (cmd) {
      case 'search': {
        const opts = { city: '', depts: [], keyword: '' };
        for (let i = 1; i < args.length; i++) {
          if (args[i] === '--city' && i + 1 < args.length) opts.city = args[++i];
          else if (args[i] === '--depts' && i + 1 < args.length) opts.depts = args[++i].split(/[,，]/).map(s => s.trim()).filter(Boolean);
          else if (args[i] === '--keyword' && i + 1 < args.length) opts.keyword = args[++i];
        }
        await cmdSearch(opts);
        break;
      }
      case 'list-depts':
        await cmdList('list_depts');
        break;
      case 'list-cities':
        await cmdList('list_cities');
        break;
      default:
        console.log('未知命令: ' + cmd);
    }
  } catch (err) {
    console.error('错误: ' + err.message);
    process.exit(1);
  }
}

main().catch(err => { console.error('Fatal:', err.message); process.exit(1); });
