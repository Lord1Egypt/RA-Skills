const fs = require('fs');
const path = require('path');

function ensurePixelmatchRuntimePresent() {
  const required = ['pngjs', 'pixelmatch'];
  const missing = [];

  for (const name of required) {
    try {
      require.resolve(name);
    } catch {
      missing.push(name);
    }
  }

  if (!missing.length) return;

  throw new Error([
    `Missing dependencies: ${missing.join(', ')}`,
    'Install them in the host environment:',
    'npm install pixelmatch pngjs',
  ].join('\n'));
}

function loadModule(name, fallbacks = []) {
  const candidates = [name, ...fallbacks].filter(Boolean);
  for (const candidate of candidates) {
    try {
      return require(candidate);
    } catch {}
  }
  throw new Error(`Module not found: ${candidates.join(', ')}`);
}

function cropToSize(PNG, img, width, height) {
  if (img.width === width && img.height === height) return img;
  const out = new PNG({ width, height });
  PNG.bitblt(img, out, 0, 0, width, height, 0, 0);
  return out;
}

function runPixelmatch(img1Path, img2Path, diffPath) {
  if (!img1Path || !img2Path || !diffPath) {
    throw new Error('Usage: node scripts/pixelmatch-runner.cjs <img1> <img2> <diffPath>');
  }

  ensurePixelmatchRuntimePresent();

  const pngjsOverride = process.env.PNGJS_MODULE_PATH;
  const pixelmatchOverride = process.env.PIXELMATCH_MODULE_PATH;
  const { PNG } = loadModule('pngjs', [pngjsOverride]);
  const pm = loadModule('pixelmatch', [pixelmatchOverride]);
  const pixelmatch = pm.default || pm;

  const resolvedDiffPath = path.resolve(diffPath);
  fs.mkdirSync(path.dirname(resolvedDiffPath), { recursive: true });

  const img1 = PNG.sync.read(fs.readFileSync(img1Path));
  const img2 = PNG.sync.read(fs.readFileSync(img2Path));
  const width = Math.min(img1.width, img2.width);
  const height = Math.min(img1.height, img2.height);

  const a = cropToSize(PNG, img1, width, height);
  const b = cropToSize(PNG, img2, width, height);
  const diff = new PNG({ width, height });
  const diffPixels = pixelmatch(a.data, b.data, diff.data, width, height, { threshold: 0.1 });
  fs.writeFileSync(resolvedDiffPath, PNG.sync.write(diff));

  return {
    width,
    height,
    diffPixels,
    diffPercent: +(diffPixels / (width * height) * 100).toFixed(2),
    diffPath: resolvedDiffPath
  };
}

module.exports = { runPixelmatch };
