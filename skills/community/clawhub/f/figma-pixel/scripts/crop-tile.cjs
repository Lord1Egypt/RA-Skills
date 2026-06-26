#!/usr/bin/env node
// Usage: node crop-tile.cjs <src.png> <dst.png> <y> <height>
'use strict';
const { PNG } = require('pngjs');
const fs = require('fs');

const [src, dst, yStr, hStr] = process.argv.slice(2);
if (!src || !dst || !yStr || !hStr) {
  console.error('Usage: crop-tile.cjs <src.png> <dst.png> <y> <height>');
  process.exit(1);
}

const y = parseInt(yStr, 10);
const h = parseInt(hStr, 10);
const img = PNG.sync.read(fs.readFileSync(src));
const out = new PNG({ width: img.width, height: h });

for (let row = 0; row < h; row++)
  for (let col = 0; col < img.width; col++) {
    const si = ((y + row) * img.width + col) * 4;
    const di = (row * img.width + col) * 4;
    out.data[di]   = img.data[si];
    out.data[di+1] = img.data[si+1];
    out.data[di+2] = img.data[si+2];
    out.data[di+3] = img.data[si+3];
  }

fs.writeFileSync(dst, PNG.sync.write(out));
