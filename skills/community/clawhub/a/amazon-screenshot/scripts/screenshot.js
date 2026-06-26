const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');
const { ZipArchive } = require('archiver');
const nodemailer = require('nodemailer');

// 反爬检测注入脚本：在页面加载前修补自动化特征
const STEALTH_SCRIPT = `
Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
window.chrome = { runtime: {} };
Object.defineProperty(window, 'callPhantom', { get: () => undefined });
Object.defineProperty(window, '_phantom', { get: () => undefined });
Object.defineProperty(window, '__webdriver_evaluate', { get: () => undefined });
Object.defineProperty(window, 'selenium', { get: () => undefined });
Object.defineProperty(window, '__selenium_evaluate', { get: () => undefined });
Object.defineProperty(window, '__webdriver_script_function', { get: () => undefined });
Object.defineProperty(window, '__webdriver_script_func', { get: () => undefined });
Object.defineProperty(window, '__webdriver_script_nonce', { get: () => undefined });
Object.defineProperty(window, 'ga', { get: () => undefined });
Object.defineProperty(window, 'gtag', { get: () => undefined });
Object.defineProperty(navigator, 'permissions', { get: () => Promise.resolve({ query: () => Promise.resolve({ state: 'granted' }) }) });
`;

// 输出到 skill 目录下的 outputs 文件夹
const OUTPUT_DIR = path.join(__dirname, '..', 'outputs');
const LOCK_FILE = path.join(OUTPUT_DIR, '.screenshot_lock');
// 固定 Chrome Profile 目录，保持登录状态
const USER_DATA_DIR = path.join(__dirname, '..', 'chrome_profile');

// 自动检测当前活跃的 X Display 编号（aios 用户的 Chrome 窗口所在）
function autoDetectDisplay() {
  try {
    const { execSync } = require('child_process');
    const display = execSync('python3 - <<EOF\nimport os,glob\nsocks=[s for s in glob.glob("/tmp/.X11-unix/X*") if os.stat(s).st_uid==1000]\nprint(socks[0].split("X")[-1] if socks else "")\nEOF\n', { encoding: 'utf8' }).trim();
    if (display) {
      console.log(`[Display] 自动检测到活跃显示: :${display}`);
      return `:${display}`;
    }
  } catch (e) {}
  return ':10'; // 默认 fallback
}

// 设置 DISPLAY 环境变量
process.env.DISPLAY = autoDetectDisplay();

// MOSS 邮箱配置
const EMAIL_CONFIG = {
  host: 'smtp.feishu.cn',
  port: 465,
  secure: true,
  user: 'moss@campsnail.com',
  pass: 'rDs70BwDDg6U9YbO',
  from: 'MOSS <moss@campsnail.com>'
};

const BATCH_SIZE = 9999; // 全一批，无数量限制

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function buildAmazonUrl(asin) {
  return `https://www.amazon.com/dp/${asin}`;
}

function getTimestamp() {
  const now = new Date();
  const y = now.getFullYear();
  const m = String(now.getMonth() + 1).padStart(2, '0');
  const d = String(now.getDate()).padStart(2, '0');
  const h = String(now.getHours()).padStart(2, '0');
  const min = String(now.getMinutes()).padStart(2, '0');
  const s = String(now.getSeconds()).padStart(2, '0');
  return `${y}${m}${d}_${h}${min}${s}`;
}

// 检查锁文件，防止并发执行
function checkLock() {
  if (fs.existsSync(LOCK_FILE)) {
    const lockContent = fs.readFileSync(LOCK_FILE, 'utf8').trim();
    const [lockTime, lockAsins] = lockContent.split('|');
    console.error('❌ 脚本正在执行中，请等待当前任务完成后再试。');
    console.error(`   当前任务: ${lockAsins}`);
    console.error(`   开始时间: ${lockTime}`);
    process.exit(1);
  }
}

// 检查邮箱域名是否合法
function validateEmail(email) {
  const allowedDomain = '@campsnail.com';
  if (!email.endsWith(allowedDomain)) {
    console.error(`❌ 只支持 ${allowedDomain} 邮箱，当前为: ${email}`);
    process.exit(1);
  }
}

// 创建锁文件
function createLock(asins) {
  const timestamp = getTimestamp();
  fs.writeFileSync(LOCK_FILE, `${timestamp}|${asins.join(',')}`);
}

