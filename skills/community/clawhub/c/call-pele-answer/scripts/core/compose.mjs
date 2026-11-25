// compose.mjs — from routed blocks to a page that is "alive":
//  1. compose()  picks the whole page's combination, not each block in isolation: a classifier's
//                probabilities are the base score, then page-level penalties (repetition, interaction
//                budget, device, over-escalation) decide.
//  2. derive()   turns a block into a form deterministically when the shape is simple enough
//                (dated events, number pairs, linear steps, state transitions). Deriver plugins can add more.
//  3. scaffold() writes the draft: when several forms can be derived for one block, the block becomes a
//                ```views fence, so the reader can switch between representations of the same content.
import { TYPES } from '../routers/catalog.mjs';
import { STRUCTURAL } from '../routers/engine.mjs';

export const DEFAULT_POLICY = {
  device: 'desktop',
  minScore: 0.15,            // a family below this probability is not a candidate
  promote: 0.55,             // a prose block is only upgraded when the router was at least this sure
  promoteStructure: 0.45,    // …or this sure, for a structural picture (hierarchy, structure, state, sequence, landscape, grammar)
  bonus: { structure: 0.1 }, // a structural family gains this when the block lists 3+ items: the picture shows the shape prose hides
  maxViews: 3,               // representations offered per block, original text included
  budget: { interactive: 2 },// slider / tabs / steps per page
  penalty: { repeat: 0.15, overBudget: 0.5, short: 0.45, mobileWide: 0.1 },
};
const INTERACTIVE = new Set(['slider', 'tabs', 'steps']);
const WIDE = new Set(['structure', 'tabs', 'table']);

const listy = t => (t.match(/[、；;]|\n\s*[-*\d]/g) || []).length + 1;
export function compose(blocks, policy = {}) {
  const P = { ...DEFAULT_POLICY, ...policy, budget: { ...DEFAULT_POLICY.budget, ...policy.budget }, penalty: { ...DEFAULT_POLICY.penalty, ...policy.penalty }, bonus: { ...DEFAULT_POLICY.bonus, ...policy.bonus } };
  let prev = null, interactive = 0;
  for (const b of blocks) {
    const scores = b.scores && Object.keys(b.scores).length ? { ...b.scores } : { [b.family]: b.confidence };
    if (b.gated) { for (const k of Object.keys(scores)) if (k !== b.family) scores[k] = Math.min(scores[k], 0.1); scores[b.family] = Math.max(scores[b.family] || 0, 0.9); }
    const cands = Object.entries(scores).filter(([f, s]) => s >= P.minScore && f !== 'prose');
    const ranked = cands.map(([f, s]) => {
      let v = s; const why = [];
      if (f === prev) { v -= P.penalty.repeat; why.push('与上一块同形式'); }
      if (INTERACTIVE.has(f) && interactive >= P.budget.interactive) { v -= P.penalty.overBudget; why.push('交互预算已满'); }
      if (b.text.length < 40) { v -= P.penalty.short; why.push('一句话能说清'); }
      if (P.device === 'mobile' && WIDE.has(f)) { v -= P.penalty.mobileWide; why.push('窄屏'); }
      if (STRUCTURAL.has(f) && listy(b.text) >= 3) v += P.bonus.structure;
      return { family: f, score: +v.toFixed(3), why };
    }).sort((x, y) => y.score - x.score);
    const best = ranked[0];
    // the composer may re-rank and demote, but it never promotes a block the router left as prose:
    // a non-prose pick must clear the router's own confidence bar (MIN_CONF) before penalties.
    const ok = best && best.score >= (STRUCTURAL.has(best.family) ? 0.45 : 0.5) && (b.family !== 'prose' || (scores[best.family] ?? 0) >= (STRUCTURAL.has(best.family) ? P.promoteStructure : P.promote));
    const pick = ok ? best.family : 'prose';
    const lost = ranked.find(r => r.family === b.family);
    if (pick !== b.family) b.recomposed = `${b.family} → ${pick}${lost?.why.length ? '（' + lost.why.join('、') + '）' : ''}`;
    if (pick !== b.family && TYPES[pick]) b.type = Object.keys(TYPES[pick])[0];
    b.family = pick;
    b.alternatives = ranked.filter(r => r.family !== pick && r.score >= 0.25).map(r => r.family);
    if (INTERACTIVE.has(pick)) interactive++;
    prev = pick;
  }
  return blocks;
}

// ---------- derivers ----------
const q = s => `"${String(s).replace(/"/g, "'").trim()}"`;
const clean = s => String(s).replace(/^[，,。；;：:\s]+|[，,。；;：:\s]+$/g, '').trim();
const isList = t => /^\s*(\d+[.)]|[-*+])\s+\S/m.test(t);
const id = s => s.replace(/[^\w\u4e00-\u9fa5]/g, '');

