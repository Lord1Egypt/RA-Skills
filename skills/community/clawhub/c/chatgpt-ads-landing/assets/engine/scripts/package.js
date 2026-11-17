#!/usr/bin/env node
/**
 * Build + check + zip one page for a static site-hosting platform.
 *
 *   node scripts/package.js my-page          → out/my-page-<yyyymmdd-hhmm>.zip
 *   node scripts/package.js my-page --force  → zip even if check fails
 *                                               (first deploy, before page.json url is known)
 *
 * The zip has index.html / robots.txt / sitemap.xml at its root (the platform
 * serves one site per subdomain and maps "/" to the entry file) and never
 * contains __MACOSX or dotfiles — a Finder-made zip does, and the platform will
 * happily pick "__MACOSX/._index.html" as the entry.
 */
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const args = process.argv.slice(2);
const force = args.includes('--force');
const slug = args.find((a) => !a.startsWith('--'));
if (!slug) { console.error('usage: node scripts/package.js <slug> [--force]'); process.exit(1); }

const run = (script, extra) => execFileSync(process.execPath, [path.join(__dirname, script), ...extra], { stdio: 'inherit' });

try { run('build.js', [slug]); } catch (e) { process.exit(1); }
try {
  run('check.js', [slug]);
} catch (e) {
  if (!force) { console.error('\n✖ check 未通过,未打包。首次部署(还没有访问地址)可加 --force'); process.exit(1); }
  console.warn('\n⚠ check 未通过,--force 继续打包(仅用于首次部署拿访问地址,不要拿去投放)');
}

const stamp = new Date().toISOString().replace(/[-:]/g, '').replace('T', '-').slice(0, 13);
const outDir = path.join(ROOT, 'out');
const zipPath = path.join(outDir, `${slug}-${stamp}.zip`);
fs.mkdirSync(outDir, { recursive: true });
execFileSync('zip', ['-r', '-X', '-q', zipPath, '.', '-x', '.*', '*/.*', '__MACOSX/*'], { cwd: path.join(ROOT, 'dist', slug), stdio: 'inherit' });

console.log(`\n✔ ${path.relative(ROOT, zipPath)}  (${(fs.statSync(zipPath).size / 1048576).toFixed(1)}MB)`);
// publish.mjs uploads dist/<slug>/ itself and sets BV_PUBLISH — the manual steps below would mislead.
if (process.env.BV_PUBLISH) { process.exit(0); }

const page = JSON.parse(fs.readFileSync(path.join(ROOT, 'pages', slug, 'page.json'), 'utf8'));
console.log(`
上传到托管平台:
  主入口文件   index.html
  加密访问     关闭(开了 OAI-AdsBot 抓不到,广告过不了审)
  ${String(page.url || '').includes('REPLACE')
    ? '首次部署:拿到访问地址后填进 pages/' + slug + '/page.json 的 url,重新打包,用「部署新版本」覆盖'
    : '已有站点:在该站点上用「部署新版本」上传'}`);
