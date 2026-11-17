// curl 封装。用子进程而不是 Node fetch：重定向、压缩、系统代理都由 curl 处理。
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';

const exec = promisify(execFile);

const UA =
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36';

// 单次响应上限。抓分享页最大也就几 MB，512MB 只会放大资源耗尽风险。
const MAX_BYTES = 64 * 1024 * 1024;

// 只接受 http/https 的绝对地址。
// 挡住两类输入：file:// / gopher:// 这类能读本地资源的协议，以及以 - 开头、
// 会被 curl 当成选项解析的字符串（虽然下面还加了 -- 终止符，这里是第二道）。
export function assertHttpUrl(raw) {
  const s = String(raw == null ? '' : raw).trim();
  if (!s || s.startsWith('-')) throw new Error('拒绝的 URL 形式：' + s.slice(0, 200));
  let u;
  try {
    u = new URL(s);
  } catch {
    throw new Error('不是合法的绝对 URL：' + s.slice(0, 200));
  }
  if (u.protocol !== 'http:' && u.protocol !== 'https:') {
    throw new Error('只允许 http/https，收到 ' + u.protocol + '：' + s.slice(0, 200));
  }
  return s;
}

export async function httpGet(url, { headers = [], timeout = 45 } = {}) {
  const target = assertHttpUrl(url);
  const args = ['-sSL', '--compressed', '-m', String(timeout), '-A', UA];
  for (const h of headers) args.push('-H', h);
  // -- 结束选项解析，之后的内容一律当位置参数，即使以 - 开头
  args.push('--', target);
  const { stdout } = await exec('curl', args, { maxBuffer: MAX_BYTES });
  return stdout;
}

export async function httpGetJson(url, opts) {
  const text = await httpGet(url, opts);
  try {
    return JSON.parse(text);
  } catch {
    const hint = /Just a moment|cf-challenge/.test(text)
      ? '被 Cloudflare 挑战拦截，这个站点需要浏览器通道'
      : '返回不是 JSON';
    throw new Error(`${hint}（${url}）`);
  }
}

// 从 HTML 里捞一段内联 JSON 对象（按括号配平截取）
export function sliceJsonObject(html, startIndex) {
  let depth = 0;
  let inStr = false;
  let esc = false;
  for (let i = startIndex; i < html.length; i++) {
    const ch = html[i];
    if (inStr) {
      if (esc) esc = false;
      else if (ch === '\\') esc = true;
      else if (ch === '"') inStr = false;
      continue;
    }
    if (ch === '"') inStr = true;
    else if (ch === '{') depth++;
    else if (ch === '}') {
      depth--;
      if (depth === 0) return html.slice(startIndex, i + 1);
    }
  }
  return null;
}
