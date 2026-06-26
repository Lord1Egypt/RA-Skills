#!/usr/bin/env node

/**
 * 打包技能为 ZIP 文件
 * 
 * 用法：node scripts/package.js [输出文件名]
 * 示例：node scripts/package.js browser-local-chrome-v1.1.0.zip
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const archiver = require('archiver');

const SKILL_DIR = path.join(__dirname, '..');
const OUTPUT_FILE = process.argv[2] || 'browser-local-chrome.zip';

console.log('📦 打包 browser-local-chrome 技能...\n');

// 检查 archiver 是否安装
try {
  require.resolve('archiver');
} catch (e) {
  console.log('⚠️  archiver 模块未安装，尝试使用系统 zip 命令...\n');
  useSystemZip();
  return;
}

// 使用 archiver 打包
function createZip() {
  const output = fs.createWriteStream(path.join(SKILL_DIR, OUTPUT_FILE));
  const archive = archiver('zip', {
    zlib: { level: 9 } // 最高压缩级别
  });

  output.on('close', () => {
    const sizeMB = (archive.pointer() / 1024 / 1024).toFixed(2);
    console.log(`✅ 打包完成！`);
    console.log(`   文件：${OUTPUT_FILE}`);
    console.log(`   大小：${sizeMB} MB`);
    console.log(`   位置：${SKILL_DIR}`);
  });

  archive.on('error', (err) => {
    console.error('❌ 打包失败:', err);
    process.exit(1);
  });

  archive.pipe(output);

  console.log('📁 添加文件...');
  
  // 添加所有文件（排除 node_modules 和 zip 文件）
  archive.glob('**/*', {
    cwd: SKILL_DIR,
    ignore: [
      'node_modules/**',
      '*.zip',
      '.git/**'
    ]
  });

  archive.finalize();
}

// 使用系统 zip 命令
function useSystemZip() {
  const zipFile = path.join(SKILL_DIR, OUTPUT_FILE);
  const platform = process.platform;
  
  let command;
  
  if (platform === 'win32') {
    // Windows: 使用 PowerShell Compress-Archive
    command = `Compress-Archive -Path "${SKILL_DIR}\\*" -DestinationPath "${zipFile}" -Force`;
    console.log('🔧 使用 PowerShell Compress-Archive...\n');
  } else {
    // macOS/Linux: 使用 zip 命令
    const cwd = path.dirname(SKILL_DIR);
    const skillName = path.basename(SKILL_DIR);
    command = `cd "${cwd}" && zip -r "${OUTPUT_FILE}" "${skillName}" -x "*.zip" -x "node_modules/*" -x ".git/*"`;
    console.log('🔧 使用系统 zip 命令...\n');
  }
  
  exec(command, { cwd: platform === 'win32' ? undefined : cwd }, (error, stdout, stderr) => {
    if (error) {
      console.error('❌ 打包失败:', error.message);
      console.error('💡 提示：安装 archiver 模块：npm install archiver');
      process.exit(1);
    }
    
    const stats = fs.statSync(zipFile);
    const sizeMB = (stats.size / 1024 / 1024).toFixed(2);
    
    console.log('✅ 打包完成！');
    console.log(`   文件：${OUTPUT_FILE}`);
    console.log(`   大小：${sizeMB} MB`);
    console.log(`   位置：${zipFile}`);
  });
}

// 检查并打包
console.log('📂 技能目录:', SKILL_DIR);
console.log('📄 输出文件:', OUTPUT_FILE);
console.log('🖥️  平台:', process.platform);
console.log('');

// 列出将要打包的文件
console.log('📋 文件清单:');
const files = fs.readdirSync(SKILL_DIR, { recursive: true })
  .filter(f => {
    const fullPath = path.join(SKILL_DIR, f);
    const stat = fs.statSync(fullPath);
    return stat.isFile() && 
           !f.includes('node_modules') && 
           !f.endsWith('.zip');
  });

files.forEach(f => {
  console.log(`   - ${f}`);
});

console.log('');
console.log(`📊 共 ${files.length} 个文件`);
console.log('');

createZip();
