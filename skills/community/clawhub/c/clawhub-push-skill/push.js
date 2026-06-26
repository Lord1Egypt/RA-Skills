#!/usr/bin/env node
/**
 * ClawHub Push Skill
 * 一键推送 skill 到 ClawHub registry，自动处理 acceptLicenseTerms bug
 */

import fs from 'fs/promises';
import path from 'path';
import { execSync } from 'child_process';
import yaml from 'js-yaml';

const REGISTRY = 'https://clawhub.ai';
const API_BASE = `${REGISTRY}/api/v1`;

// Token 路径（支持新旧版本）
const TOKEN_PATHS = [
  `${process.env.HOME}/.config/clawhub/token.json`,
  `${process.env.HOME}/.clawhub/token`,
];

// 需要排除的文件/目录
const EXCLUDE_PATTERNS = [
  '.git',
  'node_modules',
  '.DS_Store',
  '*.log',
];

/**
 * 解析 SKILL.md 的 frontmatter
 */
function parseFrontmatter(content) {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) throw new Error('No frontmatter found');
  try {
    const fm = yaml.load(match[1]);
    if (!fm) throw new Error('Frontmatter parsed as null');
    return fm;
  } catch (e) {
    throw new Error(`YAML parse error: ${e.message}`);
  }
}

/**
 * 获取 ClawHub token
 */
async function getToken() {
  for (const tokenPath of TOKEN_PATHS) {
    try {
      const content = await fs.readFile(tokenPath, 'utf8');
      // 新版 JSON 格式
      if (tokenPath.endsWith('.json')) {
        const parsed = JSON.parse(content);
        if (parsed.token) return parsed.token;
      } else {
        // 旧版纯文本
        return content.trim();
      }
    } catch {}
  }
  throw new Error('Token not found. Run `clawhub login` first.');
}

/**
 * 检查文件是否应该被排除
 */
function shouldExclude(filePath) {
  const base = path.basename(filePath);
  return EXCLUDE_PATTERNS.some(pattern => {
    if (pattern.includes('*')) {
      const regex = new RegExp(pattern.replace('*', '.*'));
      return regex.test(base);
    }
    return base === pattern || filePath.includes(`/${pattern}/`);
  });
}

/**
 * 获取 skill 目录下的所有文件
 */
async function getSkillFiles(skillPath) {
  const files = [];
  
  async function walk(dir, relativePath = '') {
    try {
      const items = await fs.readdir(dir);
      for (const item of items) {
        if (shouldExclude(item)) continue;
        
        const fullPath = path.join(dir, item);
        const relPath = relativePath ? `${relativePath}/${item}` : item;
        
        const stat = await fs.stat(fullPath);
        if (stat.isDirectory()) {
          await walk(fullPath, relPath);
        } else {
          const content = await fs.readFile(fullPath, 'utf8');
          files.push({
            path: relPath,
            content,
            fullPath
          });
        }
      }
    } catch (e) {
      console.error(`Error reading ${dir}: ${e.message}`);
    }
  }
  
  await walk(skillPath);
  return files;
}

/**
 * 推送 skill 到 ClawHub
 */
async function pushSkill(skillPath, options = {}) {
  skillPath = path.resolve(skillPath || '.');
  const skillName = path.basename(skillPath);
  
  console.log(`🚀 Publishing ${skillName}...`);
  
  // 1. 读取 SKILL.md 获取元数据
  const skillMdPath = path.join(skillPath, 'SKILL.md');
  try {
    await fs.access(skillMdPath);
  } catch {
    throw new Error('SKILL.md not found');
  }
  
  const skillMdContent = await fs.readFile(skillMdPath, 'utf8');
  const fm = parseFrontmatter(skillMdContent);
  
  const slug = options.slug || fm.slug || fm.name.toLowerCase().replace(/\s+/g, '-');
  const displayName = options.name || fm.name;
  const version = options.version || fm.version;
  
  if (!slug) throw new Error('Missing slug');
  if (!displayName) throw new Error('Missing name');
  if (!version) throw new Error('Missing version');
  
  console.log(`   📦 ${displayName} v${version}`);
  console.log(`   🏷️  Slug: ${slug}`);
  
  // 2. 获取 token
  const token = await getToken();
  console.log(`   🔑 Token loaded`);
  
  // 3. 获取所有文件
  const files = await getSkillFiles(skillPath);
  if (files.length === 0) {
    throw new Error('No files found');
  }
  console.log(`   📄 ${files.length} files`);
  
  // 4. 构建 FormData
  const payload = {
    slug,
    version,
    displayName,
    tags: ['latest'],
    acceptLicenseTerms: true,
  };
  
  if (fm.description) {
    payload.description = fm.description;
  }
  
  // 5. 发送请求
  const formData = new FormData();
  formData.append('payload', JSON.stringify(payload));
  
  // 添加文件
  for (const file of files) {
    const blob = new Blob([file.content], { type: 'text/plain' });
    formData.append('files', blob, file.path);
  }
  
  // 6. 调用 API
  const url = `${API_BASE}/skills`;
  
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
      },
      body: formData,
    });
    
    const result = await response.json();
    
    if (response.ok) {
      console.log(`✅ Published!`);
      console.log(`   🌐 https://clawhub.ai/skills/${slug}`);
      console.log(`   📦 Skill ID: ${result.skillId}`);
      console.log(`   📝 Version ID: ${result.versionId}`);
      console.log(`   🔍 Embedding ID: ${result.embeddingId}`);
      return result;
    } else {
      throw new Error(result.error || JSON.stringify(result));
    }
  } catch (error) {
    throw new Error(`Publish failed: ${error.message}`);
  }
}

// CLI
const args = process.argv.slice(2);
const skillPath = args[0] || '.';

// 解析命令行参数
const options = {};
for (let i = 1; i < args.length; i++) {
  if (args[i] === '--slug' && args[i + 1]) {
    options.slug = args[++i];
  } else if (args[i] === '--version' && args[i + 1]) {
    options.version = args[++i];
  } else if (args[i] === '--name' && args[i + 1]) {
    options.name = args[++i];
  }
}

pushSkill(skillPath, options).catch(error => {
  console.error(`❌ ${error.message}`);
  process.exit(1);
});
