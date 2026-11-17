// opencli 后端：复用本机已装的 opencli（Chrome 扩展 + 本地 daemon）。
// 优点是不用管 Chrome 启动与登录态；缺点是只有装了 opencli 的机器有，所以它是可选后端。
//
// 三条硬约束（实测，改之前先看 references/sites.md）：
// 1. opencli 是 git-bash 包装脚本，必须经 bash 调用且 shell:false，否则 URL 里的 & 被当命令分隔
// 2. eval 单次入参超过约 5k 字符会 SyntaxError，超长脚本要分片
// 3. 单引号、花括号、模板字符串在 shell:false 下都能原样传进去，不需要转义
//
// 分片用 JSON 字符串字面量而不是 base64：内容保持明文可读，
// 静态扫描不会把它当成混淆载荷（这是安全审计里的高危误判项）。
import { execFile } from 'node:child_process';
import { config, norm } from '../config.mjs';
import os from 'node:os';
import path from 'node:path';
import { promisify } from 'node:util';
import { existsSync } from 'node:fs';
import { setTimeout as sleep } from 'node:timers/promises';
import { which } from '../which.mjs';

const exec = promisify(execFile);
// 实测 6k 会挂，4k 留足余量
const DIRECT_MAX = 4000;
const CHUNK = 2000;
const VAR = 'window.__csr';

export function findOpencli() {
  const candidates = [
    process.env.OPENCLI_BIN,
    norm(config().opencliBin),
    norm(path.join(os.homedir(), 'bin', 'opencli')),
    '/usr/local/bin/opencli',
    '/opt/homebrew/bin/opencli',
  ].filter(Boolean);
  for (const p of candidates) if (existsSync(p)) return p;

  // PATH 里找（Windows 上的裸名脚本由 which 自己兜底）
  return which('opencli');
}

export function available() {
  return !!findOpencli();
}

export async function createSession({ name = 'csr', bin } = {}) {
  const exe = bin || findOpencli();
  if (!exe) throw new Error('没有可用的 opencli');

  async function raw(...args) {
    const { stdout } = await exec('bash', [exe, 'browser', name, ...args], {
      maxBuffer: 512 * 1024 * 1024,
      shell: false,
    });
    return stdout;
  }

  async function cmd(...args) {
    let last;
    for (let i = 0; i < 4; i++) {
      try {
        return await raw(...args);
      } catch (e) {
        last = e;
        await sleep(2500);
      }
    }
    throw new Error(
      `opencli 调用失败：${args.join(' ')} :: ${String((last && last.stderr) || last).slice(0, 300)}`
    );
  }

  return {
    backend: 'opencli',
    name,

    async open(url, opts) {
      // 有些站（Gemini）在后台标签会被浏览器节流，Angular 不渲染，必须前台窗口打开
      const win = (opts && opts.window) || 'background';
      await cmd('open', url, '--window', win);
    },

    async eval(code) {
      const text = String(code == null ? '' : code);
      // 短脚本直接传，一条命令就能在命令行里看清执行了什么
      if (text.length <= DIRECT_MAX) return cmd('eval', text);

      const parts = [];
      for (let i = 0; i < text.length; i += CHUNK) parts.push(text.slice(i, i + CHUNK));
      await cmd('eval', `${VAR} = []`);
      for (const p of parts) {
        await cmd('eval', `${VAR}.push(${JSON.stringify(p)})`);
      }
      return cmd('eval', `eval(${VAR}.join(""))`);
    },

    async waitReady({ minText = 200, tries = 10, delay = 3000, probe } = {}) {
      for (let i = 0; i < tries; i++) {
        const code =
          probe || 'JSON.stringify({len: document.body.innerText.length, url: location.href})';
        let out;
        try {
          out = await raw('eval', code);
        } catch {
          await sleep(delay);
          continue;
        }
        try {
          const j = JSON.parse(out.slice(out.indexOf('{'), out.lastIndexOf('}') + 1));
          if (probe ? j.ok : j.len >= minText) return j;
        } catch {
          /* 还没渲染 */
        }
        await sleep(delay);
      }
      throw new Error('页面在超时内没有渲染出内容');
    },

    async close() {
      try {
        await raw('close');
      } catch {
        /* 关不掉就算了 */
      }
    },
  };
}
