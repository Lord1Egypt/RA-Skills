#!/usr/bin/env node
/**
 * catchlinger-env.mjs —— 读取 CatchLinger 的配置。
 *
 * 配置来源（环境变量优先，文件只补缺失项）：
 *   · 环境变量 CATCHLINGER_API_BASE / CATCHLINGER_API_KEY
 *   · ~/.config/catchlinger/env（KEY=VALUE 格式，每行一条）
 *
 * 三个脚本共用：catchlinger-api.mjs / tag-resolver.mjs / github-stars.mjs。
 * 零依赖，只用 Node 内置 API。
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const ENV_FILE = path.join(os.homedir(), '.config', 'catchlinger', 'env');

/** 读取 ~/.config/catchlinger/env；已存在的环境变量不会被文件覆盖。 */
export function loadEnvFile(file = ENV_FILE) {
  if (!fs.existsSync(file)) return;
  for (const line of fs.readFileSync(file, 'utf8').split(/\r?\n/)) {
    const t = line.trim();
    if (!t || t.startsWith('#')) continue;
    const i = t.indexOf('=');
    if (i < 0) continue;
    const key = t.slice(0, i).trim();
    const value = t.slice(i + 1).trim().replace(/^["']|["']$/g, '');
    if (key && !(key in process.env)) process.env[key] = value;
  }
}

/**
 * 读取 CatchLinger API 的配置。
 * @returns {{ base: string, key: string } | null} 没配全时返回 null
 */
export function loadCatchLingerEnv() {
  loadEnvFile();
  const base = (process.env.CATCHLINGER_API_BASE ?? '').replace(/\/$/, '');
  const key = process.env.CATCHLINGER_API_KEY ?? '';
  if (!base || !key) return null;
  return { base, key };
}

/** 读取 GitHub 相关的可选配置。 */
export function loadGithubEnv() {
  loadEnvFile();
  return {
    token: (process.env.GITHUB_TOKEN ?? '').trim(),
    username: (process.env.GITHUB_USERNAME ?? '').trim(),
  };
}
