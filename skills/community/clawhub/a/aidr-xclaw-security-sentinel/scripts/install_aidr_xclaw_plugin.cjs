#!/usr/bin/env node
/**
 * aidr-xclaw-security-sentinel Plugin Installer
 *
 * 功能：
 * 1. 安装 @ellawu2211/aidr-xclaw-security-sentinel 插件
 *
 * 使用方式：
 *   node install_aidr_xclaw_plugin.cjs
 */

const { spawn } = require('child_process');
const path = require('path');

const PLUGIN_NAME = '@ellawu2211/aidr-xclaw-security-sentinel@latest';

// 获取 baseDir（脚本所在目录的父目录）
const scriptDir = __dirname;
const baseDir = path.dirname(scriptDir);

/**
 * 打印带前缀的日志
 */
function log(prefix, message) {
  const timestamp = new Date().toISOString().substring(11, 19);
  console.log(`[${timestamp}] [${prefix}] ${message}`);
}

/**
 * 执行 shell 命令（Promise 封装）
 */
function execCommand(command, args, cwd) {
  return new Promise((resolve, reject) => {
    log('CMD', `Executing: ${command} ${args.join(' ')}`);
    const proc = spawn(command, args, {
      cwd: cwd || process.cwd(),
      shell: true,
      stdio: 'inherit'
    });

    proc.on('close', (code) => {
      if (code === 0) {
        resolve(code);
      } else {
        reject(new Error(`Command exited with code ${code}`));
      }
    });

    proc.on('error', (err) => {
      reject(err);
    });
  });
}

/**
 * 执行 shell 命令并捕获输出（Promise 封装）
 */
function execCommandWithOutput(command, args, cwd) {
  return new Promise((resolve, reject) => {
    log('CMD', `Executing: ${command} ${args.join(' ')}`);
    let stdout = '';
    let stderr = '';

    const proc = spawn(command, args, {
      cwd: cwd || process.cwd(),
      shell: true
    });

    proc.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    proc.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    proc.on('close', (code) => {
      if (code === 0) {
        resolve({ code, stdout, stderr });
      } else {
        reject(new Error(`Command exited with code ${code}`));
      }
    });

    proc.on('error', (err) => {
      reject(err);
    });
  });
}

/**
 * 检查 Node.js 是否安装且版本 >= 22
 */
async function checkNode() {
  try {
    const { stdout } = await execCommandWithOutput('node', ['--version']);
    const version = stdout.trim();
    log('INFO', `Node.js 版本: ${version}`);

    const match = version.match(/^v(\d+)/);
    if (!match) {
      log('ERROR', '无法解析 Node.js 版本');
      return false;
    }

    const majorVersion = parseInt(match[1], 10);
    if (majorVersion < 22) {
      log('ERROR', `Node.js 版本过低 (当前: ${majorVersion}, 需要: 22+)`);
      return false;
    }

    log('INFO', 'Node.js 版本符合要求');
    return true;
  } catch (err) {
    log('ERROR', 'Node.js 未安装或不可用');
    return false;
  }
}

/**
 * 检查 openclaw CLI 是否可用
 */
async function checkOpenclawCLI() {
  try {
    await execCommand('openclaw', ['--version']);
    log('INFO', 'openclaw CLI 已安装');
    return true;
  } catch (err) {
    log('ERROR', 'openclaw CLI 未安装');
    return false;
  }
}

/**
 * 安装插件
 */
async function installPlugin() {
  log('INFO', `正在安装插件: ${PLUGIN_NAME}`);
  try {
    await execCommand('openclaw', ['plugins', 'install', PLUGIN_NAME], baseDir);
    log('INFO', '插件安装成功');
    return true;
  } catch (err) {
    log('ERROR', `插件安装失败: ${err.message}`);
    return false;
  }
}

/**
 * 主函数
 */
async function main() {
  console.log('═══════════════════════════════════════════════════════════════');
  console.log('  aidr-xclaw-security-sentinel 插件安装程序');
  console.log('═══════════════════════════════════════════════════════════════');
  console.log('');

  // 检查 Node.js
  log('STEP', '1/2 - 检查环境');
  const nodeOk = await checkNode();
  if (!nodeOk) {
    console.error('错误: 需要安装 Node.js (v22 或更高版本)');
    process.exit(1);
  }

  // 检查 openclaw CLI
  const cliOk = await checkOpenclawCLI();
  if (!cliOk) {
    console.error('错误: 需要安装 openclaw CLI');
    console.error('提示: npm install -g @ai-assistant/openclaw');
    process.exit(1);
  }

  // 安装插件
  console.log('');
  log('STEP', '2/2 - 安装插件');
  const installOk = await installPlugin();
  if (!installOk) {
    console.error('错误: 插件安装失败');
    process.exit(1);
  }

  // 完成
  console.log('');
  console.log('═══════════════════════════════════════════════════════════════');
  log('DONE', '插件安装完成');
  console.log('═══════════════════════════════════════════════════════════════');
  console.log('');
  log('INFO', `插件: ${PLUGIN_NAME}`);
  console.log('');
}

main().catch((err) => {
  console.error('安装过程出错:', err.message);
  process.exit(1);
});
