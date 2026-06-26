/**
 * 自动检测依赖状态
 * 检查依赖是否已安装，如未安装则提示用户手动安装
 */

import { existsSync, readdirSync } from 'fs';
import { homedir } from 'os';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

let checkResult: { hasDeps: boolean; hasBrowser: boolean } | null = null;

/**
 * 获取 Playwright 浏览器缓存目录
 */
function getPlaywrightCacheDir(): string {
  const platform = process.platform;
  const home = homedir();
  
  switch (platform) {
    case 'win32':
      return join(home, 'AppData', 'Local', 'ms-playwright');
    case 'darwin':
      return join(home, 'Library', 'Caches', 'ms-playwright');
    default:
      return join(home, '.cache', 'ms-playwright');
  }
}

/**
 * 检查 node_modules 是否存在
 */
function hasNodeModules(): boolean {
  const nodeModulesPath = join(__dirname, '..', 'node_modules');
  const playwrightPath = join(nodeModulesPath, 'playwright');
  return existsSync(nodeModulesPath) && existsSync(playwrightPath);
}

/**
 * 检查 Chromium 浏览器是否已安装（跨平台）
 */
function hasChromiumInstalled(): boolean {
  const cacheDir = getPlaywrightCacheDir();
  
  if (!existsSync(cacheDir)) {
    return false;
  }
  
  try {
    const files = readdirSync(cacheDir);
    return files.some(file => file.startsWith('chromium-'));
  } catch {
    return false;
  }
}

/**
 * 检查依赖状态并返回安装提示
 * 不自动执行安装命令，而是提示用户手动安装
 */
export async function checkAndInstall(): Promise<{ ready: boolean; message: string }> {
  if (checkResult) {
    const { hasDeps, hasBrowser } = checkResult;
    if (hasDeps && hasBrowser) {
      return { ready: true, message: 'All dependencies are ready.' };
    }
  }
  
  const hasDeps = hasNodeModules();
  const hasBrowser = hasChromiumInstalled();
  
  checkResult = { hasDeps, hasBrowser };
  
  if (hasDeps && hasBrowser) {
    return { ready: true, message: 'All dependencies are ready.' };
  }
  
  // 构建安装提示信息
  const instructions: string[] = [];
  
  if (!hasDeps) {
    instructions.push('npm dependencies not found. Please run:');
    instructions.push('  cd ' + join(__dirname, '..'));
    instructions.push('  npm install --registry=https://registry.npmmirror.com');
  }
  
  if (!hasBrowser) {
    instructions.push('Playwright browser not found. Please run:');
    instructions.push('  npm run install:browser:cn');
    instructions.push('or:');
    instructions.push('  npx playwright install chromium');
  }
  
  return { 
    ready: false, 
    message: 'Missing dependencies:\n' + instructions.join('\n')
  };
}

/**
 * 快速检查（不自动安装）
 */
export function quickCheck(): { hasDeps: boolean; hasBrowser: boolean } {
  return {
    hasDeps: hasNodeModules(),
    hasBrowser: hasChromiumInstalled()
  };
}

export default {
  checkAndInstall,
  quickCheck
};
