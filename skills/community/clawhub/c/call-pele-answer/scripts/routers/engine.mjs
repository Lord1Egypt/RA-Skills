// engine.mjs — routing strategies. A strategy decides WHAT to ask about each block; a System One
// adapter (systemone.mjs) decides WHO answers. Strategies:
//   fast    family + diagram type, one question set, no gates          (good on a batch adapter)
//   full    fast + gates: real numbers? source? branches? alternatives? complexity  (confidence-gated routing)
//   hybrid  fast on one adapter, then full only for blocks where a wrong form costs most
//   local   keyword rules, offline
import { FAMILIES, TYPES } from './catalog.mjs';
export const MIN_CONF = 0.55;
// Families whose picture carries structure that prose hides (nesting, links, positions). They clear a lower bar.
export const STRUCTURAL = new Set(['hierarchy', 'structure', 'state', 'sequence', 'landscape', 'grammar']);
export const MIN_CONF_STRUCT = 0.45;

const CUES = {
  timeline: [/(19|20)\d{2}\s*年?/g, /\b(19|20)\d{2}\b/g, /(版本|里程碑|历史|发布|上线)/g],
  chart: [/\d+(\.\d+)?\s*%/g, /(占比|份额|增长|下降|销售额|同比|环比|万元|亿元)/g],
  sequence: [/(发送|返回|回复|请求|响应|回|发)\s*(给)?/g, /\b(SYN|ACK|request|response|reply)\b/gi],
  state: [/(状态|变成|变为|转为|进入|超时则|生命周期|待办|进行中|已完成|看板)/g],
  steps: [/(首先|先|然后|再|接着|随后|最后|第[一二三四五六七八九十]步|如果|否则|失败就|成功则)/g],
  hierarchy: [/(目录|分为|包括|包含|层级|子类|分类|放源码|文件夹|大类|小类|分支|几类|几种|几个方面|方面|维度|要素|一是|二是|三是|分别是|主要有|涵盖|知识点|体系)/g, /[：:][^。；\n]*、[^。；\n]*、/g],
  structure: [/(架构|组件|模块|服务|依赖|调用|数据库|网关|表|字段|外部系统|用例|角色|参与者|需求|验收|满足|事件溯源|读模型|CQRS|字节|比特|报文|协议头)/gi, /(角色|管理员|客服|顾客|访客|用户).{0,6}可以/g],
  table: [/(对比|比较|相比|区别|优缺点|vs\.?|方面)/gi],
  slider: [/(调到|调大|调小|增大|减小|越大|越小|取值|参数)/g],
  tabs: [/(方案[一二三ABC]|选项[一二三ABC]|做法[一二三])/g],
  landscape: [/(价值链|演进|成熟度|商品化|定制|Wardley|沃德利|Cynefin|混沌|繁杂|复杂域|清晰域|可预测)/gi],
  grammar: [/(语法|文法|BNF|EBNF|正则|产生式|格式为|关键字|标识符|token)/gi],
};
function classifyLocal(text) {
  const scores = {};
  for (const [fam, rxs] of Object.entries(CUES)) scores[fam] = rxs.reduce((n, rx) => n + (text.match(rx) || []).length, 0);
  const best = Object.entries(scores).sort((a, b) => b[1] - a[1])[0];
  const total = Object.values(scores).reduce((a, b) => a + b, 0);
  if (!best || best[1] < 2) return { label: 'prose', confidence: 0.6 };
  const second = Object.values(scores).sort((a, b) => b - a)[1] || 0;
  return { label: best[0], confidence: Math.min(0.9, 0.5 + 0.1 * (best[1] - second) + 0.05 * best[1]) };
}
const LOCAL_TYPE = {
  steps: t => (/(如果|否则|失败|成功|是否|\?|？)/.test(t) ? 'flowchart' : 'numbered'),
  structure: t => (/(字节|比特|报文|协议头|\bbit)/i.test(t) ? 'packet' : /(事件溯源|读模型|CQRS)/i.test(t) ? 'eventmodeling' : /(用例|参与者|哪些角色|(角色|管理员|客服|顾客|访客).{0,6}(能|可以))/.test(t) ? 'usecase' : /(需求|验收)/.test(t) && /(满足|验证|测试)/.test(t) ? 'requirement' : /(外部系统|系统上下文|C4)/.test(t) ? 'c4' : /(表|字段|主键|外键)/.test(t) ? 'erDiagram' : 'flowchart'),
  hierarchy: t => (/(目录|文件|src|\.js|\.md)/.test(t) ? 'treeView' : /(原因|导致|为什么)/.test(t) ? 'ishikawa' : /\d+\s*(%|万|亿|元)/.test(t) ? 'treemap' : 'mindmap'),
  landscape: t => (/(Cynefin|混沌|繁杂|复杂域|清晰域|可预测)/i.test(t) ? 'cynefin' : 'wardley'),
  grammar: () => 'railroad',
  timeline: t => (/(天|周|任务|排期)/.test(t) && !/(19|20)\d{2}/.test(t) ? 'gantt' : 'timeline'),
  chart: t => (/%/.test(t) ? 'pie' : /(月|年|季度)/.test(t) ? 'line' : 'bar'),
  state: t => (/(看板|待办|进行中)/.test(t) && !/(变成|变为|转为|超时)/.test(t) ? 'kanban' : 'stateDiagram'), sequence: () => 'sequenceDiagram',
};


