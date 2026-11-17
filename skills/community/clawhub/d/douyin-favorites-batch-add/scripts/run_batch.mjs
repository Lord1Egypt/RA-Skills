// Batch runner: create folders from queue, move items in, verify, resumable.
// Reuses run2.mjs conventions: reads via same-origin fetch, writes via window.axiosInstance.
import fs from 'node:fs';
import http from 'node:http';
import WebSocket from 'ws';

const PORT = Number(process.env.CDP_PORT || 9333);
const DIR = 'D:/Tools/mylike-fav-import';
const QDIR = DIR + '/douyin-queue';
const STATE = QDIR + '/state.json';
const LOG = DIR + '/log.csv';
const ROUNDS = DIR + '/rounds.jsonl';
const argv = process.argv.slice(2);
const cmd = argv[0] || 'plan';
const flag = (n, d = null) => { const i = argv.indexOf('--' + n); return i < 0 ? d : argv[i + 1]; };
const has = n => argv.includes('--' + n);
const sleep = ms => new Promise(r => setTimeout(r, ms));
const rnd = (a, b) => a + Math.floor(Math.random() * (b - a + 1));

// 节奏参数（单账号保守值，改这一组就够）
const PACE = {
  itemGapNear: [8000, 13000],    // 70%：正常快
  itemGapMid: [13000, 22000],    // 25%：多停一会
  itemGapFar: [30000, 60000],    // 5%：走神
  pNear: 0.70, pMid: 0.95,
  longEvery: [30, 50],           // 每 30~50 条随机插一次长停
  longPause: [150000, 360000],   // 长停 2.5~6 分钟
  collectMove: [2500, 5000],     // 收藏→入夹
  verifyGap: [1200, 2500],       // 入夹→回读
  folderPause: [30000, 90000],   // 建夹后
};
function itemGap() {
  const r = Math.random();
  if (r < PACE.pNear) return rnd(...PACE.itemGapNear);
  if (r < PACE.pMid) return rnd(...PACE.itemGapMid);
  return rnd(...PACE.itemGapFar);
}

function httpJson(method, path) {
  return new Promise((resolve, reject) => {
    const req = http.request({ host: '127.0.0.1', port: PORT, path, method, timeout: 10000 }, res => {
      let data = '';
      res.setEncoding('utf8');
      res.on('data', c => (data += c));
      res.on('end', () => { try { resolve(JSON.parse(data)); } catch { reject(new Error('bad json')); } });
    });
    req.on('error', reject); req.on('timeout', () => req.destroy(new Error('timeout')));
    req.end();
  });
}

class Sess {
  constructor(ws) {
    this.ws = ws; this.id = 0; this.waiters = new Map();
    this.ws.on('message', m => {
      const d = JSON.parse(m.toString());
      if (d.id && this.waiters.has(d.id)) {
        const { res, rej } = this.waiters.get(d.id); this.waiters.delete(d.id);
        d.error ? rej(new Error(d.error.message)) : res(d.result);
      }
    });
  }
  send(method, params = {}) {
    const id = ++this.id;
    return new Promise((res, rej) => {
      this.waiters.set(id, { res, rej });
      this.ws.send(JSON.stringify({ id, method, params }));
      setTimeout(() => { if (this.waiters.delete(id)) rej(new Error('cdp timeout ' + method)); }, 60000);
    });
  }
  async eval(expression) {
    const r = await this.send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
    if (r.exceptionDetails) throw new Error('page error: ' + JSON.stringify(r.exceptionDetails).slice(0, 300));
    return r.result.value;
  }
}

async function openSession() {
  const list = await httpJson('GET', '/json/list');
  const page = list.find(t => t.type === 'page' && t.url.includes('douyin.com'));
  if (!page) throw new Error('no douyin page open');
  const ws = new WebSocket(page.webSocketDebuggerUrl, { perMessageDeflate: false });
  await new Promise((res, rej) => { ws.once('open', res); ws.once('error', rej); });
  const s = new Sess(ws);
  await s.send('Page.enable');
  return s;
}

