#!/usr/bin/env node

/**
 * aria2 JSON-RPC 远程控制脚本
 * 支持：add, list, pause, unpause, remove, batch
 * 无外部依赖，使用 Node.js 原生 https 模块
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

// 配置文件路径（workspace 根目录）
const CONFIG_PATH = process.env.ARIA2_CONFIG || path.resolve(process.env.HOME || '/home/node', '.openclaw/workspace/.aria2-config.json');

/**
 * 读取配置
 */
function loadConfig() {
  if (!fs.existsSync(CONFIG_PATH)) {
    console.error('❌ 配置文件不存在：' + CONFIG_PATH);
    console.error('');
    console.error('请创建 .aria2-config.json：');
    console.error(JSON.stringify({ url: 'https://your-server.com/jsonrpc', token: 'your-secret-token' }, null, 2));
    process.exit(1);
  }

  try {
    const config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
    if (!config.url || !config.token) {
      console.error('❌ 配置文件缺少 url 或 token');
      process.exit(1);
    }
    return config;
  } catch (e) {
    console.error('❌ 配置文件格式错误：' + e.message);
    process.exit(1);
  }
}

/**
 * 发送 JSON-RPC 请求
 */
function rpc(config, method, params = []) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      jsonrpc: '2.0',
      id: Date.now(),
      method: method,
      params: ['token:' + config.token, ...params]
    });

    const url = new URL(config.url);
    const isHttps = url.protocol === 'https:';
    const lib = isHttps ? https : http;

    const options = {
      hostname: url.hostname,
      port: url.port || (isHttps ? 443 : 80),
      path: url.pathname || '/jsonrpc',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body)
      }
    };

    const req = lib.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (json.error) {
            reject(new Error(json.error.message || JSON.stringify(json.error)));
          } else {
            resolve(json.result);
          }
        } catch (e) {
          reject(new Error('解析响应失败：' + data.substring(0, 200)));
        }
      });
    });

    req.on('error', (e) => reject(e));
    req.setTimeout(15000, () => {
      req.destroy();
      reject(new Error('请求超时'));
    });

    req.write(body);
    req.end();
  });
}

/**
 * 格式化文件大小
 */
function formatSize(bytes) {
  if (!bytes || bytes === 0) return '未知';
  const units = ['B', 'KB', 'MB', 'GB', 'TB'];
  let i = 0;
  while (bytes >= 1024 && i < units.length - 1) {
    bytes /= 1024;
    i++;
  }
  return bytes.toFixed(1) + ' ' + units[i];
}

/**
 * 格式化速度
 */
function formatSpeed(bytesPerSec) {
  if (!bytesPerSec || bytesPerSec === 0) return '0 B/s';
  return formatSize(bytesPerSec) + '/s';
}

/**
 * 格式化进度条
 */
function progressBar(completed, total) {
  if (!total || total === 0) return '░░░░░░░░░░ ???%';
  const pct = Math.min(100, (completed / total) * 100);
  const filled = Math.round(pct / 10);
  const empty = 10 - filled;
  return '▓'.repeat(filled) + '░'.repeat(empty) + ' ' + pct.toFixed(1) + '%';
}

/**
 * 获取任务名称
 */
function getTaskName(task) {
  const bittorrent = task.bittorrent;
  if (bittorrent && bittorrent.info && bittorrent.info.name) {
    return bittorrent.info.name;
  }
  const files = task.files;
  if (files && files.length > 0) {
    const uris = files[0].uris;
    if (uris && uris.length > 0) {
      const uri = uris[0].uri;
      // 从 URL 提取文件名
      try {
        const urlPath = new URL(uri).pathname;
        const name = path.basename(decodeURIComponent(urlPath));
        if (name) return name;
      } catch (e) {}
      // 从磁力链接提取
      if (uri.startsWith('magnet:')) {
        const match = uri.match(/dn=([^&]+)/);
        if (match) return decodeURIComponent(match[1]);
        return 'magnet:' + uri.substring(8, 20) + '...';
      }
      return uri.substring(0, 50) + (uri.length > 50 ? '...' : '');
    }
  }
  return '未知';
}

