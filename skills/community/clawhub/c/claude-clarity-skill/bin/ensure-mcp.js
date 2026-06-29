#!/usr/bin/env node
/**
 * ensure-mcp.js — 心虫 MCP 启动保障脚本
 *
 * 确保心虫守护进程和 MCP 包装器均已就绪。
 * 可在会话启动时运行，保证 18 个 MCP 工具可用。
 *
 * 用法:
 *   node bin/ensure-mcp.js              # 确保守护进程运行，输出状态
 *   node bin/ensure-mcp.js --check      # 只检查不启动
 *   node bin/ensure-mcp.js --wrapper    # 同时确保 MCP 包装器（stdio 代理）运行
 *
 * 返回码:
 *   0 = 一切正常
 *   1 = 守护进程未运行（--check 模式）
 *   2 = 启动失败
 */

const path = require('path');
const fs = require('fs');
const { spawn } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const SOCKET_PATH = '/tmp/claude-clarity.sock';
const DAEMON_JS = path.join(ROOT, 'daemon', 'mcp-daemon.js');
const WRAPPER_JS = path.join(ROOT, 'daemon', 'mcp-wrapper.js');
const PID_FILE = '/tmp/claude-clarity.pid';

const args = process.argv.slice(2);
const onlyCheck = args.includes('--check');
const needWrapper = args.includes('--wrapper');

// ─── 工具函数 ─────────────────────────────────────────
function daemonExists() {
  return fs.existsSync(SOCKET_PATH);
}

function readPid() {
  try {
    return parseInt(fs.readFileSync(PID_FILE, 'utf8').trim());
  } catch { return null; }
}

function pidAlive(pid) {
  try {
    process.kill(pid, 0);
    return true;
  } catch { return false; }
}

function statusReport(daemonOk, wrapperOk) {
  const report = {
    timestamp: new Date().toISOString(),
    daemon: {
      running: daemonOk,
      socket: SOCKET_PATH,
      pid: readPid(),
      pidAlive: daemonOk ? pidAlive(readPid()) : false,
    },
    wrapper: { running: wrapperOk },
    tools: 18,
  };
  return report;
}

function printStatus(report) {
  const lines = [
    '╔══════════════════════════════════╗',
    '║  心虫引擎 MCP 状态              ║',
    '╠══════════════════════════════════╣',
    `║  守护进程: ${report.daemon.running ? '✅ 运行中' : '❌ 未运行'}               ║`,
    `║  PID:       ${report.daemon.pid || 'N/A'}                      ║`,
    `║  Socket:    ${SOCKET_PATH} ║`,
    `║  MCP 工具:  ${report.tools} 个                     ║`,
    `║  包装器:    ${report.wrapper.running ? '✅ 正常' : '❌ 未连接'}                 ║`,
    '╚══════════════════════════════════╝',
  ];
  console.log(lines.join('\n'));
}

// 启动 MCP 包装器
function startWrapper() {
  console.error('[ensure-mcp] MCP 包装器未运行，正在启动...');
  const wrapper = spawn(process.execPath, [WRAPPER_JS], {
    detached: true,
    stdio: 'ignore',
  });
  wrapper.unref();
  console.error(`[ensure-mcp] MCP 包装器已启动 (PID ${wrapper.pid})`);
}

// ─── 主逻辑 ───────────────────────────────────────────
function main() {
  const daemonOk = daemonExists();
  const pid = readPid();
  const pidOk = pid ? pidAlive(pid) : false;

  // 检查包装器进程（仅限 --wrapper）
  let wrapperOk = false;
  if (needWrapper) {
    try {
      const { spawnSync } = require('child_process');
      const result = spawnSync('ps', ['aux'], { encoding: 'utf8', timeout: 2000 });
      wrapperOk = result.stdout.includes('mcp-wrapper.js');
    } catch { wrapperOk = false; }
  }

  if (onlyCheck) {
    const report = statusReport(daemonOk && pidOk, wrapperOk);
    printStatus(report);
    process.exit(daemonOk && pidOk ? 0 : 1);
  }

  // 启动守护进程（如未运行）
  if (!daemonOk || !pidOk) {
    console.error('[ensure-mcp] 心虫守护进程未运行，正在启动...');
    try { fs.unlinkSync(PID_FILE); } catch { /* 忽略 */ }
    try { fs.unlinkSync(SOCKET_PATH); } catch { /* 忽略 */ }

    const child = spawn(process.execPath, [DAEMON_JS], {
      detached: true,
      stdio: 'ignore',
    });
    child.unref();

    // 最多等 8 秒
    let waited = 0;
    const interval = setInterval(() => {
      waited += 200;
      if (daemonExists()) {
        clearInterval(interval);
        const newPid = readPid();
        console.error(`[ensure-mcp] 守护进程已启动 (PID ${newPid})`);

        // 启动包装器（如需要）
        if (needWrapper && !wrapperOk) {
          startWrapper();
          wrapperOk = true;
        }

        const report = statusReport(true, wrapperOk);
        printStatus(report);
        process.exit(0);
      }
      if (waited > 8000) {
        clearInterval(interval);
        const report = statusReport(false, false);
        printStatus(report);
        console.error('[ensure-mcp] 启动超时');
        process.exit(2);
      }
    }, 200);
  } else {
    console.error(`[ensure-mcp] 守护进程已在运行 (PID ${pid})`);

    // 启动包装器（如需要）
    if (needWrapper && !wrapperOk) {
      startWrapper();
      wrapperOk = true;
    }

    const report = statusReport(true, wrapperOk);
    printStatus(report);
    process.exit(0);
  }
}

main();
