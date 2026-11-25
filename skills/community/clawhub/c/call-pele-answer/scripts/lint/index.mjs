// Built-in lint rules over the IR. A rule is { id, check(doc, report, ctx) }; plugins add domain rules
// (e.g. "every number in a finance page cites a source") the same way.
import { walk } from '../core/markdown.mjs';
import { lintProse, lintRouting, normLang, detectLang } from './rules.mjs';
import { tableShape } from '../core/tableshape.mjs';

export function proseUnits(nodes) {
  const units = [];
  walk(nodes, n => {
    if (n.quiet) return;
    if (n.kind === 'p') units.push({ text: n.text, line: n.line, kind: 'desc', para: true });
    else if (n.kind === 'quote') units.push({ text: n.text, line: n.line, kind: 'desc', para: true });
    else if (n.kind === 'list') n.items.forEach(it => units.push({ text: it.text, line: it.line, kind: n.ordered ? 'step' : 'desc' }));
    else if (n.kind === 'table') n.rows.forEach((r, k) => { if (!r.some(c => /^no(\s|$)/.test(c))) r.forEach(c => units.push({ text: c.replace(/^(ok|warn)\s*/, ''), line: n.line + 2 + k, kind: 'desc' })); });
  });
  return units;
}
export const docLang = doc => normLang(doc.meta.lang) || detectLang([...proseUnits(doc.lead), ...doc.panels.flatMap(p => proseUnits(p.nodes))].map(u => u.text).join('\n'));

