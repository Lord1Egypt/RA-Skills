// 输出语言：英文用户看到英文，中文用户看到中文。
//
// 判定顺序：
//   1. CSR_LANG 环境变量（zh / en）
//   2. 系统 locale（LC_ALL / LANG / LANGUAGE）
//   3. 都拿不到时回落到中文
//
// 只影响终端输出和导出文件的元信息标题。SKILL.md 与 README 各有中英两份，不走这里。

const explicit = (process.env.CSR_LANG || '').toLowerCase().trim();
const sysLocale = (
  process.env.LC_ALL ||
  process.env.LC_MESSAGES ||
  process.env.LANG ||
  process.env.LANGUAGE ||
  ''
).toLowerCase();

function resolve() {
  if (explicit) return explicit.startsWith('zh') ? 'zh' : 'en';
  if (sysLocale) return sysLocale.startsWith('zh') ? 'zh' : 'en';
  return 'zh';
}

export const lang = resolve();
export const isZh = lang === 'zh';

/** 两个版本的同一句话，按当前语言取一个 */
export function t(zh, en) {
  return isZh ? zh : en;
}

/** 角色名统一在这里翻译，解析器里存中文，输出时映射 */
const ROLE_MAP = {
  用户: 'User',
  助手: 'Assistant',
  课堂笔记: 'Notes',
  逐字稿: 'Transcript',
  Assistant: 'Assistant',
  User: 'User',
};

export function role(name) {
  if (isZh) return name;
  return ROLE_MAP[name] || name;
}
