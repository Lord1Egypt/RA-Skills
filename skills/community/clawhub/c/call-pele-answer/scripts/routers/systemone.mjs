// systemone.mjs — the System One adapter layer.
//
// A routing strategy only says WHAT to ask: typed questions (choice / score / noul) about each block.
// An adapter says WHO answers. Every adapter implements one batched call:
//
//     ask(states: string[], questions: Record<id, Question>) → Promise<Answers[]>   (one Answers per state)
//
// with answers in TypeSafe's System One shape: { [id]: { type, choice?, probabilities?, confidence?,
// score?, noul? } }. Two families of adapter exist:
//
//   native  speaks System One on the wire (state + questions, one call per state, questions evaluated in
//           parallel inside the call). TypeSafe direct, classifier.dev's /v1/systemone, a self-hosted proxy.
//   shim    emulates System One on a plain batch classifier (/v1/classify: many texts, one label set):
//           one call per QUESTION over all states. choice → labels; noul → yes/no; score → ordinal labels.
//
// So the same strategy runs on any of them, and a new provider is one adapter definition in config.

const sleep = ms => new Promise(r => setTimeout(r, ms));
export async function pool(items, n, fn) {
  const out = new Array(items.length); let k = 0;
  await Promise.all(Array.from({ length: Math.min(n, items.length) }, async () => { while (k < items.length) { const i = k++; out[i] = await fn(items[i], i); } }));
  return out;
}
async function post(url, body, { key, timeoutMs = 6000 } = {}) {
  const waits = [400, 900, 1600];
  for (let attempt = 0; attempt <= waits.length; attempt++) {
    const ac = new AbortController(); const timer = setTimeout(() => ac.abort(), timeoutMs);
    try {
      const res = await fetch(url, { method: 'POST', signal: ac.signal, headers: { 'content-type': 'application/json', ...(key ? { authorization: `Bearer ${key}` } : {}) }, body: JSON.stringify(body) });
      const json = await res.json().catch(() => ({}));
      if (res.status === 429 && attempt < waits.length) { await sleep(Number(res.headers.get('retry-after-ms')) || waits[attempt]); continue; }
      if (!res.ok) throw new Error(`${res.status} ${json.code || json.error?.code || ''} ${typeof json.error === 'string' ? json.error : ''}`.trim());
      return json;
    } catch (e) { if (e.name === 'AbortError') throw new Error(`timeout ${timeoutMs}ms`); throw e; }
    finally { clearTimeout(timer); }
  }
}
import { readKey as env, checkKeyEnv } from '../core/keys.mjs';
// A keyed request goes over https, or plain http only to this machine (self-hosted proxy, tests).
function checkUrl(url, keyEnv, who) {
  const u = new URL(url);
  const local = ['localhost', '127.0.0.1', '[::1]'].includes(u.hostname);
  if (u.protocol !== 'https:' && !(u.protocol === 'http:' && local)) throw new Error(`适配器 ${who} 的 url 必须是 https（或本机 http）：${url}`);
  checkKeyEnv(keyEnv, who);
}

// native: one System One call per state, `concurrency` at a time
export function nativeAdapter({ name, url, keyEnv = [], anonymousKey, concurrency = 4, keyedConcurrency = 16, model = 'jev-latest', describe }) {
  checkUrl(url, keyEnv, name);
  return {
    name, kind: 'native', describe,
    available: () => !!(env(keyEnv) || anonymousKey),
    async ask(states, questions) {
      const key = env(keyEnv) || anonymousKey;
      const n = env(keyEnv) ? keyedConcurrency : concurrency;
      const rs = await pool(states, n, s => post(url, { state: s, model, questions }, { key }));
      return Object.assign(rs.map(r => r.answers), { model: rs[0]?.model });
    },
  };
}

// shim: emulate System One on a batch classifier; one request per question, all states at once
export function shimAdapter({ name, url, keyEnv = [], concurrency = 4, keyedConcurrency = 16, describe }) {
  checkUrl(url, keyEnv, name);
  return {
    name, kind: 'shim', describe,
    available: () => true,
    async ask(states, questions) {
      const key = env(keyEnv);
      const ids = Object.keys(questions);
      let model = '';
      const per = await pool(ids, key ? keyedConcurrency : concurrency, async id => {
        const q = questions[id];
        let labels, instructions;
        if (q.type === 'choice') { labels = Object.keys(q.criteria); instructions = `${q.instructions}: ` + labels.map(l => `${l} = ${q.criteria[l]}`).join('; '); }
        else if (q.type === 'noul') { labels = ['yes', 'no']; instructions = `Is this true of the text? ${q.instructions}`; }
        else if (q.type === 'score') { labels = q.criteria.map((_, k) => String(k)); instructions = `${q.instructions}: ` + q.criteria.map((c, k) => `${k} = ${c}`).join('; '); }
        else return null;
        try {
          const r = await post(url, { inputs: states, labels, instructions }, { key });
          model ||= r.model;
          return r.results.map(x => {
            const p = x.scores || { [x.label]: x.confidence ?? 1 };
            if (q.type === 'choice') return { type: 'choice', choice: x.label, confidence: x.confidence ?? 0, probabilities: p };
            if (q.type === 'noul') return { type: 'noul', noul: p.yes ?? (x.label === 'yes' ? x.confidence : 1 - (x.confidence ?? 0)) };
            const sum = Object.values(p).reduce((a, b) => a + (b || 0), 0) || 1;
            return { type: 'score', score: Object.entries(p).reduce((a, [k, v]) => a + Number(k) * (v || 0), 0) / sum, confidence: x.confidence ?? 0, probabilities: p };
          });
        } catch (e) { if (id === ids[0]) throw e; return null; } // the first question is the one strategies depend on
      });
      return Object.assign(states.map((_, i) => Object.fromEntries(ids.map((id, k) => [id, per[k]?.[i]]).filter(([, v]) => v))), { model });
    },
  };
}

// Built-in adapters. Users add their own in config: { "adapters": [{ "name": "my-proxy", "kind": "native",
// "url": "https://…/v1/systemone", "keyEnv": ["PE_KEY_MY_PROXY"] }] } — user config only
export const BUILTIN_ADAPTERS = [
  nativeAdapter({ name: 'typesafe', url: 'https://api.typesafe.ai/v1/systemone', keyEnv: ['TYPESAFE_API_KEY'], describe: 'TypeSafe 直连 System One（需 TYPESAFE_API_KEY）' }),
  nativeAdapter({ name: 'classifier-systemone', url: 'https://classifier.dev/v1/systemone', keyEnv: ['CLASSIFIER_API_KEY', 'CLASSIFY_API_KEY'], anonymousKey: 'unused', keyedConcurrency: 4, describe: 'classifier.dev 转发的 System One（无 key 用 IP 免费额度，4 并发）' }),
  shimAdapter({ name: 'classifier', url: 'https://classifier.dev/v1/classify', keyEnv: ['CLASSIFIER_API_KEY', 'CLASSIFY_API_KEY'], describe: 'classifier.dev 批量分类，按问题批量模拟 System One（无 key 可用）' }),
];
