#!/usr/bin/env node
// ast-helper.js — AST utilities for JS/TS via acorn.
// Resolves acorn from the skill's own node_modules so it works regardless
// of cwd or NODE_PATH.

const fs = require('fs');
const path = require('path');

const SKILL_ROOT = path.resolve(__dirname, '..', '..');

function loadAcorn() {
  // 1) Bundled with the skill
  try { return require(path.join(SKILL_ROOT, 'node_modules', 'acorn')); }
  catch (_) {}
  // 2) NODE_PATH (set by lib/paths.sh)
  try { return require('acorn'); }
  catch (_) {}
  // 3) Project-local
  try { return require(path.join(process.cwd(), 'node_modules', 'acorn')); }
  catch (_) {}
  console.error(JSON.stringify({
    status: 'error',
    error: 'acorn not available. Install the skill with its bundled node_modules, or `npm install acorn` in the project.'
  }));
  process.exit(1);
}

const acorn = loadAcorn();

function parse(source, options = {}) {
  return acorn.parse(source, {
    ecmaVersion: 'latest',
    sourceType: 'module',
    locations: true,
    allowHashBang: true,
    ...options,
  });
}

function walk(node, visitor, parent = null) {
  if (!node || typeof node !== 'object') return;
  if (node.type && visitor[node.type]) visitor[node.type](node, parent);
  for (const key of Object.keys(node)) {
    if (key === 'loc' || key === 'range' || key === 'parent') continue;
    const child = node[key];
    if (Array.isArray(child)) child.forEach(c => walk(c, visitor, node));
    else if (child && typeof child === 'object' && child.type) walk(child, visitor, node);
  }
}

function findSymbols(source) {
  const ast = parse(source);
  const symbols = [];
  walk(ast, {
    FunctionDeclaration(n) {
      symbols.push({ type: 'function', name: n.id?.name, line: n.loc.start.line, end: n.loc.end.line });
    },
    ClassDeclaration(n) {
      symbols.push({ type: 'class', name: n.id?.name, line: n.loc.start.line, end: n.loc.end.line });
    },
    VariableDeclaration(n) {
      for (const decl of n.declarations) {
        if (decl.init && (decl.init.type === 'FunctionExpression' || decl.init.type === 'ArrowFunctionExpression')) {
          symbols.push({ type: 'function', name: decl.id?.name, line: n.loc.start.line, end: n.loc.end.line });
        }
      }
    },
    MethodDefinition(n) {
      symbols.push({
        type: 'method',
        name: n.key?.name || (n.key?.value),
        line: n.loc.start.line,
        end: n.loc.end.line,
      });
    },
  });
  return symbols;
}

function renameSymbol(source, oldName, newName) {
  const ast = parse(source);
  const edits = [];
  const seen = new Set();
  walk(ast, {
    Identifier(n) {
      if (n.name === oldName && n.loc) {
        // Object shorthand `{ foo }` creates two Identifier nodes with
        // identical positions (key + value). Deduplicate by start position.
        const key = `${n.start}:${n.end}`;
        if (seen.has(key)) return;
        seen.add(key);
        edits.push({ start: n.start, end: n.end, replacement: newName });
      }
    },
  });
  edits.sort((a, b) => b.start - a.start);
  let result = source;
  for (const e of edits) result = result.slice(0, e.start) + e.replacement + result.slice(e.end);
  return { source: result, count: edits.length };
}

function extractSymbol(source, name) {
  const ast = parse(source);
  let result = null;
  walk(ast, {
    FunctionDeclaration(n) { if (n.id?.name === name) result = source.slice(n.start, n.end); },
    ClassDeclaration(n)    { if (n.id?.name === name) result = source.slice(n.start, n.end); },
    VariableDeclaration(n) {
      for (const decl of n.declarations) {
        if (decl.id?.name === name && decl.init &&
            (decl.init.type === 'FunctionExpression' || decl.init.type === 'ArrowFunctionExpression')) {
          result = source.slice(n.start, n.end);
        }
      }
    },
  });
  return result;
}

function replaceSymbol(source, name, newCode) {
  const ast = parse(source);
  let edit = null;
  walk(ast, {
    FunctionDeclaration(n) { if (n.id?.name === name) edit = { start: n.start, end: n.end }; },
    ClassDeclaration(n)    { if (n.id?.name === name) edit = { start: n.start, end: n.end }; },
  });
  if (!edit) throw new Error(`Symbol not found: ${name}`);
  return source.slice(0, edit.start) + newCode + source.slice(edit.end);
}

// CLI
const [,, cmd, ...args] = process.argv;
try {
  switch (cmd) {
    case 'symbols': {
      const src = fs.readFileSync(args[0], 'utf8');
      process.stdout.write(JSON.stringify({ status: 'success', file: args[0], symbols: findSymbols(src) }) + '\n');
      break;
    }
    case 'rename': {
      const [file, oldName, newName] = args;
      const src = fs.readFileSync(file, 'utf8');
      const { source: out, count } = renameSymbol(src, oldName, newName);
      const pending = file + '.oce.pending';
      fs.writeFileSync(pending, out);
      process.stdout.write(JSON.stringify({ status: 'ready', count, pending }) + '\n');
      break;
    }
    case 'extract': {
      const [file, name] = args;
      const src = fs.readFileSync(file, 'utf8');
      const code = extractSymbol(src, name);
      if (code) process.stdout.write(code);
      else { console.error(`Symbol not found: ${name}`); process.exit(1); }
      break;
    }
    case 'replace-symbol': {
      const [file, name] = args;
      const src = fs.readFileSync(file, 'utf8');
      const newCode = fs.readFileSync(0, 'utf8'); // stdin
      const out = replaceSymbol(src, name, newCode);
      const pending = file + '.oce.pending';
      fs.writeFileSync(pending, out);
      process.stdout.write(JSON.stringify({ status: 'ready', pending }) + '\n');
      break;
    }
    default:
      console.error('Usage: ast-helper.js <symbols|rename|extract|replace-symbol> [args]');
      process.exit(1);
  }
} catch (e) {
  console.error(JSON.stringify({ status: 'error', error: e.message }));
  process.exit(1);
}
