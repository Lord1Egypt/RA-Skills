// 本机配置。路径类的东西不写进代码，放这里，方便换机器和对外发布。
//
// 位置：$CSR_CONFIG 或 ~/.chat-share-reader/config.json
// 可选项：
//   opencliBin      opencli 可执行文件路径
//   convolvgerBin   convolvger 可执行文件路径
//   chromeBin       Chrome / Edge 路径
//   profile         CDP 后端用的 Chrome profile 目录
//   port            CDP 调试端口，默认 9333
//   backend         auto | opencli | cdp，默认 auto
import { readFileSync, existsSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';

let cache = null;

export function configPath() {
  return process.env.CSR_CONFIG || path.join(os.homedir(), '.chat-share-reader', 'config.json');
}

export function config() {
  if (cache) return cache;
  const file = configPath();
  if (!existsSync(file)) return (cache = {});
  try {
    cache = JSON.parse(readFileSync(file, 'utf8'));
  } catch {
    cache = {};
  }
  return cache;
}

// 去掉末尾分隔符，避免路径拼接出现双斜杠
export function norm(p) {
  return typeof p === 'string' ? p.replace(/[\\/]+$/, '') : p;
}
