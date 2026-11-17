#!/usr/bin/env node
'use strict';

const http = require('http');
const fs = require('fs');
const path = require('path');

const root = __dirname;
const port = Number(process.env.FDE_POC_PORT || 4173);
const mime = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8' };

http.createServer((request, response) => {
  const requested = decodeURIComponent((request.url || '/').split('?')[0]);
  const relative = requested === '/' ? 'index.html' : requested.replace(/^\/+/, '');
  const file = path.resolve(root, relative);
  if (!file.startsWith(`${root}${path.sep}`)) {
    response.writeHead(403).end('Forbidden');
    return;
  }
  fs.readFile(file, (error, data) => {
    if (error) {
      response.writeHead(error.code === 'ENOENT' ? 404 : 500).end('Not found');
      return;
    }
    response.writeHead(200, { 'Content-Type': mime[path.extname(file)] || 'application/octet-stream' });
    response.end(data);
  });
}).listen(port, '127.0.0.1', () => {
  console.log(`{{POC_NAME}} started:http://127.0.0.1:${port}`);
});
