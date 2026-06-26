import { logger } from './logger.js';

/**
 * 带重试的异步操作
 */
export async function withRetry(fn, { maxRetries = 3, delayMs = 3000, label = '' } = {}) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (err) {
      if (attempt === maxRetries) {
        logger.error(`${label} 重试 ${maxRetries} 次后仍失败: ${err.message}`);
        throw err;
      }
      logger.warn(`${label} 第 ${attempt} 次失败，${delayMs}ms 后重试: ${err.message}`);
      await new Promise(r => setTimeout(r, delayMs));
    }
  }
}

/**
 * 等待用户手动处理验证码等
 */
export async function waitForUserAction(page, message, timeoutMs = 120000) {
  logger.warn(`⚠️ 需要手动操作: ${message}`);
  logger.warn(`等待最多 ${timeoutMs / 1000} 秒...`);
  
  // 等待页面上验证码消失或用户完成操作
  const startTime = Date.now();
  while (Date.now() - startTime < timeoutMs) {
    await new Promise(r => setTimeout(r, 2000));
    // 检查是否还有验证码弹窗
    const hasVerifyPopup = await page.evaluate(() => {
      const popups = document.querySelectorAll('.verify-modal, .captcha, [class*="verify"], [class*="captcha"]');
      return popups.length > 0;
    }).catch(() => false);
    
    if (!hasVerifyPopup) {
      logger.info('验证码已处理，继续执行');
      return true;
    }
  }
  
  logger.error('等待超时，跳过当前操作');
  return false;
}
