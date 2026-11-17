// Built-in outputs. An output is { name, ext, write(doc, ctx) → string }.
//   html      one offline page: theme CSS + the CSS/JS of only the forms the page uses
//   markdown  the chat carrier: interactive forms flattened (steps → numbered beats, views → the pick)
//   json      the IR itself, versioned — the contract for other renderers (React, note apps, slides)
import { createRenderer, esc } from '../core/render.mjs';
import { paletteCss, paletteJs } from '../themes/palette-ui.mjs';
import { annotateCss, annotateJs, DEFAULT_KINDS } from '../themes/annotate-ui.mjs';

const BASE_JS = `(()=>{const d=document.documentElement;d.classList.replace('nojs','js');window.PE={reduce:matchMedia('(prefers-reduced-motion: reduce)').matches};
const tb=document.querySelector('.pe-theme'),order=['auto','light','dark'],lab={auto:'自动',light:'浅色',dark:'深色'};
const setT=t=>{if(t==='auto')d.removeAttribute('data-theme');else d.dataset.theme=t;if(tb)tb.textContent='主题：'+lab[t];try{localStorage.setItem('pe-theme',t)}catch(e){}};
let cur=(()=>{try{return localStorage.getItem('pe-theme')}catch(e){}})()||d.dataset.default||'auto';setT(cur);
tb&&tb.addEventListener('click',()=>{cur=order[(order.indexOf(cur)+1)%3];setT(cur)});
const cp=document.querySelector('[data-copy]');cp&&cp.addEventListener('click',()=>{navigator.clipboard?.writeText(document.getElementById('pe-source').textContent);cp.textContent='已复制'});`;

function html(doc, ctx) {
  const { registry, theme: themeName = 'pele', lang } = ctx;
  const theme = registry.theme(themeName) || registry.theme('pele');
  const r = createRenderer(registry, 'html');
  const lead = r.nodes(doc.lead);
  const panels = doc.panels.map((p, k) => `<section class="pe-panel" id="s${k + 1}"><h2><span class="pe-n">${String(k + 1).padStart(2, '0')}</span>${esc(p.title)}</h2>${r.nodes(p.nodes)}</section>`).join('\n');
  const forms = [...r.used].map(n => registry.form(n)).filter(f => f?.assets);
  // precedence: draft front matter (palette: off / on) > CLI/env/config (ctx.palette, default on)
  const fm = String(doc.meta.palette || '').trim();
  const studio = fm === 'off' ? false : fm === 'on' || /=/.test(fm) ? true : ctx.palette !== false;
  const fa = String(doc.meta.annotate || '').trim();
  const notes = fa === 'off' ? false : fa === 'on' ? true : ctx.annotate !== false;
  const kinds = registry.annotations?.().length ? registry.annotations() : DEFAULT_KINDS;
  const css = [theme.css, ...forms.map(f => f.assets.css || ''), studio ? paletteCss(registry) : '', notes ? annotateCss(kinds) : ''].join('\n');
  const js = [BASE_JS, ...forms.map(f => f.assets.js || ''), theme.js || '', '})();', studio ? paletteJs(registry) : '', notes ? annotateJs(kinds) : ''].join('\n');
  const meta = doc.meta;
  const htmlLang = meta.lang || (lang === 'zh' ? 'zh-CN' : lang === 'neutral' ? 'und' : lang || 'und');
  const extra = Object.entries(meta).filter(([k]) => !['title', 'subtitle', 'lang', 'theme', 'ste', 'router', 'palette', 'annotate'].includes(k));
  return `<!doctype html>
<html lang="${esc(htmlLang)}" class="nojs" data-default="${esc(ctx.mode || meta.mode || 'auto')}" data-theme-name="${esc(theme.name)}"${studio && meta.palette ? ` data-palette="${esc(meta.palette)}"` : ''}${studio && /page=(\w+)/.test(meta.palette || '') && meta.palette.match(/page=(\w+)/)[1] !== 'ink' ? ` data-pal="${esc(meta.palette.match(/page=(\w+)/)[1])}"` : ''}>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; img-src data:">
<meta name="generator" content="call-pele-answer ir${doc.ir}; forms=${[...r.used].join(',')}">
<title>${esc(meta.title || 'Explainer')}</title>
<style>${css}</style></head>
<body><main>
<header class="pe-head"><div class="pe-meta"><span>${new Date().toISOString().slice(0, 10)}</span>${extra.map(([k, v]) => `<span>${esc(k)} · ${esc(v)}</span>`).join('')}${studio ? '<button type="button" class="pe-pal" aria-pressed="false" style="margin-left:auto">调色</button>' : ''}<button type="button" class="pe-theme"${studio ? ' style="margin-left:0"' : ''}>主题</button></div>
<h1>${esc(meta.title || '')}</h1>${meta.subtitle ? `<p class="pe-sub">${esc(meta.subtitle)}</p>` : ''}</header>
${lead.trim() ? `<div class="pe-lead">${lead}</div>` : ''}
${panels}
<footer class="pe-foot"><details><summary>原稿（Markdown，可复制给 Agent 修改）</summary><button type="button" data-copy style="margin-top:.5rem;padding:0 .6rem">复制原稿</button><pre>${esc(doc.source)}</pre></details>
<p>离线单文件${notes ? ' · 每块内容左侧 ✎ 可批注，批注可一键复制给 Agent' : ''}</p></footer>
</main>
<script type="text/markdown" id="pe-source">${doc.source.replace(/<\/script>/gi, '<\\/script>')}</script>
<script>${js}</script>
</body></html>`;
}

function markdown(doc, ctx) {
  const r = createRenderer(ctx.registry, 'markdown');
  return [doc.meta.title ? `**${doc.meta.title}**` : '', r.nodes(doc.lead), ...doc.panels.map(p => `### ${p.title}\n\n${r.nodes(p.nodes)}`)].filter(Boolean).join('\n\n') + '\n';
}

function json(doc, ctx) {
  const lean = ctx.lean;
  return JSON.stringify(doc, (k, v) => (lean && (k === 'svg' || k === 'narrowSvg') ? undefined : k === 'source' && lean ? undefined : v), 2);
}

export default {
  name: 'builtin-outputs', apiVersion: 1,
  setup(api) {
    api.output({ name: 'html', ext: 'html', write: html, describe: '离线单页（默认）' });
    api.output({ name: 'markdown', ext: 'md', write: markdown, describe: '聊天载体：交互形式压平，图保留为 mermaid 围栏' });
    api.output({ name: 'json', ext: 'json', write: json, describe: 'IR v1（--lean 去掉 SVG 与原稿）' });
  },
};
