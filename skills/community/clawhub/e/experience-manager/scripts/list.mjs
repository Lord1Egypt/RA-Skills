#!/usr/bin/env node
/**
 * 经验列表脚本
 * 显示所有经验包及学习状态（支持按 Agent 查看）
 */

import fs from 'fs';
import path from 'path';
import yaml from 'js-yaml';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const EXPERIENCES_DIR = path.join(process.env.HOME, '.openclaw', 'experiences');
const PACKAGES_DIR = path.join(EXPERIENCES_DIR, 'packages');
const EXTRACTED_DIR = path.join(EXPERIENCES_DIR, 'extracted');
const INDEX_FILE = path.join(EXPERIENCES_DIR, 'index.json');

// 读取索引（新格式：按 Agent 分组）
function readIndex() {
  if (!fs.existsSync(INDEX_FILE)) {
    return { agents: {} };
  }
  const data = JSON.parse(fs.readFileSync(INDEX_FILE, 'utf8'));
  // 兼容旧格式
  if (data.experiences && !data.agents) {
    return { agents: {} };
  }
  return data;
}

// 扫描 packages 目录
function scanPackages() {
  if (!fs.existsSync(PACKAGES_DIR)) {
    return [];
  }
  
  const packages = [];
  const files = fs.readdirSync(PACKAGES_DIR);
  
  for (const file of files) {
    if (file.endsWith('.zip')) {
      const name = path.basename(file, '.zip');
      packages.push({
        name,
        path: path.join(PACKAGES_DIR, file)
      });
    }
  }
  
  return packages;
}

// 读取经验包信息
function readPackageInfo(name) {
  const extractPath = path.join(EXTRACTED_DIR, name);
  const expPath = path.join(extractPath, 'exp.yml');
  
  if (!fs.existsSync(expPath)) {
    return null;
  }
  
  try {
    const content = fs.readFileSync(expPath, 'utf8');
    return yaml.load(content);
  } catch (err) {
    return null;
  }
}

// 获取经验类型
function getExpType(info) {
  if (!info) return 'unknown';
  // v1 格式
  if (info.schema?.includes('v1')) {
    if (info.soul && info.agents && info.tools) return 'full';
    if (info.soul) return 'soul+agents';
    if (info.agents) return 'agents';
    return 'basic';
  }
  // 旧格式
  return info.core?.type || 'unknown';
}

// 获取经验版本
function getExpVersion(info) {
  if (!info) return 'unknown';
  // v1 格式
  if (info.metadata?.version) return info.metadata.version;
  // 旧格式
  return info.meta?.version || 'unknown';
}

// 获取经验标题
function getExpTitle(info, name) {
  if (!info) return name;
  // v1 格式
  if (info.description) return info.description;
  // 旧格式
  return info.meta?.title || name;
}

// 主函数
function main() {
  const args = process.argv.slice(2);
  const targetAgent = args.find(arg => arg.startsWith('--agent='))?.replace('--agent=', '');
  
  console.log('📚 经验列表\n');
  
  const index = readIndex();
  const packages = scanPackages();
  
  if (packages.length === 0) {
    console.log('暂无经验包');
    console.log('\n💡 提示: 使用 "记录经验 <描述>" 来创建经验包');
    return;
  }
  
  // 如果指定了 Agent，只显示该 Agent 的学习记录
  if (targetAgent) {
    showAgentExperiences(index, targetAgent, packages);
    return;
  }
  
  // 显示所有 Agent 的学习统计
  showAllAgents(index, packages);
}

// 显示指定 Agent 的学习记录
function showAgentExperiences(index, agentName, packages) {
  const agentData = index.agents?.[agentName];
  
  if (!agentData || !agentData.experiences || agentData.experiences.length === 0) {
    console.log(`Agent "${agentName}" 暂无学习记录`);
    return;
  }
  
  console.log(`🎯 Agent: ${agentName}`);
  console.log(`📁 工作空间: ${agentData.workspace || 'unknown'}\n`);
  
  console.log(`✅ 已学习 (${agentData.experiences.length})`);
  for (const exp of agentData.experiences) {
    console.log(`  ${exp.name.padEnd(30)} v${exp.version.padEnd(6)} ${exp.title}`);
    console.log(`     学习时间: ${new Date(exp.learned_at).toLocaleString('zh-CN')}`);
    console.log(`     应用到: ${exp.applied_to?.join(', ') || 'unknown'}`);
  }
}

// 显示所有 Agent 的学习统计
function showAllAgents(index, packages) {
  // 收集所有经验包信息
  const allPackages = [];
  for (const pkg of packages) {
    const info = readPackageInfo(pkg.name);
    allPackages.push({
      name: pkg.name,
      version: getExpVersion(info),
      title: getExpTitle(info, pkg.name),
      type: getExpType(info)
    });
  }
  
  // 获取所有 Agent
  const agents = Object.keys(index.agents || {});
  
  if (agents.length === 0) {
    console.log('暂无学习记录');
    console.log(`\n⏳ 未学习经验包 (${allPackages.length})`);
    for (const pkg of allPackages) {
      console.log(`  ${pkg.name.padEnd(30)} v${pkg.version.padEnd(6)} ${pkg.title}`);
    }
    return;
  }
  
  // 显示每个 Agent 的学习记录
  for (const agentName of agents) {
    const agentData = index.agents[agentName];
    const learnedNames = new Set(agentData.experiences?.map(e => e.name) || []);
    
    console.log(`🎯 ${agentName}`);
    console.log(`   已学习: ${learnedNames.size} 个经验包`);
    
    // 显示该 Agent 学习的经验
    for (const exp of (agentData.experiences || [])) {
      console.log(`     ✅ ${exp.name} v${exp.version}`);
    }
    console.log();
  }
  
  // 显示未学习的经验包
  const allLearned = new Set();
  for (const agentData of Object.values(index.agents || {})) {
    for (const exp of (agentData.experiences || [])) {
      allLearned.add(exp.name);
    }
  }
  
  const unlearned = allPackages.filter(pkg => !allLearned.has(pkg.name));
  
  if (unlearned.length > 0) {
    console.log(`⏳ 未学习 (${unlearned.length})`);
    for (const pkg of unlearned) {
      console.log(`  ${pkg.name.padEnd(30)} v${pkg.version.padEnd(6)} ${pkg.title}`);
    }
  }
  
  // 统计
  console.log(`\n总计: ${packages.length} 个经验包`);
  console.log(`  已学习: ${allLearned.size}`);
  console.log(`  未学习: ${unlearned.length}`);
  console.log(`  Agent 数: ${agents.length}`);
  
  console.log('\n💡 提示:');
  console.log('  查看指定 Agent: node list.mjs --agent=严哥');
}

main();
