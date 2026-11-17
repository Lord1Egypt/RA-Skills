#!/usr/bin/env node
// doc-consistency — long-document consistency check. Local, deterministic, zero-dependency.
// 长文档一致性体检。纯本地、确定性、零依赖 —— 文档不出这台机器。
import { readdirSync, statSync, existsSync } from 'node:fs';
import { join, extname, resolve } from 'node:path';
import { readDoc } from './lib/read.mjs';
import { runRules, parseGlossary } from './lib/rules.mjs';
import { renderReport } from './lib/report.mjs';

const SUPPORTED = new Set(['.docx', '.md', '.markdown', '.txt', '.text']);
const SEV_RANK = { high: 0, medium: 1, low: 2 };

const USAGE = `
doc-consistency — 长文档一致性体检 / long-document consistency check

用法 / Usage:
  node check.mjs <文件或目录…> [选项]

选项 / Options:
  --all                  列出全部红点（默认只列前 20 条，汇总始终是完整的）
  --limit <n>            清单显示条数上限（默认 20）
  --json                 输出 JSON（完整清单，不截断），给程序用
  --glossary <file>      术语表：每行 "正名 = 变体1, 变体2"
  --baseline <路径…>     基准稿，用于合稿丢段比对（可给文件或目录）
  --fail-on <level>      有 high|medium|low 及以上时退出码为 1（默认不因发现而失败）
  --lang <zh|en>         报告语言（默认 zh）
  -h, --help             本帮助

示例 / Examples:
  node check.mjs 教材终稿.docx
  node check.mjs ./书稿/ --all --fail-on high
  node check.mjs 投标文件.docx --baseline 上一版.docx
  node check.mjs manuscript.md --lang en --json

本工具不联网、不上传、不调用任何模型。
Runs entirely offline. No upload, no model calls.
`.trim();

function parseArgs(argv) {
  const o = { files: [], all: false, limit: 20, json: false, glossary: null, baseline: [], failOn: null, lang: 'zh' };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '-h' || a === '--help') { console.log(USAGE); process.exit(0); }
    else if (a === '--all') o.all = true;
    else if (a === '--json') o.json = true;
    else if (a === '--limit') o.limit = Math.max(1, parseInt(argv[++i], 10) || 20);
    else if (a === '--glossary') o.glossary = argv[++i];
    else if (a === '--lang') o.lang = argv[++i] === 'en' ? 'en' : 'zh';
    else if (a === '--fail-on') {
      const v = String(argv[++i] || '').toLowerCase();
      if (!(v in SEV_RANK)) fail(`--fail-on 只能是 high / medium / low，收到 "${v}"`);
      o.failOn = v;
    } else if (a === '--baseline') {
      while (argv[i + 1] && !argv[i + 1].startsWith('--')) o.baseline.push(argv[++i]);
    } else if (a.startsWith('--')) fail(`未知选项 ${a}（--help 看用法）`);
    else o.files.push(a);
  }
  return o;
}

function fail(msg, code = 2) {
  console.error(`✗ ${msg}`);
  process.exit(code);
}

function expand(paths) {
  const out = [];
  for (const p of paths) {
    const abs = resolve(p);
    if (!existsSync(abs)) fail(`找不到：${p}`);
    if (statSync(abs).isDirectory()) {
      for (const name of readdirSync(abs).sort()) {
        if (name.startsWith('~$') || name.startsWith('.')) continue;
        const f = join(abs, name);
        if (statSync(f).isFile() && SUPPORTED.has(extname(name).toLowerCase())) out.push(f);
      }
    } else out.push(abs);
  }
  return out;
}

function load(paths, label) {
  const docs = [];
  for (const f of paths) {
    try {
      docs.push(readDoc(f));
    } catch (e) {
      console.error(`⚠ 跳过 ${f}：${e.message}`);
    }
  }
  if (!docs.length) fail(`${label}里没有可读文件（支持 .docx / .md / .txt）`);
  return docs;
}

// ── main ─────────────────────────────────────────────────────────────────────
const opts = parseArgs(process.argv.slice(2));
if (!opts.files.length) { console.log(USAGE); process.exit(0); }

const files = expand(opts.files);
if (!files.length) fail('没有匹配到受支持的文件（.docx / .md / .txt）');

const docs = load(files, '受检文件');
const baseDocs = opts.baseline.length ? load(expand(opts.baseline), '基准稿') : null;

let glossary = null;
if (opts.glossary) {
  if (!existsSync(opts.glossary)) fail(`术语表不存在：${opts.glossary}`);
  glossary = parseGlossary(opts.glossary);
  if (!glossary.length) console.error('⚠ 术语表没解析出任何条目，格式应为 "正名 = 变体1, 变体2"');
}

const { findings, stats } = runRules(docs, { glossary, baseDocs });

// Word 自动编号是域，不落在正文文字里 —— 明确告知，不装作查过了
const autoNum = docs.filter((d) => d.hasAutoNumbering).map((d) => d.file);
const notes = [];
if (autoNum.length) {
  notes.push(`${autoNum.join('、')} 使用了 Word 自动编号（域）。域不落在正文文字里，本工具读不到，这部分编号未纳入检查。`);
}

const cmd = `node ${process.argv[1].includes(' ') ? `"${process.argv[1]}"` : 'check.mjs'} ${opts.files.map((f) => (f.includes(' ') ? `"${f}"` : f)).join(' ')}`;

if (opts.json) {
  console.log(JSON.stringify({
    ok: true,
    files: docs.map((d) => ({ file: d.file, blocks: d.blocks.length })),
    stats: {
      ...stats,
      total: findings.length,
      high: findings.filter((f) => f.severity === 'high').length,
      medium: findings.filter((f) => f.severity === 'medium').length,
      low: findings.filter((f) => f.severity === 'low').length,
    },
    notes,
    findings: findings.map(({ block, ...f }) => f),
  }, null, 2));
} else {
  console.log(renderReport({ findings, docs, stats, cmd }, opts));
  if (notes.length) console.log(`\n> ⚠ 已知限制：${notes.join(' ')}\n`);
}

if (opts.failOn) {
  const worst = Math.min(...findings.map((f) => SEV_RANK[f.severity]), 99);
  if (worst <= SEV_RANK[opts.failOn]) process.exit(1);
}
process.exit(0);
