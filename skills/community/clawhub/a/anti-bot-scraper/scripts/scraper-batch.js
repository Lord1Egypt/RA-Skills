#!/usr/bin/env node
/**
 * scraper-batch.js - 批量抓取模式
 *
 * Usage:
 *   node scripts/scraper-batch.js [options] <URL1> <URL2> ...
 *   node scripts/scraper-batch.js --file urls.txt [options]
 *
 * Options:
 *   --file <path>        URL 列表文件（每行一个 URL）
 *   --concurrency <n>    并发数（默认 3）
 *   --stealth            使用隐身模式
 *   --wait <ms>          每个页面的等待时间（默认 2000）
 *   --selector <css>     CSS 选择器
 *   --output <path>      输出 JSON 文件路径（默认 stdout）
 */

const { execFile } = require('child_process');
const fs = require('fs');
const path = require('path');

// ── 参数解析 ──────────────────────────────────────────
function parseArgs(argv) {
  const args = argv.slice(2);
  const opts = {
    urls: [],
    file: null,
    concurrency: 3,
    stealth: false,
    wait: 2000,
    selector: null,
    output: null,
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--file':
        opts.file = args[++i];
        break;
      case '--concurrency':
        opts.concurrency = parseInt(args[++i], 10);
        break;
      case '--stealth':
        opts.stealth = true;
        break;
      case '--wait':
        opts.wait = parseInt(args[++i], 10);
        break;
      case '--selector':
        opts.selector = args[++i];
        break;
      case '--output':
        opts.output = args[++i];
        break;
      default:
        if (!args[i].startsWith('--')) {
          opts.urls.push(args[i]);
        }
    }
  }

  // 从文件读取 URL
  if (opts.file) {
    try {
      const content = fs.readFileSync(opts.file, 'utf-8');
      const lines = content
        .split(/\r?\n/)
        .map((l) => l.trim())
        .filter((l) => l && !l.startsWith('#'));
      opts.urls.push(...lines);
    } catch (e) {
      console.error(`Error reading URL file: ${e.message}`);
      process.exit(1);
    }
  }

  if (opts.urls.length === 0) {
    console.error(
      'Usage: node scraper-batch.js [--file <path>] [--concurrency <n>] [--stealth] [--wait <ms>] [--selector <css>] [--output <path>] <URL1> <URL2> ...'
    );
    process.exit(1);
  }

  return opts;
}

// ── 单个 URL 抓取 ────────────────────────────────────
function scrapeOne(url, opts) {
  return new Promise((resolve) => {
    const scriptName = opts.stealth ? 'scraper-stealth.js' : 'scraper-simple.js';
    const scriptPath = path.join(__dirname, scriptName);
    const args = [scriptPath, url];

    if (opts.wait) {
      args.push('--wait', String(opts.wait));
    }
    if (opts.selector) {
      args.push('--selector', opts.selector);
    }

    const child = execFile('node', args, { maxBuffer: 10 * 1024 * 1024, timeout: 120000 }, (error, stdout, stderr) => {
      if (error) {
        // 尝试解析 stdout 中的错误 JSON
        try {
          const result = JSON.parse(stdout);
          resolve(result);
        } catch {
          resolve({
            success: false,
            url,
            error: error.message,
            stderr: stderr || '',
          });
        }
      } else {
        try {
          resolve(JSON.parse(stdout));
        } catch {
          resolve({
            success: false,
            url,
            error: 'Invalid JSON output',
            rawOutput: stdout.slice(0, 500),
          });
        }
      }
    });
  });
}

// ── 随机延迟 ──────────────────────────────────────────
function randomDelay(min = 1000, max = 5000) {
  return new Promise((resolve) => {
    const delay = Math.floor(Math.random() * (max - min + 1)) + min;
    setTimeout(resolve, delay);
  });
}

// ── 并发控制器 ────────────────────────────────────────
async function runWithConcurrency(tasks, concurrency) {
  const results = [];
  const running = new Set();
  const queue = [...tasks];

  while (queue.length > 0 || running.size > 0) {
    // 填充到并发上限
    while (queue.length > 0 && running.size < concurrency) {
      const task = queue.shift();
      const promise = task().then((result) => {
        running.delete(promise);
        results.push(result);
      });
      running.add(promise);
    }

    // 等待任意一个完成
    if (running.size > 0) {
      await Promise.race(running);
    }
  }

  return results;
}

// ── 主流程 ────────────────────────────────────────────
async function main() {
  const opts = parseArgs(process.argv);
  const startTime = Date.now();

  const totalUrls = opts.urls.length;
  process.stderr.write(
    `\n🕷️  Batch Scraper\n` +
      `   URLs: ${totalUrls}\n` +
      `   Concurrency: ${opts.concurrency}\n` +
      `   Mode: ${opts.stealth ? 'Stealth 🕵️' : 'Simple'}\n\n`
  );

  let completed = 0;

  // 构建任务列表，每个任务之间有随机延迟
  const tasks = opts.urls.map((url, index) => {
    return async () => {
      // 非第一个任务加随机延迟
      if (index > 0) {
        await randomDelay(1000, 4000);
      }

      process.stderr.write(`  [${completed + 1}/${totalUrls}] ${url}\n`);
      const result = await scrapeOne(url, opts);
      completed++;

      if (result.success) {
        process.stderr.write(`    ✅ ${result.title || '(no title)'} (${result.elapsedSeconds}s)\n`);
      } else {
        process.stderr.write(`    ❌ ${result.error}\n`);
      }

      return result;
    };
  });

  const results = await runWithConcurrency(tasks, opts.concurrency);

  const summary = {
    total: totalUrls,
    success: results.filter((r) => r.success).length,
    failed: results.filter((r) => !r.success).length,
    elapsedSeconds: parseFloat(((Date.now() - startTime) / 1000).toFixed(2)),
    results,
  };

  const output = JSON.stringify(summary, null, 2);

  if (opts.output) {
    const outDir = path.dirname(path.resolve(opts.output));
    if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });
    fs.writeFileSync(opts.output, output, 'utf-8');
    process.stderr.write(`\n📄 Results saved to: ${opts.output}\n`);
  } else {
    console.log(output);
  }

  process.stderr.write(
    `\n✨ Done! ${summary.success}/${summary.total} succeeded (${summary.elapsedSeconds}s)\n`
  );
}

main().catch((e) => {
  console.error('Fatal error:', e);
  process.exit(1);
});
