#!/usr/bin/env node
const fs = require('fs');

const svg = fs.readFileSync(process.argv[2] || 'alice.svg', 'utf8');

const w = +svg.match(/width="(\d+)"/)[1];
const h = +svg.match(/height="(\d+)"/)[1];
const grid = Array.from({ length: h }, () => Array(w).fill([0, 0, 0]));

for (const m of svg.matchAll(/d="M(\d+) (\d+)v1h(\d+)v-1"[^>]*fill="(#[0-9a-fA-F]{6})/g)) {
  const x = +m[1], y = +m[2], dw = +m[3], hex = m[4];
  const r = parseInt(hex.slice(1, 3), 16);
  const g = parseInt(hex.slice(3, 5), 16);
  const b = parseInt(hex.slice(5, 7), 16);
  for (let col = x; col < Math.min(x + dw, w); col++) grid[y][col] = [r, g, b];
}

for (const row of grid) {
  console.log(row.map(([r, g, b]) => `\x1b[48;2;${r};${g};${b}m  \x1b[0m`).join(''));
}