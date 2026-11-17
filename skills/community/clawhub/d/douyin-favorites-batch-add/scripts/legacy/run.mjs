// MyLike-compatible: add Douyin videos into an existing favorite folder via in-page fetch.
// Usage: node run.mjs <status|folders|add|shot> [--folder NAME] [--limit N] [--dry] [--out PATH]
import fs from 'node:fs';
import http from 'node:http';
import WebSocket from 'ws';

const PORT = Number(process.env.CDP_PORT || 9333);
const BASE = 'https://www.douyin.com';
const DIR = 'D:/Tools/mylike-fav-import';
const LOG = DIR + '/log.csv';

const argv = process.argv.slice(2);
const cmd = argv[0];
const flag = (n, d = null) => {
  const i = argv.indexOf('--' + n);
  return i < 0 ? d : argv[i + 1];
};
const has = n => argv.includes('--' + n);
const sleep = ms => new Promise(r => setTimeout(r, ms));

function httpJson(method, path) {
  return new Promise((resolve, reject) => {
    const req = http.request({ host: '127.0.0.1', port: PORT, path, method, timeout: 10000 }, res => {
      let data = '';
      res.setEncoding('utf8');
      res.on('data', c => (data += c));
      res.on('end', () => { try { resolve(JSON.parse(data)); } catch (e) { reject(new Error('bad json: ' + data.slice(0, 200))); } });
    });
    req.on('error', reject); req.on('timeout', () => req.destroy(new Error('timeout')));
    req.end();
  });
}

class Sess {
  constructor(ws) { this.ws = ws; this.id = 0; this.waiters = new Map(); this.ws.on('message', m => { const d = JSON.parse(m.toString()); if (d.id && this.waiters.has(d.id)) { const { res, rej } = this.waiters.get(d.id); this.waiters.delete(d.id); d.error ? rej(new Error(d.error.message)) : res(d.result); } }); }
  send(method, params = {}) {
    const id = ++this.id;
    return new Promise((res, rej) => { this.waiters.set(id, { res, rej }); this.ws.send(JSON.stringify({ id, method, params })); setTimeout(() => { if (this.waiters.delete(id)) rej(new Error('cdp timeout ' + method)); }, 60000); });
  }
  async eval(expression) {
    const r = await this.send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
    if (r.exceptionDetails) throw new Error('page error: ' + JSON.stringify(r.exceptionDetails).slice(0, 400));
    return r.result.value;
  }
}

async function openSession() {
  const list = await httpJson('GET', '/json/list');
  let page = list.find(t => t.type === 'page' && t.url.includes('douyin.com'));
  if (!page) {
    const created = await httpJson('PUT', '/json/new');
    const ws = new WebSocket(created.webSocketDebuggerUrl, { perMessageDeflate: false });
    await new Promise((res, rej) => { ws.once('open', res); ws.once('error', rej); });
    const s = new Sess(ws);
    await s.send('Page.enable');
    await s.send('Page.navigate', { url: BASE + '/' });
    await sleep(6000);
    return s;
  }
  const ws = new WebSocket(page.webSocketDebuggerUrl, { perMessageDeflate: false });
  await new Promise((res, rej) => { ws.once('open', res); ws.once('error', rej); });
  const s = new Sess(ws);
  await s.send('Page.enable');
  return s;
}

