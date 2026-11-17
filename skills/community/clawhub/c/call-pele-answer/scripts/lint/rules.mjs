// lint.mjs — STE-style prose check + routing check for call-pele-answer drafts.
// Zero dependencies. Rules: controlled-language sentence-shape rules, simplified technical
// Chinese limits, and "say less" rules.
// Hedges (可能/大约/约/may/might) are content, never flagged.

const HAN = /[\u3400-\u9fff\uf900-\ufaff]/g;
const KANA = /[\u3040-\u30ff]/;

export function normLang(tag) {
  const t = String(tag || '').toLowerCase();
  if (!t || t === 'auto') return null;
  if (t.startsWith('zh')) return 'zh';
  if (t.startsWith('en')) return 'en';
  if (t.startsWith('ja')) return 'ja';
  return 'neutral';
}

export function detectLang(text) {
  if (KANA.test(text)) return 'ja';
  const han = (text.match(HAN) || []).length;
  const latin = (text.match(/[A-Za-z]+/g) || []).length;
  if (han >= 4 && han >= latin / 2) return 'zh';
  if (latin > 0) return 'en';
  return 'neutral';
}

const LIMITS = {
  flavored: { zh: { step: 35, desc: 45 }, en: { step: 20, desc: 25 }, neutral: { step: 30, desc: 40 } },
  strict:   { zh: { step: 30, desc: 40 }, en: { step: 20, desc: 25 }, neutral: { step: 25, desc: 30 } },
};

const ZH_FILLER = ['赋能', '抓手', '闭环', '打通', '全方位', '多维度', '深度融合', '显著提升', '至关重要',
  '不可或缺', '综上所述', '总而言之', '众所周知', '毋庸置疑', '一站式', '底层逻辑', '颗粒度', '值得注意的是'];
const ZH_PREAMBLE = /^(下面(我)?(来|将)?(为你|给你)?(介绍|讲解|说明|解释)|接下来(我)?(会|将)|希望(这|以上|本文)?(对你|能)?有(所)?帮助|如有(任何)?问题)/;
const ZH_TYPO = { '登陆账号': '登录账号', '帐号': '账号', '阀值': '阈值', '布署': '部署', '其它': '其他' };
const ZH_UNIFY = { '单击': '点击', '点按': '点击', '键入': '输入', '缺省': '默认', '入参': '参数', '出参': '返回值' };
const ZH_VAGUE = { '尽快': '写出期限', '若干': '写出数量' };
const ZH_LIGHT = [/进行(?!中|时|了?一)[\u4e00-\u9fa5]{2}/g, /(?:加以|予以)[\u4e00-\u9fa5]{2}/g, /(?<![制创写])作出[\u4e00-\u9fa5]{2}/g, /做出(?!来)[\u4e00-\u9fa5]{2}/g];

const EN_PHRASAL = /\b(spin(?:ning|s)? up|spun up|reach(?:ing|es|ed)? out|div(?:e|es|ing|ed) into|kick(?:ing|s|ed)? off|circl(?:e|es|ing|ed) back)\b/gi;
const EN_MARKETING = /\b(seamless(?:ly)?|robust(?:ly)?|cutting-edge|effortless(?:ly)?|blazing[- ]fast|world-class|state-of-the-art|game-chang(?:ing|er)|powerful)\b/gi;
const EN_NOMINAL = /\b(perform|performs|performed|conduct|conducts|conducted|carry out|carried out)\s+(?:a|an|the)\s+\w+(?:tion|sion|ment|ance|ence|ysis)\b/gi;
const EN_FILLER = { 'in order to': 'to', 'utilize': 'use', 'prior to': 'before', 'in the event that': 'if', 'it is important to note that': '(delete)', 'here is an overview': '(start with the answer)' };
const EN_PASSIVE = /\b(is|are|was|were|be|been)\s+(\w+ed|done|given|taken|made|sent|set|run|kept|held|built)\b/gi;

