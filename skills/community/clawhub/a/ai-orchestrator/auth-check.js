/**
 * Auth State Checker
 * Проверяет состояние авторизации DeepSeek перед отправкой промпта.
 * Возвращает статус и, если нужно, бросает ошибку или выдаёт предупреждение.
 * 
 * Использование:
 *   const auth = await checkAuth(page, tracer);
 *   if (auth.needsLogin) throw new Error('Требуется авторизация...');
 *   if (auth.hasCaptcha) { tracer.skip('auth_check', 'CAPTCHA detected'); }
 */

const URL_PATTERNS = {
  LOGIN:    [/login/i, /signin/i, /sign-in/i, /auth/i, /account/i],
  CAPTCHA:  [/captcha/i, /challenge/i, /verify/i],
  RATE_LIMIT: [/rate.?limit/i, /too.?many/i],
};

const LOGIN_INDICATORS = [
  // Текст на странице
  { type: 'text', value: 'sign in', weight: 2 },
  { type: 'text', value: 'log in', weight: 2 },
  { type: 'text', value: 'войти', weight: 2 },
  { type: 'text', value: 'авторизац', weight: 2 },
  { type: 'text', value: 'создать аккаунт', weight: 2 },
  { type: 'text', value: 'sign up', weight: 2 },
  // Кнопки
  { type: 'button', value: 'sign in', weight: 3 },
  { type: 'button', value: 'log in', weight: 3 },
  { type: 'button', value: 'войти', weight: 3 },
  // Формы
  { type: 'form', value: 'login', weight: 3 },
  { type: 'input', value: 'email', weight: 2 },
  { type: 'input', value: 'password', weight: 3 },
];

const CHAT_INDICATORS = [
  // Composer / input field
  { type: 'selector', value: 'textarea[placeholder*="Message"]', weight: 5 },
  { type: 'selector', value: 'textarea[placeholder*="Введите"]', weight: 5 },
  { type: 'selector', value: 'textarea[placeholder*="Type"]', weight: 5 },
  { type: 'selector', value: 'div[contenteditable="true"]', weight: 4 },
  { type: 'selector', value: 'textarea', weight: 3 },
  // URL
  { type: 'url', value: '/a/chat/', weight: 5 },
  { type: 'url', value: 'deepseek.com/a/chat', weight: 5 },
  // Текст
  { type: 'text', value: 'new chat', weight: 2 },
  { type: 'text', value: 'deepseek', weight: 1 },
];

/**
 * @param {import('puppeteer').Page} page
 * @param {Object} tracer - PipelineTrace instance (optional)
 * @returns {Promise<{status: string, needsLogin: boolean, hasCaptcha: boolean, score: number, details: Object}>}
 */
