#!/usr/bin/env node
// Enhanced Daemon Health Check
//
// Проверяет демон НЕ ТОЛЬКО по endpoint файлу, а реально:
// 1. Endpoint файл существует и валиден
// 2. Puppeteer может подключиться
// 3. Chrome отвечает на CDP команды
// 4. Страница DeepSeek загружена (composer присутствует)
//
// Запуск: node daemon-healthcheck.js
// Автозапуск: PM2 cron каждые 5 минут
//
const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const BASE_DIR = __dirname;
const DAEMON_ENDPOINT_FILE = path.join(BASE_DIR, '.daemon-ws-endpoint');
const CONNECT_TIMEOUT = 15000;  // 15 сек на подключение
const COMPOSER_TIMEOUT = 20000;  // 20 сек на поиск composer
const LOG_FILE = path.join(BASE_DIR, '.healthcheck.log');
const FAILED_COUNT_FILE = path.join(BASE_DIR, '.healthcheck-failed-count');

const LOG = (level, ...args) => {
  const ts = new Date().toISOString();
  const msg = `[${ts}] [${level}] ${args.join(' ')}`;
  console.log(msg);
  try { fs.appendFileSync(LOG_FILE, msg + '\n', 'utf8'); } catch {}
};

const sleep = ms => new Promise(r => setTimeout(r, ms));

async function getChromeMemoryMB(client) {
  try {
    const metrics = await client.send('Performance.getMetrics');
    const jsHeap = metrics.metrics?.find(s => s.name === 'JSHeapUsedSize');
    return jsHeap ? Math.round(Number(jsHeap.value) / 1024 / 1024) : null;
  } catch { return null; }
}

async function checkPageLoad(client) {
  try {
    const result = await client.send('Runtime.evaluate', {
      expression: `(
        function() {
          var composers = document.querySelectorAll(
            'textarea[placeholder*="Message" i], ' +
            'textarea[placeholder*="Введите" i], ' +
            'textarea[placeholder*="Type" i], ' +
            'div[contenteditable="true"][role="textbox"], ' +
            'textarea'
          );
          for (var i = 0; i < composers.length; i++) {
            var el = composers[i];
            var rect = el.getBoundingClientRect();
            if (rect.width > 0 && rect.height > 0 && el.offsetParent !== null) {
              return { found: true, tag: el.tagName, placeholder: el.placeholder || el.getAttribute('data-placeholder') || '', w: Math.round(rect.width), h: Math.round(rect.height) };
            }
          }
          // Проверяем заголовок страницы
          var title = document.title || '';
          var url = window.location.href || '';
          var bodyLen = (document.body?.innerText || '').length;
          return { found: false, title, url, bodyLen };
        }
      )()`,
      returnByValue: true,
    });
    if (result && !result.exceptionDetails) {
      return result.result?.value || null;
    }
  } catch (e) {
    LOG('WARN', `Page load check failed: ${e.message}`);
  }
  return null;
}

