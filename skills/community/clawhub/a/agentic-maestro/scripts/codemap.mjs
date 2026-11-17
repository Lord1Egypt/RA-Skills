// Generates docs/CODEMAP.md so executors navigate from a map instead of exploring.
// Usage: node scripts/codemap.mjs <repo-root> [group ...]          (JS/TS workspace mode)
//        node scripts/codemap.mjs <repo-root> --generic [dir ...]  (any language; git-tracked files)
// Writes <repo-root>/docs/CODEMAP.md.
//
// Workspace mode: one section per child package that has a package.json under the group directories
// (default: apps, packages, packages/adapters). Sources are read from the package's src/, app/, lib/,
// components/, pages/ and server/ directories (never the package root, so configs are not listed);
// the main exports come from src/index.ts(x). If no package is found, it falls back to generic mode.
// Generic mode: one section per top-level directory (or per given dir), listing the git-tracked
// source files with their first header-comment sentence (//, #, /* */, """ docstrings).
// Both modes leave out tests (test/, tests/, __tests__/, __mocks__/, e2e/, fixtures/, *.test.*,
// *.spec.*, test_*.py, *_test.go), generated and vendored code. Exports are APPROXIMATE (regex, not a
// parser). Symlinks are never followed. Regenerate after merges that add, move or rename files.
import { readFileSync, readdirSync, writeFileSync, existsSync, mkdirSync, lstatSync } from 'node:fs';
import { join, relative } from 'node:path';
import { execFileSync } from 'node:child_process';

const root = process.argv[2];
if (!root) {
  console.error('usage: node scripts/codemap.mjs <repo-root> [group ...] | --generic [dir ...]');
  process.exit(2);
}
const rest = process.argv.slice(3);
const forceGeneric = rest[0] === '--generic';
const LARGE = 200;

const SKIP_DIRS = new Set(['node_modules', 'dist', 'build', 'out', '.next', '.turbo', 'coverage', 'generated',
  'vendor', 'target', '.venv', 'venv', '__pycache__', 'test', 'tests', '__tests__', '__mocks__', 'e2e',
  'fixtures', '.git']);
const SOURCE_EXTS = new Set(['ts', 'tsx', 'mts', 'cts', 'js', 'jsx', 'mjs', 'cjs', 'py', 'go', 'rs', 'rb', 'java', 'kt',
  'swift', 'cs', 'php', 'c', 'cc', 'cpp', 'h', 'hpp', 'sh', 'sql']);
const isSource = (name) => SOURCE_EXTS.has(name.slice(name.lastIndexOf('.') + 1)) && name.includes('.');
const isTestFile = (name) =>
  /\.(test|spec)\.[^.]+$/.test(name) || /^test_.*\.py$/.test(name) || /_test\.(go|py)$/.test(name) || /\.d\.ts$/.test(name);
const isSkippedPath = (rel) => rel.split('/').some((seg) => SKIP_DIRS.has(seg));

const firstSentence = (text) => {
  const s = text.replace(/\s+/g, ' ').trim();
  const m = s.match(/^(.{1,220}?[.!?])(\s|$)/);
  return (m ? m[1] : s.slice(0, 220)).trim();
};

