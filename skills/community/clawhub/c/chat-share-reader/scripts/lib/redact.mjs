// 导出内容脱敏。
//
// 对话正文里出现本机路径是常态：agent 报错会带上完整路径，工具输出会带用户名，
// 一段日志里可能同时有 C:\Users\alice\... 和 /home/alice/...。这些内容一旦导出
// 成文件再分享出去，泄露的是账号名和目录结构，不是对话本身。
//
// 三档，默认 home：
//   off    不处理
//   home   家目录和同机其他用户的家目录换成 ~ / ~user，保留目录结构；令牌一律遮
//   strict 在 home 之上再遮邮箱、内网 IP
//
// 只做文本替换，不改 markdown 结构。替换是幂等的：脱敏后的文本再跑一次不会二次变化
// （替换成 ~ 之后不再匹配原始家目录路径），所以重复处理同一份文件是安全的。

import os from 'node:os';

export const LEVELS = ['off', 'home', 'strict'];

function esc(s) {
  return String(s).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

const isWin = process.platform === 'win32';

// 同一个路径在文本里可能是反斜杠、正斜杠两种写法，两种都要盖到。
// 长的排前面，避免短前缀先替换掉导致长路径只被改了一半。
function homeVariants() {
  const home = os.homedir();
  if (!home) return [];
  const set = new Set([
    home,
    home.replace(/\\/g, '/'),
    home.replace(/\//g, '\\'),
    // JSON 里常见的转义反斜杠写法：C:\\Users\\alice
    home.replace(/\\/g, '\\\\'),
  ]);
  return [...set].filter(Boolean).sort((a, b) => b.length - a.length);
}

// 令牌类。宁可多遮：这些字符串一旦是假的，遮掉也没损失；一旦是真的，漏出去就是事故。
const SECRET_RULES = [
  // OpenAI / Anthropic 风格
  /\bsk-[A-Za-z0-9_-]{16,}/g,
  // GitHub
  /\bgh[pousr]_[A-Za-z0-9]{16,}/g,
  /\bgithub_pat_[A-Za-z0-9_]{20,}/g,
  // AWS
  /\bAKIA[0-9A-Z]{16}\b/g,
  // Slack
  /\bxox[abprs]-[A-Za-z0-9-]{10,}/g,
  // JWT（三段点分 base64url）
  /\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{6,}/g,
  // Authorization 头
  /\b(Bearer|Basic)\s+[A-Za-z0-9._~+/=-]{16,}/g,
  // 微信/企业微信的 agent ticket 一类长串
  /\b(agt1|xoxb)-[A-Za-z0-9_-]{20,}/g,
];

const EMAIL = /\b([A-Za-z0-9._%+-])([A-Za-z0-9._%+-]*)@([A-Za-z0-9.-]+\.[A-Za-z]{2,})\b/g;

// 只遮内网段。公网 IP 可能是有意义的信息（比如用户在排查某个服务），不碰。
const PRIVATE_IP =
  /\b(?:10\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])|192\.168)\.\d{1,3}\.\d{1,3}\b/g;

/**
 * 造一个脱敏器。hits 记录本次累计替换处数，用于在文件头标注。
 * 每次 buildDoc 造一个新的，不要跨文档复用，否则计数会累加。
 */
export function createRedactor(level = 'home') {
  const lv = LEVELS.includes(level) ? level : 'home';
  let hits = 0;

  function sub(re, text, fn) {
    return text.replace(re, (...a) => {
      hits++;
      return typeof fn === 'function' ? fn(...a) : fn;
    });
  }

  const homes = lv === 'off' ? [] : homeVariants();

  // 同机的其它用户目录。这两个根下的第二段就是用户名。
  const userRoots = [
    /([A-Za-z]:[\\/]+Users[\\/]+)([^\\/\s"'`<>|:]+)/gi,
    /(\/(?:home|Users)\/)([^/\s"'`<>|:]+)/g,
  ];

  function apply(text) {
    let s = String(text ?? '');
    if (lv === 'off' || !s) return s;

    for (const h of homes) {
      const re = new RegExp(esc(h), isWin ? 'gi' : 'g');
      s = sub(re, s, '~');
    }

    for (const re of userRoots) {
      s = s.replace(re, (m, root, name) => {
        // 已经是 ~ 说明上面替换过家目录，不再动
        if (m.includes('~')) return m;
        hits++;
        return `~${name}${m.slice(root.length + name.length)}`;
      });
    }

    // 令牌在所有档位都遮（off 除外）。这类串没有「导出后还要保留」的合法用途，
    // 而一旦是真凭据漏进一个会被转发的文件，代价不对称。home 档以前不遮，是漏网。
    for (const re of SECRET_RULES) s = sub(re, s, '[redacted]');

    if (lv === 'strict') {
      s = sub(EMAIL, s, (m, first, rest, domain) => `${first}***@${domain}`);
      s = sub(PRIVATE_IP, s, (m) => m.split('.').slice(0, 2).join('.') + '.x.x');
    }

    return s;
  }

  return { level: lv, apply, hits: () => hits };
}

/** 一次性脱敏，不需要计数的场合用 */
export function redact(text, level = 'home') {
  return createRedactor(level).apply(text);
}