const HELPER = `
window.__ml = {
  params(extra){
    const p = new URLSearchParams({device_platform:'webapp',aid:'6383',channel:'channel_pc_web',version_code:'290100',version_name:'29.1.0',update_version_code:'170400',cookie_enabled:'true',platform:'PC'});
    const m = document.cookie.match(/(?:^|;\\\\s*)msToken=([^;]+)/); if (m) p.set('msToken', decodeURIComponent(m[1]));
    for (const [k,v] of Object.entries(extra||{})) p.set(k, String(v));
    return p;
  },
  async read(path, query, method){
    const p = this.params(query);
    const r = await fetch('https://www.douyin.com'+path+'?'+p, {credentials:'include', cache:'no-store', method: method||'GET', headers:{accept:'application/json, text/plain, */*'}});
    const t = await r.text();
    let j=null; try{ j=JSON.parse(t); }catch(e){}
    return {http:r.status, json:j, raw:t.slice(0,600)};
  },
  async write(path, query, body){
    const inst = window.axiosInstance;
    if (!inst || typeof inst.request !== 'function') return {error:'no-axios-instance'};
    const params = {channel:'channel_pc_web', pc_client_type:'1', version_code:'170400', version_name:'17.4.0', aid:'6383', device_platform:'webapp', ...query};
    const r = await inst.request({
      url: path, method:'POST', params,
      paramsSerializer: p => { const s=new URLSearchParams(); for(const [k,v] of Object.entries(p)){ if(v==null) continue; if(Array.isArray(v)) v.forEach(x=>s.append(k,String(x))); else s.append(k,String(v)); } return s.toString(); },
      data: body && Object.keys(body).length ? new URLSearchParams(body).toString() : '',
      headers: {'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'},
      withCredentials: true, timeout: 18000, responseType:'text',
      transformResponse: [raw => raw], validateStatus: () => true
    });
    let j=null; try{ j=JSON.parse(r.data); }catch(e){}
    return {http:r.status, code: j && j.status_code, msg: j && j.status_msg, raw:String(r.data).slice(0,200)};
  },
  self(){ return this.read('/aweme/v1/web/user/profile/self/', {}); },
  detail(id){ return this.read('/aweme/v1/web/aweme/detail/', {aweme_id:id}); },
  folders(cursor){ return this.read('/aweme/v1/web/collects/list/', {cursor:cursor||0, count:20, pc_client_type:1}); },
  folderItems(id,cursor,count){ return this.read('/aweme/v1/web/collects/video/list/', {collects_id:id, cursor:cursor||0, count:count||20, pc_client_type:1}); },
  collect(id,type){ return this.write('/aweme/v1/web/aweme/collect/', {}, {aweme_id:id, action:'1', aweme_type:String(type==null?'0':type)}); },
  move(id,folderId,itemType){ return this.write('/aweme/v1/web/collects/video/move/', {item_ids:[id], item_type:String(itemType||2), to_collects_id:folderId, update_collects_sort:'true'}, {}); },
  createFolder(name){ return this.write('/aweme/v1/web/collects/maintain/', {}, {action:'1', collects_name:name, secret:'1'}); }
};
true;
`;

async function loggedIn(s) {
  return s.eval('(async()=>{ const r = await window.__ml.self(); return {code:r.json&&r.json.status_code, nick:(r.json&&r.json.user&&r.json.user.nickname)||null}; })()');
}

async function allFolders(s) {
  const out = []; let cursor = 0;
  for (let i = 0; i < 30; i++) {
    const r = await s.eval(`(async()=>{ const r = await window.__ml.folders(${cursor}); const j = r.json||{}; return {code:j.status_code, has:j.has_more, cursor:j.cursor, list:(j.collects_list||j.collects||[]).map(x=>({id:String(x.collects_id_str||x.collects_id), name:x.collects_name, count:x.aweme_count||x.total_number, status:x.status}))}; })()`);
    if (r.code !== 0) throw new Error('folder list failed: ' + JSON.stringify(r).slice(0, 200));
    out.push(...r.list);
    if (!r.has) break;
    if (!r.cursor || String(r.cursor) === String(cursor)) break;
    cursor = r.cursor; await sleep(600);
  }
  return out;
}

async function folderHas(s, folderId, workId) {
  let cursor = 0;
  for (let i = 0; i < 60; i++) {
    const r = await s.eval(`(async()=>{ const r = await window.__ml.folderItems(${JSON.stringify(folderId)}, ${cursor}, 20); const j=r.json||{}; return {code:j.status_code, has:j.has_more, cursor:j.cursor, hit: r.raw.includes(${JSON.stringify(workId)}) || JSON.stringify(j).includes(${JSON.stringify(workId)})}; })()`);
    if (r.code !== 0) throw new Error('folder items failed: ' + JSON.stringify(r).slice(0, 200));
    if (r.hit) return true;
    if (!r.has) return false;
    if (!r.cursor || String(r.cursor) === String(cursor)) return false;
    cursor = r.cursor; await sleep(500);
  }
  return false;
}