const docOf = (src) => {
  // Only a HEADER comment counts: one that starts before the first code statement.
  const lines = src.split('\n');
  let i = 0;
  while (i < lines.length && (/^#!/.test(lines[i]) || /^\s*$/.test(lines[i]) || /^\s*(['"]use |# -\*-)/.test(lines[i]))) i++;
  const head = lines.slice(i).join('\n');
  let m = head.match(/^\s*\/\*\*?([\s\S]*?)\*\//);
  if (m) return firstSentence(m[1].replace(/^\s*\*\s?/gm, ' '));
  m = head.match(/^\s*(?:"""|''')([\s\S]*?)(?:"""|''')/);
  if (m) return firstSentence(m[1]);
  const block = [];
  for (const l of lines.slice(i)) {
    const c = l.match(/^\s*(?:\/\/|#)\s?(.*)$/);
    if (!c) break;
    block.push(c[1]);
  }
  return block.length ? firstSentence(block.join(' ')) : '';
};

const exportsOf = (src) => {
  const names = new Set();
  for (const m of src.matchAll(/export\s+(?:async\s+)?(?:function|const|class|type|interface|enum)\s+([A-Za-z0-9_]+)/g)) names.add(m[1]);
  for (const m of src.matchAll(/export\s+(?:type\s+)?\{([^}]+)\}/g)) {
    for (const part of m[1].split(',')) {
      const n = part.trim().split(/\s+as\s+/).pop()?.replace(/^type\s+/, '').trim();
      if (n) names.add(n);
    }
  }
  return [...names];
};

const walk = (dir, out) => {
  const entries = readdirSync(dir, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name));
  for (const d of entries) {
    const p = join(dir, d.name);
    if (d.isSymbolicLink()) continue; // never follow symlinks (files or directories)
    if (d.isDirectory()) {
      if (!SKIP_DIRS.has(d.name)) walk(p, out);
    } else if (isSource(d.name) && !isTestFile(d.name)) out.push(p);
  }
  return out;
};

const fileLine = (abs) => {
  const src = readFileSync(abs, 'utf8');
  const doc = docOf(src);
  return `- \`${relative(root, abs)}\` (${src.split('\n').length} lines)${doc ? ` — ${doc}` : ''}\n`;
};

const header = (mode) =>
  `# Code map\n\nGenerated from the source by agentic-maestro scripts/codemap.mjs (${mode} mode; do not edit by hand; regenerated after merges that add, move or rename files).\nEach section lists source files (tests excluded) with their first header-comment sentence${mode === 'workspace' ? ', plus the main exports of the package entry point (approximate — matched by regex, not a parser)' : ''}. Read the sections your task touches instead of exploring.\n`;

const SRC_DIRS = ['src', 'app', 'lib', 'components', 'pages', 'server'];

function workspaceMap(groups) {
  const pkgs = [];
  for (const g of groups) {
    const dir = join(root, g);
    if (!existsSync(dir)) continue;
    for (const d of readdirSync(dir, { withFileTypes: true }).filter((e) => e.isDirectory()).map((e) => e.name).sort()) {
      if (d === 'adapters' && g === 'packages') continue;
      const p = join(dir, d);
      if (existsSync(join(p, 'package.json'))) pkgs.push(p);
    }
  }
  if (pkgs.length === 0) return null;
  let md = header('workspace');
  for (const p of pkgs) {
    const pj = JSON.parse(readFileSync(join(p, 'package.json'), 'utf8'));
    md += `\n## ${pj.name} (\`${relative(root, p)}\`)\n`;
    if (pj.description) md += `${pj.description}\n`;
    const files = [];
    for (const s of SRC_DIRS) {
      const sd = join(p, s);
      if (existsSync(sd) && lstatSync(sd).isDirectory()) walk(sd, files);
    }
    if (files.length === 0) continue;
    if (files.length > LARGE) md += `_Large package: ${files.length} source files, all listed below._\n`;
    const index = ['src/index.ts', 'src/index.tsx'].map((f) => join(p, f)).find(existsSync);
    if (index) {
      const ex = exportsOf(readFileSync(index, 'utf8'));
      if (ex.length) md += `Exports: ${ex.slice(0, 60).join(', ')}${ex.length > 60 ? `, … (${ex.length} total)` : ''}\n`;
    }
    for (const f of files) md += fileLine(f);
  }
  return { md, count: pkgs.length, unit: 'packages' };
}

function genericMap(dirs) {
  let tracked;
  try {
    tracked = execFileSync('git', ['-C', root, 'ls-files', '-z'], { encoding: 'utf8', maxBuffer: 256 * 1024 * 1024 })
      .split('\0')
      .filter(Boolean);
  } catch {
    console.error('codemap.mjs: generic mode needs a git repository at the root');
    process.exit(2);
  }
  const files = tracked
    .filter((f) => isSource(f.split('/').pop()) && !isTestFile(f.split('/').pop()) && !isSkippedPath(f))
    .filter((f) => dirs.length === 0 || dirs.some((d) => f === d || f.startsWith(d.replace(/\/$/, '') + '/')))
    .filter((f) => {
      try {
        return lstatSync(join(root, f)).isFile();
      } catch {
        return false; // deleted in the working tree
      }
    })
    .sort();
  const sections = new Map();
  for (const f of files) {
    const top = f.includes('/') ? f.split('/')[0] : '(root)';
    if (!sections.has(top)) sections.set(top, []);
    sections.get(top).push(f);
  }
  let md = header('generic');
  for (const [top, list] of sections) {
    md += `\n## ${top}\n`;
    if (list.length > LARGE) md += `_Large section: ${list.length} source files, all listed below._\n`;
    for (const f of list) md += fileLine(join(root, f));
  }
  return { md, count: sections.size, unit: 'sections' };
}

let result = null;
if (!forceGeneric) result = workspaceMap(rest.length ? rest : ['apps', 'packages', 'packages/adapters']);
if (!result) result = genericMap(forceGeneric ? rest.slice(1) : []);
mkdirSync(join(root, 'docs'), { recursive: true });
writeFileSync(join(root, 'docs/CODEMAP.md'), result.md);
console.log(`docs/CODEMAP.md: ${result.count} ${result.unit}, ${result.md.length} bytes`);
