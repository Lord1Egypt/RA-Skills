#!/usr/bin/env node
/**
 * 保存日报到文件
 * Usage: node save-report.mjs <content>
 */

import { writeFileSync, mkdirSync, existsSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';

const REPORTS_DIR = process.env.REPORTS_DIR || join(homedir(), 'reports');
const today = new Date().toISOString().split('T')[0];
const filename = `${today}.md`;
const filepath = join(REPORTS_DIR, filename);

// 确保目录存在
if (!existsSync(REPORTS_DIR)) {
  mkdirSync(REPORTS_DIR, { recursive: true });
}

// 从命令行参数获取内容
const content = process.argv[2];

if (!content) {
  console.error('Usage: node save-report.mjs <content>');
  process.exit(1);
}

// 写入文件
writeFileSync(filepath, content, 'utf-8');
console.log(`日报已保存: ${filepath}`);