const readState = () => JSON.parse(fs.readFileSync(STATE, 'utf8'));
const writeState = st => { st.updated = new Date().toISOString(); fs.writeFileSync(STATE, JSON.stringify(st, null, 1)); };
const itemsOf = f => JSON.parse(fs.readFileSync(QDIR + '/' + f.file, 'utf8'));

function ensureLog() {
  if (!fs.existsSync(LOG)) fs.writeFileSync(LOG, '\uFEFFfolder,id,title,author,collect_code,move_code,verified,note,at\n');
}

function remaining(st) { return st.folders.reduce((a, f) => a + (f.total - f.cursor), 0); }

async function ensureFolder(s, st, f, folders) {
  if (f.folder_id) {
    const hit = folders.find(x => x.id === f.folder_id);
    if (hit) return hit;
  }
  let hit = folders.find(x => x.name === f.name);
  if (hit) { f.folder_id = hit.id; f.status = f.cursor >= f.total ? 'done' : 'active'; return hit; }
  const c = await s.eval(`(async()=>{ const r = await window.__ml.createFolder(${JSON.stringify(f.name)}); return {code:r.code, msg:r.msg, error:r.error, raw:r.raw}; })()`);
  if (c.code !== 0) throw new Error('CREATE_FOLDER_FAILED ' + f.name + ' :: ' + (c.msg || c.error || c.raw));
  await sleep(1500);
  const after = await allFolders(s);
  hit = after.find(x => x.name === f.name);
  if (!hit) throw new Error('CREATE_FOLDER_UNVERIFIED ' + f.name);
  f.folder_id = hit.id; f.status = 'active'; f.created_at = new Date().toISOString();
  folders.push(hit);
  console.log(JSON.stringify({ step: 'folder-created', name: f.name, id: hit.id }));
  await sleep(rnd(...PACE.folderPause));
  return hit;
}

function acquireLock() {
  const lock = QDIR + '/.run.lock';
  try {
    const st = fs.existsSync(lock) ? JSON.parse(fs.readFileSync(lock, 'utf8')) : null;
    if (st && Date.now() - (st.ts || 0) < 5400 * 1000) {
      const alive = (() => { try { process.kill(st.pid, 0); return true; } catch { return false; } })();
      if (alive) return { ok: false, holder: st };
    }
  } catch { }
  fs.writeFileSync(lock, JSON.stringify({ pid: process.pid, ts: Date.now() }));
  return { ok: true, lock };
}
const releaseLock = () => { try { fs.unlinkSync(QDIR + '/.run.lock'); } catch { } };

