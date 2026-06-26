#!/usr/bin/env node
/**
 * set-token.js - 保存 token 到 .env
 * 用法: node set-token.js <token>
 */
const fs = require('fs');
const path = require('path');

const token = process.argv[2];
if (!token) {
  console.error('Usage: node set-token.js <token>');
  process.exit(1);
}

const envPath = path.join(__dirname, '..', '.env');
fs.writeFileSync(envPath, `ELASTOLINK_TOKEN=${token}\n`);
console.log('Token saved to .env');
