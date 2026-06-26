#!/usr/bin/env node
/**
 * get-token.js - 读取保存的 token
 * 路径: D:\workspace\demo\elastolink\scripts\get-token.js
 */
const fs = require('fs');
const path = require('path');

const envPath = path.join(__dirname, '..', '.env');

if (!fs.existsSync(envPath)) {
  console.log('NO_TOKEN');
  process.exit(1);
}

const content = fs.readFileSync(envPath, 'utf-8');
const match = content.match(/ELASTOLINK_TOKEN=(.+)/);
if (match) {
  console.log(match[1].trim());
} else {
  console.log('NO_TOKEN');
  process.exit(1);
}
