// PATH 查找。抽出来的原因很实际：vendor.mjs 和 backend/opencli.mjs 各写过一份，
// 谁改谁忘，行为会悄悄分叉。
//
// 保留的一个细节：`where` 在 Windows 上可能返回多行（同名命令散落在多个 PATH 目录），
// 要取第一个真实存在的，不能盲取第一行——第一行可能指向一个已被删掉的旧安装，
// 那种失败表现是"明明装了却说没有"。
//
// 实测过、结论是否定的：Windows 的 `where` 并不只匹配 PATHEXT，无扩展名的
// bash 脚本（opencli 就是 `#!/usr/bin/env bash`）也能直接查到，不需要自己扫 PATH。
import { execFileSync } from 'node:child_process';
import { existsSync } from 'node:fs';

// 只缓存命中结果。找不到就不缓存，免得同一进程里装完还读不到。
const hits = new Map();

export function which(name) {
  if (!name) return '';
  if (hits.has(name)) return hits.get(name);
  const found = lookup(name);
  if (found) hits.set(name, found);
  return found;
}

function lookup(name) {
  const cmd = process.platform === 'win32' ? 'where' : 'which';
  let out;
  try {
    out = execFileSync(cmd, [name], {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'ignore'],
    });
  } catch {
    return '';
  }
  for (const line of out.split(/\r?\n/)) {
    const p = line.trim();
    if (p && existsSync(p)) return p;
  }
  return '';
}
