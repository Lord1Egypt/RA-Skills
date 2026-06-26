/**
 * 行为模拟引擎
 */

function randInt(min, max) { return Math.floor(Math.random() * (max - min + 1)) + min; }

async function randomDelay(min, max) {
  await new Promise(r => setTimeout(r, randInt(min, max)));
}

function randomPick(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function loadKeywords(path) {
  try {
    const fs = require('fs');
    if (fs.existsSync(path)) {
      const lines = fs.readFileSync(path, 'utf-8').split('\n').map(l => l.trim()).filter(l => l);
      if (lines.length > 0) return lines;
    }
  } catch (e) {}
  return [
    'basketball jersey', 'football jersey', 'baseball jersey',
    'NBA jerseys', 'NFL jerseys', 'MLB jerseys',
    'custom sports jersey', 'team apparel', 'sports hoodies',
    'vintage sportswear', 'college football gear',
  ];
}

module.exports = { randomDelay, randomPick, loadKeywords };