/**
 * 格式化单个任务
 */
function formatTask(task) {
  const gid = task.gid;
  const name = getTaskName(task);
  const completed = parseInt(task.completedLength) || 0;
  const total = parseInt(task.totalLength) || 0;
  const speed = parseInt(task.downloadSpeed) || 0;
  const status = task.status;

  let line = `[${gid}] `;

  if (status === 'active') {
    line += progressBar(completed, total) + ' | ';
    line += formatSpeed(speed) + ' | ';
    line += formatSize(completed) + '/' + formatSize(total) + ' | ';
    line += name;
  } else if (status === 'waiting') {
    line += '⏳ 等待中 | ' + name;
  } else if (status === 'paused') {
    line += '⏸️ 已暂停 | ' + progressBar(completed, total) + ' | ' + name;
  } else if (status === 'complete') {
    line += '✅ 完成 | ' + formatSize(total) + ' | ' + name;
  } else if (status === 'error') {
    line += '❌ 错误 | ' + (task.errorMessage || '未知错误') + ' | ' + name;
  } else if (status === 'removed') {
    line += '🗑️ 已删除 | ' + name;
  } else {
    line += status + ' | ' + name;
  }

  return line;
}

// ============ 命令处理 ============

/**
 * 添加下载
 */
async function addDownload(url) {
  if (!url) {
    console.error('❌ 请提供下载链接');
    process.exit(1);
  }

  const config = loadConfig();
  try {
    const gid = await rpc(config, 'aria2.addUri', [[url]]);
    console.log('✅ 已添加下载');
    console.log('GID: ' + gid);
    console.log('链接: ' + (url.length > 60 ? url.substring(0, 60) + '...' : url));
  } catch (e) {
    console.error('❌ 添加失败：' + e.message);
    process.exit(1);
  }
}

/**
 * 查看所有任务
 */
async function listTasks() {
  const config = loadConfig();
  try {
    const [active, waiting, stopped] = await Promise.all([
      rpc(config, 'aria2.tellActive', [['gid', 'status', 'totalLength', 'completedLength', 'downloadSpeed', 'files', 'bittorrent', 'errorMessage']]),
      rpc(config, 'aria2.tellWaiting', [0, 100, ['gid', 'status', 'totalLength', 'completedLength', 'downloadSpeed', 'files', 'bittorrent', 'errorMessage']]),
      rpc(config, 'aria2.tellStopped', [0, 50, ['gid', 'status', 'totalLength', 'completedLength', 'downloadSpeed', 'files', 'bittorrent', 'errorMessage']])
    ]);

    if (active.length > 0) {
      console.log('📋 活跃任务 (' + active.length + '):');
      active.forEach(t => console.log('  ' + formatTask(t)));
    }

    if (waiting.length > 0) {
      console.log('');
      console.log('⏳ 等待中 (' + waiting.length + '):');
      waiting.forEach(t => console.log('  ' + formatTask(t)));
    }

    const paused = stopped.filter(t => t.status === 'paused');
    if (paused.length > 0) {
      console.log('');
      console.log('⏸️ 已暂停 (' + paused.length + '):');
      paused.forEach(t => console.log('  ' + formatTask(t)));
    }

    const completed = stopped.filter(t => t.status === 'complete');
    if (completed.length > 0) {
      console.log('');
      console.log('✅ 已完成 (' + completed.length + '):');
      completed.forEach(t => console.log('  ' + formatTask(t)));
    }

    const errors = stopped.filter(t => t.status === 'error');
    if (errors.length > 0) {
      console.log('');
      console.log('❌ 错误 (' + errors.length + '):');
      errors.forEach(t => console.log('  ' + formatTask(t)));
    }

    const total = active.length + waiting.length + stopped.length;
    if (total === 0) {
      console.log('📭 当前没有下载任务');
    }
  } catch (e) {
    console.error('❌ 获取任务列表失败：' + e.message);
    process.exit(1);
  }
}

/**
 * 暂停任务
 */
