// render.mjs — IR nodes → a target format. Core kinds are rendered here; fences are delegated to their
// form's render[target]. A form that has no renderer for a target falls back: html → code block,
// markdown → the original fence, so a new output never breaks on an unknown form.
export const esc = s => String(s ?? '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

export function inline(s) {
  const codes = [];
  s = String(s ?? '').replace(/`([^`]+)`/g, (_, c) => { codes.push(c); return `\u0000${codes.length - 1}\u0000`; });
  s = esc(s)
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/(^|[^*])\*([^*\s][^*]*)\*/g, '$1<em>$2</em>')
    .replace(/~~([^~]+)~~/g, '<del>$1</del>')
    .replace(/\[([^\]]+)\]\((https?:[^)\s]+|#[^)\s]*)\)/g, '<a href="$2">$1</a>');
  return s.replace(/\u0000(\d+)\u0000/g, (_, i) => `<code>${esc(codes[i])}</code>`);
}

const BADGE = { ok: ['✓', 'ok'], no: ['✗', 'no'], warn: ['!', 'warn'] };
const isNoRow = r => r.some(c => /^no(\s|$)/.test(c));
function cell(c) {
  const m = c.match(/^(ok|no|warn)(\s+(.*))?$/);
  if (!m) return inline(c);
  const [sym, cls] = BADGE[m[1]];
  return `<span class="pe-badge pe-${cls}">${sym}</span>${m[3] ? ' ' + inline(m[3]) : ''}`;
}

const CORE = {
  html: {
    p: n => `<p>${inline(n.text)}</p>`,
    heading: n => `<h${n.level}>${inline(n.text)}</h${n.level}>`,
    quote: n => `<blockquote>${inline(n.text)}</blockquote>`,
    list: n => `<${n.ordered ? 'ol' : 'ul'}>${n.items.map(it => `<li>${inline(it.text)}</li>`).join('')}</${n.ordered ? 'ol' : 'ul'}>`,
    table: n => `<div class="pe-table"><table><thead><tr>${n.head.map(c => `<th>${inline(c)}</th>`).join('')}</tr></thead><tbody>${n.rows.map(r => `<tr${isNoRow(r) ? ' class="pe-row-no"' : ''}>${r.map(c => `<td>${cell(c)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`,
    fallbackFence: n => `<figure class="pe-code"><pre><code class="lang-${esc(n.lang)}">${esc(n.body.join('\n'))}</code></pre></figure>`,
  },
  markdown: {
    p: n => n.text,
    heading: n => `${'#'.repeat(n.level)} ${n.text}`,
    quote: n => `> ${n.text}`,
    list: n => n.items.map((it, k) => `${n.ordered ? `${k + 1}.` : '-'} ${it.text}`).join('\n'),
    table: n => [`| ${n.head.join(' | ')} |`, `|${n.head.map(() => '---').join('|')}|`, ...n.rows.map(r => `| ${r.map(c => c.replace(/^ok\b/, '✓').replace(/^no\b/, '✗').replace(/^warn\b/, '!')).join(' | ')} |`)].join('\n'),
    fallbackFence: n => ['```' + n.lang + (n.info ? ' ' + n.info : ''), ...n.body, '```'].join('\n'),
  },
};

export function createRenderer(registry, target) {
  const core = CORE[target] || CORE.html;
  const used = new Set();
  const r = {
    target, esc, inline, used,
    nodes: nodes => nodes.map(r.node).filter(Boolean).join(target === 'markdown' ? '\n\n' : '\n'),
    node(n) {
      if (n.kind !== 'fence') return core[n.kind] ? core[n.kind](n) : '';
      const form = n.form && registry.form(n.form);
      if (form) used.add(form.name);
      const fn = form?.render?.[target];
      return fn ? fn(n, r) : core.fallbackFence(n);
    },
  };
  return r;
}
