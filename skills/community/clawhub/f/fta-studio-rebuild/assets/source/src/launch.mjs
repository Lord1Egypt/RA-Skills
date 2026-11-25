#!/usr/bin/env node
/**
 * FTA Studio 启动器 (launcher)
 *
 * 解决"打不开 / 无法访问此页面"的几类常见问题：
 *   1. 浏览器打开过早     → 服务真正就绪后再打开浏览器
 *   2. 端口被占用 / 多开   → 默认端口若已是本程序，则复用而非另开（避免端口蔓延 + 旧标签页死链）
 *   3. 公司代理拦截本机    → 强制 127.0.0.1 / localhost 走直连，不经 HTTP_PROXY（Node24 fetch 会读代理）
 *   4. 出错闪退           → 明确打印错误并保留窗口（由 .bat pause 兜底）
 *
 * 用法:
 *   node src/launch.mjs                 # 默认 8777，就绪后自动开浏览器
 *   node src/launch.mjs --port 9000
 *   node src/launch.mjs --no-open       # 不打开浏览器（服务器/CI）
 *   node src/launch.mjs --selftest      # 自检：就绪后立即退出（用于验证）
 */

// ---- 0) 让本机回环流量绕过任何 HTTP 代理 ----
// Node 24 的全局 fetch 会读取 HTTP_PROXY/HTTPS_PROXY；企业代理一旦拦截 127.0.0.1，
//  readiness 探测与浏览器都会"无法访问此页面"。本工具无任何外部请求，故直接清掉代理变量。
for (const k of Object.keys(process.env)) {
  if (/proxy/i.test(k)) delete process.env[k];
}
process.env.no_proxy = '127.0.0.1,localhost,::1';
process.env.NO_PROXY = '127.0.0.1,localhost,::1';

import { spawn } from 'node:child_process';
import { createServer } from './server.mjs';

const argv = process.argv.slice(2);

function flag(name) {
  return argv.includes(name);
}
function opt(name, fallback) {
  const i = argv.indexOf(name);
  return i >= 0 && argv[i + 1] ? argv[i + 1] : fallback;
}

const NO_OPEN = flag('--no-open');
const SELFTEST = flag('--selftest');
const START_PORT = Number(opt('--port', process.env.FTA_PORT || 8777));

function listen(server, port) {
  return new Promise((resolve, reject) => {
    const onErr = (e) => { server.removeListener('listening', onOk); reject(e); };
    const onOk = () => { server.removeListener('error', onErr); resolve(server.address().port); };
    server.once('error', onErr);
    server.once('listening', onOk);
    server.listen(port, '127.0.0.1');
  });
}

/** 判断某端口是否已经是"我们的" FTA Studio 实例（用于单实例复用） */
async function isOurs(port) {
  try {
    const r = await fetch(`http://127.0.0.1:${port}/api/capabilities`);
    if (!r.ok) return false;
    const j = await r.json();
    return !!(j && (j.name || j.product || j.ok || j.capabilities));
  } catch {
    return false;
  }
}

/** 轮询直到服务真正可响应（直连回环，不经过代理） */
async function waitReady(port) {
  const url = `http://127.0.0.1:${port}/`;
  for (let i = 0; i < 60; i++) {
    try {
      const r = await fetch(`${url}api/capabilities`);
      if (r.ok) return url;
    } catch { /* 尚未监听 */ }
    await new Promise((r) => setTimeout(r, 100));
  }
  return null; // 超时：返回 null 便于上层给出明确提示
}

function openBrowser(url) {
  try {
    if (process.platform === 'win32') {
      // 用 localhost 而非 127.0.0.1：多数浏览器/系统对 localhost 默认绕过代理
      spawn('cmd', ['/c', 'start', '', url], { detached: true, stdio: 'ignore', windowsHide: true }).unref();
    } else if (process.platform === 'darwin') {
      spawn('open', [url], { detached: true, stdio: 'ignore' }).unref();
    } else {
      spawn('xdg-open', [url], { detached: true, stdio: 'ignore' }).unref();
    }
  } catch { /* 打不开浏览器不影响服务 */ }
}

function banner(port) {
  return [
    '',
    '  ============================================================',
    '     FTA Studio  已启动',
    '  ============================================================',
    '',
    `     图形编辑器 :  http://localhost:${port}/`,
    `     (本机备用) :  http://127.0.0.1:${port}/`,
    '',
    '     浏览器会自动打开；若未打开或显示"无法访问"，请手动复制上面的地址。',
    '     请保持本窗口开启，按 Ctrl+C 停止服务。',
    '',
  ].join('\n');
}

async function main() {
  // ---- 单实例：默认端口若已是本程序，则直接复用，避免端口蔓延与旧标签页死链 ----
  if (await isOurs(START_PORT)) {
    const url = `http://localhost:${START_PORT}/`;
    console.log('');
    console.log('  [提示] FTA Studio 已在运行，直接为你打开已有页面：');
    console.log(`          ${url}`);
    console.log('');
    if (!NO_OPEN) openBrowser(url);
    else console.log('  (--no-open：已跳过自动打开浏览器)');
    return; // 不启动第二个实例
  }

  let server = createServer();
  let bound = null;

  for (let p = START_PORT; p < START_PORT + 20; p++) {
    try {
      bound = await listen(server, p);
      break;
    } catch (e) {
      if (e && e.code === 'EADDRINUSE') {
        if (p === START_PORT) console.log(`  [提示] 端口 ${p} 已被占用，自动尝试下一个…`);
        server = createServer();
        continue;
      }
      throw e;
    }
  }
  if (!bound) {
    console.error('  [错误] 连续 20 个端口都被占用，无法启动。');
    process.exit(1);
  }

  const ready = await waitReady(bound);
  if (!ready) {
    console.error('');
    console.error('  [错误] 服务已监听但未能就绪（/api/capabilities 无响应）。');
    console.error('         常见原因：本机 HTTP 代理拦截了 localhost。');
    console.error(`         请尝试手动打开: http://localhost:${bound}/`);
    console.error('');
    // 仍尝试打开浏览器，并在控制台给出明确地址
    if (!NO_OPEN) openBrowser(`http://localhost:${bound}/`);
    const shutdown = () => { server.close(() => process.exit(0)); setTimeout(() => process.exit(0), 800); };
    process.on('SIGINT', shutdown);
    process.on('SIGTERM', shutdown);
    return;
  }

  console.log(banner(bound));

  if (SELFTEST) {
    console.log('  [selftest] 服务就绪，自检通过，退出。');
    server.close(() => process.exit(0));
    setTimeout(() => process.exit(0), 500);
    return;
  }

  if (!NO_OPEN) openBrowser(`http://localhost:${bound}/`);
  else console.log('  (--no-open：已跳过自动打开浏览器)');

  const shutdown = () => {
    console.log('\n  正在停止服务…');
    server.close(() => process.exit(0));
    setTimeout(() => process.exit(0), 800);
  };
  process.on('SIGINT', shutdown);
  process.on('SIGTERM', shutdown);
}

main().catch((e) => {
  console.error('\n  [错误] 启动失败: ' + (e && e.message ? e.message : e));
  process.exit(1);
});