async function pauseTask(gid) {
  if (!gid) {
    console.error('❌ 请提供 GID');
    process.exit(1);
  }
  const config = loadConfig();
  try {
    await rpc(config, 'aria2.pause', [gid]);
    console.log('⏸️ 已暂停：' + gid);
  } catch (e) {
    console.error('❌ 暂停失败：' + e.message);
    process.exit(1);
  }
}

/**
 * 恢复任务
 */
async function unpauseTask(gid) {
  if (!gid) {
    console.error('❌ 请提供 GID');
    process.exit(1);
  }
  const config = loadConfig();
  try {
    await rpc(config, 'aria2.unpause', [gid]);
    console.log('▶️ 已恢复：' + gid);
  } catch (e) {
    console.error('❌ 恢复失败：' + e.message);
    process.exit(1);
  }
}

/**
 * 删除任务
 */
async function removeTask(gid) {
  if (!gid) {
    console.error('❌ 请提供 GID');
    process.exit(1);
  }
  const config = loadConfig();
  try {
    await rpc(config, 'aria2.remove', [gid]);
    console.log('🗑️ 已删除：' + gid);
  } catch (e) {
    console.error('❌ 删除失败：' + e.message);
    process.exit(1);
  }
}

/**
 * 批量下载（从 stdin 读取链接）
 */
async function batchDownload(input) {
  const config = loadConfig();
  const lines = input.split('\n').map(l => l.trim()).filter(l => l && !l.startsWith('#'));

  if (lines.length === 0) {
    console.error('❌ 没有有效的链接');
    process.exit(1);
  }

  console.log('📥 批量下载 (' + lines.length + ' 个链接):');

  let success = 0;
  let failed = 0;

  for (let i = 0; i < lines.length; i++) {
    const url = lines[i];
    try {
      const gid = await rpc(config, 'aria2.addUri', [[url]]);
      const displayName = url.length > 50 ? url.substring(0, 50) + '...' : url;
      console.log('  ✅ [' + (i + 1) + '] ' + displayName + ' → GID: ' + gid);
      success++;
    } catch (e) {
      console.log('  ❌ [' + (i + 1) + '] ' + url + ' → 失败: ' + e.message);
      failed++;
    }
  }

  console.log('');
  console.log('📊 结果：成功 ' + success + ' / 失败 ' + failed + ' / 总计 ' + lines.length);
}

/**
 * 显示帮助
 */
function showHelp() {
  console.log('aria2 JSON-RPC 远程控制');
  console.log('');
  console.log('用法：node aria2.js <command> [args]');
  console.log('');
  console.log('命令：');
  console.log('  add <url>        添加下载（磁力/HTTP/FTP）');
  console.log('  list             查看所有任务');
  console.log('  pause <gid>      暂停任务');
  console.log('  unpause <gid>    恢复任务');
  console.log('  remove <gid>     删除任务');
  console.log('  batch            批量下载（从 stdin 读取，每行一个链接）');
  console.log('  help             显示帮助');
  console.log('');
  console.log('配置文件：.aria2-config.json');
  console.log(JSON.stringify({ url: 'https://your-server.com/jsonrpc', token: 'your-secret-token' }, null, 2));
}

// ============ 主入口 ============

async function main() {
  const command = process.argv[2];
  const arg = process.argv[3];

  switch (command) {
    case 'add':
      await addDownload(arg);
      break;
    case 'list':
      await listTasks();
      break;
    case 'pause':
      await pauseTask(arg);
      break;
    case 'unpause':
      await unpauseTask(arg);
      break;
    case 'remove':
      await removeTask(arg);
      break;
    case 'batch':
      {
        const input = await new Promise((resolve) => {
          let data = '';
          process.stdin.setEncoding('utf8');
          process.stdin.on('data', (chunk) => data += chunk);
          process.stdin.on('end', () => resolve(data));
          process.stdin.on('error', () => resolve(''));
        });
        await batchDownload(input);
      }
      break;
    case 'help':
    default:
      showHelp();
      break;
  }
}

main().catch(e => {
  console.error('❌ 错误：' + e.message);
  process.exit(1);
});