export function questions(level = 'full') {
  const q = { family: { type: 'choice', instructions: 'Best visual form to explain this block of an answer', criteria: { ...FAMILIES } } };
  for (const [fam, types] of Object.entries(TYPES)) {
    const names = Object.keys(types);
    if (names.length > 1) q[`${fam}_type`] = { type: 'choice', instructions: `If this block is ${fam}, which diagram type fits`, criteria: Object.fromEntries(names.map(n => [n, types[n].desc])) };
  }
  if (level === 'fast') return q;
  q.has_real_numbers = { type: 'noul', instructions: 'The text states concrete numeric values' };
  q.cites_source = { type: 'noul', instructions: 'The text names where its numbers come from' };
  q.has_branches = { type: 'noul', instructions: 'The text describes a condition or branch, such as if/else or success/failure' };
  q.alternatives = { type: 'noul', instructions: 'The text lays out two or more named alternative approaches or options, each with its own details' };
  q.complexity = { type: 'score', instructions: 'How hard this block is to follow as plain text', criteria: ['one simple idea', 'a few linked ideas', 'many linked parts'] };
  return q;
}

// Gates turn System One signals into routing decisions (confidence-gated routing).
function gate(b, s) {
  if (!s) return b;
  b.signals = { numbers: s.has_real_numbers?.noul, source: s.cites_source?.noul, branches: s.has_branches?.noul, complexity: s.complexity?.score };
  if (b.family === 'prose' && (s.alternatives?.noul ?? 0) > 0.7 && b.text.length > 60) { b.family = 'tabs'; b.gated = '多个备选方案 → 标签页'; }
  if (b.family === 'chart' && (s.has_real_numbers?.noul ?? 1) < 0.5) { b.family = 'prose'; b.gated = '没有可用的真实数字，不画数据图'; }
  if (b.family === 'steps' && (s.has_branches?.noul ?? 0) < 0.5 && b.type !== 'swimlane') b.type = 'numbered';
  if (['steps', 'structure', 'hierarchy', 'state', 'landscape', 'grammar'].includes(b.family) && (s.complexity?.score ?? 2) < 0.4 && b.text.length < 60) { b.family = 'prose'; b.gated = '一句话能说清，不升级'; }
  return b;
}

const blank = texts => texts.map(text => ({ text, family: 'prose', confidence: 0, proposed: 'prose', type: null }));
function setFam(b, label, conf) { b.proposed = label; b.confidence = conf ?? 0; b.family = b.confidence >= (STRUCTURAL.has(label) ? MIN_CONF_STRUCT : MIN_CONF) ? label : 'prose'; }
const typeOf = (b, pick) => { if (!TYPES[b.family]) return null; const n = Object.keys(TYPES[b.family]); return n.length === 1 ? n[0] : pick(b.family) || LOCAL_TYPE[b.family]?.(b.text) || n[0]; };
function apply(b, a, { gates = true, refamily = true } = {}) {
  if (!a?.family) return;
  if (refamily) { setFam(b, a.family.choice, a.family.confidence); b.scores = a.family.probabilities || { [a.family.choice]: a.family.confidence }; }
  b.type = typeOf(b, f => a[`${f}_type`]?.choice);
  if (gates) gate(b, a);
}

export async function routeLocal(texts) {
  const blocks = blank(texts);
  blocks.forEach(b => { const r = classifyLocal(b.text); setFam(b, r.label, r.confidence); b.scores = { [r.label]: r.confidence }; b.type = typeOf(b, () => null); });
  return { blocks, by: 'local' };
}

export async function routeAsk(texts, adapter, level) {
  const blocks = blank(texts);
  const answers = await adapter.ask(texts, questions(level));
  answers.forEach((a, i) => apply(blocks[i], a, { gates: level === 'full' }));
  return { blocks, by: `${adapter.name}${answers.model ? '/' + answers.model : ''} · ${level}` };
}

export async function routeHybrid(texts, fastAdapter, gateAdapter) {
  const res = await routeAsk(texts, fastAdapter, 'fast');
  const { blocks } = res;
  const idx = blocks.map((_, i) => i).filter(i => ['chart', 'steps', 'slider', 'prose'].includes(blocks[i].family) || blocks[i].confidence < 0.8);
  if (idx.length) {
    try {
      const answers = await gateAdapter.ask(idx.map(i => texts[i]), questions('full'));
      answers.forEach((a, k) => { const b = blocks[idx[k]]; apply(b, a, { refamily: b.confidence < 0.8 }); });
      res.by += ` + ${gateAdapter.name} gates`;
    } catch (e) { res.note = `复核跳过（${e.message}）`; }
  }
  return res;
}
