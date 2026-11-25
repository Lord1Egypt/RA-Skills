// code — the default for every fence no other form claims. src= quotes a real file (inside cwd only),
// so code on the page is never retyped or invented by the model.
import { readFileSync, existsSync, realpathSync } from 'node:fs';
import { resolve, relative, isAbsolute } from 'node:path';
// containment by real path: a sibling with the same prefix (../project-x) or a symlink pointing out is outside
const within = (root, p) => { const r = relative(root, p); return r === '' || (!r.startsWith('..') && !isAbsolute(r)); };
export default {
  name: 'code',
  fences: ['', 'js', 'ts', 'tsx', 'jsx', 'py', 'python', 'go', 'rust', 'rs', 'java', 'sh', 'bash', 'json', 'yaml', 'sql', 'html', 'css', 'diff', 'c', 'cpp', 'text'],
  parse(node, ctx) {
    let code = node.body.join('\n'); let title = node.attrs.title || '';
    const src = node.attrs.src;
    if (src) {
      const root = process.cwd(); const p = resolve(root, src);
      const out = () => ctx.err(node.line, 'code/outside', `src 指向当前目录之外：${src}`, '只引用当前项目里的文件');
      if (!within(root, p)) out();
      else if (!existsSync(p)) ctx.err(node.line, 'code/missing', `找不到文件：${src}`, '检查路径');
      else if (!within(realpathSync(root), realpathSync(p))) ctx.err(node.line, 'code/outside', `src 指向当前目录之外：${src}`, '只引用当前项目里的文件');
      else {
        const all = readFileSync(p, 'utf8').split('\n');
        const [s, e] = String(node.attrs.lines || `1-${all.length}`).split('-').map(Number);
        code = all.slice(s - 1, e || s).join('\n'); title = title || `${src}:${s}${e ? '-' + e : ''}`;
        ctx.embedded.push(src);
      }
    }
    const n = code.split('\n').length;
    if (n > 40) ctx.warn(node.line, 'code/long', `代码块 ${n} 行`, '只留说明要点的 10–40 行');
    node.data = { code, title };
  },
  render: {
    html: (n, r) => `<figure class="pe-code">${n.data.title ? `<figcaption>${r.esc(n.data.title)}</figcaption>` : ''}<pre><code class="lang-${r.esc(n.lang)}">${r.esc(n.data.code)}</code></pre></figure>`,
    markdown: n => (n.data.title ? `\`${n.data.title}\`\n` : '') + ['```' + n.lang, n.data.code, '```'].join('\n'),
  },
};
