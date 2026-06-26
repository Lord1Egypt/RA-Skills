#!/usr/bin/env node

/**
 * City Life Copilot - 依赖安装脚本 v2.0
 * 具备真实系统终端调用能力，自动安装所有必需依赖
 */

const { execSync, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

// ============================================================================
// 配置与常量
// ============================================================================

// 核心依赖清单（精简版）
const REQUIRED_DEPENDENCIES = [
  {
    name: 'amap-lbs-skill',
    type: 'direct',
    source: 'https://www.modelscope.cn/skills/@AMap-Web/amap-lbs-skill',
    description: '高德地图综合服务'
  },
  {
    name: 'agent-browser',
    type: 'skillhub',
    description: '浏览器自动化（⚠️ 小红书等反爬虫网站必须使用）',
    required: true
  },
  {
    name: 'web-fetch',
    type: 'clawhub',
    source: 'https://clawhub.ai/dlutwuwei/web-anti-crawl-fetch',
    description: '网页内容抓取（普通网页）',
    required: false,
    note: '可选：仅用于无强反爬虫机制的普通网页'
  }
];

const SKILLS_DIR = path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'workspace', 'skills');
const SKILLHUB_CONFIG_PATH = path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'config', 'skillhub.json');

// ============================================================================
// 工具函数
// ============================================================================

/**
 * 执行系统命令并输出结果
 * @param {string} command - 要执行的命令
 * @param {boolean} silent - 是否静默执行
 */
function execCommand(command, silent = false) {
  if (!silent) {
    console.log(`\n📦 执行命令：${command}\n`);
  }
  
  try {
    const result = execSync(command, {
      stdio: silent ? 'pipe' : 'inherit',
      encoding: 'utf-8'
    });
    return { success: true, output: result };
  } catch (error) {
    console.error(`❌ 命令执行失败：${error.message}`);
    return { success: false, error: error.message };
  }
}

/**
 * 检测指定技能是否已安装
 * @param {string} skillName - 技能名称
 * @returns {boolean} - 是否已安装
 */
function checkSkillInstalled(skillName) {
  const skillPath = path.join(SKILLS_DIR, skillName);
  
  if (fs.existsSync(skillPath)) {
    const skillMdPath = path.join(skillPath, 'SKILL.md');
    return fs.existsSync(skillMdPath);
  }
  
  return false;
}

/**
 * 检测 SkillHub 是否已安装
 * @returns {boolean} - 是否已安装
 */
function checkSkillHubInstalled() {
  // 检查配置文件是否存在
  if (fs.existsSync(SKILLHUB_CONFIG_PATH)) {
    return true;
  }
  
  // 检查 skillhub 命令是否可用
  try {
    execSync('which skillhub', { stdio: 'pipe' });
    return true;
  } catch (e) {
    return false;
  }
}

/**
 * 安装 SkillHub
 */
function installSkillHub() {
  console.log('\n🔧 SkillHub 未安装，开始安装...\n');
  
  // 参考安装指南：https://skillhub.cn/install/skillhub.md
  const installCommands = [
    'npm install -g @skillhub/cli',
    'skillhub init'
  ];
  
  for (const cmd of installCommands) {
    const result = execCommand(cmd);
    if (!result.success) {
      console.error('❌ SkillHub 安装失败，请手动安装后重试');
      console.error('安装指南：https://skillhub.cn/install/skillhub.md');
      return false;
    }
  }
  
  console.log('\n✅ SkillHub 安装成功\n');
  return true;
}

/**
 * 通过 SkillHub 安装技能
 * @param {string} skillName - 技能名称
 */
function installViaSkillHub(skillName) {
  console.log(`\n📦 通过 SkillHub 安装：${skillName}`);
  
  const command = `skillhub install ${skillName}`;
  const result = execCommand(command);
  
  if (result.success) {
    console.log(`✅ ${skillName} 安装成功`);
    return true;
  } else {
    console.error(`❌ ${skillName} 安装失败`);
    return false;
  }
}

/**
 * 直接安装技能（从 ModelScope）
 * @param {string} skillName - 技能名称
 * @param {string} source - 源地址
 */
function installDirect(skillName, source) {
  console.log(`\n📦 直接安装：${skillName}`);
  console.log(`源：${source}`);
  
  const command = `npx skills add ${source}`;
  const result = execCommand(command);
  
  if (result.success) {
    console.log(`✅ ${skillName} 安装成功`);
    return true;
  } else {
    console.error(`❌ ${skillName} 安装失败`);
    return false;
  }
}

/**
 * 从 ClawHub 安装技能
 * @param {string} skillName - 技能名称
 * @param {string} source - ClawHub URL
 */
