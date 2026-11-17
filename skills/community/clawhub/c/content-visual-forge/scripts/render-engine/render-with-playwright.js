const { chromium } = require('playwright');
const fs = require('fs');
const os = require('os');
const path = require('path');
const { pathToFileURL } = require('url');

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function renderValue(value) {
  if (Array.isArray(value)) {
    return `<ul>${value.map(item => `<li>${renderValue(item)}</li>`).join('')}</ul>`;
  }
  if (value && typeof value === 'object') {
    const parts = Object.entries(value)
      .map(([key, nested]) => `<span class="field-${escapeHtml(key)}">${renderValue(nested)}</span>`);
    return parts.join(' ');
  }
  return escapeHtml(value ?? '');
}

function applyTemplate(template, data) {
  return template.replace(/\{\{\s*([a-zA-Z0-9_.-]+)\s*\}\}/g, (_match, key) => {
    const value = key.split('.').reduce((current, part) => {
      if (current && Object.prototype.hasOwnProperty.call(current, part)) {
        return current[part];
      }
      return undefined;
    }, data);
    return renderValue(value);
  });
}

function isRemoteUrl(value) {
  return /^https?:\/\//i.test(String(value || ''));
}

function collectAssetRefs(data) {
  const refs = [];
  if (data.background_asset) {
    refs.push({
      asset_id: data.background_asset.asset_id,
      url: data.background_asset.url,
      role: 'background',
    });
  }
  if (Array.isArray(data.pages)) {
    for (const page of data.pages) {
      if (page && page.image_asset && page.image_asset.source) {
        refs.push({
          asset_id: page.image_asset.asset_id,
          url: page.image_asset.source,
          role: page.image_asset.type || 'visual',
        });
      }
    }
  }
  return refs.filter(ref => ref.asset_id && ref.asset_id !== 'none' && ref.url);
}

function validateAssetSources(data) {
  const refs = collectAssetRefs(data);
  if (refs.length === 0) {
    return;
  }

  const records = new Map((data.asset_source_record || []).map(record => [record.asset_id, record]));
  const missing = refs.filter(ref => !records.has(ref.asset_id));
  if (missing.length > 0) {
    throw new Error(`Missing asset_source_record for: ${missing.map(ref => ref.asset_id).join(', ')}`);
  }

  const blocked = refs.filter(ref => {
    const record = records.get(ref.asset_id);
    return record.source_type === 'unknown_or_restricted' || record.decision === 'reject';
  });
  if (blocked.length > 0) {
    throw new Error(`Blocked asset source used in render data: ${blocked.map(ref => ref.asset_id).join(', ')}`);
  }

  const remoteWithoutDecision = refs.filter(ref => {
    const record = records.get(ref.asset_id);
    return isRemoteUrl(ref.url) && record.decision !== 'use' && record.decision !== 'request_confirmation';
  });
  if (remoteWithoutDecision.length > 0) {
    throw new Error(`Remote asset URLs require an asset_source_record decision: ${remoteWithoutDecision.map(ref => ref.asset_id).join(', ')}`);
  }
}

function buildRenderableHtml(htmlPath, dataPath) {
  const template = fs.readFileSync(htmlPath, 'utf8');
  if (!dataPath) {
    return { htmlPath, cleanup: () => {} };
  }

  const data = JSON.parse(fs.readFileSync(dataPath, 'utf8'));
  validateAssetSources(data);
  const rendered = applyTemplate(template, data).replace(
    /<head>/i,
    `<head>\n  <base href="${pathToFileURL(path.resolve(path.dirname(htmlPath)) + path.sep).href}">`
  );
  if (/\{\{[^}]+\}\}/.test(rendered)) {
    throw new Error('Rendered template still contains unresolved placeholders.');
  }
  const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'content-visual-render-'));
  const tempPath = path.join(tempDir, path.basename(htmlPath));
  fs.writeFileSync(tempPath, rendered, 'utf8');
  return {
    htmlPath: tempPath,
    cleanup: () => fs.rmSync(tempDir, { recursive: true, force: true }),
  };
}

async function render(htmlPath, outputPath, width = 1200, height = 675, dataPath) {
  const renderable = buildRenderableHtml(htmlPath, dataPath);
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
    await page.goto('file://' + path.resolve(renderable.htmlPath));
    const unresolved = await page.locator('text=/\\{\\{[^}]+\\}\\}/').count();
    if (unresolved > 0) {
      throw new Error('Rendered template still contains unresolved placeholders.');
    }
    await page.screenshot({ path: outputPath, fullPage: false });
  } finally {
    await browser.close();
    renderable.cleanup();
  }
}

const htmlPath = process.argv[2];
const outputPath = process.argv[3] || 'output.png';
const width = Number(process.argv[4] || 1200);
const height = Number(process.argv[5] || 675);
const dataPath = process.argv[6];

if (!htmlPath) {
  console.error('Usage: node render-with-playwright.js <htmlPath> <outputPath> [width] [height] [dataJson]');
  process.exit(1);
}

render(htmlPath, outputPath, width, height, dataPath).catch(err => {
  console.error(err);
  process.exit(1);
});