const extract = {
  events: t => [...t.matchAll(/((?:19|20)\d{2})\s*年?\s*(?:(\d{1,2})\s*月\s*(?:(\d{1,2})\s*日)?)?\s*([^，,。；;]+)/g)]
    .map(m => [m[2] ? `${m[1]}-${m[2].padStart(2, '0')}${m[3] ? '-' + m[3].padStart(2, '0') : ''}` : m[1], clean(m[4])]).filter(e => e[1]),
  pairs: t => [...t.matchAll(/([\u4e00-\u9fa5A-Za-z][\u4e00-\u9fa5A-Za-z0-9 ]{1,12}?)\s*[：:]?\s*(\d+(?:\.\d+)?)\s*(%|万|亿|元|个|次|ms|秒)?/g)]
    .map(m => [clean(m[1]).replace(/^(去年|今年)?(订单来源|销售额|占比|营收)?[：:]?/, '') || clean(m[1]), Number(m[2]), m[3] || '']),
  transitions(t) {
    const out = [...t.matchAll(/从\s*([^，,。；;变]+?)\s*(?:变成|变为|转为|进入)\s*([^，,。；;]+)/g)].map(m => [clean(m[1]), clean(m[2]), '']);
    for (const m of t.matchAll(/([\u4e00-\u9fa5]{2,6})(超时|失败|取消后?)则\s*([\u4e00-\u9fa5]{2,6})/g)) out.push([m[1], m[3], m[2]]);
    return out;
  },
  steps: t => /^\s*(\d+[.)]|[-*+])\s+\S/m.test(t) ? t.split('\n').filter(l => /^\s*(\d+[.)]|[-*+])\s+\S/.test(l)).map(l => clean(l.replace(/^\s*(\d+[.)]|[-*+])\s+/, '').replace(/`/g, '').split(/[，,；;：:（(]/)[0])) : t.split(/(?:首先|先|然后|再|接着|随后|最后|，|,|；|;|。)/).map(clean).filter(s => s.length >= 2),
};

// Each deriver: (block) → { label, md } | null. label names the view in the switcher.
export const DERIVERS = {
  timeline: [
    b => { const ev = extract.events(b.text); return ev.length >= 2 ? { label: '时间线', md: ['```mermaid', 'timeline', ...ev.map(([y, e]) => `  ${y} : ${e.replace(/:/g, '：')}`), '```'].join('\n') } : null; },
    b => { const ev = extract.events(b.text); return ev.length >= 2 ? { label: '表格', md: ['| 时间 | 事件 |', '|---|---|', ...ev.map(([y, e]) => `| ${y} | ${e} |`)].join('\n') } : null; },
  ],
  chart: [
    b => { const kv = extract.pairs(b.text); if (kv.length < 2 || kv.length > 8) return null;
      if ((kv.every(k => k[2] === '%') || b.type === 'pie') && kv.every(k => k[1] > 0)) return { label: '饼图', md: ['```mermaid', 'pie title 占比（来源：待补）', ...kv.map(([k, v]) => `  ${q(k)} : ${v}`), '```'].join('\n') };
      const max = Math.max(...kv.map(k => k[1]));
      return { label: b.type === 'line' ? '折线图' : '柱状图', md: ['```mermaid', 'xychart', '  title "对比（来源：待补）"', `  x-axis [${kv.map(k => q(k[0])).join(', ')}]`, `  y-axis "${kv[0][2] || '数值'}" 0 --> ${Math.ceil(max * 1.1)}`, `  ${b.type === 'line' ? 'line' : 'bar'} [${kv.map(k => k[1]).join(', ')}]`, '```'].join('\n') }; },
    b => { const kv = extract.pairs(b.text); return kv.length >= 2 && kv.length <= 12 ? { label: '表格', md: ['| 项 | 数值 |', '|---|---|', ...kv.map(([k, v, u]) => `| ${k} | ${v}${u} |`)].join('\n') } : null; },
  ],
  state: [
    b => { const tr = extract.transitions(b.text); return tr.length ? { label: '状态图', md: ['```mermaid', 'stateDiagram-v2', `  [*] --> ${id(tr[0][0])}`, ...tr.map(([a, c, ev]) => `  ${id(a)} --> ${id(c)}${ev ? ' : ' + ev : ''}`), '```'].join('\n') } : null; },
    b => { const tr = extract.transitions(b.text); return tr.length >= 2 ? { label: '转移表', md: ['| 从 | 到 | 触发 |', '|---|---|---|', ...tr.map(([a, c, ev]) => `| ${a} | ${c} | ${ev || '—'} |`)].join('\n') } : null; },
  ],
  steps: [
    // branches need judgment about which step leads where: those stay with the model's skeleton
    b => { const s = extract.steps(b.text); return s.length >= 3 && !isList(b.text) && !/(失败|否则|如果|成功|没有.{0,4}就)/.test(b.text) ? { label: '步骤', md: s.map((x, k) => `${k + 1}. ${x}`).join('\n') } : null; },
    b => { const s = extract.steps(b.text); return s.length >= 3 && s.length <= 8 && !/(失败|否则|如果|成功|没有.{0,4}就)/.test(b.text) ? { label: '流程图', md: ['```mermaid', 'flowchart LR', ...s.map((x, k) => `  S${k}[${q(x)}]`), '  ' + s.map((_, k) => `S${k}`).join(' --> '), '```'].join('\n') } : null; },
  ],
};

export function derive(b, derivers = DERIVERS) {
  const views = [];
  for (const fam of [b.family, ...(b.alternatives || [])]) for (const d of derivers[fam] || []) { const v = d(b); if (v && !views.some(x => x.label === v.label)) views.push(v); }
  return views;
}

// auto: the draft is rendered as-is (one-pass mode) — no TODO notes; blocks without a safe derivation stay prose.
export function scaffold({ title, lead, blocks, derivers = DERIVERS, policy = {}, auto = false, frontMatter = null }) {
  const maxViews = policy.maxViews ?? DEFAULT_POLICY.maxViews;
  const out = [...(frontMatter ? ['---', frontMatter, '---'] : ['---', `title: ${title || '解释'}`, '---']), lead || '（在这里写 1–2 句核心结论）', ''];
  blocks.forEach((b, i) => {
    const tag = [`${b.family}${b.type && b.family !== 'prose' ? '/' + b.type : ''} ${b.confidence.toFixed(2)}`, b.gated, b.recomposed].filter(Boolean).join(' · ');
    out.push(`## ${b.title || `块 ${i + 1}`}`); if (!auto) out.push(`<!-- route: ${tag} -->`);
    // a block the author already wrote in Pele form (fence or table) is kept verbatim: deriving from it
    // would read fence lines as prose and duplicate the content
    const authored = /^\s*(```|~~~)/m.test(b.text) || /^\s*\|.*\|\s*$/m.test(b.text);
    const views = b.family === 'prose' || authored ? [] : derive(b, derivers).slice(0, maxViews - 1);
    const safeText = b.text.replace(/-->/g, '→');
    // one-pass mode: a single derived view never sits next to the same text (that reads as duplication);
    // the reader switches between the component and the original instead
    if (views.length >= 2 || (auto && views.length === 1 && !['timeline', 'chart'].includes(b.family))) {
      out.push('```views', ...views.flatMap(v => [`=== ${v.label}`, v.md.replace(/```/g, '~~~')]), '=== 原文', b.text, '```', '');
    } else if (views.length === 1) {
      out.push(views[0].md, '', ['timeline', 'chart'].includes(b.family) ? `<!-- 原文：${safeText} -->` : b.text, '');
    } else {
      out.push(b.text, '');
      if (auto) { if (!authored && b.family !== 'prose' && b.family !== 'table') b.underived = true; return; }
      const skel = b.type && TYPES[b.family]?.[b.type]?.skel;
      if (b.family === 'table') out.push('<!-- TODO 改成表格：行 = 选项，列 = 维度，状态列写 ok/no/warn -->', '');
      else if (b.family === 'slider') out.push('<!-- TODO 改成 ```slider label="参数"，每个 @ 取值写结果 -->', '');
      else if (b.family === 'tabs') out.push('<!-- TODO 改成 ```tabs，每个 === 一个方案 -->', '');
      else if (skel) out.push(`<!-- TODO 按下面的图表骨架改写这块，删掉正文里重复的描述\n\`\`\`mermaid\n${skel}\n\`\`\`\n-->`, '');
    }
  });
  return out.join('\n');
}

// Input: a plain answer. ## sections become blocks; otherwise blank-line paragraphs do. The text before
// the first ## (or the first paragraph) is the lead and is never routed: the conclusion is always words.
export function splitAnswer(text) {
  const src = text.replace(/\r\n/g, '\n').replace(/^---\n[\s\S]*?\n---\n/, '');
  const titleM = text.match(/^title:\s*(.+)$/m);
  const frontMatter = text.replace(/\r\n/g, '\n').match(/^---\n([\s\S]*?)\n---\n/)?.[1] || null;
  if (/^##\s/m.test(src)) {
    const [head, ...secs] = src.split(/^##\s+/m);
    return { title: titleM?.[1], frontMatter, lead: head.trim(), blocks: secs.map(s => { const [t, ...b] = s.split('\n'); return { title: t.trim(), text: b.join('\n').trim() }; }).filter(b => b.text) };
  }
  const paras = src.split(/\n\s*\n/).map(s => s.trim()).filter(Boolean);
  return { title: titleM?.[1], frontMatter, lead: paras[0] || '', blocks: paras.slice(1).map(p => ({ title: null, text: p })) };
}
