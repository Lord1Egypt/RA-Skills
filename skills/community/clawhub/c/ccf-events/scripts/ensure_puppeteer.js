#!/usr/bin/env node

/**
 * Puppeteer 环境检测与自动修复脚本（纯文件系统版本）
 * 安全合规要求：
 * 1. 必须获得用户明确授权才能安装
 * 2. 仅本地安装，不修改全局环境
 * 3. 固定版本号 24.15.0
 * 4. 优先复用已有安装
 * 5. 优先使用系统 Chrome/Chromium
 * 6. 不执行任何 shell 命令（仅文件系统操作）
 * 
 * 使用方法：
 *   node scripts/ensure_puppeteer.js           # 检测模式
 *   node scripts/ensure_puppeteer.js --fix     # 自动检测并修复缺失项
 *   node scripts/ensure_puppeteer.js --verify  # 验证模式
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const readline = require('readline');

// ---------- 配置 ----------
const CONFIG = {
  PUPPETEER_VERSION: '24.15.0',
  PUPPETEER_CACHE_DIR: path.join(os.homedir(), '.cache', 'puppeteer'),
  SCRIPT_NAME: 'scripts/ensure_puppeteer.js'
};

// ---------- 工具函数 ----------
function log(msg, type = 'info') {
  const prefixes = {
    info: '[INFO]',
    success: '[OK]',
    error: '[ERROR]',
    warning: '[WARN]',
    step: '[STEP]',
    auth: '[AUTH]',
    location: '[DIR]',
    fix: '[FIX]'
  };
  console.log(`${prefixes[type] || '[LOG]'} ${msg}`);
}

function askUserConfirmation(question, autoYes = false) {
  if (autoYes) {
    log(`自动确认: ${question}`, 'info');
    return Promise.resolve(true);
  }
  
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      rl.close();
      resolve(answer.toLowerCase() === 'yes' || answer.toLowerCase() === 'y');
    });
  });
}

function detectLinuxDistro() {
  if (process.platform !== 'linux') return 'not-linux';
  try {
    const osRelease = fs.readFileSync('/etc/os-release', 'utf-8');
    if (osRelease.includes('ubuntu') || osRelease.includes('debian')) return 'debian';
    if (osRelease.includes('centos') || osRelease.includes('rocky')) return 'rhel';
    if (osRelease.includes('rhel')) return 'rhel';
    if (osRelease.includes('fedora')) return 'fedora';
  } catch (e) {}
  return 'unknown';
}

// ---------- 查找系统浏览器（纯文件系统，不执行命令）----------
function findSystemBrowser() {
  const platform = process.platform;
  let paths = [];
  
  if (platform === 'win32') {
    paths = [
      'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
      'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
      process.env.LOCALAPPDATA + '\\Google\\Chrome\\Application\\chrome.exe',
      process.env.ProgramW6432 + '\\Google\\Chrome\\Application\\chrome.exe',
      'C:\\Program Files\\Chromium\\Application\\chrome.exe',
      'C:\\Program Files (x86)\\Chromium\\Application\\chrome.exe'
    ];
  } else if (platform === 'darwin') {
    paths = [
      '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
      '/Applications/Chromium.app/Contents/MacOS/Chromium',
      '/usr/bin/google-chrome',
      '/usr/bin/chromium-browser'
    ];
  } else {
    paths = [
      '/usr/bin/google-chrome',
      '/usr/bin/google-chrome-stable',
      '/usr/bin/chromium-browser',
      '/usr/bin/chromium',
      '/usr/local/bin/chromium',
      '/snap/bin/chromium'
    ];
  }
  
  for (const p of paths) {
    if (p && fs.existsSync(p)) {
      return p;
    }
  }
  
  return null;
}

// ---------- 检测函数 ----------
function checkNodejs() {
  // 只检查 node_modules 是否存在，不执行命令
  // 实际 Node.js 是否存在需要用户自行确认
  return { ok: true, message: 'Node.js 检测（请确保已安装）' };
}

function checkNpm() {
  // 只检查 package.json 或 node_modules，不执行命令
  const hasPackageJson = fs.existsSync(path.join(process.cwd(), 'package.json'));
  const hasNodeModules = fs.existsSync(path.join(process.cwd(), 'node_modules'));
  if (hasPackageJson || hasNodeModules) {
    return { ok: true, message: 'npm 项目已初始化' };
  }
  return { ok: false, message: 'npm 未初始化' };
}

function checkProjectInitialized() {
  const packageJson = path.join(process.cwd(), 'package.json');
  return fs.existsSync(packageJson);
}

function checkPuppeteerInstalled() {
  const localNodeModules = path.join(process.cwd(), 'node_modules', 'puppeteer');
  if (fs.existsSync(localNodeModules)) {
    try {
      const packageJson = path.join(localNodeModules, 'package.json');
      const data = JSON.parse(fs.readFileSync(packageJson, 'utf-8'));
      return { 
        ok: true, 
        message: `Puppeteer@${data.version} 已安装`,
        local: true,
        version: data.version
      };
    } catch {
      return { ok: true, message: 'Puppeteer 已安装', local: true };
    }
  }
  return { ok: false, message: 'Puppeteer 未安装', local: false };
}

function checkChromiumInstalled() {
  // 优先查找系统浏览器
  const systemBrowser = findSystemBrowser();
  if (systemBrowser) {
    return { ok: true, message: `浏览器已安装: ${path.basename(systemBrowser)}`, path: systemBrowser };
  }
  
  // 检查 Puppeteer 缓存目录
  const cacheDir = CONFIG.PUPPETEER_CACHE_DIR;
  if (fs.existsSync(cacheDir)) {
    try {
      const items = fs.readdirSync(cacheDir);
      for (const item of items) {
        const chromePath = path.join(cacheDir, item, 
          process.platform === 'win32' ? 'chrome.exe' : 'chrome');
        if (fs.existsSync(chromePath)) {
          return { ok: true, message: `Chromium 已安装`, path: chromePath };
        }
      }
    } catch(e) {}
  }
  
  return { ok: false, message: '未找到浏览器', path: null };
}

function checkVersionMatch(installedVersion) {
  if (!installedVersion) return false;
  return installedVersion === CONFIG.PUPPETEER_VERSION;
}

// ---------- 验证安装（不执行命令）----------
async function verifyInstallation() {
  console.log('\n' + '='.repeat(60));
  log('验证 Puppeteer 安装', 'info');
  console.log('='.repeat(60));
  
  const puppeteerCheck = checkPuppeteerInstalled();
  if (!puppeteerCheck.ok) {
    log('Puppeteer 未安装', 'error');
    console.log('\n请手动执行以下命令安装：');
    console.log('  npm install puppeteer@24.15.0 --save-exact --save-dev');
    return false;
  }
  
  // 获取浏览器路径
  let browserPath = null;
  
  // 先检查环境变量文件
  const envFile = path.join(process.cwd(), '.env');
  if (fs.existsSync(envFile)) {
    try {
      const envContent = fs.readFileSync(envFile, 'utf-8');
      const match = envContent.match(/PUPPETEER_EXECUTABLE_PATH=(.+)/);
      if (match && fs.existsSync(match[1])) {
        browserPath = match[1];
      }
    } catch(e) {}
  }
  
  // 查找系统浏览器
  if (!browserPath) {
    browserPath = findSystemBrowser();
  }
  
  // 检查 Puppeteer 缓存
  if (!browserPath) {
    const chromiumCheck = checkChromiumInstalled();
    if (chromiumCheck.path) {
      browserPath = chromiumCheck.path;
    }
  }
  
  if (browserPath) {
	const normalizedBrowserPath = browserPath.replace(/\\/g, '/');
    log(`找到浏览器: ${browserPath}`, 'success');
    log('Puppeteer 环境已就绪（请手动运行测试脚本验证）', 'success');
    console.log('\n手动验证命令：');
    console.log(`  node -e "const puppeteer = require('puppeteer'); (async () => { try { const browser = await puppeteer.launch({ executablePath: '${normalizedBrowserPath}', args: ['--no-sandbox', '--disable-setuid-sandbox'] }); const page = await browser.newPage(); console.log('[TEST] 正在访问 CCF 官网...'); await page.goto('https://ccf.org.cn', { timeout: 30000 }); const title = await page.title(); console.log('[SUCCESS] 验证通过！页面标题:', title); await browser.close(); process.exit(0); } catch (err) { console.error('[ERROR] 验证失败:', err.message); process.exit(1); } })();"`);
    return true;
  }
  
  log('未找到浏览器，请安装 Chrome/Chromium 或设置 PUPPETEER_EXECUTABLE_PATH', 'warning');
  console.log('\n配置方法：');
  console.log('  1. 创建 .env 文件，添加：');
  console.log('     PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser');
  console.log('  2. 或安装 Chromium：');
  if (process.platform === 'win32') {
    console.log('     下载安装: https://www.google.com/chrome/');
  } else if (process.platform === 'darwin') {
    console.log('     brew install chromium');
  } else {
    const distro = detectLinuxDistro();
    if (distro === 'rhel') {
      console.log('     sudo yum install -y chromium');
    } else if (distro === 'debian') {
      console.log('     sudo apt-get install -y chromium-browser');
    } else {
      console.log('     使用系统包管理器安装 chromium');
    }
  }
  return false;
}

// ---------- 安装提示（不自动执行命令）----------
async function installPuppeteer(autoYes = false) {
  log('检测到 Puppeteer 缺失', 'warning');
  console.log(`   目标版本: ${CONFIG.PUPPETEER_VERSION}`);
  
  const confirmed = await askUserConfirmation('是否查看安装指南？(yes/no): ', autoYes);
  if (!confirmed) {
    log('用户取消', 'warning');
    return false;
  }
  
  // 检查是否有系统浏览器
  const systemBrowser = findSystemBrowser();
  if (systemBrowser) {
    log(`找到系统浏览器: ${systemBrowser}`, 'success');
    console.log('\n推荐使用系统浏览器，无需下载 Chromium。');
  }
  
  console.log('\n' + '='.repeat(60));
  console.log('手动安装指南');
  console.log('='.repeat(60));
  console.log('\n1. 初始化项目（如果没有 package.json）：');
  console.log('   npm init -y');
  console.log('\n2. 安装 Puppeteer：');
  console.log(`   npm install puppeteer@${CONFIG.PUPPETEER_VERSION} --save-exact --save-dev`);
  console.log('\n3. 配置浏览器路径（创建 .env 文件）：');
  if (systemBrowser) {
    console.log(`   PUPPETEER_EXECUTABLE_PATH=${systemBrowser}`);
    console.log('   PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true');
  } else {
    console.log('   # 使用系统浏览器（推荐）');
    if (process.platform === 'win32') {
      console.log('   PUPPETEER_EXECUTABLE_PATH=C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe');
    } else {
      console.log('   PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser');
    }
    console.log('   PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true');
    console.log('\n   # 或使用国内镜像下载 Chromium');
    console.log('   PUPPETEER_DOWNLOAD_HOST=https://registry.npmmirror.com/-/binary/chrome-for-testing');
  }
  console.log('\n4. 验证安装：');
  console.log(`   node ${CONFIG.SCRIPT_NAME} --verify`);
  console.log('='.repeat(60));
  
  return true;
}

// ---------- 创建配置文件 ----------
function createEnvFile() {
  const systemBrowser = findSystemBrowser();
  if (!systemBrowser) {
    log('未找到系统浏览器，无法创建配置文件', 'warning');
    return false;
  }
  
  const envPath = path.join(process.cwd(), '.env');
  const envContent = `# Puppeteer 配置
PUPPETEER_EXECUTABLE_PATH=${systemBrowser}
PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
`;
  
  fs.writeFileSync(envPath, envContent);
  log(`配置文件已创建: ${envPath}`, 'success');
  log(`浏览器路径: ${systemBrowser}`, 'info');
  return true;
}

// ---------- 主函数 ----------
async function main() {
  const args = process.argv.slice(2);
  const isFix = args.includes('--fix');
  const isAuto = args.includes('--auto');
  const isVerify = args.includes('--verify');
  const isJson = args.includes('--json');
  const isConfig = args.includes('--config');
  
  if (isJson) {
    const puppeteer = checkPuppeteerInstalled();
    const browser = checkChromiumInstalled();
    
    const result = {
      system: {
        platform: process.platform,
        release: os.release(),
        arch: os.arch(),
        node_version: process.version,
        cwd: process.cwd()
      },
      config: {
        puppeteer_version: CONFIG.PUPPETEER_VERSION,
        cache_dir: CONFIG.PUPPETEER_CACHE_DIR,
        script: CONFIG.SCRIPT_NAME
      },
      checks: {
        puppeteer: puppeteer,
        browser: browser,
        package_json: checkProjectInitialized()
      }
    };
    console.log(JSON.stringify(result, null, 2));
    return;
  }
  
  if (isConfig) {
    await createEnvFile();
    return;
  }
  
  if (isVerify) {
    await verifyInstallation();
    return;
  }
  
  if (isFix || isAuto) {
    await installPuppeteer(isAuto);
    return;
  }
  
  // 默认：检测模式
  console.log('\n' + '='.repeat(60));
  log('Puppeteer 环境检测', 'info');
  console.log('='.repeat(60));
  
  const puppeteer = checkPuppeteerInstalled();
  const browser = checkChromiumInstalled();
  const hasPackageJson = checkProjectInitialized();
  const hasEnvFile = fs.existsSync(path.join(process.cwd(), '.env'));
  
  console.log(`\n[OS] 操作系统: ${process.platform} ${os.release()}`);
  if (process.platform === 'linux') {
    console.log(`[DISTRO] 发行版: ${detectLinuxDistro()}`);
  }
  console.log(`[DIR] 当前目录: ${process.cwd()}`);
  console.log(`[VERSION] 目标版本: ${CONFIG.PUPPETEER_VERSION}`);
  console.log('-'.repeat(50));
  
  console.log(`\n${hasPackageJson ? '[OK]' : '[NO]'} package.json`);
  console.log(`${hasEnvFile ? '[OK]' : '[NO]'} .env 配置文件`);
  console.log(`${puppeteer.ok ? '[OK]' : '[NO]'} ${puppeteer.message}`);
  console.log(`${browser.ok ? '[OK]' : '[NO]'} ${browser.message}`);
  
  console.log('-'.repeat(50));
  
  const allOk = hasPackageJson && puppeteer.ok && browser.ok;
  
  if (allOk) {
    log('Puppeteer 环境就绪', 'success');
    console.log(`\n[VERIFY] 运行验证: node ${CONFIG.SCRIPT_NAME} --verify`);
  } else {
    log('Puppeteer 环境不完整', 'warning');
    if (!browser.ok) {
      console.log('\n[浏览器] 未找到 Chrome/Chromium');
      if (process.platform === 'win32') {
        console.log('   请安装 Chrome: https://www.google.com/chrome/');
      } else if (process.platform === 'darwin') {
        console.log('   安装: brew install chromium');
      } else {
        const distro = detectLinuxDistro();
        if (distro === 'rhel') {
          console.log('   安装: sudo yum install -y chromium');
        } else if (distro === 'debian') {
          console.log('   安装: sudo apt-get install -y chromium-browser');
        }
      }
    }
    if (!puppeteer.ok) {
      console.log(`\n[FIX] 查看安装指南: node ${CONFIG.SCRIPT_NAME} --fix`);
    }
    if (browser.ok && !hasEnvFile) {
      console.log(`\n[CONFIG] 创建配置文件: node ${CONFIG.SCRIPT_NAME} --config`);
    }
  }
  
  console.log('\n[SECURITY] 安全说明：');
  console.log('   - 本脚本不执行任何 shell 命令');
  console.log('   - 仅进行文件系统检查和输出指南');
  console.log(`   - 请手动执行上述命令完成安装`);
}

main().catch((error) => {
  log(`脚本执行失败: ${error.message}`, 'error');
  process.exit(1);
});