// Injectable page helper: same-origin fetch with page cookies/signing.
const HELPER = `
window.__ml = {
  basic(extra){
    const p = new URLSearchParams({device_platform:'webapp',aid:'6383',channel:'channel_pc_web',version_code:'290100',version_name:'29.1.0',update_version_code:'170400',cookie_enabled:'true',platform:'PC'});
    const m = document.cookie.match(/(?:^|;\\s*)msToken=([^;]+)/); if (m) p.set('msToken', decodeURIComponent(m[1]));
    for (const [k,v] of Object.entries(extra||{})) p.set(k, String(v));
    return p;
  },
  async call(path, opts){
    const p = this.basic(opts.query);
    const init = {credentials:'include', cache:'no-store', method: opts.method||'GET', headers:{accept:'application/json, text/plain, */*'}};
    if (opts.body){ init.method='POST'; init.headers['content-type']='application/x-www-form-urlencoded;charset=UTF-8'; init.body = new URLSearchParams(opts.body).toString(); }
    const r = await fetch('https://www.douyin.com'+path+'?'+p, init);
    const t = await r.text();
    let j=null; try{ j=JSON.parse(t); }catch(e){}
    return {http:r.status, json:j, len:t.length, head:t.slice(0,200)};
  },
  self(){ return this.call('/aweme/v1/web/user/profile/self/', {}); },
  detail(id){ return this.call('/aweme/v1/web/aweme/detail/', {query:{aweme_id:id}}); },
  folders(cursor){ return this.call('/aweme/v1/web/collects/list/', {query:{cursor:cursor||0,count:20,pc_client_type:1}}); },
  folderItems(id,cursor,count){ return this.call('/aweme/v1/web/collects/video/list/', {query:{collects_id:id,cursor:cursor||0,count:count||20,pc_client_type:1}}); },
  collect(id,type){ return this.call('/aweme/v1/web/aweme/collect/', {method:'POST', body:{aweme_id:id, action:'1', aweme_type:String(type==null?'0':type)}}); },
  move(id,folderId,folderName){ return this.call('/aweme/v1/web/collects/video/move/', {method:'POST', body:{aweme_id:id,item_ids:id,item_type:'2',to_collects_id:folderId,collects_name:folderName,update_collects_sort:'true'}}); },
  createFolder(name,secret){ return this.call('/aweme/v1/web/collects/maintain/', {method:'POST', query:{version_code:'230000',version_name:'23.0.0'}, body:{action:'1', collects_name:name, secret: secret? '1':'0'}}); }
};
true;
`;

async function loggedIn(s) {
  const r = await s.eval('(async()=>{ const r = await window.__ml.self(); return {code:r.json&&r.json.status_code, nick:(r.json&&r.json.user&&r.json.user.nickname)||null, http:r.http}; })()');
  return r;
}

async function allFolders(s) {
  const out = [];
  let cursor = 0;
  for (let i = 0; i < 20; i++) {
    const r = await s.eval(`(async()=>{ const r = await window.__ml.folders(${cursor}); const j = r.json||{}; return {code:j.status_code, has:j.has_more, cursor:j.cursor, list:(j.collects||[]).map(x=>({id:String(x.collects_id_str||x.collects_id), name:x.collects_name, count:x.aweme_count, status:x.status}))}; })()`);
    if (r.code !== 0) throw new Error('folder list failed: ' + JSON.stringify(r));
    out.push(...r.list);
    if (!r.has) break;
    if (!r.cursor || String(r.cursor) === String(cursor)) break;
    cursor = r.cursor;
    await sleep(600);
  }
  return out;
}

