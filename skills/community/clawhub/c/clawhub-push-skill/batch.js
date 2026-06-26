#!/usr/bin/env node
/**
 * ClawHub Batch Push
 * 批量推送 skills 目录下所有变更的 skill
 */

import fs from 'fs/promises';
import path from 'path';
import { execSync } from 'child_process';

const REGISTRY = 'https://clawhub.ai';

/**
 * 检查 skill 是否有更新
 */
async function needsUpdate(skillPath) {
  const skillMdPath = path.join(skillPath, 'SKILL.md');
  try {
    const content = await fs.readFile(skillMdPath, 'utf8');
    const match = content.match(/^---\n([\s\S]*?)\n---/);
    if (!match) return false;
    
    // TODO: 可以添加逻辑检查 registry 上的版本
    return true;
  } catch {
    return false;
  }
}

/**
 * 批量推送
 */
async function batchPush(skillsDir) {
  skillsDir = path.resolve(skillsDir || '.');
  
  console.log(`🔍 Scanning ${skillsDir}...`);
  
  const items = await fs.readdir(skillsDir);
  const skills = [];
  
  for (const item of items) {
    const itemPath = path.join(skillsDir, item);
    const stat = await fs.stat(itemPath);
    
    if (stat.isDirectory()) {
      const skillMdPath = path.join(itemPath, 'SKILL.md');
      try {
        await fs.access(skillMdPath);
        if (await needsUpdate(itemPath)) {
          skills.push(itemPath);
        }
      } catch {}
    }
  }
  
  console.log(`📦 Found ${skills.length} skills to push\n`);
  
  for (const skillPath of skills) {
    const skillName = path.basename(skillPath);
    console.log(`\n${'='.repeat(60)}`);
    console.log(`Pushing ${skillName}...`);
    console.log('='.repeat(60));
    
    try {
      const result = await import('./push.js').then(m => m.pushSkill(skillPath));
      console.log('');
    } catch (error) {
      console.error(`❌ Failed: ${error.message}\n`);
    }
  }
  
  console.log('\n✅ Batch push complete!');
}

// CLI
const args = process.argv.slice(2);
const skillsDir = args[0] || './skills';

batchPush(skillsDir).catch(error => {
  console.error(`❌ ${error.message}`);
  process.exit(1);
});