// Remove spans that must not be checked. Quoted terms are meta-mentions: skip them.
export function stripSpans(s) {
  return s
    .replace(/`[^`]*`/g, ' ')
    .replace(/\$\$[^$]*\$\$|\$[^$\n]+\$/g, ' ')
    .replace(/~~.*?~~/g, ' ')
    .replace(/!\[[^\]]*\]\([^)]*\)/g, ' ')
    .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')
    .replace(/[“「『"]([^”」』"]{1,20})[”」』"]/g, '“”')
    .replace(/<[^>]+>/g, ' ')
    .replace(/\*\*?([^*]+)\*\*?/g, '$1');
}

function splitSentences(text) {
  // Split on CJK terminal punctuation, and on . ! ? followed by space/end.
  return text.split(/(?<=[。！？；!?])|(?<=[.](?=\s|$))/).map(s => s.trim()).filter(s => s.length > 1);
}

function sentenceLang(s, docLang) {
  if (docLang === 'ja') return 'ja';
  const han = (s.match(HAN) || []).length;
  if (han >= 4) return 'zh';
  if (docLang === 'neutral') return 'neutral';
  return /[A-Za-z]/.test(s) ? 'en' : 'neutral';
}

function measure(s, lang) {
  if (lang === 'zh' || lang === 'ja') return (s.match(HAN) || []).length + (s.match(/[\u3040-\u30ff]/g) || []).length;
  return (s.match(/[A-Za-z0-9'’-]+/g) || []).length;
}

// unit: { text, line, kind: 'step'|'desc', para: bool }
export function lintProse(units, { lang = 'zh', mode = 'flavored' } = {}) {
  const out = [];
  if (mode === 'off') return out;
  const L = LIMITS[mode] || LIMITS.flavored;
  for (const u of units) {
    const text = stripSpans(u.text);
    const sents = splitSentences(text);
    if (u.para && sents.length > 6) out.push([u.line, 'paragraph-length', `段落 ${sents.length} 句（上限 6）`, '拆段，或改成列表']);
    for (const s of sents) {
      const sl = sentenceLang(s, lang);
      const lim = (L[sl === 'ja' ? 'zh' : sl] || L.neutral)[u.kind];
      const n = measure(s, sl);
      if (n > lim) out.push([u.line, 'sentence-length', `${n}${sl === 'zh' || sl === 'ja' ? ' 字' : ' words'}（${u.kind === 'step' ? '步骤' : '描述'}上限 ${lim}）`, '一句只写一个事实，拆成两句']);
      if (sl === 'zh') {
        const de = (s.match(/的/g) || []).length;
        if (de >= 4) out.push([u.line, 'de-chain', `一句里有 ${de} 个“的”`, '拆句，或把修饰语改成独立短句']);
      }
    }
    const zhText = (text.match(HAN) || []).length >= 2;
    if ((lang === 'zh' || zhText) && lang !== 'ja') {
      for (const w of ZH_FILLER) if (text.includes(w)) out.push([u.line, 'filler', `“${w}”`, '换成具体事实或数字']);
      if (ZH_PREAMBLE.test(text.trim())) out.push([u.line, 'preamble', '开场白/客套结尾', '删掉，直接给结论']);
      for (const [b, g] of Object.entries(ZH_TYPO)) if (text.includes(b)) out.push([u.line, 'typo', `“${b}”`, `改为“${g}”`]);
      for (const [b, g] of Object.entries(ZH_VAGUE)) if (text.includes(b)) out.push([u.line, 'vague', `“${b}”`, g]);
      if (mode === 'strict') for (const [b, g] of Object.entries(ZH_UNIFY)) if (text.includes(b)) out.push([u.line, 'one-word-one-meaning', `“${b}”`, `统一用“${g}”`]);
      for (const rx of ZH_LIGHT) for (const m of text.matchAll(rx)) out.push([u.line, 'light-verb', `“${m[0]}”`, '直接用动词']);
      if (/(?<![相平对同均])等[。.]?\s*$/.test(text) && u.kind !== 'step') out.push([u.line, 'open-list', '列表以“等”结尾', '列全，或写出完整清单在哪里']);
    }
    if (lang === 'en' || /[A-Za-z]{3,}/.test(text)) {
      for (const rx of [EN_PHRASAL, EN_MARKETING, EN_NOMINAL]) for (const m of text.matchAll(rx)) out.push([u.line, rx === EN_PHRASAL ? 'phrasal-verb' : rx === EN_MARKETING ? 'marketing-word' : 'nominalization', `'${m[0]}'`, rx === EN_NOMINAL ? 'use the verb' : 'use a plain verb or a measurement']);
      for (const [b, g] of Object.entries(EN_FILLER)) if (new RegExp(`\\b${b}\\b`, 'i').test(text)) out.push([u.line, 'filler', `'${b}'`, `use '${g}'`]);
      if (mode === 'strict' && text.includes(';')) out.push([u.line, 'semicolon', "';'", 'split into two sentences']);
      if (u.kind === 'step') for (const m of text.matchAll(EN_PASSIVE)) out.push([u.line, 'passive-voice', `'${m[0]}'`, 'say who does it (advisory)']);
      if (/\b(etc\.?|and so on)\s*$/i.test(text)) out.push([u.line, 'open-list', "list ends with 'etc.'", 'list every item']);
    }
  }
  return out;
}

const SEQ_ZH = /(首先|然后|接着|随后|之后|最后|第[一二三四五六七八九十]步)/g;
const SEQ_EN = /\b(first|then|next|after that|finally)\b/gi;
const COMPARE = /(相比|对比|而|vs\.?|versus|更(快|慢|便宜|贵|大|小))/g;

// panel: { title, line, prose: [units], blocks: [{type, line, src, nodes, edges}], tables: [{line, cols}] }
export function lintRouting(doc) {
  const out = [];
  const { panels, lead } = doc;
  if (!lead || !lead.trim()) out.push([1, 'route/no-lead', '缺开头结论句', '在第一个 ## 前写 1–2 句核心结论']);
  if (panels.length > 8) out.push([panels[8].line, 'route/too-many', `${panels.length} 个块（上限 8）`, '拆成两页，或删掉不影响结论的块']);
  const visual = panels.some(p => p.blocks.some(b => b.type !== 'callout' && b.type !== 'code') || p.tables.length);
  if (panels.length <= 2 && !visual) out.push([1, 'route/text-is-enough', '全页只有文字，没有图表/交互', '直接用文字回答，不出页面']);
  for (const p of panels) {
    const prose = p.prose.map(u => u.text).join('\n');
    const seq = (prose.match(SEQ_ZH) || []).length + (prose.match(SEQ_EN) || []).length;
    const hasVis = p.blocks.some(b => !['callout', 'code'].includes(b.type));
    if (seq >= 3 && !hasVis) out.push([p.line, 'route/sequence-in-prose', `「${p.title}」用 ${seq} 个顺序词描述流程`, '改成 flowchart / sequenceDiagram，或 steps 分步']);
    const cmp = (prose.match(COMPARE) || []).length;
    if (cmp >= 3 && !p.tables.length && !hasVis) out.push([p.line, 'route/compare-in-prose', `「${p.title}」在正文里做了 ${cmp} 处比较`, '改成表格：行是选项，列是维度']);
    if (prose.length > 600 && !hasVis && !p.tables.length) out.push([p.line, 'route/wall', `「${p.title}」超过 600 字纯文字`, '拆块，或给关系/流程配图']);
    for (const t of p.tables) if (t.cols < 3 && t.rows > 0 && t.rows <= 6) out.push([t.line, 'route/thin-table', `${t.cols} 列表格`, '两列且行少：写成句子或 kv 列表']);
    for (const b of p.blocks) {
      if (b.type === 'mermaid' && /^(xychart|pie|sankey|radar|quadrantChart|treemap)/.test(b.kind || '') && !/(来源|数据源|示意|source|illustrative)/i.test(prose + b.src)) out.push([b.line, 'route/data-source', '数据图没有来源或“示意”标注', '写出数据来源；模拟数据标“示意”']);
    }
  }
  return out;
}