async function main() {
  const s = await openSession();
  await s.eval(HELPER);

  if (cmd === 'status') {
    const st = await loggedIn(s);
    console.log(JSON.stringify({ ...st, logged_in: st.code === 0 }, null, 2));
    return;
  }
  if (cmd === 'eval') {
    const out = await s.eval(flag('js', 'null'));
    console.log(JSON.stringify({ ok: true, value: out }));
    return;
  }
  if (cmd === 'shot') {
    const out = flag('out', DIR + '/screen.png');
    const r = await s.send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(out, Buffer.from(r.data, 'base64'));
    console.log(JSON.stringify({ ok: true, path: out }));
    return;
  }
  if (cmd === 'folders') {
    console.log(JSON.stringify(await allFolders(s), null, 2));
    return;
  }

  if (cmd === 'add') {
    const name = flag('folder', '<夹名>');
    const limit = Number(flag('limit', '0')) || 0;
    const dry = has('dry');
    const st = await loggedIn(s);
    if (st.code !== 0) { console.log(JSON.stringify({ ok: false, error: 'NOT_LOGGED_IN', detail: st })); process.exitCode = 3; return; }
    console.log(JSON.stringify({ step: 'login', nickname: st.nick }));

    let folders = await allFolders(s);
    let folder = folders.find(f => f.name === name);
    if (!folder) {
      if (dry) { console.log(JSON.stringify({ ok: false, error: 'FOLDER_MISSING', folders: folders.map(f => f.name), dry })); return; }
      const r = await s.eval(`(async()=>{ const r = await window.__ml.createFolder(${JSON.stringify(name)}, true); return {code:r.json&&r.json.status_code, msg:r.json&&r.json.status_msg, info:r.json&&r.json.collects_info&&{id:String(r.json.collects_info.collects_id_str||r.json.collects_info.collects_id),name:r.json.collects_info.collects_name}}; })()`);
      console.log(JSON.stringify({ step: 'create-folder', result: r }));
      if (r.code !== 0) { console.log(JSON.stringify({ ok: false, error: 'CREATE_FAILED' })); process.exitCode = 4; return; }
      await sleep(1200);
      folders = await allFolders(s);
      folder = folders.find(f => f.name === name) || { id: String(r.info && r.info.id), name, count: 0 };
    }
    console.log(JSON.stringify({ step: 'folder', folder }));

    const items = JSON.parse(fs.readFileSync(DIR + '/items.json', 'utf8'));
    const todo = limit ? items.slice(0, limit) : items;
    if (!fs.existsSync(LOG)) fs.writeFileSync(LOG, '\uFEFFid,title,author,collect_result,collect_code,move_code,note,at\n');
    const results = [];
    for (const it of todo) {
      const d = await s.eval(`(async()=>{ const r = await window.__ml.detail(${JSON.stringify(it.id)}); const a=r.json&&r.json.aweme_detail; return {code:r.json&&r.json.status_code, stat:a?a.collect_stat:null, type:a?a.aweme_type:null, msg:r.json&&r.json.status_msg}; })()`);
      let note = '', collectCode = '', moveCode = '';
      if (d.stat == null) { note = 'detail-unavailable:' + (d.msg || d.code); }
      else {
        if (String(d.stat) !== '1') {
          const c = await s.eval(`(async()=>{ const r = await window.__ml.collect(${JSON.stringify(it.id)}, ${JSON.stringify(d.type == null ? 0 : d.type)}); return {code:r.json&&r.json.status_code, msg:r.json&&r.json.status_msg}; })()`);
          collectCode = String(c.code);
          if (c.code !== 0) note = 'collect-failed:' + c.msg;
          await sleep(1200);
        } else note = 'already-collected';
        if (collectCode === '' || collectCode === '0') {
          const m = await s.eval(`(async()=>{ const r = await window.__ml.move(${JSON.stringify(it.id)}, ${JSON.stringify(folder.id)}, ${JSON.stringify(folder.name)}); return {code:r.json&&r.json.status_code, msg:r.json&&r.json.status_msg}; })()`);
          moveCode = String(m.code);
          if (m.code !== 0) note = (note ? note + '|' : '') + 'move-failed:' + m.msg;
        }
      }
      const row = { id: it.id, title: (it.title || '').replace(/\s+/g, ' ').slice(0, 80), author: it.author, collect: collectCode || 'skip', move: moveCode || '-', note };
      results.push(row);
      fs.appendFileSync(LOG, [it.id, JSON.stringify(it.title || ''), JSON.stringify(it.author || ''), collectCode || 'skip', collectCode, moveCode, JSON.stringify(note), new Date().toISOString()].join(',') + '\n');
      console.log(JSON.stringify(row));
      await sleep(2000 + Math.floor(Math.random() * 1500));
    }
    const okCount = results.filter(r => r.note === 'already-collected' || (r.collect !== 'skip' || r.move === '0')).length;
    console.log(JSON.stringify({ ok: true, processed: results.length, folder: folder.name, log: LOG }, null, 2));
    return;
  }

  if (cmd === 'verify') {
    const name = flag('folder', '<夹名>');
    const folders = await allFolders(s);
    const f = folders.find(x => x.name === name);
    if (!f) { console.log(JSON.stringify({ ok: false, error: 'FOLDER_MISSING' })); return; }
    const ids = new Set();
    let cursor = 0;
    for (let i = 0; i < 40; i++) {
      const r = await s.eval(`(async()=>{ const r = await window.__ml.folderItems(${JSON.stringify(f.id)}, ${cursor}, 20); const j=r.json||{}; return {code:j.status_code, has:j.has_more, cursor:j.cursor, list:(j.aweme_list||j.collects_video_list||[]).map(x=>String(x.aweme_id||(x.aweme_info&&x.aweme_info.aweme_id)))}; })()`);
      if (r.code !== 0) throw new Error('items failed ' + JSON.stringify(r).slice(0, 300));
      r.list.forEach(x => ids.add(x));
      if (!r.has) break;
      if (!r.cursor || String(r.cursor) === String(cursor)) break;
      cursor = r.cursor;
      await sleep(600);
    }
    const items = JSON.parse(fs.readFileSync(DIR + '/items.json', 'utf8')).map(x => x.id);
    const missing = items.filter(x => !ids.has(x));
    console.log(JSON.stringify({ folder: f.name, remote_count: f.count, scanned: ids.size, expected: items.length, missing: missing.length, missing_sample: missing.slice(0, 5) }, null, 2));
    return;
  }

  console.log('unknown command');
}

main().then(() => process.exit(0)).catch(e => { console.log(JSON.stringify({ ok: false, error: String(e && e.message || e) })); process.exit(1); });
