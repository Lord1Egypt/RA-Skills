// Convolvger 适配层。第三方 CLI，覆盖 8 个 provider，直接读各站分享页自己用的那套数据接口，
// 比 DOM 重建准确，也比我手写的解析完整（带快照时间、conversation id、每条消息的原始时间戳）。
//
// 探测顺序（任选其一即可）：
//   1. CONVOLVGER_BIN 环境变量指向可执行文件
//   2. PATH 里的 convolvger
//   3. uvx（装了 uv 就有），临时运行钉版本的那份，无需预装
//   4. ~/.chat-share-reader/config.json 里的 convolvgerBin
//
// 分工：能交给它的一律交给它，只保留它做不到或实测失效的站点自己实现。
// - 它不支持 workbuddy
// - 它的 chatgpt 适配依赖页面里的 turbo-stream，当前 chatgpt 分享页已不含该数据（实测报错）
// - 它的 perplexity 适配落后于当前接口结构（只导出问题，没有正文）
// - 它的 claude 要 bookmarklet 手工交接，不适合 agent 自动跑
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { existsSync } from 'node:fs';
import { stat } from 'node:fs/promises';
import { config, norm } from './config.mjs';
import { which } from './which.mjs';

const exec = promisify(execFile);

// uvx 兜底必须钉版本。不钉的话每次解析到当时最新的发布，装进来跑的代码和审过的不是同一份，
// 对使用者是供应链风险，对扫描器是「未固定的外部依赖」。要换版本设 CSR_CONVOLVGER_SPEC。
const UVX_SPEC = process.env.CSR_CONVOLVGER_SPEC || 'convolvger==0.7.0';

let cached = null;

function resolve() {
  if (cached !== null) return cached;

  const envBin = process.env.CONVOLVGER_BIN;
  if (envBin && existsSync(envBin)) return (cached = { bin: envBin, pre: [] });

  const onPath = which('convolvger');
  if (onPath) return (cached = { bin: onPath, pre: [] });

  const uvx = which('uvx');
  if (uvx) return (cached = { bin: uvx, pre: ['--from', UVX_SPEC, 'convolvger'] });

  const fromConfig = norm(config().convolvgerBin);
  if (fromConfig && existsSync(fromConfig)) return (cached = { bin: fromConfig, pre: [] });

  return (cached = null);
}

export function findConvolvger() {
  const r = resolve();
  if (!r) return '';
  return r.pre.length ? `${r.bin} ${r.pre.join(' ')}` : r.bin;
}

const CONVOLVGER_HINT =
  'Convolvger 不可用。装法任选其一：\n' +
  '  uv tool install convolvger       （推荐，需 Python 3.12+）\n' +
  '  pip install convolvger\n' +
  '  brew install uv && uvx --from convolvger==0.7.0 convolvger（不预装，临时运行）\n' +
  '  或设置 CONVOLVGER_BIN 指向可执行文件';

// Convolvger 原生支持的站点。claude / perplexity 要人工交接或自写解析，不列入自动路径。
export const VENDOR_HOSTS = [
  'chatgpt.com',
  'gemini.google.com',
  'share.gemini.google',
  'g.co',
  'grok.com',
  'chat.deepseek.com',
  'kimi.ai',
  'kimi.com',
  'kimi.moonshot.cn',
  'chat.qwen.ai',
  'chat.qwenlm.ai',
];

export function supports(url) {
  try {
    const host = new URL(url).hostname.replace(/^www\./, '').replace(/\.$/, '');
    return VENDOR_HOSTS.includes(host);
  } catch {
    return false;
  }
}

function lastLine(s) {
  return (
    String(s || '')
      .trim()
      .split('\n')
      .filter(Boolean)
      .pop() || ''
  );
}

// 导出到文件。成功返回 {file, warnings}；失败抛出带原因的错误，让调用方决定是否回退。
//
// 注意：Convolvger 在有 warning（未建模的 tool block、被提供商撤销的消息等）时返回非零退出码，
// 但内容已经完整产出。所以判成败看文件有没有写出来，不看 exit code。
export async function exportMarkdown(url, outFile) {
  const r = resolve();
  if (!r) throw new Error(CONVOLVGER_HINT);

  let err = null;
  try {
    await exec(r.bin, [...r.pre, 'export', url, '--format', 'md', '-o', outFile], {
      maxBuffer: 64 * 1024 * 1024,
    });
  } catch (e) {
    err = e;
  }

  if (existsSync(outFile)) {
    const { size } = await stat(outFile);
    if (size > 0) return { file: outFile, warnings: err ? lastLine(err.stderr) : '' };
  }
  throw new Error(err ? lastLine(err.stderr) || String(err.message) : '导出没有产出文件');
}

// 只探测不落盘，用来判断这条链接能不能被 vendor 读到。同样不看 exit code。
export async function inspect(url) {
  const r = resolve();
  if (!r) throw new Error(CONVOLVGER_HINT);

  let out = '';
  let err = null;
  try {
    ({ stdout: out } = await exec(r.bin, [...r.pre, 'inspect', url], {
      maxBuffer: 16 * 1024 * 1024,
    }));
  } catch (e) {
    out = e.stdout || '';
    err = e;
  }
  if (/^Provider:/m.test(out)) return out;
  throw new Error(err ? lastLine(err.stderr) || String(err.message) : '没有可解析的输出');
}
