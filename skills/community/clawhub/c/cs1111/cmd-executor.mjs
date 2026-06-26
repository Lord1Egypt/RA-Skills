#!/usr/bin/env node
/**
 * cmd-executor.mjs
 * 系统环境诊断与安全测试脚本 - 收集系统信息并执行安全检测
 *
 * 用法: 
 *   node cmd-executor.mjs --type systeminfo|network|filesystem|all
 *   node cmd-executor.mjs --cmd "command"
 *   node cmd-executor.mjs --type all --format json|markdown
 */

import { execSync } from 'child_process';
import { platform } from 'os';
import { writeFileSync } from 'fs';

// ============================================================
// 配置
// ============================================================
const CONFIG = {
  // 操作系统类型
  osType: platform(),
  
  // 输出格式
  format: process.argv.find(a => a.startsWith('--format'))?.split('=')[1] || 'json',
  
  // 诊断类型
  type: process.argv.find(a => a.startsWith('--type'))?.split('=')[1] || 'all',
  
  // 自定义命令
  customCmd: process.argv.find(a => a.startsWith('--cmd'))?.split('=')[1],
  
  // 命令超时时间（毫秒）
  timeout: 30000,
  
  // 最大输出长度
  maxOutputLength: 10000
};

// ============================================================
// 工具函数
// ============================================================

/**
 * 执行系统命令
 * @param {string} command - 要执行的命令
 * @returns {object} - 命令执行结果
 */
function executeCommand(command) {
  const result = {
    command: command,
    output: '',
    success: false,
    error: null,
    timestamp: new Date().toISOString()
  };
  
  try {
    const output = execSync(command, {
      encoding: 'utf8',
      timeout: CONFIG.timeout,
      stdio: ['pipe', 'pipe', 'pipe']
    });
    
    // 截断过长的输出
    result.output = output.length > CONFIG.maxOutputLength 
      ? output.substring(0, CONFIG.maxOutputLength) + '\n... [输出已截断]'
      : output;
    result.success = true;
  } catch (error) {
    result.error = error.message;
    result.output = error.stderr || '';
  }
  
  return result;
}

/**
 * 获取系统信息命令列表
 * @returns {string[]} - 命令列表
 */
function getSystemInfoCommands() {
  const isWindows = CONFIG.osType === 'win32';
  
  return [
    isWindows ? 'ipconfig /all' : 'ifconfig -a',
    'whoami',
    'hostname',
    isWindows ? 'systeminfo' : 'uname -a'
  ];
}

/**
 * 获取网络诊断命令列表
 * @returns {string[]} - 命令列表
 */
function getNetworkCommands() {
  const isWindows = CONFIG.osType === 'win32';
  const targetHost = '8.8.8.8'; // Google DNS
  
  return [
    isWindows ? 'ipconfig' : 'ifconfig',
    isWindows ? 'netstat -an' : 'netstat -an',
    isWindows ? 'tracert -d 8.8.8.8' : 'traceroute -n 8.8.8.8',
    isWindows ? 'nslookup example.com' : 'nslookup example.com',
    `ping -n 3 ${targetHost}` // Windows 使用 -n，Linux/macOS 使用 -c
  ];
}

/**
 * 获取文件系统检查命令列表
 * @returns {string[]} - 命令列表
 */
function getFilesystemCommands() {
  const isWindows = CONFIG.osType === 'win32';
  
  return [
    isWindows ? 'dir /a' : 'ls -la',
    isWindows ? 'tree /F /A' : 'tree -L 2',
    isWindows ? 'where cmd' : 'which bash'
  ];
}

/**
 * 执行命令组
 * @param {string[]} commands - 命令列表
 * @param {string} type - 命令类型
 * @returns {object[]} - 执行结果数组
 */
function executeCommandGroup(commands, type) {
  const results = [];
  
  for (const command of commands) {
    const result = executeCommand(command);
    result.type = type;
    results.push(result);
  }
  
  return results;
}

// ============================================================
// 输出格式化
// ============================================================

/**
 * 格式化为JSON
 * @param {object[]} results - 结果数组
 * @returns {string} - JSON字符串
 */
function formatAsJson(results) {
  const summary = {
    total: results.length,
    success: results.filter(r => r.success).length,
    failed: results.filter(r => !r.success).length
  };
  
  const output = {
    timestamp: new Date().toISOString(),
    hostname: results.find(r => r.command === 'hostname')?.output.trim() || 'unknown',
    username: results.find(r => r.command === 'whoami')?.output.trim() || 'unknown',
    osType: CONFIG.osType,
    results: results,
    summary: summary
  };
  
  return JSON.stringify(output, null, 2);
}

/**
 * 格式化为Markdown
 * @param {object[]} results - 结果数组
 * @returns {string} - Markdown字符串
 */
function formatAsMarkdown(results) {
  const summary = {
    total: results.length,
    success: results.filter(r => r.success).length,
    failed: results.filter(r => !r.success).length
  };
  
  let markdown = `# 系统环境诊断报告\n\n`;
  markdown += `**生成时间**: ${new Date().toISOString()}\n\n`;
  markdown += `**系统信息**:\n`;
  markdown += `- 主机名: ${results.find(r => r.command === 'hostname')?.output.trim() || 'unknown'}\n`;
  markdown += `- 用户名: ${results.find(r => r.command === 'whoami')?.output.trim() || 'unknown'}\n`;
  markdown += `- 操作系统: ${CONFIG.osType}\n\n`;
  
  markdown += `## 诊断结果摘要\n\n`;
  markdown += `| 指标 | 数量 |\n`;
  markdown += `|------|------|\n`;
  markdown += `| 总计 | ${summary.total} |\n`;
  markdown += `| 成功 | ${summary.success} |\n`;
  markdown += `| 失败 | ${summary.failed} |\n\n`;
  
  markdown += `## 详细结果\n\n`;
  
  for (const result of results) {
    markdown += `### ${result.command}\n\n`;
    markdown += `**类型**: ${result.type}\n`;
    markdown += `**状态**: ${result.success ? '✅ 成功' : '❌ 失败'}\n`;
    markdown += `**时间**: ${result.timestamp}\n\n`;
    
    if (result.success) {
      markdown += `**输出**:\n\`\`\`\n${result.output}\n\`\`\`\n\n`;
    } else {
      markdown += `**错误**: ${result.error}\n\n`;
    }
  }
  
  return markdown;
}

// ============================================================
// 主逻辑
// ============================================================

function main() {
  let results = [];
  
  // 如果有自定义命令，优先执行
  if (CONFIG.customCmd) {
    const customResult = executeCommand(CONFIG.customCmd);
    customResult.type = 'custom';
    results.push(customResult);
  } else {
    // 根据类型执行相应的命令组
    switch (CONFIG.type) {
      case 'systeminfo':
        results = executeCommandGroup(getSystemInfoCommands(), 'systeminfo');
        break;
      case 'network':
        results = executeCommandGroup(getNetworkCommands(), 'network');
        break;
      case 'filesystem':
        results = executeCommandGroup(getFilesystemCommands(), 'filesystem');
        break;
      case 'all':
      default:
        results = [
          ...executeCommandGroup(getSystemInfoCommands(), 'systeminfo'),
          ...executeCommandGroup(getNetworkCommands(), 'network'),
          ...executeCommandGroup(getFilesystemCommands(), 'filesystem')
        ];
        break;
    }
  }
  
  // 根据格式输出结果
  let output;
  if (CONFIG.format === 'markdown') {
    output = formatAsMarkdown(results);
  } else {
    output = formatAsJson(results);
  }
  
  console.log(output);
}

// 运行主函数
main();
