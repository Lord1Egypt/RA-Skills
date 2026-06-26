const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const PROFILE_DIR = path.join(__dirname, '.profile');
const SESSIONS_DIR = path.join(__dirname, '.sessions');
const SESSION_FILE = path.join(SESSIONS_DIR, 'daemon.json');
const DAEMON_ENDPOINT_FILE = path.join(__dirname, '.daemon-ws-endpoint');
const DS_URL = 'https://chat.deepseek.com/';

function unlinkIfMatches(filePath, expectedContent) {
  try {
    if (!fs.existsSync(filePath)) return;
    const current = fs.readFileSync(filePath, 'utf8');
    if (current === expectedContent) {
      fs.unlinkSync(filePath);
    }
  } catch (e) {}
}

(async () => {
  console.log('🚀 Запуск DeepSeek Daemon...');
  
  // Создаём директории
  fs.mkdirSync(PROFILE_DIR, { recursive: true });
  fs.mkdirSync(SESSIONS_DIR, { recursive: true });

  // Запускаем браузер
  const browser = await puppeteer.launch({
    headless: 'new',
    userDataDir: PROFILE_DIR,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-blink-features=AutomationControlled',
      '--no-first-run',
      '--no-default-browser-check',
      '--disable-gpu',
      '--window-size=1280,800',
    ],
  });

  const page = (await browser.pages())[0];

  // Сохраняем endpoint сразу, чтобы клиенты могли подключиться пока грузится DeepSeek
  const endpoint = browser.wsEndpoint();
  const sessionPayload = JSON.stringify({ 
    browserWSEndpoint: endpoint,
    pid: process.pid,
    created: new Date().toISOString() 
  });
  fs.writeFileSync(DAEMON_ENDPOINT_FILE, endpoint);
  fs.writeFileSync(SESSION_FILE, sessionPayload);
  console.log(`✅ Endpoint готов: ${endpoint}`);
  console.log(`📁 Endpoint file: ${DAEMON_ENDPOINT_FILE}`);
  
  // Переходим на DeepSeek с retry
  const MAX_NAV_RETRIES = 3;
  for (let attempt = 1; attempt <= MAX_NAV_RETRIES; attempt++) {
    try {
      console.log(`📍 Навигация на DeepSeek (попытка ${attempt}/${MAX_NAV_RETRIES})...`);
      await page.goto(DS_URL, { timeout: 60000, waitUntil: 'domcontentloaded' });
      console.log('✅ DeepSeek page loaded');
      break;
    } catch (navErr) {
      console.log(`⚠️ Навигация не удалась (попытка ${attempt}): ${navErr.message}`);
      if (attempt < MAX_NAV_RETRIES) {
        const waitMs = Math.min(attempt * 5000, 15000);
        console.log(`⏳ Ожидание ${waitMs / 1000}s перед повторной попыткой...`);
        await new Promise(r => setTimeout(r, waitMs));
        try { await page.reload({ waitUntil: 'domcontentloaded', timeout: 30000 }); } catch {}
      } else {
        console.error('❌ Не удалось загрузить DeepSeek после ' + MAX_NAV_RETRIES + ' попыток');
        console.log('⚠️ Демон работает, но страница не загружена. ask-puppeteer.js попытается перенавигацию.');
      }
    }
  }

  // ─── Обработка крашей страницы + авто-восстановление ───
  page.on('error', async (err) => {
    console.error('⚠️ Страница упала, перезагружаем...', err.message);
    try {
      await page.reload({ waitUntil: 'domcontentloaded', timeout: 30000 });
      console.log('✅ Страница перезагружена');
    } catch (e) {
      console.error('❌ Не удалось перезагрузить страницу:', e.message);
    }
  });

  // Периодическая проверка: если страница на chrome-error — перезагружаем
  let _pageHealthy = true;
  setInterval(async () => {
    try {
      const url = page.url();
      if (url.includes('chrome-error://') || url.includes('chrome-error')) {
        console.log('⚠️ Страница на error page, перезагружаем...');
        await page.goto(DS_URL, { timeout: 30000, waitUntil: 'domcontentloaded' });
        console.log('✅ Страница восстановлена: ' + page.url());
        _pageHealthy = true;
      }
    } catch (e) {
      if (_pageHealthy) {
        console.log('⚠️ Проверка здоровья страницы не удалась: ' + e.message);
        _pageHealthy = false;
      }
    }
  }, 30000);

  // Graceful shutdown
  const shutdown = async (signal) => {
    console.log(`\n(System) Получен ${signal}, останавливаю демон...`);
    try {
      await browser.close();
    } catch (e) {}
    try {
      unlinkIfMatches(DAEMON_ENDPOINT_FILE, endpoint);
      unlinkIfMatches(SESSION_FILE, sessionPayload);
      console.log('✅ Демон остановлен');
    } catch (e) {}
    process.exit(0);
  };

  process.on('SIGTERM', () => shutdown('SIGTERM'));
  process.on('SIGINT', () => shutdown('SIGINT'));
  process.on('SIGHUP', () => shutdown('SIGHUP'));

  // Логируем PID
  console.log(`🆔 PID: ${process.pid}`);
  console.log('💡 Для остановки: kill ' + process.pid);
  console.log('💡 Или: node ' + __filename + ' --stop');
})();
