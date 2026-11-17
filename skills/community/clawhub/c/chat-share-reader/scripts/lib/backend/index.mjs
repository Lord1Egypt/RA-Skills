// 后端选择。两个后端实现同一组方法：open / eval / waitReady / close。
//
// auto 的顺序：有 opencli 用 opencli（本机省事、复用已有登录态），否则用 CDP 拉真 Chrome。
// 都没有就报错，并说明浏览器通道能做什么、纯 HTTP 通道还能跑哪些站。
import { config } from '../config.mjs';
import * as opencliBackend from './opencli.mjs';
import * as cdpBackend from './cdp.mjs';

export function describe() {
  return {
    opencli: opencliBackend.available() ? opencliBackend.findOpencli() : '',
    chrome: cdpBackend.findChrome(),
    profile: cdpBackend.defaultProfile(),
  };
}

// 有没有任何一条浏览器通道可用。
// 调用方只该问"能不能开浏览器"，不该关心是哪一个后端——早先几处直接 import
// opencli.mjs，导致装了 Chrome 但没装 opencli 的机器明明能跑却被判成不能用。
export function available() {
  return opencliBackend.available() || cdpBackend.available();
}

export async function createSession(opts = {}) {
  const want = (process.env.CSR_BACKEND || opts.backend || config().backend || 'auto').toLowerCase();

  if (want === 'opencli') {
    return await opencliBackend.createSession(opts);
  }
  if (want === 'cdp') {
    return await cdpBackend.createSession(opts);
  }

  if (opencliBackend.available()) {
    try {
      return await opencliBackend.createSession(opts);
    } catch (e) {
      if (!cdpBackend.available()) throw e;
      // opencli 装了但连不上（扩展没开、daemon 挂了），退到 CDP
      console.error('[提示] opencli 不可用，改用 CDP 后端：' + String(e.message).slice(0, 120));
    }
  }
  if (cdpBackend.available()) {
    return await cdpBackend.createSession(opts);
  }

  throw new Error(
    'No browser backend available.\n' +
      '  Option 1: install opencli (Chrome extension + CLI) and set OPENCLI_BIN\n' +
      '  Option 2: install Chrome or Edge, the script launches it automatically\n' +
      '  (first visit to a Cloudflare-protected site needs one manual check in the popup)\n' +
      '  Sites that still work over plain HTTP: chatgpt.com / workbuddy.link\n' +
      '没有可用的浏览器后端。装 opencli 并设 OPENCLI_BIN，或装 Chrome/Edge 让脚本自动拉起。\n' +
      '纯 HTTP 通道仍可用的站点：chatgpt.com / workbuddy.link'
  );
}
