#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

SLUG="${1:-amath-skill}"
VERSION="${2:-1.0.0}"
CHANGELOG="${3:-Initial public release}"
TAGS="${4:-latest,education,math,olympiad,socratic,learning}"
NAME="${CLAWHUB_NAME:-amath skill}"

if ! command -v clawhub >/dev/null 2>&1; then
  echo "clawhub CLI not found. Install it first with: npm i -g clawhub" >&2
  exit 1
fi

cat <<EOF
Publishing to ClawHub with:
- path: $SCRIPT_DIR
- slug: $SLUG
- name: $NAME
- version: $VERSION
- tags: $TAGS
EOF

set +e
publish_output="$(clawhub publish "$SCRIPT_DIR" \
  --slug "$SLUG" \
  --name "$NAME" \
  --version "$VERSION" \
  --changelog "$CHANGELOG" \
  --tags "$TAGS" 2>&1)"
publish_status=$?
set -e

if [[ $publish_status -eq 0 ]]; then
  printf '%s\n' "$publish_output"
  exit 0
fi

printf '%s\n' "$publish_output" >&2

echo "Retrying with compatibility fallback..." >&2

export AMATH_CLAWHUB_SLUG="$SLUG"
export AMATH_CLAWHUB_NAME="$NAME"
export AMATH_CLAWHUB_VERSION="$VERSION"
export AMATH_CLAWHUB_CHANGELOG="$CHANGELOG"
export AMATH_CLAWHUB_TAGS="$TAGS"

node <<'NODE'
const fs = require('node:fs/promises');
const path = require('node:path');
const os = require('node:os');

const TEXT_EXTENSIONS = new Set([
  'md','mdx','txt','json','json5','yaml','yml','toml','js','cjs','mjs','ts','tsx','jsx','py','sh','rb','go','rs','swift','kt','java','cs','cpp','c','h','hpp','sql','csv','ini','cfg','env','xml','html','css','scss','sass','svg'
]);

function getConfigPath() {
  const override = (process.env.CLAWHUB_CONFIG_PATH || process.env.CLAWDHUB_CONFIG_PATH || '').trim();
  if (override) return path.resolve(override);
  const xdg = process.env.XDG_CONFIG_HOME;
  if (xdg) return path.join(xdg, 'clawhub', 'config.json');
  return path.join(os.homedir(), '.config', 'clawhub', 'config.json');
}

async function walk(dir, root, files) {
  const entries = await fs.readdir(dir, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.name.startsWith('.')) continue;
    if (entry.name === 'node_modules') continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      await walk(full, root, files);
      continue;
    }
    if (!entry.isFile()) continue;
    const rel = path.relative(root, full).split(path.sep).join('/');
    const ext = rel.split('.').pop()?.toLowerCase() || '';
    if (!ext || !TEXT_EXTENSIONS.has(ext)) continue;
    files.push({ full, rel });
  }
}

async function main() {
  const root = process.cwd();
  const configPath = getConfigPath();
  const cfg = JSON.parse(await fs.readFile(configPath, 'utf8'));
  if (!cfg.token) throw new Error('Not logged in. Run: clawhub login');
  const registry = (cfg.registry || 'https://clawhub.ai').replace(/\/$/, '');
  const files = [];
  await walk(root, root, files);
  if (!files.some((file) => ['skill.md', 'skills.md'].includes(file.rel.toLowerCase()))) {
    throw new Error('SKILL.md required');
  }

  const payload = {
    slug: process.env.AMATH_CLAWHUB_SLUG,
    displayName: process.env.AMATH_CLAWHUB_NAME,
    version: process.env.AMATH_CLAWHUB_VERSION,
    changelog: process.env.AMATH_CLAWHUB_CHANGELOG,
    tags: process.env.AMATH_CLAWHUB_TAGS.split(',').map((s) => s.trim()).filter(Boolean),
    acceptLicenseTerms: true,
  };

  const form = new FormData();
  form.set('payload', JSON.stringify(payload));
  for (const file of files) {
    const bytes = await fs.readFile(file.full);
    form.append('files', new Blob([bytes], { type: 'text/plain' }), file.rel);
  }

  const response = await fetch(`${registry}/api/v1/skills`, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      Authorization: `Bearer ${cfg.token}`,
    },
    body: form,
  });

  const text = await response.text();
  if (!response.ok) {
    throw new Error(text || `HTTP ${response.status}`);
  }
  const json = JSON.parse(text || '{}');
  console.log(`OK. Published ${payload.slug}@${payload.version}${json.versionId ? ` (${json.versionId})` : ''}`);
}

main().catch((error) => {
  console.error(error.message || String(error));
  process.exit(1);
});
NODE
