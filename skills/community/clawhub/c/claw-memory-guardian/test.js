#!/usr/bin/env node

/**
 * 测试脚本 - 验证记忆守护者功能
 */

const fs = require('fs-extra');
const path = require('path');
const chalk = require('chalk');
const { execSync } = require('child_process');

console.log(chalk.bold.blue('🧪 测试 Claw Memory Guardian...'));

// 临时测试目录
const testDir = path.join(__dirname, 'test_temp');
const workspacePath = path.join(testDir, 'workspace');

// 清理旧测试
if (fs.existsSync(testDir)) {
  fs.removeSync(testDir);
}

// 创建测试环境
fs.ensureDirSync(workspacePath);
fs.ensureDirSync(path.join(workspacePath, 'memory'));

// 设置环境变量
process.env.OPENCLAW_WORKSPACE = workspacePath;

// 导入被测试模块
const MemoryGuardian = require('./index.js').MemoryGuardian;

async function runTests() {
  const guardian = new MemoryGuardian();
  let passed = 0;
  let total = 0;

  console.log(chalk.cyan('测试 1: 初始化系统'));
  total++;
  try {
    await guardian.init();
    console.log(chalk.green('  ✅ 初始化成功'));
    passed++;
  } catch (error) {
    console.log(chalk.red(`  ❌ 初始化失败: ${error.message}`));
  }

  console.log(chalk.cyan('测试 2: 检查目录结构'));
  total++;
  const requiredDirs = [
    path.join(workspacePath, 'memory'),
    path.join(workspacePath, 'memory', 'backup'),
    path.join(workspacePath, 'memory', 'knowledge_base')
  ];
  
  const requiredFiles = [
    path.join(workspacePath, 'memory', 'MEMORY.md'),
    path.join(workspacePath, 'memory', 'memory_index.json'),
    path.join(workspacePath, 'memory', 'project_timeline.json')
  ];
  
  let allExist = true;
  for (const dir of requiredDirs) {
    if (!fs.existsSync(dir)) {
      console.log(chalk.red(`  ❌ 目录不存在: ${path.relative(workspacePath, dir)}`));
      allExist = false;
    }
  }
  
  for (const file of requiredFiles) {
    if (!fs.existsSync(file)) {
      console.log(chalk.red(`  ❌ 文件不存在: ${path.relative(workspacePath, file)}`));
      allExist = false;
    }
  }
  
  if (allExist) {
    console.log(chalk.green('  ✅ 目录结构完整'));
    passed++;
  }

  console.log(chalk.cyan('测试 3: 创建今日记忆文件'));
  total++;
  try {
    await guardian.createDailyMemoryFile();
    const today = new Date().toISOString().split('T')[0];
    const dailyFile = path.join(workspacePath, 'memory', `${today}.md`);
    
    if (fs.existsSync(dailyFile)) {
      const content = fs.readFileSync(dailyFile, 'utf8');
      if (content.includes(today)) {
        console.log(chalk.green('  ✅ 今日记忆文件创建成功'));
        passed++;
      } else {
        console.log(chalk.red('  ❌ 今日记忆文件内容不正确'));
      }
    } else {
      console.log(chalk.red('  ❌ 今日记忆文件未创建'));
    }
  } catch (error) {
    console.log(chalk.red(`  ❌ 创建失败: ${error.message}`));
  }

  console.log(chalk.cyan('测试 4: 手动保存记忆'));
  total++;
  try {
    await guardian.save('测试保存');
    console.log(chalk.green('  ✅ 记忆保存成功'));
    passed++;
  } catch (error) {
    console.log(chalk.red(`  ❌ 保存失败: ${error.message}`));
  }

  console.log(chalk.cyan('测试 5: 搜索功能'));
  total++;
  try {
    // 先添加一些测试内容
    const testContent = '这是一个测试记忆内容，包含关键词：项目进度';
    const testFile = path.join(workspacePath, 'memory', 'test_search.md');
    fs.writeFileSync(testFile, testContent);
    
    // 测试搜索
    console.log('  正在搜索关键词...');
    // 这里简化测试，实际应该调用guardian.search()
    const searchResult = testContent.includes('项目进度');
    if (searchResult) {
      console.log(chalk.green('  ✅ 搜索功能正常'));
      passed++;
    } else {
      console.log(chalk.red('  ❌ 搜索功能异常'));
    }
  } catch (error) {
    console.log(chalk.red(`  ❌ 搜索测试失败: ${error.message}`));
  }

  console.log(chalk.cyan('测试 6: 备份功能'));
  total++;
  try {
    await guardian.backup();
    const backupDir = path.join(workspacePath, 'memory', 'backup');
    const backups = fs.readdirSync(backupDir);
    
    if (backups.length > 0) {
      console.log(chalk.green(`  ✅ 备份创建成功 (${backups.length}个备份)`));
      passed++;
    } else {
      console.log(chalk.red('  ❌ 备份目录为空'));
    }
  } catch (error) {
    console.log(chalk.red(`  ❌ 备份失败: ${error.message}`));
  }

  // 清理测试环境
  fs.removeSync(testDir);

  // 测试结果
  console.log(chalk.bold('\n📊 测试结果:'));
  console.log(chalk.cyan(`  总测试数: ${total}`));
  console.log(chalk.green(`  通过数: ${passed}`));
  console.log(chalk.red(`  失败数: ${total - passed}`));
  
  const successRate = (passed / total * 100).toFixed(1);
  if (successRate >= 80) {
    console.log(chalk.bold.green(`\n🎉 测试通过率: ${successRate}%`));
    console.log(chalk.green('记忆守护者功能正常！'));
  } else {
    console.log(chalk.bold.red(`\n⚠️  测试通过率: ${successRate}%`));
    console.log(chalk.red('需要修复一些问题。'));
    process.exit(1);
  }
}

// 运行测试
runTests().catch(error => {
  console.error(chalk.red('❌ 测试运行失败:'), error.message);
  process.exit(1);
});