export default {
  name: 'builtin-rules', apiVersion: 1,
  setup(api) {
    api.rule({
      id: 'ste', describe: 'STE 风格文字：句长、段长、“的”链、轻动词、空话、开场白…（语气词不查）',
      check(doc, report, ctx) {
        const lang = docLang(doc);
        const units = [...proseUnits(doc.lead), ...doc.panels.flatMap(p => proseUnits(p.nodes))];
        for (const f of lintProse(units, { lang, mode: ctx.ste || doc.meta.ste || 'flavored' })) report(...f);
      },
    });
    api.rule({
      id: 'route', describe: '形式选择：缺结论、文字墙、正文写流程/比较、两列表格、数据图无来源…',
      check(doc, report) {
        const legacy = {
          lead: doc.lead.map(n => n.text || '').join('\n'),
          panels: doc.panels.map(p => {
            const fences = []; walk(p.nodes, n => { if (n.kind === 'fence') fences.push({ type: n.form || 'code', line: n.line, edges: n.data?.edges || 0, kind: n.data?.kind, src: n.data?.src || '' }); });
            return { title: p.title, line: p.line, prose: proseUnits(p.nodes), tables: p.nodes.filter(n => n.kind === 'table').map(t => ({ line: t.line, cols: t.head.length, rows: t.rows.length, shape: tableShape(t) })), blocks: fences };
          }),
        };
        for (const f of lintRouting(legacy)) report(...f);
      },
    });
    api.rule({
      id: 'tables', describe: '整页以表格为主（只有表格的块 >1 且没有 pe:use 标记就不出页）、表格形状不是横向对照、同一数字在多块重复',
      check(doc, report, ctx) {
        const marked = new Set();
        for (const part of (ctx.draft || '').split(/^(?=##\s)/m)) { const t = part.match(/^##\s+(.*)$/m)?.[1].trim(); if (t && /<!--\s*pe:use\s+[^>]*\btable\b/.test(part)) marked.add(t); }
        const visualOf = nodes => { let v = false; walk(nodes, n => { if (n.kind === 'fence' && n.form && !['callout', 'code', 'views', 'tabs'].includes(n.form)) v = true; }); return v; };
        const tablesOf = nodes => { const ts = []; walk(nodes, n => { if (n.kind === 'table') ts.push(n); }); return ts; };
        const only = doc.panels.filter(p => tablesOf(p.nodes).length && !visualOf(p.nodes));
        const unmarked = only.filter(p => !marked.has(p.title));
        if (only.length > 1 && unmarked.length) {
          const hint = unmarked.map(p => { const sh = tablesOf(p.nodes).map(tableShape); const s = sh.find(x => x.kind !== 'comparison' && x.use.length) || sh.find(x => x.kind !== 'comparison') || sh[0]; return s.kind === 'comparison' ? `「${p.title}」是真对照（${s.why}），保留就加标记` : `「${p.title}」${s.why}${s.use.length ? '，可改 ' + s.use.join('/') : ''}`; }).join('；');
          ctx.error(unmarked[0].line, 'route/table-heavy', `${only.length} 块只有表格：${hint}`, '先跑 pe options 看每块的候选和“接近门槛”，用 pe assemble 换成别的组件；真要保留表格，就用 pe assemble --use table（会留下 <!-- pe:use table --> 标记）');
        }
        for (const p of doc.panels) for (const t of tablesOf(p.nodes)) {
          const sh = tableShape(t);
          if (sh.kind === 'numbers') report(t.line, 'route/number-table', `「${p.title}」把互不相干的数字拼成一张表`, '每个数字放回讲它的那块，一个事实只写一次');
          else if (['sequence', 'placed', 'states', 'options'].includes(sh.kind) && t.head.length >= 3) report(t.line, 'route/table-shape', `「${p.title}」的表格${sh.why}，不是横向对照`, `改用 ${sh.use.join(' / ')}（pe assemble --use ${sh.use[0]}）`);
        }
        // the same number with a unit in two blocks: a fact written twice
        const NUM = /(?<![\w.])\d+(?:\.\d+)?\s*(?:%|ms|秒|分钟|小时|天|次|条|元|美元|万|亿|KB|MB|GB|倍)(?![\w])/g;
        const textOf = nodes => { let t = ''; walk(nodes, n => { if (n.kind === 'fence' && n.form === 'code') return; if (n.text) t += n.text + '\n'; if (n.kind === 'table') t += [n.head, ...n.rows].flat().join(' ') + '\n'; }); return t; };
        const where = new Map();
        doc.panels.forEach(p => { for (const m of new Set((textOf(p.nodes).match(NUM) || []).map(x => x.replace(/\s/g, '')))) where.set(m, [...(where.get(m) || []), p]); });
        const dup = [...where].filter(([, ps]) => ps.length >= 2);
        if (dup.length) report(dup[0][1][1].line, 'route/dup-fact', `${dup.slice(0, 4).map(([n, ps]) => `${n}（${ps.map(p => '「' + p.title + '」').join('、')}）`).join('，')} 在多块重复`, '只在讲它的那块写一次，其他块引用结论或删掉');
      },
    });
    api.rule({
      id: 'evidence', describe: '可机械判断的形式与出处问题：装饰交互、图重复表格、具体数字无出处',
      check(doc, report) {
        const textOf = nodes => { let t = ''; walk(nodes, n => { if (n.text) t += n.text + '\n'; if (n.kind === 'table') t += [n.head, ...n.rows].flat().join(' ') + '\n'; }); return t; };
        const hasVisual = nodes => { let v = false; walk(nodes, n => { if (n.kind === 'table' || (n.kind === 'fence' && n.form && !['callout', 'code'].includes(n.form))) v = true; }); return v; };
        for (const p of doc.panels) {
          // 1. interaction whose every step/tab/value only swaps a short paragraph: a list or table says the same
          walk(p.nodes, n => {
            if (n.kind !== 'fence' || !['tabs', 'slider', 'steps'].includes(n.form) || !n.children?.length) return;
            const kids = n.children.map(c => c.nodes || []);
            const noDigits = k => !/\d/.test(textOf(k).replace(/\d+[.、)]/g, ''));
            if (kids.every(k => !hasVisual(k) && (n.form !== 'slider' || noDigits(k) || textOf(k).trim().length <= 160)))
              report(n.line, 'route/decorative-interaction', `${n.form} 每一档只换一小段文字`, '改成列表或表格；交互只用在图或数字随档位变化时');
          });
          // 2. a diagram that redraws a table in the same block
          const cells = p.nodes.filter(n => n.kind === 'table').flatMap(t => t.rows.flat()).map(c => c.replace(/[*`]/g, '').trim()).filter(c => c.length >= 2);
          if (cells.length) walk(p.nodes, n => {
            if (n.kind !== 'fence' || n.form !== 'mermaid') return;
            const src = (n.body || []).join('\n');
            const labels = [...src.matchAll(/[\[\(\{"]+([^\]\)\}"\n]{2,40})[\]\)\}"]+/g)].map(m => m[1].trim());
            const hit = labels.filter(l => cells.some(c => c.includes(l) || l.includes(c)));
            if (labels.length >= 4 && hit.length / labels.length >= 0.7)
              report(n.line, 'route/duplicate-figure', `图里 ${hit.length}/${labels.length} 个标签已在同块表格里`, '删掉图或表其一；图只画表格表达不了的关系');
          });
          // 2b. a diagram that is only a grouped or linear list: mindmap, or a flowchart chain with no branch or edge label
          walk(p.nodes, n => {
            if (n.kind !== 'fence' || n.form !== 'mermaid') return;
            const src = (n.body || []).join('\n');
            const kind = (src.trim().split(/\s/)[0] || '').toLowerCase();
            if (kind === 'mindmap') { report(n.line, 'route/list-diagram', 'mindmap 只是把要点分组成树', '改成分组列表；只有分支之间有关系、过程或量级时才画图'); return; }
            if (!/^(flowchart|graph)$/.test(kind) || /subgraph|-->\s*\||--\s*[^->\s][^>]*-->|-\.|==>/.test(src)) return;
            const edges = [...src.matchAll(/(\w+)\s*(?:\[[^\]]*\]|\([^)]*\)|\{[^}]*\})?\s*-->\s*(\w+)/g)].map(m => [m[1], m[2]]);
            const nodes = new Set(edges.flat()); if (nodes.size < 4) return;
            const deg = (i) => { const c = {}; edges.forEach(e => c[e[i]] = (c[e[i]] || 0) + 1); return Math.max(...Object.values(c)); };
            if (deg(0) <= 1 && deg(1) <= 1) report(n.line, 'route/list-diagram', `flowchart 是 ${nodes.size} 个方框的单链，没有分支或条件`, '改成编号列表；图要表达分支、条件、回路或并行');
          });
          // 2c. boilerplate copied from the skill or repeated reading hints
          walk(p.nodes, n => { if (n.text && /读者会明白/.test(n.text)) report(n.line, 'route/boilerplate', '正文出现“读者会明白”套话', '删掉这句；块标题本身写清读者会明白什么'); });
          // 3. specific statistics with no source / 示意 / 估算 marker in the same block
          const prose = textOf(p.nodes.filter(n => n.kind !== 'fence'));
          const stats = prose.match(/[>≥<≤约]?\s?\d[\d,.]*\s?(%|％|倍|亿|万(?![一个])|美元|元|小时|GB|TB|ms\b)|[$¥€]\s?\d[\d,.]*\s?[BMK亿万]?/g) || [];
          if (stats.length >= 2 && !/(来源|出处|据|引自|示意|估算|估计|约|大约|左右|未核实|报告|论文|官方|文档|source|estimate|approx|~)/i.test(prose))
            report(p.line, 'route/unsourced-number', `「${p.title}」有 ${stats.length} 个具体数字没写来源（如 ${stats.slice(0, 2).join('、')}）`, '同一块里写出来源，或标“示意/估算”；写不出就改成定性说法');
        }
        // page level: every visual is a flowchart or a table on a page of 4+ blocks: other forms were probably not considered
        { const kinds = new Set(); let tables = 0;
          walk(doc.panels.flatMap(p => p.nodes), n => { if (n.kind === 'fence' && n.form === 'mermaid') kinds.add(((n.body || []).join('\n').trim().split(/\s/)[0] || '').toLowerCase().replace(/^graph$/, 'flowchart')); if (n.kind === 'table') tables++; });
          if (doc.panels.length >= 4 && [...kinds].every(k => k === 'flowchart')) report(doc.panels[0]?.line || 1, 'route/monotone-forms', `${doc.panels.length} 块只用了${kinds.size ? '流程图' : ''}${kinds.size && tables ? '和' : ''}${tables ? '表格' : ''}`, '逐块再问一遍：跨角色先后→sequenceDiagram，状态/生命周期→stateDiagram-v2，目录→treeView-beta，同一内容两种看法→views；真不适用就保留'); }
        // page level: repeated 看哪里 hints, unexplained acronyms (zh pages)
        const all = [textOf(doc.lead), ...doc.panels.map(p => p.title + '\n' + textOf(p.nodes.filter(n => n.kind !== 'fence' || ['tabs', 'steps', 'slider', 'views', 'callout'].includes(n.form))))].join('\n');
        const hints = (all.match(/看哪里/g) || []).length;
        if (hints >= 2) report(doc.panels[0]?.line || 1, 'route/boilerplate', `“看哪里”提示出现 ${hints} 次`, '只给最复杂的一张图留一句，写成普通句子，不用“看哪里：”标签');
        if (docLang(doc) === 'zh') {
          const common = new Set('AI API APP HTML CSS URL PDF CPU GPU USB ID OK PC TV CEO GDP CPI PPT VS FAQ DIY VIP GPS WIFI SQL JSON HTTP HTTPS IT UI UX PS NBA MBA PM AM TCP IP DNS CDN LLM GPT RAM ROM SSD HDD BMI DNA RNA CO2 IOS UTC FPS QR'.split(' '));
          const seen = new Map();
          for (const m of all.matchAll(/(?<![A-Za-z])([A-Z][A-Z0-9]{1,7}(?:-[A-Z0-9]+)?)(?![A-Za-z])/g)) {
            const a = m[1]; if (common.has(a) || /^[A-Z]\d+$/.test(a) || (a.match(/[A-Z]/g) || []).length < 2) continue;
            const around = all.slice(Math.max(0, m.index - 2), m.index + a.length + 2);
            const explained = /[（(]/.test(around.slice(-2)) || /[（(]$/.test(all.slice(Math.max(0, m.index - 1), m.index)) || /[\u4e00-\u9fa5][（(]$/.test(all.slice(Math.max(0, m.index - 2), m.index));
            if (!seen.has(a)) seen.set(a, explained); else if (explained) seen.set(a, true);
          }
          const bare = [...seen].filter(([, e]) => !e).map(([a]) => a);
          if (bare.length >= 3) report(doc.panels[0]?.line || 1, 'route/unexplained-term', `${bare.length} 个缩写没解释：${bare.slice(0, 6).join('、')}`, '第一次出现时写“中文名（缩写）”或在括号里用一句话解释；读者用不到的就删');
        }
      },
    });
    api.rule({
      id: 'forms', describe: '各形式自己的检查（form.lint）',
      check(doc, report, ctx) { walk([...doc.lead, ...doc.panels.flatMap(p => p.nodes)], n => { const f = n.form && ctx.registry.form(n.form); if (f?.lint) f.lint(n, report); }); },
    });
  },
};
