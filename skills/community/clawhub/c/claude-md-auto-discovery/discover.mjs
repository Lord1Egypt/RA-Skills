#!/usr/bin/env node
/**
 * CLAUDE.md Auto-Discovery
 * 
 * 自动发现并加载项目根目录的 CLAUDE.md 文件
 * 参考 Claude Code 实现
 * 
 * 使用方式: node claude-md-discover.js [--cwd /path/to/dir]
 */

import { readFileSync, existsSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const MAX_CHARS = 40000;

function discoverClaudeMdFiles(cwd = process.cwd()) {
  const paths = [];
  let current = resolve(cwd);
  
  // 向上查找 4 层
  for (let i = 0; i < 4; i++) {
    paths.push(resolve(current, 'CLAUDE.md'));
    paths.push(resolve(current, ' CLAUDE.md')); // 空格前缀
    const parent = dirname(current);
    if (parent === current) break;
    current = parent;
  }
  
  // 去重
  const seen = new Set();
  const found = [];
  for (const p of paths) {
    if (!seen.has(p) && existsSync(p)) {
      seen.add(p);
      found.push(p);
    }
  }
  return found;
}

function loadContent(files) {
  if (!files?.length) return null;
  
  const contents = [];
  for (const f of files.reverse()) { // 逆序，后面的优先级高
    try {
      contents.push(`# ${f}\n\n${readFileSync(f, 'utf-8')}`);
    } catch (e) {
      // skip
    }
  }
  
  if (!contents.length) return null;
  
  let combined = contents.join('\n\n---\n\n');
  if (combined.length > MAX_CHARS) {
    combined = combined.slice(0, MAX_CHARS) + '\n\n... (truncated)';
  }
  return combined;
}

// 执行
const cwd = process.argv[2] === '--cwd' ? process.argv[3] : process.cwd();
const files = discoverClaudeMdFiles(cwd);
const content = loadContent(files);

if (content) {
  console.log(content);
} else {
  console.log('No CLAUDE.md files found');
}