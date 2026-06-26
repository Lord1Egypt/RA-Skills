#!/usr/bin/env bash
# oce-tree — Project structure viewer with sane excludes.

OCE_CALLER="${BASH_SOURCE[0]}"
source "$(dirname "$0")/lib/paths.sh"
source "$(dirname "$0")/lib/common.sh"

DEPTH=3; ROOT="."; SHOW_HIDDEN=0

while [ $# -gt 0 ]; do
  case "$1" in
    --depth|-d)   DEPTH="$2"; shift 2 ;;
    --depth=*)    DEPTH="${1#*=}"; shift ;;
    --hidden)     SHOW_HIDDEN=1; shift ;;
    --json)       OCE_JSON_MODE="1"; shift ;;
    -h|--help)
      cat <<'EOF'
oce tree [path] [--depth N] [--hidden]
  Show project structure, skipping noise dirs.
  --depth N   Max depth (default 3)
  --hidden    Include dotfiles
EOF
      exit 0 ;;
    -*) die "Unknown flag: $1" ;;
    *)  ROOT="$1"; shift ;;
  esac
done

[ -d "$ROOT" ] || die "Not a directory: $ROOT"

# Build a Node script that walks the tree with filters
node - "$ROOT" "$DEPTH" "$SHOW_HIDDEN" "$OCE_JSON_MODE" <<'NODE'
const fs = require('fs');
const path = require('path');
const [,, root, depth, showHidden, jsonMode] = process.argv;
const maxDepth = parseInt(depth, 10);
const json = jsonMode === '1';
const SKIP = new Set([
  'node_modules','.git','dist','build','.next','__pycache__',
  'vendor','target','.venv','venv','.oce','coverage','.cache',
  '.idea','.vscode','.DS_Store','out','.turbo','.parcel-cache'
]);

function walk(dir, level, prefix, lines, treeJson) {
  if (level > maxDepth) return;
  let entries;
  try { entries = fs.readdirSync(dir, { withFileTypes: true }); }
  catch { return; }
  entries = entries
    .filter(e => showHidden === '1' || !e.name.startsWith('.'))
    .filter(e => !SKIP.has(e.name))
    .sort((a, b) => {
      if (a.isDirectory() !== b.isDirectory()) return a.isDirectory() ? -1 : 1;
      return a.name.localeCompare(b.name);
    });
  entries.forEach((e, i) => {
    const last = i === entries.length - 1;
    const branch = last ? '└── ' : '├── ';
    const full = path.join(dir, e.name);
    const node = { name: e.name, type: e.isDirectory() ? 'dir' : 'file', children: [] };
    treeJson.push(node);
    lines.push(prefix + branch + e.name + (e.isDirectory() ? '/' : ''));
    if (e.isDirectory()) {
      walk(full, level + 1, prefix + (last ? '    ' : '│   '), lines, node.children);
    }
  });
}

const lines = [root];
const tree = { name: root, type: 'dir', children: [] };
walk(root, 1, '', lines, tree.children);

if (json) {
  process.stdout.write(JSON.stringify({status:'success', root, depth: maxDepth, tree}) + '\n');
} else {
  process.stdout.write(lines.join('\n') + '\n');
}
NODE
