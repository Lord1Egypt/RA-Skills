#!/usr/bin/env node

// Simple wrapper around bc
const { spawn } = require('child_process');

function runBc(expr) {
  return new Promise((resolve, reject) => {
    const bc = spawn('bc', ['-l', '-q']);
    let out = '';
    let err = '';
    bc.stdout.on('data', chunk => (out += chunk));
    bc.stderr.on('data', chunk => (err += chunk));
    bc.on('error', reject);
    bc.on('close', code => {
      if (code !== 0) reject(new Error(err.trim() || `bc exited with code ${code}`));
      else resolve(out.trim());
    });
    bc.stdin.write(expr + '\n');
    bc.stdin.end();
  });
}

async function main() {
  const expr = process.argv.slice(2).join(' ');
  if (!expr) {
    // read from stdin
    let input = '';
    process.stdin.setEncoding('utf8');
    for await (const chunk of process.stdin) input += chunk;
    if (!input.trim()) {
      console.error('No expression provided');
      process.exit(1);
    }
    runBc(input.trim()).then(console.log).catch(err => {
      console.error(err.message);
      process.exit(1);
    });
  } else {
    try {
      const result = await runBc(expr);
      console.log(result);
    } catch (err) {
      console.error(err.message);
      process.exit(1);
    }
  }
}

if (require.main === module) main();
