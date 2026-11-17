#!/usr/bin/env bash
set -euo pipefail

ROOT="${1:-.}"
ROOT_REAL="$(realpath "$ROOT")"

echo "# Frontend Environment"
echo
echo "Root: $ROOT_REAL"
echo

if [[ -f "$ROOT_REAL/package.json" ]]; then
  echo "## Package"
  echo "- package.json: yes"
  if [[ -f "$ROOT_REAL/pnpm-lock.yaml" ]]; then echo "- package manager: pnpm"; fi
  if [[ -f "$ROOT_REAL/yarn.lock" ]]; then echo "- package manager: yarn"; fi
  if [[ -f "$ROOT_REAL/package-lock.json" ]]; then echo "- package manager: npm"; fi
  if [[ -f "$ROOT_REAL/bun.lockb" || -f "$ROOT_REAL/bun.lock" ]]; then echo "- package manager: bun"; fi

  if command -v node >/dev/null 2>&1; then
    node - "$ROOT_REAL/package.json" <<'NODE'
const fs = require('fs');
const file = process.argv[2];
const pkg = JSON.parse(fs.readFileSync(file, 'utf8'));
const deps = {...(pkg.dependencies || {}), ...(pkg.devDependencies || {})};
const has = (name) => Object.prototype.hasOwnProperty.call(deps, name);
const frameworks = [];
if (has('next')) frameworks.push('Next.js');
if (has('react')) frameworks.push('React');
if (has('vue')) frameworks.push('Vue');
if (has('svelte')) frameworks.push('Svelte');
if (has('@angular/core')) frameworks.push('Angular');
if (has('vite')) frameworks.push('Vite');
if (has('tailwindcss') || has('@tailwindcss/vite') || has('@tailwindcss/postcss')) frameworks.push('Tailwind');
const ui = [];
for (const name of ['@mui/material', '@chakra-ui/react', '@mantine/core', '@radix-ui/themes', 'antd', '@carbon/react', '@fluentui/react-components']) {
  if (has(name)) ui.push(name);
}
const icons = [];
for (const name of ['lucide-react', '@phosphor-icons/react', '@tabler/icons-react', '@radix-ui/react-icons', 'react-icons']) {
  if (has(name)) icons.push(name);
}
const scripts = pkg.scripts || {};
console.log(`- frameworks/tools: ${frameworks.length ? frameworks.join(', ') : 'not detected from package.json'}`);
console.log(`- UI libraries: ${ui.length ? ui.join(', ') : 'not detected'}`);
console.log(`- icon libraries: ${icons.length ? icons.join(', ') : 'not detected'}`);
for (const key of ['dev', 'build', 'typecheck', 'lint', 'test', 'preview']) {
  if (scripts[key]) console.log(`- script ${key}: ${scripts[key]}`);
}
NODE
  fi
else
  echo "## Package"
  echo "- package.json: not found"
fi

echo
echo "## Config Files"
for file in \
  "next.config.js" "next.config.mjs" "vite.config.ts" "vite.config.js" \
  "tailwind.config.js" "tailwind.config.ts" "postcss.config.js" \
  "tsconfig.json" "biome.json" "eslint.config.js" ".eslintrc.js"; do
  if [[ -f "$ROOT_REAL/$file" ]]; then
    echo "- $file"
  fi
done

echo
echo "## Source Hints"
for dir in "src" "app" "pages" "components" "styles" "public"; do
  if [[ -d "$ROOT_REAL/$dir" ]]; then
    echo "- $dir/"
  fi
done
