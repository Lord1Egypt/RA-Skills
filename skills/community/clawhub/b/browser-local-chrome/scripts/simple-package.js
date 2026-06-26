#!/usr/bin/env node

/**
 * 简单打包脚本（无需依赖）
 * 
 * 用法：node scripts/simple-package.js [版本]
 * 示例：node scripts/simple-package.js 1.1.0
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

const SKILL_DIR = path.join(__dirname, '..');
const VERSION = process.argv[2] || '1.1.0';
const ZIP_FILE = `browser-local-chrome-v${VERSION}.zip`;

console.log('📦 打包 browser-local-chrome 技能...\n');
console.log(`📝 版本：v${VERSION}`);
console.log(`📄 输出：${ZIP_FILE}\n`);

// 使用 PowerShell Compress-Archive (Windows)
function packageWindows() {
  const excludePatterns = [
    'node_modules',
    '*.zip',
    '.git'
  ].join('\",\"');
  
  const command = `
    $files = Get-ChildItem -Path "${SKILL_DIR}" -Recurse -File | 
             Where-Object { 
               $_.FullName -notmatch 'node_modules' -and 
               $_.FullName -notmatch '\\.zip$' -and 
               $_.FullName -notmatch '\\.git' 
             }
    Compress-Archive -Path $files.FullName -DestinationPath "${path.join(SKILL_DIR, ZIP_FILE)}" -Force
  `;
  
  exec(`powershell -Command "${command}"`, (error, stdout, stderr) => {
    if (error) {
      console.error('❌ 打包失败:', error.message);
      fallbackPackage();
      return;
    }
    
    showSuccess();
  });
}

// 使用 zip 命令 (macOS/Linux)
function packageUnix() {
  const cwd = path.dirname(SKILL_DIR);
  const skillName = path.basename(SKILL_DIR);
  
  const command = `cd "${cwd}" && zip -r "${ZIP_FILE}" "${skillName}" \\
    -x "*.zip" \\
    -x "*/node_modules/*" \\
    -x "*/.git/*"`;
  
  exec(command, (error, stdout, stderr) => {
    if (error) {
      console.error('❌ 打包失败:', error.message);
      fallbackPackage();
      return;
    }
    
    showSuccess();
  });
}

// 备用方案：手动复制文件
function fallbackPackage() {
  console.log('\n⚠️  自动打包失败，使用备用方案...\n');
  console.log('📋 请手动创建 ZIP 文件，包含以下文件:\n');
  
  const files = fs.readdirSync(SKILL_DIR, { recursive: true })
    .filter(f => {
      const fullPath = path.join(SKILL_DIR, f);
      const stat = fs.statSync(fullPath);
      return stat.isFile() && 
             !f.includes('node_modules') && 
             !f.endsWith('.zip') &&
             !f.includes('.git');
    });
  
  files.forEach(f => {
    console.log(`   - ${f}`);
  });
  
  console.log(`\n📊 共 ${files.length} 个文件`);
  console.log('\n💡 手动打包方法:');
  console.log('   1. 复制 browser-local-chrome 文件夹');
  console.log('   2. 右键 -> 发送到 -> 压缩 (ZIP) 文件夹 (Windows)');
  console.log('   3. 或使用 zip 命令：zip -r browser-local-chrome.zip browser-local-chrome');
}

function showSuccess() {
  const zipPath = path.join(SKILL_DIR, ZIP_FILE);
  
  if (fs.existsSync(zipPath)) {
    const stats = fs.statSync(zipPath);
    const sizeKB = (stats.size / 1024).toFixed(2);
    
    console.log('✅ 打包完成！\n');
    console.log('📦 文件信息:');
    console.log(`   文件名：${ZIP_FILE}`);
    console.log(`   大小：${sizeKB} KB`);
    console.log(`   位置：${zipPath}`);
    console.log('\n📋 包含文件:');
    
    const files = fs.readdirSync(SKILL_DIR, { recursive: true })
      .filter(f => {
        const fullPath = path.join(SKILL_DIR, f);
        const stat = fs.statSync(fullPath);
        return stat.isFile() && 
               !f.includes('node_modules') && 
               !f.endsWith('.zip') &&
               !f.includes('.git');
      });
    
    files.forEach(f => {
      console.log(`   - ${f}`);
    });
    
    console.log(`\n📊 共 ${files.length} 个文件`);
    console.log('\n🚀 安装方法:');
    console.log('   1. 将 ZIP 文件复制到目标主机');
    console.log('   2. 解压到 ~/.openclaw/workspace/skills/');
    console.log('   3. 运行：node scripts/start-chrome.js');
  } else {
    console.log('❌ ZIP 文件创建失败');
  }
}

// 开始打包
console.log('🖥️  平台:', process.platform);
console.log('');

if (process.platform === 'win32') {
  packageWindows();
} else {
  packageUnix();
}
