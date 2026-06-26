#!/usr/bin/env node

/**
 * BBDown 自动安装脚本
 * 安装 bilibit 时自动下载 BBDown
 */

const { execSync, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

console.log('🔍 检查 BBDown 依赖...\n');

// 检查 BBDown 是否已安装
function checkBBDown() {
  try {
    execSync('which BBDown', { stdio: 'ignore' });
    console.log('✅ BBDown 已安装\n');
    return true;
  } catch (error) {
    console.log('⚠️  BBDown 未安装\n');
    return false;
  }
}

// 下载并解压 BBDown
function downloadBBDown() {
  const platform = os.platform();
  const arch = os.arch();

  console.log('📦 正在下载 BBDown...\n');

  // 选择正确的版本
  let downloadUrl = '';
  let binaryName = 'BBDown';

  if (platform === 'darwin') {
    if (arch === 'arm64') {
      downloadUrl = 'https://github.com/nilaoda/BBDown/releases/download/1.6.3/BBDown_1.6.3_20240814_macos-arm64.zip';
    } else {
      downloadUrl = 'https://github.com/nilaoda/BBDown/releases/download/1.6.3/BBDown_1.6.3_20240814_macos-x64.zip';
    }
  } else if (platform === 'linux') {
    if (arch === 'arm64') {
      downloadUrl = 'https://github.com/nilaoda/BBDown/releases/download/1.6.3/BBDown_1.6.3_20240814_linux-arm64.zip';
    } else {
      downloadUrl = 'https://github.com/nilaoda/BBDown/releases/download/1.6.3/BBDown_1.6.3_20240814_linux-x64.zip';
    }
  } else if (platform === 'win32') {
    binaryName = 'BBDown.exe';
    downloadUrl = 'https://github.com/nilaoda/BBDown/releases/download/1.6.3/BBDown_1.6.3_20240814_win-x64.zip';
  } else {
    console.log('❌ 不支持的操作系统:', platform);
    console.log('请手动安装：https://github.com/nilaoda/BBDown/releases\n');
    return Promise.resolve(false);
  }

  const installDir = path.join(__dirname, '..', 'node_modules', '.bin');
  const zipPath = path.join(installDir, 'bbdown.zip');

  try {
    if (!fs.existsSync(installDir)) {
      fs.mkdirSync(installDir, { recursive: true });
    }
  } catch (e) {}

  return new Promise((resolve) => {
    // 使用 curl 下载（自动跟进重定向）
    const curl = spawn('curl', ['-L', '-o', zipPath, downloadUrl], { stdio: 'ignore' });

    curl.on('close', (code) => {
      if (code !== 0 || !fs.existsSync(zipPath)) {
        console.log('❌ 下载失败');
        console.log('请手动安装：https://github.com/nilaoda/BBDown/releases\n');
        fs.unlink(zipPath, () => {});
        resolve(false);
        return;
      }

      console.log('📦 解压中...\n');

      // 解压 zip
      const unzip = spawn('unzip', ['-o', '-q', zipPath, '-d', installDir], { stdio: 'ignore' });

      unzip.on('close', (unzipCode) => {
        fs.unlink(zipPath, () => {});

        if (unzipCode !== 0) {
          console.log('❌ 解压失败');
          resolve(false);
          return;
        }

        const installPath = path.join(installDir, binaryName);

        if (!fs.existsSync(installPath)) {
          console.log('❌ 解压后未找到 BBDown 二进制文件');
          console.log('安装目录内容:', fs.readdirSync(installDir));
          resolve(false);
          return;
        }

        fs.chmodSync(installPath, '755');
        console.log('✅ BBDown 安装成功:', installPath);
        console.log('🎉 bilibit 已就绪！\n');
        console.log('使用示例：');
        console.log('  bilibit https://b23.tv/BV1xx');
        console.log('  bilibit https://b23.tv/BV1xx --quality 1080P --danmaku\n');
        resolve(true);
      });

      unzip.on('error', (err) => {
        fs.unlink(zipPath, () => {});
        console.log('❌ 解压失败:', err.message);
        resolve(false);
      });
    });

    curl.on('error', (err) => {
      fs.unlink(zipPath, () => {});
      console.log('❌ 下载失败:', err.message);
      console.log('请手动安装：https://github.com/nilaoda/BBDown/releases\n');
      resolve(false);
    });
  });
}

// 主流程
async function main() {
  console.log('════════════════════════════════════════');
  console.log('🎬 bilibit 依赖安装');
  console.log('════════════════════════════════════════\n');

  if (checkBBDown()) {
    return;
  }

  await downloadBBDown();
}

main();
