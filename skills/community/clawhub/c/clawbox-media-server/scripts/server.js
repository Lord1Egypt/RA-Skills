#!/usr/bin/env node
// LAN Media Server — lightweight static file server for AI agent media sharing
const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = parseInt(process.env.MEDIA_PORT || '18801', 10);
const BIND_ADDR = process.env.BIND_ADDR || '0.0.0.0';
const MEDIA_ROOT = path.resolve(process.env.MEDIA_ROOT || path.join(process.env.HOME, 'projects/shared-media'));

const MIME = {
  '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png',
  '.gif': 'image/gif', '.webp': 'image/webp', '.svg': 'image/svg+xml',
  '.mp4': 'video/mp4', '.webm': 'video/webm', '.mp3': 'audio/mpeg',
  '.ogg': 'audio/ogg', '.wav': 'audio/wav', '.pdf': 'application/pdf',
  '.html': 'text/html', '.json': 'application/json', '.txt': 'text/plain',
  '.css': 'text/css', '.js': 'application/javascript', '.zip': 'application/zip',
};

function escapeHtml(str) {
  return String(str).replace(/[&<>"']/g, ch => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
  }[ch]));
}

const server = http.createServer((req, res) => {
  if (req.method !== 'GET') {
    res.writeHead(405); res.end('Method Not Allowed'); return;
  }

  let urlPath;
  try {
    urlPath = decodeURIComponent(req.url.split('?')[0]);
  } catch {
    res.writeHead(400); res.end('Bad request'); return;
  }

  // Block null bytes and double-encoded traversal
  if (urlPath.includes('\0') || urlPath.includes('..')) {
    res.writeHead(403); res.end('Forbidden'); return;
  }

  const safePath = path.normalize(urlPath);
  const filePath = path.join(MEDIA_ROOT, safePath);

  // Block path traversal
  if (!filePath.startsWith(MEDIA_ROOT + path.sep) && filePath !== MEDIA_ROOT) {
    res.writeHead(403); res.end('Forbidden'); return;
  }

  // If root path, return an HTML directory listing
  if (filePath === MEDIA_ROOT || filePath === MEDIA_ROOT + '/') {
    fs.readdir(MEDIA_ROOT, (err, files) => {
      if (err) {
        res.writeHead(404);
        res.end('Directory not found');
        return;
      }
      const items = [];
      files.forEach(file => {
        const full = path.join(MEDIA_ROOT, file);
        try {
          const stats = fs.statSync(full);
          if (stats.isFile()) {
            items.push({
              name: file,
              size: stats.size,
              mtime: stats.mtime
            });
          }
        } catch (e) {}
      });
      items.sort((a, b) => b.mtime - a.mtime);
      const hostHeader = req.headers.host || 'localhost:18801';
      const hostname = hostHeader.split(':')[0] || 'localhost';
      let html = `<!DOCTYPE html><html><head><title>LAN Media Server</title><style>body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;max-width:900px;margin:40px auto;padding:20px;background:#f5f5f5;color:#333}h1{margin-bottom:10px}.list{background:white;border-radius:8px;padding:15px}li{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #eee}li:last-child{border-bottom:none}a{color:#0066cc;text-decoration:none}small{color:#666}.note{margin-top:20px;padding:12px;background:#fff3cd;border-radius:6px;font-size:14px;color:#856404}</style></head><body><h1>📁 Shared Files</h1><p>Upload new files via <a href="http://${hostname}:18802/">http://${hostname}:18802/</a></p><ul class="list">`;
      items.forEach(item => {
        const size = item.size > 1024 * 1024 ? (item.size / (1024 * 1024)).toFixed(1) + ' MB' : item.size > 1024 ? (item.size / 1024).toFixed(1) + ' KB' : item.size + ' B';
        const date = item.mtime.toLocaleString();
        html += `<li><a href="/${encodeURIComponent(item.name)}">${escapeHtml(item.name)}</a><small>${size} • ${date}</small></li>`;
      });
      html += `</ul><div class="note">Files are served on this port (18801). Upload new files via port 18802.</div></body></html>`;
      res.writeHead(200, { 'Content-Type': 'text/html', 'Cache-Control': 'no-cache' });
      res.end(html);
      return;
    });
    return;
  }

  fs.stat(filePath, (err, stats) => {
    if (err || !stats.isFile()) {
      res.writeHead(404); res.end('Not found'); return;
    }
    const ext = path.extname(filePath).toLowerCase();
    res.writeHead(200, {
      'Content-Type': MIME[ext] || 'application/octet-stream',
      'Content-Length': stats.size,
      'Cache-Control': 'public, max-age=3600',
      'X-Content-Type-Options': 'nosniff',
      'Content-Security-Policy': "default-src 'self'; img-src 'self'; media-src 'self'; style-src 'unsafe-inline'; script-src 'unsafe-inline' 'unsafe-eval'",
    });
    fs.createReadStream(filePath).pipe(res);
  });
});

server.listen(PORT, BIND_ADDR, () => {
  console.log(`LAN Media Server running on http://${BIND_ADDR}:${PORT}`);
  console.log(`Serving: ${MEDIA_ROOT}`);
});