// 删除锁文件
function removeLock() {
  if (fs.existsSync(LOCK_FILE)) {
    fs.unlinkSync(LOCK_FILE);
  }
}

async function takeScreenshot(asin) {
  const timestamp = getTimestamp();
  const outputPath = path.join(OUTPUT_DIR, `${asin}_${timestamp}.png`);

  const context = await chromium.launchPersistentContext(USER_DATA_DIR, {
    executablePath: '/usr/bin/google-chrome',
    headless: false,
    args: ['--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
  });

  // 注入反爬脚本到所有新页面
  context.on('page', page => {
    page.addInitScript(STEALTH_SCRIPT);
  });

  const page = context.pages()[0] || await context.newPage();
  await page.setViewportSize({ width: 1920, height: 1080 });
  // 注入反爬脚本
  await page.addInitScript(STEALTH_SCRIPT);

  // 先访问首页，等待地址从 Profile 加载
  console.log(`[${asin}] Loading Amazon homepage...`);
  await page.goto('https://www.amazon.com', { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(5000);

  const url = buildAmazonUrl(asin);
  console.log(`[${asin}] Opening: ${url}`);

  try {
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(3000);

    // 检测人机校验页面（Captcha）
    const captchaButton = page.locator('button:has-text("Continue shopping"), input[value*="Continue"], button[type="submit"]');
    const captchaCount = await captchaButton.count();

    if (captchaCount > 0) {
      console.log(`[${asin}] 检测到人机校验页面，点击 Continue...`);
      try {
        await captchaButton.first().click({ timeout: 5000 });
        await page.waitForTimeout(5000);
        console.log(`[${asin}] 已跳转，等待详情页加载...`);
      } catch (e) {
        console.log(`[${asin}] 点击失败，尝试其他方式...`);
      }
    }

    await page.screenshot({ path: outputPath, fullPage: true });
    console.log(`[${asin}] ✓ Saved: ${outputPath}`);
  } catch (err) {
    console.error(`[${asin}] ✗ Failed: ${err.message}`);
  }

  await context.close();
  return outputPath;
}

async function buildZip(imagePaths, zipPath) {
  const validPaths = imagePaths.filter(p => p);
  if (validPaths.length === 0) {
    console.error('没有成功的截图，跳过生成压缩包');
    return null;
  }

  return new Promise((resolve, reject) => {
    const output = fs.createWriteStream(zipPath);
    const archive = new ZipArchive({ zlib: { level: 9 } });

    output.on('close', () => {
      console.log(`✓ 压缩包已生成: ${zipPath} (${archive.pointer()} bytes)`);
      resolve(zipPath);
    });

    archive.on('error', err => reject(err));
    archive.pipe(output);

    for (const filePath of validPaths) {
      archive.file(filePath, { name: path.basename(filePath) });
    }

    archive.finalize();
  });
}

async function sendEmailWithZip(toEmail, zipPath, asinCount, batchNum, totalBatches) {
  return new Promise((resolve, reject) => {
    const transporter = nodemailer.createTransport({
      host: EMAIL_CONFIG.host,
      port: EMAIL_CONFIG.port,
      secure: EMAIL_CONFIG.secure,
      auth: {
        user: EMAIL_CONFIG.user,
        pass: EMAIL_CONFIG.pass
      }
    });

    const timestamp = getTimestamp();
    const subject = totalBatches > 1
      ? `📦 亚马逊 ASIN 截图 (${batchNum}/${totalBatches}) - ${timestamp}`
      : `📦 亚马逊 ASIN 截图 - ${timestamp}`;

    const mailOptions = {
      from: EMAIL_CONFIG.from,
      to: toEmail,
      subject: subject,
      text: `您好！\n\n附件是您的 ${asinCount} 个亚马逊 ASIN 截图压缩包${totalBatches > 1 ? ` (第${batchNum}批，共${totalBatches}批)` : ''}。\n\n-- MOSS`,
      attachments: [
        {
          filename: path.basename(zipPath),
          path: zipPath
        }
      ]
    };

    transporter.sendMail(mailOptions, (error, info) => {
      if (error) {
        console.error(`✗ 邮件发送失败: ${error.message}`);
        reject(error);
      } else {
        console.log(`✓ 邮件已发送至: ${toEmail}`);
        resolve(info);
      }
    });
  });
}

function cleanupFiles(imagePaths, zipPath) {
  console.log('\n🗑️ 开始清理文件...');
  let cleaned = 0;

  // 删除截图
  for (const imgPath of imagePaths) {
    if (imgPath && fs.existsSync(imgPath)) {
      try {
        fs.unlinkSync(imgPath);
        cleaned++;
      } catch (e) {
        console.error(`✗ 删除失败: ${imgPath}`);
      }
    }
  }

  // 删除 ZIP
  if (zipPath && fs.existsSync(zipPath)) {
    try {
      fs.unlinkSync(zipPath);
      cleaned++;
    } catch (e) {
      console.error(`✗ 删除失败: ${zipPath}`);
    }
  }

  console.log(`✓ 已清理 ${cleaned} 个文件`);
}

// 将数组拆分成指定大小的块
function chunkArray(arr, size) {
  const chunks = [];
  for (let i = 0; i < arr.length; i += size) {
    chunks.push(arr.slice(i, i + size));
  }
  return chunks;
}

async function processBatch(asins, toEmail, batchNum, totalBatches) {
  console.log(`\n========== 批次 ${batchNum}/${totalBatches} ==========`);
  console.log(`ASIN 数量: ${asins.length}`);
  console.log(`收件邮箱: ${toEmail}\n`);

  const imagePaths = [];

  for (let i = 0; i < asins.length; i++) {
    const asin = asins[i].trim();
    const imgPath = await takeScreenshot(asin);
    imagePaths.push(imgPath);

    if (i < asins.length - 1) {
      console.log(`  → 等待 2 秒...\n`);
      await sleep(2000);
    }
  }

  // 生成 ZIP 压缩包
  const zipTimestamp = getTimestamp();
  const zipPath = path.join(OUTPUT_DIR, `screenshots_${zipTimestamp}.zip`);
  const zipResult = await buildZip(imagePaths, zipPath);

  if (zipResult) {
    // 发送邮件
    console.log(`\n→ 正在发送邮件至 ${toEmail}...`);
    try {
      await sendEmailWithZip(toEmail, zipPath, asins.length, batchNum, totalBatches);
      console.log(`✓ 批次 ${batchNum} 完成`);
      // 发送成功后清理文件
      cleanupFiles(imagePaths, zipPath);
    } catch (e) {
      console.error(`\n❌ 批次 ${batchNum} 邮件发送失败`);
      throw e;
    }
  } else {
    console.error(`\n❌ 批次 ${batchNum} 无截图可打包`);
    throw new Error('无可用截图');
  }
}

async function main() {
  const args = process.argv.slice(2);

  if (args.length < 2) {
    console.error('Usage: node screenshot.js <ASIN1> [ASIN2] [ASIN3] ... <收件邮箱>');
    console.error('Example: node screenshot.js B0GGD6242H B0GF7TF41C wangjunjie@campsnail.com');
    process.exit(1);
  }

  // 最后一个参数是邮箱地址，前面的都是 ASIN
  const toEmail = args[args.length - 1];
  const asins = args.slice(0, -1);

  // 检查邮箱域名
  validateEmail(toEmail);

  // 检查是否有其他实例在运行
  checkLock();

  // 创建锁文件
  createLock(asins);

  // 确保退出时删除锁文件
  const cleanup = () => {
    removeLock();
  };
  process.on('SIGINT', cleanup);
  process.on('SIGTERM', cleanup);
  process.on('exit', cleanup);

  try {
    // 拆分成批次
    const batches = chunkArray(asins, BATCH_SIZE);
    const totalBatches = batches.length;

    console.log(`待截图 ASIN 总数: ${asins.length}`);
    console.log(`每批数量: ${BATCH_SIZE}`);
    console.log(`总分批数: ${totalBatches}`);
    console.log(`收件邮箱: ${toEmail}\n`);

    for (let i = 0; i < batches.length; i++) {
      try {
        await processBatch(batches[i], toEmail, i + 1, totalBatches);
      } catch (e) {
        console.error(`\n❌ 批次 ${i + 1} 执行失败: ${e.message}`);
        process.exit(1);
      }
    }

    console.log('\n✅ 全部完成！');
  } finally {
    removeLock();
  }
}

main().catch(console.error);
