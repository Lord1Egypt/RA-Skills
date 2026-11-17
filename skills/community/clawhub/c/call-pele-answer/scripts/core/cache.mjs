// cache.mjs — block-level routing cache. A System One answer depends only on (adapter, questions, block
// text), so an unchanged block is never sent twice: re-rendering after an edit only pays for the blocks
// that changed. Stored next to the logs (PE_CACHE=0 turns it off). Capped, oldest dropped first.
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { createHash } from 'node:crypto';
import { LOG_DIR } from './trace.mjs';
export const CACHE = process.env.PE_CACHE_FILE || join(LOG_DIR, '..', 'cache', 'route.json');
const MAX = 5000;
const h = s => createHash('sha1').update(s).digest('hex').slice(0, 20);

export function withCache(adapter, trace) {
  if (process.env.PE_CACHE === '0' || adapter.__cached) return adapter;
  const inner = adapter.ask.bind(adapter);
  return Object.assign(Object.create(adapter), { __cached: true, async ask(states, questions) {
    let db = {}; try { db = JSON.parse(readFileSync(CACHE, 'utf8')); } catch {}
    const qh = h(JSON.stringify(questions));
    const keys = states.map(s => `${adapter.name}:${qh}:${h(s)}`);
    const miss = keys.map((k, i) => (db[k] ? -1 : i)).filter(i => i >= 0);
    trace?.count('cache_hit', states.length - miss.length); trace?.count('cache_miss', miss.length);
    let model = Object.values(db).find(v => v.a && keys.includes(v.k))?.m;
    if (miss.length) {
      const got = await trace.span(`net:${adapter.name}`, () => inner(miss.map(i => states[i]), questions));
      model = got.model || model;
      miss.forEach((i, j) => { db[keys[i]] = { k: keys[i], a: got[j], m: got.model, t: Date.now() }; });
      const all = Object.entries(db); if (all.length > MAX) db = Object.fromEntries(all.sort((a, b) => a[1].t - b[1].t).slice(-MAX));
      try { mkdirSync(dirname(CACHE), { recursive: true }); writeFileSync(CACHE, JSON.stringify(db)); } catch {}
    }
    return Object.assign(keys.map(k => db[k].a), { model: model || keys.map(k => db[k].m).find(Boolean) });
  } });
}