async function checkAuth(page, tracer = null) {
  const result = {
    status: 'unknown',
    needsLogin: false,
    hasCaptcha: false,
    score: 0,           // >0 = скорее всего чат, <0 = скорее всего логин
    details: {},
  };

  let pageUrl;
  try {
    pageUrl = page.url();
    result.details.url = pageUrl;
  } catch (e) {
    result.status = 'error';
    return result;
  }

  // 1. URL-based checks (самые надёжные)
  for (const pattern of URL_PATTERNS.LOGIN) {
    if (pattern.test(pageUrl)) {
      result.needsLogin = true;
      result.score -= 10;
      result.details.urlMatch = `login pattern: ${pattern}`;
    }
  }
  for (const pattern of URL_PATTERNS.CAPTCHA) {
    if (pattern.test(pageUrl)) {
      result.hasCaptcha = true;
      result.score -= 10;
      result.details.urlMatch = `captcha pattern: ${pattern}`;
    }
  }

  // 2. DOM-based checks
  let domData;
  try {
    domData = await page.evaluate(() => {
      const bodyText = document.body?.innerText?.toLowerCase() || '';
      const hasText = (text) => bodyText.includes(text.toLowerCase());
      
      // Ищем форму логина
      const hasLoginForm = !!document.querySelector('form[action*="login"], input[type="email"], input[name="email"], input[name="login"]');
      const hasPasswordField = !!document.querySelector('input[type="password"]');
      
      // Ищем composer
      const hasComposer = !!(
        document.querySelector('textarea[placeholder*="message" i]') ||
        document.querySelector('textarea[placeholder*="введите" i]') ||
        document.querySelector('textarea[placeholder*="type" i]') ||
        document.querySelector('div[contenteditable="true"][role="textbox"]') ||
        document.querySelector('div[role="textbox"]')
      );
      
      // Ищем кнопку отправки
      const hasSendButton = !!(
        document.querySelector('button[type="submit"]') ||
        document.querySelector('[data-testid="send"]') ||
        document.querySelector('button[aria-label*="send" i]')
      );
      
      // CAPTCHA-специфичные элементы
      const hasCaptcha = !!(
        document.querySelector('[class*="captcha" i]') ||
        document.querySelector('[id*="captcha" i]') ||
        document.querySelector('iframe[src*="captcha"]') ||
        document.querySelector('[class*="challenge" i]')
      );
      
      return {
        bodyTextLen: bodyText.length,
        hasLoginForm,
        hasPasswordField,
        hasComposer,
        hasSendButton,
        hasCaptcha,
        url: window.location.href,
      };
    });
    result.details.dom = domData;
  } catch (e) {
    result.details.domError = e.message;
  }

  // 3. Score calculation
  // Положительные признаки чата
  if (domData?.hasComposer) result.score += 5;
  if (domData?.hasSendButton) result.score += 3;
  if (pageUrl.includes('/a/chat/')) result.score += 5;
  
  // Отрицательные признаки логина
  if (domData?.hasLoginForm) result.score -= 5;
  if (domData?.hasPasswordField && domData?.hasLoginForm) result.score -= 5;
  
  // CAPTCHA
  if (result.hasCaptcha || domData?.hasCaptcha) {
    result.score -= 10;
    result.hasCaptcha = true;
  }

  // 4. Final status determination
  if (result.needsLogin || result.hasCaptcha || result.score < -2) {
    result.status = 'not_authenticated';
    result.needsLogin = true;
  } else if (result.score > 2 || (domData?.hasComposer)) {
    result.status = 'authenticated';
  } else {
    result.status = 'uncertain';
    result.details.uncertainReason = `score=${result.score}, hasComposer=${!!domData?.hasComposer}`;
  }

  return result;
}

/**
 * Проверяет авторизацию и бросает ошибку если нужно.
 * Использовать ДО отправки промпта.
 * 
 * @param {import('puppeteer').Page} page
 * @param {Object} tracer - PipelineTrace instance
 * @param {Function} logFn - функция логирования (например console.log)
 * @returns {Promise<boolean>} true если авторизован
 */
async function requireAuth(page, tracer = null, logFn = console.log) {
  const auth = await checkAuth(page, tracer);
  
  const color = auth.status === 'authenticated' ? '\x1b[32m' : '\x1b[31m';
  const reset = '\x1b[0m';
  const icon = auth.status === 'authenticated' ? '✅' : auth.hasCaptcha ? '🚫' : '⚠️';
  
  logFn(`${color}${icon} [AUTH] ${auth.status}${reset} (score: ${auth.score})`);
  if (auth.details.url) logFn(`   URL: ${auth.details.url}`);
  if (auth.details.domError) logFn(`   DOM check failed: ${auth.details.domError}`);
  if (auth.status === 'uncertain') logFn(`   ⚠️ Неопределённое состояние: ${auth.details.uncertainReason}`);
  
  if (auth.needsLogin || auth.hasCaptcha) {
    const instructions = `
╔══════════════════════════════════════════════════════════════╗
║  Требуется авторизация в DeepSeek!                          ║
╠══════════════════════════════════════════════════════════════╣
║  1. pm2 stop deepseek-daemon                                ║
║  2. Запустить Chrome вручную:                              ║
║     ~/.cache/puppeteer/chrome/linux-146.0.7680.153/         ║
║       chrome-linux64/chrome                                 ║
║       --user-data-dir=~/.openclaw/workspace/skills/        ║
║         ai-orchestrator/.profile                            ║
║       --no-sandbox                                          ║
║       https://chat.deepseek.com/                            ║
║  3. Авторизоваться, пройти CAPTCHA                         ║
║  4. Закрыть браузер                                        ║
║  5. pm2 start deepseek-daemon                              ║
╚══════════════════════════════════════════════════════════════╝`;
    logFn(`\x1b[31m${instructions}${reset}`);
    return false;
  }
  
  return true;
}

module.exports = { checkAuth, requireAuth, AUTH_URL_PATTERNS: URL_PATTERNS };
