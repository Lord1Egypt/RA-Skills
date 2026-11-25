// tableshape.mjs — what an authored Markdown table really is, and what it should become.
//
// A table is only the right form for several items compared along the same, comparable attributes.
// Tables written for anything else (steps in order, rules placed along a pipeline, unrelated numbers,
// two or three options with long prose cells) get a suggested component instead. Used by admission
// (so a table in the draft is not its own evidence), by lint (table-heavy, thin-table) and by pe options.

const cellsOf = line => line.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map(c => c.trim());
const SEP = /^\s*\|?[\s:-]*-{3,}[\s:|-]*\|?\s*$/;

// All tables in a markdown text: [{ head, rows, line }]
export function tablesIn(text) {
  const lines = text.split('\n'), out = [];
  for (let i = 0; i + 1 < lines.length; i++) {
    if (!/^\s*\|.*\|\s*$/.test(lines[i]) || !SEP.test(lines[i + 1])) continue;
    const head = cellsOf(lines[i]), rows = []; let j = i + 2;
    while (j < lines.length && /^\s*\|.*\|\s*$/.test(lines[j])) rows.push(cellsOf(lines[j++]));
    out.push({ head, rows, line: i }); i = j - 1;
  }
  return out;
}

// Replace tables by the facts they hold, one list item per row, so admission judges content, not markup.
export function deformat(text) {
  const lines = text.split('\n'), out = [];
  for (let i = 0; i < lines.length; i++) {
    if (/^\s*\|.*\|\s*$/.test(lines[i]) && SEP.test(lines[i + 1] || '')) {
      const head = cellsOf(lines[i]); let j = i + 2;
      while (j < lines.length && /^\s*\|.*\|\s*$/.test(lines[j])) {
        const r = cellsOf(lines[j++]);
        out.push(`- ${r[0]}：${r.slice(1).map((c, k) => (head[k + 1] ? `${head[k + 1]} ${c}` : c)).join('，')}`);
      }
      i = j - 1; continue;
    }
    out.push(lines[i]);
  }
  return out.join('\n');
}

const plain = c => c.replace(/[*`_]/g, '').replace(/^(ok|no|warn)\s*/, '').trim();
const isNum = c => /^[~≈约<>≤≥+-]?\s*\d[\d,.]*\s*(%|ms|s|秒|分钟|小时|天|个|次|条|元|万|亿|KB|MB|GB|k|K|x|倍)?$/.test(plain(c));
const len = c => [...plain(c)].length;
const median = a => { const s = [...a].sort((x, y) => x - y); return s.length ? s[Math.floor(s.length / 2)] : 0; };

const STEP_HEAD = /^(步骤|阶段|顺序|序号|第几步|环节|时间|时刻|step|stage|phase|order|#)$/i;
const POS_HEAD = /(哪一步|在哪|位置|拦在|发生在|触发点|何时|时机|where|when)/i;
const STATE_HEAD = /(状态|变为|转到|下一状态|state|status|transition)/i;
const NUM_ONLY = /^(数字|指标|数值|关键数字|值|metric|value|number)s?$/i;

// { kind: 'comparison'|'sequence'|'placed'|'states'|'numbers'|'options'|'pairs', use: [components], why }
export function tableShape(t) {
  const { head, rows } = t; const cols = head.length;
  const body = rows.map(r => r.slice(1));
  const attrCells = body.flat();
  if (!rows.length) return { kind: 'pairs', use: [], why: '空表' };
  if (STEP_HEAD.test(plain(head[0])) || rows.every((r, k) => new RegExp(`^(第\\s*)?${k + 1}\\b|^${k + 1}[.、)]`).test(plain(r[0]))))
    return { kind: 'sequence', use: ['flowchart', 'steps'], why: '首列是先后顺序' };
  if (head.some(h => POS_HEAD.test(h))) return { kind: 'placed', use: ['sequenceDiagram', 'flowchart'], why: `「${head.find(h => POS_HEAD.test(h))}」列说明内容沿流程分布` };
  if (head.some(h => STATE_HEAD.test(h))) return { kind: 'states', use: ['stateDiagram'], why: '有状态或转移列' };
  if (cols === 2 && (NUM_ONLY.test(plain(head[1])) || body.flat().every(isNum)))
    return { kind: 'numbers', use: [], why: '两列且一列全是数字：多半是互不相干的数字，各归到所在的块' };
  if (rows.length <= 3 && median(attrCells.map(len)) > 24) return { kind: 'options', use: ['tabs'], why: `${rows.length} 个选项、单元格都很长` };
  const numericCols = head.slice(1).filter((_, k) => rows.filter(r => isNum(r[k + 1] || '')).length >= Math.max(3, rows.length * 0.8)).length;
  if (numericCols >= 1 && rows.length >= 3 && cols <= 3) return { kind: 'comparison', use: ['table', 'xychart'], why: '有一列可比的数字' };
  if (cols >= 3 && rows.length >= 2 && median(attrCells.map(len)) <= 16) return { kind: 'comparison', use: ['table'], why: `${rows.length} 项 × ${cols - 1} 个属性，值短且可比` };
  return { kind: 'pairs', use: [], why: cols < 3 ? '两列：写成句子或 kv 列表' : '单元格太长，不是横向对照：写成段落或 tabs' };
}

export const isComparison = t => tableShape(t).kind === 'comparison';
