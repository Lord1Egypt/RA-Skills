#!/usr/bin/env node
/**
 * Generate OG image for The Agency
 * Creates a 1200x630 PNG with pixel-art style text
 */

const { createCanvas } = require('canvas');
const fs = require('fs');
const path = require('path');

const W = 1200;
const H = 630;

const canvas = createCanvas(W, H);
const ctx = canvas.getContext('2d');

// Dark background
ctx.fillStyle = '#0a0a0f';
ctx.fillRect(0, 0, W, H);

// Subtle grid pattern
ctx.fillStyle = 'rgba(42,42,62,0.3)';
for (let x = 0; x < W; x += 32) {
  for (let y = 0; y < H; y += 32) {
    if ((Math.floor(x / 32) + Math.floor(y / 32)) % 2 === 0) {
      ctx.fillRect(x, y, 32, 32);
    }
  }
}

// Vignette
const vignette = ctx.createRadialGradient(W/2, H/2, 100, W/2, H/2, 600);
vignette.addColorStop(0, 'rgba(0,0,0,0)');
vignette.addColorStop(1, 'rgba(0,0,0,0.5)');
ctx.fillStyle = vignette;
ctx.fillRect(0, 0, W, H);

// "THE AGENCY" title
ctx.fillStyle = '#ffffff';
ctx.font = 'bold 96px monospace';
ctx.textAlign = 'center';
ctx.textBaseline = 'middle';
ctx.fillText('THE AGENCY', W/2, H/2 - 80);

// Glow effect behind title
ctx.shadowColor = '#9333ea';
ctx.shadowBlur = 30;
ctx.fillStyle = '#ffffff';
ctx.fillText('THE AGENCY', W/2, H/2 - 80);
ctx.shadowBlur = 0;

// Subtitle
ctx.fillStyle = '#9ca3af';
ctx.font = '32px monospace';
ctx.fillText('11 AI Agents. One Office. Live.', W/2, H/2 + 10);

// Agent dots
const agentColors = [
  '#9333ea', '#3b82f6', '#22c55e', '#14b8a6', '#ec4899',
  '#ef4444', '#f97316', '#eab308', '#6b7280', '#06b6d4', '#94a3b8'
];
const dotStartX = W/2 - (agentColors.length * 28) / 2;
for (let i = 0; i < agentColors.length; i++) {
  ctx.beginPath();
  ctx.arc(dotStartX + i * 28 + 14, H/2 + 70, 8, 0, Math.PI * 2);
  ctx.fillStyle = agentColors[i];
  ctx.fill();
  // Inner glow
  ctx.beginPath();
  ctx.arc(dotStartX + i * 28 + 14, H/2 + 70, 4, 0, Math.PI * 2);
  ctx.fillStyle = agentColors[i] + '88';
  ctx.fill();
}

// "Built with OpenClaw" at bottom
ctx.fillStyle = '#4b5563';
ctx.font = '22px monospace';
ctx.fillText('Built with OpenClaw 🦞', W/2, H - 50);

// Accent line
ctx.fillStyle = '#9333ea';
ctx.fillRect(W/2 - 200, H/2 + 110, 400, 2);

// Save
const outPath = path.join(__dirname, '..', 'public', 'og-image.png');
const buffer = canvas.toBuffer('image/png');
fs.writeFileSync(outPath, buffer);
console.log(`OG image saved to ${outPath}`);
