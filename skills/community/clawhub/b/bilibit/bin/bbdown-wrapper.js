#!/usr/bin/env node

/**
 * BBDown wrapper
 * 调用本地安装的 BBDown
 */

const { spawnSync } = require('child_process');
const path = require('path');

const bbdownPath = path.join(__dirname, '..', 'node_modules', '.bin', 'BBDown');

const args = process.argv.slice(2);

const result = spawnSync(bbdownPath, args, {
  stdio: 'inherit',
  shell: true
});

process.exit(result.status || 0);
