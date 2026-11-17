// Built-in lint rules over the IR. A rule is { id, check(doc, report, ctx) }; plugins add domain rules
// (e.g. "every number in a finance page cites a source") the same way.
import { walk } from '../core/markdown.mjs';
import { lintProse, lintRouting, normLang, detectLang } from './rules.mjs';

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
            return { title: p.title, line: p.line, prose: proseUnits(p.nodes), tables: p.nodes.filter(n => n.kind === 'table').map(t => ({ line: t.line, cols: t.head.length, rows: t.rows.length })), blocks: fences };
          }),
        };
        for (const f of lintRouting(legacy)) report(...f);
      },
    });
    api.rule({
      id: 'forms', describe: '各形式自己的检查（form.lint）',
      check(doc, report, ctx) { walk([...doc.lead, ...doc.panels.flatMap(p => p.nodes)], n => { const f = n.form && ctx.registry.form(n.form); if (f?.lint) f.lint(n, report); }); },
    });
  },
};
