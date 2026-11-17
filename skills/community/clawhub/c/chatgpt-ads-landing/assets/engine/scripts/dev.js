#!/usr/bin/env node
/**
 * Local preview: build, serve dist/ with no caching, rebuild on change.
 *   node scripts/dev.js            → http://localhost:4123/
 *   PORT=8080 node scripts/dev.js
 * Simulate another country's geo routing by overriding the browser time
 * zone, e.g. DevTools → Sensors → Location, or launch Chrome with TZ=Europe/London.
 */
const http = require('http');
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const DIST = path.join(ROOT, 'dist');
const PORT = Number(process.env.PORT) || 4123;
const TYPES = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'application/javascript',
  '.json': 'application/json', '.xml': 'application/xml', '.txt': 'text/plain; charset=utf-8',
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp',
  '.svg': 'image/svg+xml', '.ico': 'image/x-icon',
};

const build = () => {
  try { execFileSync(process.execPath, [path.join(__dirname, 'build.js')], { stdio: 'inherit' }); } catch (e) { /* error already printed */ }
};
build();

let timer = null;
['pages', 'shared'].forEach((p) => {
  fs.watch(path.join(ROOT, p), { recursive: true }, () => {
    clearTimeout(timer);
    timer = setTimeout(build, 150);
  });
});

http.createServer((req, res) => {
  const urlPath = decodeURIComponent(req.url.split('?')[0]);
  let file = path.join(DIST, urlPath);
  if (!file.startsWith(DIST)) { res.writeHead(403).end(); return; }
  if (fs.existsSync(file) && fs.statSync(file).isDirectory()) {
    if (!urlPath.endsWith('/')) { res.writeHead(301, { Location: urlPath + '/' }).end(); return; }
    file = path.join(file, 'index.html');
  }
  if (!fs.existsSync(file)) {
    const pages = fs.readdirSync(DIST).filter((n) => fs.existsSync(path.join(DIST, n, 'index.html')));
    res.writeHead(urlPath === '/' ? 200 : 404, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(pages.map((p) => `<p><a href="/${p}/">/${p}/</a></p>`).join(''));
    return;
  }
  res.writeHead(200, { 'Content-Type': TYPES[path.extname(file)] || 'application/octet-stream', 'Cache-Control': 'no-store' });
  fs.createReadStream(file).pipe(res);
}).listen(PORT, () => console.log(`\npreview: http://localhost:${PORT}/`));
