'use strict';

const BOOLEAN = new Set(['json', 'help', 'version', 'yes', 'html']);
const SHORT = { y: 'yes', h: 'help' };

/** argv into { command, positional, flags }, or { ok: false, error }. */
function parseArgs(args) {
  const result = { command: null, positional: [], flags: {} };
  let rest = false;
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    const positional = rest || arg === '-' || !arg.startsWith('-');
    if (arg === '--' && !rest) {
      rest = true;
      continue;
    }
    if (positional) {
      if (!result.command) result.command = arg;
      else result.positional.push(arg);
      continue;
    }
    let key;
    let value;
    if (arg.startsWith('--')) {
      [key, value] = arg.slice(2).split(/=(.*)/s);
    } else {
      key = SHORT[arg.slice(1)];
      if (!key) return { ok: false, error: { code: 'INVALID_ARGUMENT', message: `unknown option: ${arg}` } };
    }
    if (BOOLEAN.has(key)) {
      result.flags[key] = true;
      continue;
    }
    if (value === undefined) {
      value = args[i + 1];
      if (value === undefined || value.startsWith('--'))
        return { ok: false, error: { code: 'MISSING_REQUIRED', message: `--${key} requires a value` } };
      i++;
    }
    result.flags[key] = value;
  }
  return { ok: true, result };
}

const ENTITIES = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ' };

// Notes writes &amp, &lt and &gt without the semicolon, so it is optional.
function decode(s) {
  return s.replace(/&(#x[\da-f]+;?|#\d+;?|amp;?|apos;?|nbsp;?|quot;?|lt;?|gt;?|[a-z]+;)/gi, (m, e) => {
    e = e.replace(/;$/, '');
    if (e[0] === '#') {
      const code = e[1] === 'x' || e[1] === 'X' ? parseInt(e.slice(2), 16) : parseInt(e.slice(1), 10);
      return Number.isFinite(code) ? String.fromCodePoint(code) : m;
    }
    return ENTITIES[e.toLowerCase()] ?? m;
  });
}

const BLOCK = new Set(['div', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'tr', 'table', 'blockquote', 'pre']);

/** Notes HTML into plain text: one line per block, lists as "- " or "1. ". */
function htmlToText(html) {
  let out = '';
  const lists = [];
  const newline = () => {
    if (out && !out.endsWith('\n')) out += '\n';
  };
  const tags = /<(\/?)([a-z0-9]+)\b[^>]*>|([^<]+)/gi;
  let m;
  while ((m = tags.exec(String(html)))) {
    if (m[3] !== undefined) {
      // Whitespace between blocks is source formatting, not text.
      if (!m[3].trim() && (!out || out.endsWith('\n'))) continue;
      out += decode(m[3].replace(/\s*\n\s*/g, ' '));
      continue;
    }
    const closing = m[1] === '/';
    const tag = m[2].toLowerCase();
    if (tag === 'br') out += '\n';
    else if (tag === 'td' || tag === 'th') {
      if (closing) out += '\t';
    } else if (tag === 'ul' || tag === 'ol') {
      newline();
      if (closing) lists.pop();
      else lists.push({ ordered: tag === 'ol', n: 0 });
    } else if (tag === 'li' && !closing) {
      newline();
      const list = lists[lists.length - 1] || { ordered: false, n: 0 };
      list.n++;
      out += '  '.repeat(Math.max(0, lists.length - 1)) + (list.ordered ? `${list.n}. ` : '- ');
    } else if (BLOCK.has(tag)) newline();
  }
  return out
    .replace(/[ \t]+\n/g, '\n')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

function escapeHtml(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

/** Plain text into the div-per-line HTML Notes writes itself. */
function textToHtml(text) {
  const lines = String(text).replace(/\r\n?/g, '\n').replace(/\n+$/, '').split('\n');
  return lines.map((l) => `<div>${l ? escapeHtml(l) : '<br>'}</div>`).join('');
}

/** A new note's body: the title as a heading, then the text. */
function noteHtml(title, body) {
  return `<div><h1>${escapeHtml(title)}</h1></div>` + (body ? textToHtml(body) : '');
}

function when(iso) {
  return iso ? iso.slice(0, 16).replace('T', ' ') : '';
}

function formatSummary(n) {
  const lines = [`${n.title || '(untitled)'}${n.locked ? '  [locked]' : ''}`];
  lines.push(`  ${n.folder}  ${when(n.modified)}  id ${n.id}`);
  if (n.snippet) lines.push(`  ${n.snippet}`);
  return lines.join('\n');
}

function formatList(d) {
  if (!d.notes.length) return 'No notes found.';
  const more = d.total > d.count ? `\n\nShowing ${d.count} of ${d.total}; --limit for more.` : '';
  return d.notes.map(formatSummary).join('\n\n') + more;
}

function formatFolders(d) {
  if (!d.folders.length) return 'No folders.';
  const w = Math.max(...d.folders.map((f) => f.name.length));
  return d.folders.map((f) => `${f.name.padEnd(w)}  ${f.account}  ${f.count} note(s)  id ${f.id}`).join('\n');
}

function formatNote(n, html) {
  const head = `${n.title}\n  ${n.account} / ${n.folder}  modified ${when(n.modified)}  id ${n.id}`;
  if (n.locked) return `${head}\n\nThis note is locked; unlock it in Notes to read it.`;
  return `${head}\n\n${html ? n.body : htmlToText(n.body)}`;
}

module.exports = {
  parseArgs,
  htmlToText,
  textToHtml,
  noteHtml,
  escapeHtml,
  formatList,
  formatFolders,
  formatNote,
  formatSummary,
};