function installFromClawHub(skillName, source) {
  console.log(`\n📦 从 ClawHub 安装：${skillName}`);
  console.log(`源：${source}`);
  
  // 使用 git clone 或 curl 下载技能
  const tempDir = path.join('/tmp', 'clawhub-install-' + Date.now());
  
  try {
    // 创建临时目录
    fs.mkdirSync(tempDir, { recursive: true });
    
    // 使用 git clone 下载技能
    console.log(`🔧 正在克隆技能仓库...`);
    const cloneResult = execCommand(`git clone ${source} ${tempDir}`, true);
    
    if (!cloneResult.success) {
      // 如果 git 失败，尝试使用 curl 下载
      console.log(`⚠️  git clone 失败，尝试使用 curl 下载...`);
      const curlResult = execCommand(`curl -L ${source}/archive/main.zip -o ${tempDir}/skill.zip`, true);
      if (curlResult.success) {
        execCommand(`unzip ${tempDir}/skill.zip -d ${tempDir}`, true);
      }
    }
    
    // 将技能复制到 skills 目录
    const skillSourcePath = path.join(tempDir, 'web-fetch');
    const skillDestPath = path.join(SKILLS_DIR, skillName);
    
    if (fs.existsSync(skillSourcePath)) {
      console.log(`📦 正在复制技能文件...`);
      execCommand(`cp -r ${skillSourcePath} ${skillDestPath}`);
      console.log(`✅ ${skillName} 安装成功`);
      
      // 清理临时目录
      execCommand(`rm -rf ${tempDir}`, true);
      return true;
    } else {
      console.error(`❌ 技能目录不存在：${skillSourcePath}`);
      return false;
    }
  } catch (error) {
    console.error(`❌ ${skillName} 安装失败：${error.message}`);
    // 清理临时目录
    try { execCommand(`rm -rf ${tempDir}`, true); } catch (e) {}
    return false;
  }
}

// ============================================================================
// 主安装流程
// ============================================================================

function main() {
  console.log('╔══════════════════════════════════════════════════════════╗');
  console.log('║       City Life Copilot - 依赖安装程序 v2.0              ║');
  console.log('╚══════════════════════════════════════════════════════════╝\n');
  
  const missingDeps = [];
  const installedDeps = [];
  
  // 阶段 1: 检查依赖状态
  console.log('🔍 阶段 1: 检查依赖状态...\n');
  
  REQUIRED_DEPENDENCIES.forEach(dep => {
    // 内置技能直接视为已安装
    if (dep.type === 'builtin') {
      console.log(`✅ ${dep.name} - 内置技能（已就绪）`);
      installedDeps.push(dep);
      return;
    }
    
    const isInstalled = checkSkillInstalled(dep.name);
    
    if (isInstalled) {
      console.log(`✅ ${dep.name} - 已安装`);
      installedDeps.push(dep);
    } else {
      console.log(`❌ ${dep.name} - 未安装`);
      missingDeps.push(dep);
    }
  });
  
  // 如果没有缺失依赖，直接退出
  if (missingDeps.length === 0) {
    console.log('\n' + '═'.repeat(60));
    console.log('✅ 依赖检查完毕，所有核心组件已就绪！\n');
    console.log('🎉 City Life Copilot 已准备就绪，可以开始使用。\n');
    process.exit(0);
  }
  
  // 阶段 2: 安装缺失依赖
  console.log('\n' + '═'.repeat(60));
  console.log(`📦 发现 ${missingDeps.length} 个缺失依赖，开始安装...\n`);
  
  let installSuccessCount = 0;
  
  missingDeps.forEach(dep => {
    console.log(`\n--- 安装 ${dep.name} (${dep.description}) ---`);
    
    if (dep.type === 'builtin') {
      // 内置技能，跳过安装
      console.log(`ℹ️  ${dep.name} 是内置技能，无需安装`);
      installSuccessCount++;
      return;
    }
    
    if (dep.type === 'direct') {
      // 直接安装（如 amap-lbs-skill）
      const success = installDirect(dep.name, dep.source);
      if (success) installSuccessCount++;
      return;
    }
    
    if (dep.type === 'skillhub') {
      // 通过 SkillHub 安装（如 agent-browser）
      
      // 先确保 SkillHub 已安装
      if (!checkSkillHubInstalled()) {
        console.log('⚠️  SkillHub 未安装，先安装 SkillHub...');
        const skillHubSuccess = installSkillHub();
        if (!skillHubSuccess) {
          console.error(`❌ ${dep.name} 安装中止（SkillHub 安装失败）`);
          return;
        }
      }
      
      // 通过 SkillHub 安装技能
      const success = installViaSkillHub(dep.name);
      if (success) installSuccessCount++;
      return;
    }
    
    if (dep.type === 'clawhub') {
      // 从 ClawHub 安装（如 web-fetch）
      const success = installFromClawHub(dep.name, dep.source);
      if (success) installSuccessCount++;
      return;
    }
  });
  
  // 阶段 3: 总结
  console.log('\n' + '═'.repeat(60));
  console.log('📊 安装总结\n');
  console.log(`应安装：${missingDeps.length}`);
  console.log(`成功：${installSuccessCount}`);
  console.log(`失败：${missingDeps.length - installSuccessCount}\n`);
  
  if (installSuccessCount === missingDeps.length) {
    console.log('✅ 所有依赖安装成功！\n');
    console.log('🎉 City Life Copilot 已准备就绪，可以开始使用。\n');
    console.log('运行测试：node scripts/dispatcher.js "周末去哪玩"\n');
    process.exit(0);
  } else {
    console.log('⚠️  部分依赖安装失败，请检查错误信息后重试。\n');
    console.log('手动安装指南：');
    console.log('  - amap-lbs-skill: npx skills add https://www.modelscope.cn/skills/@AMap-Web/amap-lbs-skill');
    console.log('  - agent-browser: skillhub install agent-browser');
    console.log('  - web-fetch: 访问 https://clawhub.ai/dlutwuwei/web-anti-crawl-fetch 下载安装\n');
    process.exit(1);
  }
}

// ============================================================================
// 导出接口
// ============================================================================

module.exports = {
  checkSkillInstalled,
  checkSkillHubInstalled,
  installSkillHub,
  installViaSkillHub,
  installDirect,
  REQUIRED_DEPENDENCIES
};

// 执行主函数
main();