async function run() {
  const max = Number(flag('max', '200'));
  const only = flag('folder', null);
  const dry = has('dry');
  ensureLog();
  const lk = dry ? { ok: true } : acquireLock();
  if (!lk.ok) { console.log(JSON.stringify({ ok: false, error: 'ALREADY_RUNNING', holder: lk.holder })); return; }
  if (!dry) process.on('exit', releaseLock);
  const st = readState();
  const todoFolders = st.folders.filter(f => (only ? f.name === only : f.cursor < f.total));
  if (!todoFolders.length) { console.log(JSON.stringify({ ok: true, done: true, remaining: 0 })); return; }

  const plan = [];
  let budget = max;
  for (const f of todoFolders) { if (budget <= 0) break; const take = Math.min(budget, f.total - f.cursor); plan.push({ name: f.name, take }); budget -= take; }
  if (dry) { console.log(JSON.stringify({ dry: true, remaining: remaining(st), plan }, null, 2)); return; }

  const s = await openSession();
  await s.eval(HELPER);
  const li = await loggedIn(s);
  if (li.code !== 0) throw new Error('NOT_LOGGED_IN ' + JSON.stringify(li));
  const folders = await allFolders(s);

  const round = { started: new Date().toISOString(), nickname: li.nick, target: max, ok: 0, failed: 0, folders: [], stop: null };
  let consecutiveFail = 0;
  let roundAdded = 0;
  let nextLongAt = rnd(...PACE.longEvery);

  for (const p of plan) {
    const f = st.folders.find(x => x.name === p.name);
    const items = itemsOf(f);
    const folder = await ensureFolder(s, st, f, folders);
    writeState(st);
    round.folders.push({ name: f.name, id: folder.id, take: p.take });
    let added = 0;
    while (added < p.take && f.cursor < f.total) {
      const it = items[f.cursor];
      let collectCode = 'skip', moveCode = '', verified = '', note = '', itemType = 2;
      try {
        const d = await s.eval(`(async()=>{ const r = await window.__ml.detail(${JSON.stringify(it.id)}); const a=r.json&&r.json.aweme_detail; return {code:r.json&&r.json.status_code, stat:a?a.collect_stat:null, type:a?a.aweme_type:null}; })()`);
        if (d.stat == null) note = 'detail-unavailable';
        else {
          if (String(d.stat) !== '1') {
            const c = await s.eval(`(async()=>{ const r = await window.__ml.collect(${JSON.stringify(it.id)}, ${JSON.stringify(d.type == null ? 0 : d.type)}); return {code:r.code, msg:r.msg, error:r.error}; })()`);
            collectCode = String(c.code);
            if (c.code !== 0) note = 'collect-failed:' + (c.msg || c.error);
            await sleep(rnd(...PACE.collectMove));
          } else collectCode = 'already';
          if (!note) {
            let m = await s.eval(`(async()=>{ const r = await window.__ml.move(${JSON.stringify(it.id)}, ${JSON.stringify(folder.id)}, 2); return {code:r.code, msg:r.msg, error:r.error}; })()`);
            moveCode = String(m.code);
            if (m.code !== 0 && it.type === '图文') {
              await sleep(rnd(...PACE.collectMove));
              m = await s.eval(`(async()=>{ const r = await window.__ml.move(${JSON.stringify(it.id)}, ${JSON.stringify(folder.id)}, 1); return {code:r.code, msg:r.msg, error:r.error}; })()`);
              moveCode = 'img:' + String(m.code); itemType = 1;
            }
            if (m.code !== 0) note = 'move-failed:' + (m.msg || m.error || 'code' + m.code);
            else {
              await sleep(rnd(...PACE.verifyGap));
              verified = (await folderHas(s, folder.id, it.id)) ? 'yes' : 'no';
              if (verified === 'no') note = 'move-unverified';
            }
          }
        }
      } catch (e) {
        note = 'exception:' + String(e && e.message || e).slice(0, 120);
      }
      if (!note) { round.ok++; f.ok = (f.ok || 0) + 1; consecutiveFail = 0; }
      else { round.failed++; f.failed = (f.failed || 0) + 1; consecutiveFail++; }
      f.cursor++;
      if (f.cursor >= f.total) f.status = 'done';
      writeState(st);
      fs.appendFileSync(LOG, [f.name, it.id, JSON.stringify(it.title || ''), JSON.stringify(it.author || ''), collectCode, moveCode, verified, JSON.stringify(note), new Date().toISOString()].join(',') + '\n');
      console.log(JSON.stringify({ f: f.name, n: f.cursor + '/' + f.total, id: it.id, collect: collectCode, move: moveCode, v: verified, note }));
      if (consecutiveFail >= 5) { round.stop = 'consecutive-5-failures'; break; }
      added++;
      roundAdded++;
      if (roundAdded >= nextLongAt) {
        const pause = rnd(...PACE.longPause);
        console.log(JSON.stringify({ pause_s: Math.round(pause / 1000), after: roundAdded }));
        await sleep(pause);
        nextLongAt = roundAdded + rnd(...PACE.longEvery);
      } else await sleep(itemGap());
    }
    if (round.stop) break;
  }

  round.finished = new Date().toISOString();
  round.remaining = remaining(st);
  round.done_folders = st.folders.filter(f => f.status === 'done').length;
  round.total_folders = st.folders.length;
  fs.appendFileSync(ROUNDS, JSON.stringify(round) + '\n');
  console.log('SUMMARY ' + JSON.stringify(round));
}

(async () => {
  if (cmd === 'plan') {
    const st = readState();
    const done = st.folders.filter(f => f.status === 'done').length;
    console.log(JSON.stringify({ remaining: remaining(st), done_folders: done, total_folders: st.folders.length, next: st.folders.filter(f => f.cursor < f.total).slice(0, 3).map(f => `${f.name} ${f.cursor}/${f.total}`) }, null, 2));
    return;
  }
  if (cmd === 'run') { await run(); return; }
  console.log('usage: node run_batch.mjs plan | run [--max 200] [--folder NAME] [--dry]');
})().then(() => process.exit(0)).catch(e => { console.log(JSON.stringify({ ok: false, error: String(e && e.message || e) })); process.exit(1); });
