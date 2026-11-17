#!/usr/bin/env bash
# capturas-tutorial-formula100k — bootstrap
# Idempotente. Corre la primera vez (o cuando falte algún paquete).
set -e

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$SKILL_DIR"

echo "→ Skill dir: $SKILL_DIR"

# 1) Node disponible
if ! command -v node >/dev/null 2>&1; then
  echo "✗ Falta node. Instálalo con: brew install node"
  exit 1
fi
echo "✓ node $(node -v)"

# 2) package.json si no existe
if [ ! -f package.json ]; then
  cat > package.json <<'EOF'
{
  "name": "capturas-tutorial-formula100k",
  "version": "1.1.0",
  "private": true,
  "type": "module",
  "dependencies": {
    "puppeteer": "^23.0.0",
    "js-yaml": "^4.1.0",
    "sharp": "^0.34.0"
  }
}
EOF
  echo "✓ package.json creado"
fi

# 3) Instalar deps
if [ ! -d node_modules/puppeteer ] || [ ! -d node_modules/js-yaml ] || [ ! -d node_modules/sharp ]; then
  echo "→ Instalando puppeteer + js-yaml + sharp (puede tardar 30-60s la primera vez)..."
  npm install --silent --no-audit --no-fund
  echo "✓ deps instaladas"
else
  echo "✓ deps ya presentes"
fi

# 4) Sanity check
node -e "import('puppeteer').then(()=>console.log('✓ puppeteer OK')).catch(e=>{console.error('✗',e.message);process.exit(1)})"

echo ""
echo "Listo. Ya puedes correr:"
echo "  node $SKILL_DIR/scripts/render.mjs --type terminal --out /tmp/test.png --data '{\"command\":\"curl -fsSL https://claude.ai/install.sh | bash\"}'"
