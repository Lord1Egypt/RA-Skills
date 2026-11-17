// MyLike-compatible: add Douyin videos into an existing favorite folder.
// Reads: same-origin fetch. Writes: the site's own axiosInstance (applies CSRF/signature
// interceptors; raw fetch gets status_code 5 "参数不合法").
import fs from 'node:fs';
import http from 'node:http';
import WebSocket from 'ws';

const PORT = Number(process.env.CDP_PORT || 9333);
const DIR = 'D:/Tools/mylike-fav-import';
const LOG = DIR + '/log.csv';
const argv = process.argv.slice(2);
const cmd = argv[0];
const flag = (n, d = null) => { const i = argv.indexOf('--' + n); return i < 0 ? d : argv[i + 1]; };
const sleep = ms => new Promise(r => setTimeout(r, ms));

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
    const m = document.cookie.match(/(?:^|;\\s*)msToken=([^;]+)/); if (m) p.set('msToken', decodeURIComponent(m[1]));
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
  move(id,folderId){ return this.write('/aweme/v1/web/collects/video/move/', {item_ids:[id], item_type:'2', to_collects_id:folderId, update_collects_sort:'true'}, {}); }
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
    cursor = r.cursor; await sleep(500);
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
    cursor = r.cursor; await sleep(400);
  }
  return false;
}

async function main() {
  const s = await openSession();
  await s.eval(HELPER);

  if (cmd === 'status') { const st = await loggedIn(s); console.log(JSON.stringify({ ...st, logged_in: st.code === 0 }, null, 2)); return; }
  if (cmd === 'eval') { console.log(JSON.stringify({ ok: true, value: await s.eval(flag('js', 'null')) })); return; }
  if (cmd === 'shot') {
    const out = flag('out', DIR + '/screen.png');
    const r = await s.send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(out, Buffer.from(r.data, 'base64'));
    console.log(JSON.stringify({ ok: true, path: out })); return;
  }
  if (cmd === 'folders') { console.log(JSON.stringify(await allFolders(s), null, 2)); return; }

  if (cmd === 'move-test') {
    const id = flag('id'); const name = flag('folder', '<夹名>');
    const folders = await allFolders(s);
    const f = folders.find(x => x.name === name);
    if (!f) { console.log(JSON.stringify({ ok: false, error: 'FOLDER_MISSING', got: folders.map(x => x.name) })); return; }
    const r = await s.eval(`(async()=>{ const r = await window.__ml.move(${JSON.stringify(id)}, ${JSON.stringify(f.id)}); return r; })()`);
    await sleep(1000);
    const hit = await folderHas(s, f.id, id);
    console.log(JSON.stringify({ folder: f, result: r, in_folder: hit }, null, 2)); return;
  }

  if (cmd === 'add') {
    const name = flag('folder', '<夹名>');
    const limit = Number(flag('limit', '0')) || 0;
    const st = await loggedIn(s);
    if (st.code !== 0) { console.log(JSON.stringify({ ok: false, error: 'NOT_LOGGED_IN', detail: st })); process.exitCode = 3; return; }
    console.log(JSON.stringify({ step: 'login', nickname: st.nick }));

    const folders = await allFolders(s);
    const folder = folders.find(f => f.name === name);
    if (!folder) { console.log(JSON.stringify({ ok: false, error: 'FOLDER_MISSING', got: folders.map(f => f.name) })); process.exitCode = 4; return; }
    console.log(JSON.stringify({ step: 'folder', folder }));

    const items = JSON.parse(fs.readFileSync(DIR + '/items.json', 'utf8'));
    const todo = limit ? items.slice(0, limit) : items;
    if (!fs.existsSync(LOG)) fs.writeFileSync(LOG, '\uFEFFid,title,author,collect_code,move_code,verified,note,at\n');
    const stats = { ok: 0, failed: 0 };
    for (const it of todo) {
      let collectCode = 'skip', moveCode = '', verified = '', note = '';
      const d = await s.eval(`(async()=>{ const r = await window.__ml.detail(${JSON.stringify(it.id)}); const a=r.json&&r.json.aweme_detail; return {code:r.json&&r.json.status_code, stat:a?a.collect_stat:null, type:a?a.aweme_type:null}; })()`);
      if (d.stat == null) note = 'detail-unavailable';
      else {
        if (String(d.stat) !== '1') {
          const c = await s.eval(`(async()=>{ const r = await window.__ml.collect(${JSON.stringify(it.id)}, ${JSON.stringify(d.type == null ? 0 : d.type)}); return {code:r.code, msg:r.msg, error:r.error}; })()`);
          collectCode = String(c.code);
          if (c.code !== 0) note = 'collect-failed:' + (c.msg || c.error);
          await sleep(1000);
        } else collectCode = 'already';
        if (!note) {
          const m = await s.eval(`(async()=>{ const r = await window.__ml.move(${JSON.stringify(it.id)}, ${JSON.stringify(folder.id)}); return {code:r.code, msg:r.msg, error:r.error}; })()`);
          moveCode = String(m.code);
          if (m.code !== 0) note = 'move-failed:' + (m.msg || m.error);
          else {
            await sleep(800);
            verified = (await folderHas(s, folder.id, it.id)) ? 'yes' : 'no';
            if (verified === 'no') note = 'move-unverified';
          }
        }
      }
      if (!note) stats.ok++; else stats.failed++;
      fs.appendFileSync(LOG, [it.id, JSON.stringify(it.title || ''), JSON.stringify(it.author || ''), collectCode, moveCode, verified, JSON.stringify(note), new Date().toISOString()].join(',') + '\n');
      console.log(JSON.stringify({ id: it.id, collect: collectCode, move: moveCode, verified, note }));
      await sleep(1800 + Math.floor(Math.random() * 1200));
    }
    console.log(JSON.stringify({ ok: true, stats, folder: folder.name, log: LOG }, null, 2));
    return;
  }

  if (cmd === 'verify') {
    const name = flag('folder', '<夹名>');
    const folders = await allFolders(s);
    const f = folders.find(x => x.name === name);
    if (!f) { console.log(JSON.stringify({ ok: false, error: 'FOLDER_MISSING' })); return; }
    const items = JSON.parse(fs.readFileSync(DIR + '/items.json', 'utf8')).map(x => x.id);
    const missing = [];
    for (const id of items) if (!(await folderHas(s, f.id, id))) missing.push(id);
    console.log(JSON.stringify({ folder: f.name, remote_count: f.count, expected: items.length, missing: missing.length, sample: missing.slice(0, 5) }, null, 2));
    return;
  }

  console.log('unknown command');
}

main().then(() => process.exit(0)).catch(e => { console.log(JSON.stringify({ ok: false, error: String(e && e.message || e) })); process.exit(1); });