async function runHealthCheck() {
  const checks = {
    endpointFile: false,
    endpointValid: false,
    puppeteerConnect: false,
    cdpSession: false,
    composerFound: false,
    memoryChecked: false,
  };
  let memoryMB = null;
  let composerInfo = null;
  let errorMsg = null;
  let browser = null;

  LOG('INFO', '═══ Health Check Started ═══');

  // 1. Проверка endpoint файла
  if (!fs.existsSync(DAEMON_ENDPOINT_FILE)) {
    errorMsg = 'Endpoint file not found';
    LOG('ERROR', errorMsg);
    return { ok: false, checks, error: errorMsg };
  }

  let endpoint;
  try {
    endpoint = fs.readFileSync(DAEMON_ENDPOINT_FILE, 'utf8').trim();
    checks.endpointFile = true;
  } catch (e) {
    errorMsg = `Cannot read endpoint file: ${e.message}`;
    LOG('ERROR', errorMsg);
    return { ok: false, checks, error: errorMsg };
  }

  if (!endpoint.startsWith('ws://') && !endpoint.startsWith('wss://')) {
    errorMsg = `Invalid endpoint format: ${endpoint.substring(0, 50)}`;
    LOG('ERROR', errorMsg);
    return { ok: false, checks, error: errorMsg };
  }

  checks.endpointValid = true;
  LOG('INFO', `Endpoint: ${endpoint.substring(0, 60)}...`);

  // 2. Подключение к браузеру
  try {
    const timeoutPromise = new Promise((_, reject) =>
      setTimeout(() => reject(new Error('connect timeout')), CONNECT_TIMEOUT)
    );

    const connectPromise = puppeteer.connect({
      browserWSEndpoint: endpoint,
      timeout: CONNECT_TIMEOUT,
    });

    browser = await Promise.race([connectPromise, timeoutPromise]);
    checks.puppeteerConnect = true;
    LOG('INFO', '✅ Puppeteer connected');
  } catch (e) {
    errorMsg = `Connection failed: ${e.message}`;
    LOG('ERROR', errorMsg);
    incrementFailedCount();
    return { ok: false, checks, error: errorMsg };
  }

  try {
    // 3. Получаем CDP session
    const pages = await browser.pages();
    const dsPage = pages.find(p => {
      try { return p.url().includes('deepseek'); } catch { return false; }
    }) || pages[0];

    if (!dsPage) {
      errorMsg = 'No pages found in browser';
      LOG('ERROR', errorMsg);
      return { ok: false, checks, error: errorMsg };
    }

    const client = await dsPage.target().createCDPSession();
    checks.cdpSession = true;
    LOG('INFO', '✅ CDP session created');

    // 4. Проверяем память Chrome
    memoryMB = await getChromeMemoryMB(client);
    checks.memoryChecked = true;
    LOG('INFO', `Chrome memory: ${memoryMB !== null ? `${memoryMB}MB` : 'N/A'}`);

    // 5. Проверяем загрузку страницы и composer
    const loadCheckStart = Date.now();
    while (Date.now() - loadCheckStart < COMPOSER_TIMEOUT) {
      composerInfo = await checkPageLoad(client);
      if (composerInfo?.found) {
        checks.composerFound = true;
        LOG('INFO', `✅ Composer found: ${composerInfo.tag} (${composerInfo.w}x${composerInfo.h}) placeholder="${composerInfo.placeholder}"`);
        break;
      }
      
      // Проверяем URL (логин/CAPTCHA)
      if (composerInfo?.url) {
        if (/login|signin|auth/i.test(composerInfo.url)) {
          LOG('WARN', `⚠️ Page shows LOGIN URL: ${composerInfo.url}`);
        }
        if (/captcha|challenge|verify/i.test(composerInfo.url)) {
          LOG('WARN', `🚫 Page shows CAPTCHA: ${composerInfo.url}`);
        }
      }
      
      await sleep(1000);
    }

    if (!checks.composerFound) {
      LOG('WARN', `⚠️ Composer NOT found within ${COMPOSER_TIMEOUT}ms. Page info: ${JSON.stringify(composerInfo)}`);
      // Не считаем это критической ошибкой — демон работает, просто страница не загрузилась
    }

  } catch (e) {
    LOG('ERROR', `CDP check failed: ${e.message}`);
    // CDP check не критичен, но запишем
  } finally {
    try { await browser.disconnect(); } catch {}
  }

  // Итог
  const allPassed = Object.values(checks).every(Boolean);
  const criticalPassed = checks.endpointFile && checks.endpointValid && checks.puppeteerConnect;
  
  if (allPassed) {
    LOG('INFO', `✅ Health check PASSED (memory: ${memoryMB}MB)`);
    resetFailedCount();
    return { ok: true, checks, memoryMB, composerInfo, error: null };
  } else if (criticalPassed) {
    LOG('WARN', `⚠️ Health check PARTIAL (composer not found, but daemon is alive)`);
    resetFailedCount();
    return { ok: true, checks, memoryMB, composerInfo, warning: 'composer_not_found', error: null };
  } else {
    LOG('ERROR', `❌ Health check FAILED: ${errorMsg}`);
    const count = incrementFailedCount();
    LOG('ERROR', `Failed count: ${count}/3`);
    return { ok: false, checks, memoryMB, composerInfo, error: errorMsg, failedCount: count };
  }
}

function incrementFailedCount() {
  let count = 0;
  try {
    if (fs.existsSync(FAILED_COUNT_FILE)) {
      count = parseInt(fs.readFileSync(FAILED_COUNT_FILE, 'utf8').trim(), 10) || 0;
    }
    count++;
    fs.writeFileSync(FAILED_COUNT_FILE, String(count), 'utf8');
  } catch {}
  return count;
}

function resetFailedCount() {
  try { fs.unlinkSync(FAILED_COUNT_FILE); } catch {}
}

// ─── Restart logic ──────────────────────────────────────────────────────────
async function restartDaemon(reason = 'health check failed') {
  LOG('WARN', `Restarting daemon (reason: ${reason})...`);
  try {
    execSync('pm2 restart deepseek-daemon', { stdio: 'inherit' });
    LOG('INFO', '✅ Daemon restart triggered');
    return true;
  } catch (e) {
    LOG('ERROR', `Failed to restart daemon: ${e.message}`);
    return false;
  }
}

// ─── Main ──────────────────────────────────────────────────────────────────
(async () => {
  try {
    const result = await runHealthCheck();
    
    if (!result.ok) {
      // Решаем: перезапускать или нет
      if (result.failedCount >= 2) {
        LOG('ERROR', `Failed ${result.failedCount} times consecutively. Forcing restart.`);
        await restartDaemon(result.error);
      } else {
        LOG('WARN', `Not restarting yet (${result.failedCount}/2 failures). Will retry next cycle.`);
        // Попробуем ещё раз подключиться через 5 секунд
        LOG('INFO', 'Waiting 5s before retry...');
        await sleep(5000);
        const retry = await runHealthCheck();
        if (!retry.ok && retry.failedCount >= 2) {
          await restartDaemon(retry.error);
        }
      }
    } else if (result.warning === 'composer_not_found') {
      // Демон жив, но страница не загружена — перезапускаем через 2 цикла
      const count = incrementFailedCount();
      if (count >= 2) {
        LOG('WARN', 'Composer missing 2 times. Restarting daemon to reload page.');
        await restartDaemon('composer_not_found');
        resetFailedCount();
      }
    } else {
      if (result.memoryMB !== null && result.memoryMB > 1500) {
        LOG('WARN', `⚠️ Chrome memory HIGH (${result.memoryMB}MB). Consider restarting.`);
        const count = incrementFailedCount();
        if (count >= 2) {
          LOG('WARN', 'Memory high for 2 cycles. Restarting daemon.');
          await restartDaemon('high_memory');
          resetFailedCount();
        }
      }
    }
  } catch (e) {
    LOG('ERROR', `Health check crashed: ${e.message}`);
    try { restartDaemon(`crash: ${e.message}`); } catch {}
    process.exit(1);
  }
})();
