// components.mjs — built-in components and their admission conditions.
//
// A component says what it is and WHEN it may be offered; it never says what it combines with.
// `pe options` / `pe answer` check every registered component against each block and hand the
// passing ones (with evidence) to the agent, which decides the combination and assembles it with
// `pe assemble`. A plugin adds a component the same way:
//
//   api.component({ name, desc, fence, skeleton, ask, min, requires })
//
//   name      what the agent writes in --use (and what usage stats count)
//   desc      one line for the agent: what it shows
//   fence     how it is written: 'mermaid' (skeleton is the diagram body), or a fence name (table, callout, steps…)
//   skeleton  a minimal body the agent replaces
//   ask       soft condition: a yes/no question System One (JEV) answers about the block text
//   min       JEV probability needed (generic shapes like mindmap need more)
//   requires  hard conditions the script checks first; all must pass, each returns evidence or null
import { TYPES } from '../routers/catalog.mjs';
import { tablesIn, tableShape } from './tableshape.mjs';

const count = (t, rx) => (t.match(rx) || []).length;
const num = t => count(t, /(?<![\w.])\d+(\.\d+)?\s*(%|ms|秒|分钟|小时|天|个|次|条|元|美元|万|亿|KB|MB|GB|k|K)?(?![\w.])/g);
// hard checks: return a short evidence string, or null
export const CHECKS = {
  numbers3: t => (num(t) >= 3 ? `${num(t)} 个数字` : null),
  percent2: t => { const n = new Set((t.match(/\d+(\.\d+)?\s*%/g) || []).map(x => x.replace(/\s/g, ''))).size; return n >= 2 ? `${n} 个不同的百分比` : null; },
  dated2: t => { const n = count(t, /\b(19|20)\d{2}\b|(19|20)\d{2}\s*年|\d{1,2}\s*月\s*\d{1,2}\s*日|\bv?\d+\.\d+(\.\d+)?\b/g); return n >= 2 ? `${n} 个日期或版本` : null; },
  paths: t => { const n = count(t, /[\w.-]+\/[\w./-]*|[\w-]+\.(m?js|ts|tsx|py|go|rs|md|json|ya?ml|toml|sh)\b/g); return n >= 3 ? `${n} 个路径或文件名` : null; },
  items3: t => { const rows = count(t, /^\s*\|.*\|\s*$/gm), li = count(t, /^\s*([-*]|\d+[.)])\s+/gm), sep = count(t, /[、；;]/g); const n = Math.max(rows ? rows - 2 : 0, li, sep + 1); return n >= 3 ? `${n} 项` : null; },
  actors2: t => (count(t, /(发送|返回|回复|请求|调用|响应|交给|转给|通知|send|return|call|request|respond|reply)/gi) >= 2 ? '有来回传递的动作' : null),
  states: t => (count(t, /(状态|变成|变为|转为|进入|超时|过期|生命周期|完成|失败|等待|pending|running|done|failed|expired|status|state)/gi) >= 2 ? '有状态词' : null),
  warning: t => (/(不要|别|务必|注意|必须|最多|至少|不会|从不|只能|上限|限制|never|must|only|at most|limit)/i.test(t) ? '有限制或提醒' : null),
  code: t => (/`[^`]+`|^\s*\$\s|\b(npm|node|git|pip|curl|npx|bash)\s/m.test(t) ? '有代码或命令' : null),
  branching: t => (/(如果|否则|失败|成功|是否|若|则|if|else|otherwise|unless|fail)/i.test(t) ? '有条件分支' : null),
  param: t => (/(越大|越小|调大|调小|增大|减小|取值|参数|阈值|larger|smaller|threshold|parameter)/i.test(t) && num(t) >= 2 ? '有可调参数和取值' : null),
  // several items along the same comparable attributes. An authored table counts only when its shape is a
  // real comparison (tableshape.mjs); otherwise ≥3 list items each carrying ≥2 attribute values.
  grid: (t, raw = t) => {
    const ts = tablesIn(raw);
    if (ts.length) { const sh = ts.map(tableShape); const ok = sh.find(x => x.kind === 'comparison'); return ok ? ok.why : null; }
    const items = (t.match(/^\s*([-*]|\d+[.)])\s+.+$/gm) || []).filter(l => (l.match(/[，,；;：:]/g) || []).length >= 2);
    return items.length >= 3 ? `${items.length} 项各带 ≥2 个属性` : null;
  },
  kw: rx => t => (rx.test(t) ? `提到「${(t.match(rx) || [''])[0]}」` : null),
};
const kw = CHECKS.kw;

const sk = (fam, type) => TYPES[fam][type].skel;
const m = (name, fam, type, ask, min = 0.8, requires = []) => ({ name, fence: 'mermaid', desc: TYPES[fam][type].desc, skeleton: sk(fam, type), ask: `The text itself contains ${ask || TYPES[fam][type].desc}`, min, requires });

export const BUILTIN_COMPONENTS = [
  { name: 'flowchart', fence: 'mermaid', desc: 'steps with decisions, or parts of a system connected by arrows', skeleton: sk('steps', 'flowchart'), ask: 'The text itself describes ordered steps with a decision, or parts of a system and how they connect', min: 0.8, requires: [] },
  m('swimlane', 'steps', 'swimlane', 'steps handed off between several named people, teams or roles', 0.9, ['items3']),
  m('agentflow', 'steps', 'agentflow', 'an AI agent or tool-calling workflow with inputs, tools and outputs', 0.9, [kw(/(agent|tool|工具|模型|LLM|MCP|调用)/i)]),
  m('sequenceDiagram', 'sequence', 'sequenceDiagram', 'two or more named actors passing requests, messages or results to each other in time order', 0.8, ['actors2']),
  m('stateDiagram', 'state', 'stateDiagram', 'one thing moving through named states or a lifecycle', 0.8, ['states']),
  m('journey', 'state', 'journey', 'a person moving through stages with a feeling or score at each', 0.9, [kw(/(体验|感受|满意|用户旅程|journey|feel)/i)]),
  m('kanban', 'state', 'kanban', 'work items grouped into columns by status', 0.9, ['items3', kw(/(待办|进行中|已完成|todo|doing|done|看板)/i)]),
  m('architecture', 'structure', 'architecture', 'infrastructure services such as servers, databases or queues grouped into boundaries', 0.9, [kw(/(服务器|数据库|队列|缓存|云|server|database|queue|cache|cloud|bucket|存储)/i)]),
  m('erDiagram', 'structure', 'erDiagram', '', 0.85, [kw(/(字段|主键|外键|数据表|实体|field|primary key|foreign key|entity|schema)/i)]),
  m('classDiagram', 'structure', 'classDiagram', '', 0.85, [kw(/(类|继承|接口|方法|class|interface|inherit|extends|method)/i)]),
  m('block', 'structure', 'block', 'modules laid out in rows and columns', 0.95, ['items3']),
  m('c4', 'structure', 'c4', 'one system with the people who use it and the external systems it talks to', 0.9, ['items3']),
  m('usecase', 'structure', 'usecase', 'roles and which actions each role can do', 0.9, [kw(/(角色|管理员|访客|权限|role|admin|permission)/i)]),
  m('requirement', 'structure', 'requirement', 'requirements and which parts satisfy or verify them', 0.95, [kw(/(需求|验收|满足|requirement|verify|satisf)/i)]),
  m('eventmodeling', 'structure', 'eventmodeling', '', 0.9, [kw(/(事件|命令|读模型|event|command|read model|CQRS)/i)]),
  m('packet', 'structure', 'packet', '', 0.85, [kw(/(字节|比特|报文|协议头|byte|bit|header|offset)/i)]),
  m('mindmap', 'hierarchy', 'mindmap', 'one topic broken into named sub-topics and their sub-points', 0.95, ['items3']),
  m('treeView', 'hierarchy', 'treeView', '', 0.8, ['paths']),
  m('treemap', 'hierarchy', 'treemap', '', 0.85, ['numbers3', 'items3']),
  m('ishikawa', 'hierarchy', 'ishikawa', '', 0.85, [kw(/(原因|导致|根因|为什么|cause|because|root)/i)]),
  m('timeline', 'timeline', 'timeline', '', 0.8, ['dated2']),
  m('gantt', 'timeline', 'gantt', '', 0.85, ['items3', kw(/(\d+\s*(天|周|月|days?|weeks?)|排期|工期|截止|deadline|schedule)/i)]),
  m('gitGraph', 'timeline', 'gitGraph', '', 0.85, [kw(/(分支|合并|提交|branch|merge|commit|rebase)/i)]),
  m('pie', 'chart', 'pie', '', 0.8, ['percent2']),
  m('bar', 'chart', 'bar', 'amounts of the same measure compared across three or more categories', 0.8, ['numbers3']),
  m('line', 'chart', 'line', 'values of one measure changing over time', 0.85, ['numbers3', 'dated2']),
  m('sankey', 'chart', 'sankey', '', 0.85, ['numbers3', kw(/(流向|流入|流出|分配|来源|去向|flow|from .* to)/i)]),
  m('radar', 'chart', 'radar', 'several items each given a score on several criteria', 0.85, ['numbers3']),
  m('quadrant', 'chart', 'quadrant', 'items rated on two numeric axes to show a trade-off', 0.9, ['numbers3']),
  m('venn', 'chart', 'venn', 'two or three sets and what they share', 0.85, [kw(/(交集|重叠|共同|都有|同时|overlap|both|intersection|shared)/i)]),
  m('wardley', 'landscape', 'wardley', '', 0.85, [kw(/(演进|成熟度|商品化|定制|evolution|commodity|genesis|Wardley)/i)]),
  m('cynefin', 'landscape', 'cynefin', '', 0.85, [kw(/(Cynefin|混沌|繁杂|复杂域|清晰域|chaotic|complicated|complex domain)/i)]),
  m('railroad', 'grammar', 'railroad', '', 0.85, [kw(/(语法|文法|BNF|产生式|格式为|syntax|grammar|token)/i)]),
  { name: 'table', fence: 'table', desc: 'several items compared along the same attributes', skeleton: '| 项 | 属性一 | 属性二 |\n|---|---|---|\n| 甲 | … | … |\n| 乙 | … | … |\n| 丙 | … | … |', ask: 'The text itself compares two or more items along the same attributes, with at least two attributes and six or more cells of facts (not steps in order, not rules placed along a process, not unrelated numbers)', min: 0.8, requires: ['grid'] },
  { name: 'callout', fence: 'callout', desc: 'one warning, hard limit or key takeaway the reader must not miss', skeleton: '一句必须记住的限制或结论。', ask: 'The text itself contains one warning, hard limit or key takeaway the reader must not miss', min: 0.7, requires: ['warning'] },
  { name: 'steps', fence: 'steps', desc: 'a click-through walkthrough, one beat at a time', skeleton: '第一拍：一两句旁白\n---\n第二拍：只变一样东西\n---\n第三拍：…', ask: 'The text itself describes a process that is easier to follow one step at a time', min: 0.85, requires: ['items3'] },
  { name: 'tabs', fence: 'tabs', desc: 'two to five alternative approaches, one per tab', skeleton: '=== 方案 A\n…\n=== 方案 B\n…', ask: 'The text itself lays out two or more named alternative approaches, each with its own details', min: 0.85, requires: [] },
  { name: 'slider', fence: 'slider', desc: 'drag one parameter and see the result change', skeleton: '@ 低\n这个取值下的结果\n@ 中\n…\n@ 高\n…', ask: 'The text itself explains how a result changes when one parameter is made larger or smaller', min: 0.85, requires: ['param'] },
  { name: 'code', fence: 'code', desc: 'a command, code or config snippet', skeleton: '# 真实命令或代码', ask: 'The text itself contains a command, code snippet or config the reader would run or copy', min: 0.7, requires: ['code'] },
];

export default {
  name: 'builtin-components', apiVersion: 1,
  setup(api) { for (const c of BUILTIN_COMPONENTS) api.component(c); },
};
