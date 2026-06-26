#!/usr/bin/env node
/**
 * src/deploy/index.js — 部署脚本
 *
 * 将生成的 HTML 页面部署到 acm_www/static/ 目录，
 * 同时将 CDN 资源路径替换为本地相对路径。
 *
 * 用法：
 *   node src/deploy/index.js nl2sql_output/cockpit_awrsx.html
 *   node src/deploy/index.js nl2sql_output/cockpit_awrsx.html --output /custom/path.html
 *
 * 集成到生成流程（可选）：
 *   const { deploy } = require('./src/deploy/index.js');
 *   await deploy('nl2sql_output/cockpit_awrsx.html');
 */

const fs = require('fs');
const path = require('path');

// ============================================================
// 配置
// ============================================================

// acm_www 与 skills/data-query 是并列目录（都在 workspace/ 下）
// __dirname = skills/data-query/src/deploy
// 往上 5 层 = workspace/
const WORKSPACE_DIR = path.join(__dirname, '../../../../');
const ACM_STATIC_DIR = path.join(WORKSPACE_DIR, 'acm_www/static');

// CDN → 本地路径映射表（可扩展）
const CDN_REPLACEMENTS = [
  {
    cdn: 'https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js',
    local: './ExtJs/echarts.min.js'
  },
  {
    cdn: 'https://cdn.jsdelivr.net/npm/crypto-js@4.1.1/crypto-js.min.js',
    local: './ExtJs/crypto-js.min.js'
  }
];

// ============================================================
// 核心部署逻辑
// ============================================================

function replaceCdn(html) {
  let replaced = 0;
  let lastHtml = html;

  for (const { cdn, local } of CDN_REPLACEMENTS) {
    if (html.includes(cdn)) {
      lastHtml = lastHtml.split(cdn).join(local);
      replaced++;
      console.log(`  ✅ ${cdn}`);
      console.log(`     → ${local}`);
    }
  }

  return { html: lastHtml, count: replaced };
}

function deploy(inputPath, options = {}) {
  const { outputName = null, localOutput = null } = options;
  // localOutput: 写入部署版（CDN→本地路径）的目标文件名
  //             如传入 'cockpit.html'，则写入 nl2sql_output/cockpit.html
  //             如不传，仅部署到 acm_www/static/（不保留本地副本）

  // 解析输入路径（预览版 HTML）
  const inputAbsolute = path.isAbsolute(inputPath)
    ? inputPath
    : path.join(process.cwd(), inputPath);

  if (!fs.existsSync(inputAbsolute)) {
    throw new Error(`文件不存在: ${inputAbsolute}`);
  }

  const baseName = path.basename(inputAbsolute);
  const targetName = outputName || baseName;

  // 读取 HTML
  const html = fs.readFileSync(inputAbsolute, 'utf-8');
  console.log(`\n📦 部署开始`);
  console.log(`  输入: ${inputAbsolute}`);
  console.log(`  大小: ${(Buffer.byteLength(html) / 1024).toFixed(1)} KB`);

  // 替换 CDN
  const { html: replacedHtml, count } = replaceCdn(html);
  if (count === 0) {
    console.log(`  ⚠️  未发现需要替换的 CDN 资源`);
  } else {
    console.log(`  ✅ CDN 替换完成 (${count} 项)`);
  }

  // ── 写入部署版到 nl2sql_output/（localOutput）───────────────────
  let nlOutput = null;
  let staticOutput = null;
  let deployedTo = null;

  if (localOutput) {
    nlOutput = path.join(WORKSPACE_DIR, 'nl2sql_output', localOutput);
    const nlDir = path.dirname(nlOutput);
    if (!fs.existsSync(nlDir)) fs.mkdirSync(nlDir, { recursive: true });
    fs.writeFileSync(nlOutput, replacedHtml, 'utf-8');
    console.log(`  ✅ 部署版已保存: ${nlOutput}`);
  }

  // ── 拷贝到 acm_www/static/（如果存在）──────────────────────────
  if (fs.existsSync(ACM_STATIC_DIR)) {
    staticOutput = path.join(ACM_STATIC_DIR, targetName);
    fs.writeFileSync(staticOutput, replacedHtml, 'utf-8');
    console.log(`  ✅ 已部署到: ${staticOutput}`);
    deployedTo = 'static';
  } else if (!nlOutput) {
    // 无 localOutput 也无 static，写入兜底目录
    const fallbackDir = path.join(WORKSPACE_DIR, 'nl2sql_output');
    if (!fs.existsSync(fallbackDir)) fs.mkdirSync(fallbackDir, { recursive: true });
    nlOutput = path.join(fallbackDir, targetName);
    fs.writeFileSync(nlOutput, replacedHtml, 'utf-8');
    console.log(`  ⚠️  acm_www/static/ 不存在，已保存到: ${nlOutput}`);
    deployedTo = 'fallback';
  }

  console.log(`  📍 访问路径: ./${targetName}`);
  console.log(`\n✅ 部署完成`);

  return {
    input: inputAbsolute,
    output: staticOutput || nlOutput,
    nlOutput,
    staticOutput,
    deployedTo,
    replacedCount: count,
    url: `./${targetName}`
  };
}

// ============================================================
// CLI 入口
// ============================================================

function parseArgs() {
  const args = process.argv.slice(2);
  const config = { input: null, output: null, help: false };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--output' || arg === '-o') {
      config.output = args[++i];
    } else if (arg === '--help' || arg === '-h') {
      config.help = true;
    } else if (!arg.startsWith('--')) {
      config.input = arg;
    }
  }

  return config;
}

function main() {
  const config = parseArgs();

  if (config.help || !config.input) {
    console.log(`
deploy.js — NL2SQL 页面部署工具

用法:
  node src/deploy/index.js <html文件> [--output <输出文件名>]
  node src/deploy/index.js nl2sql_output/cockpit_awrsx.html
  node src/deploy/index.js nl2sql_output/cockpit_awrsx.html --output my_dashboard.html

功能:
  1. 将 HTML 中的 CDN 资源路径替换为本地相对路径
  2. 复制到 acm_www/static/ 目录

CDN 替换规则:
  https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js
    → ./ExtJs/echarts.min.js

  https://cdn.jsdelivr.net/npm/crypto-js@4.1.1/crypto-js.min.js
    → ./ExtJs/crypto-js.min.js

示例:
  node src/deploy/index.js nl2sql_output/cockpit_awrsx.html
    → 部署到 acm_www/static/cockpit_awrsx.html

  node src/deploy/index.js nl2sql_output/cockpit_awrsx.html --output my.html
    → 部署到 acm_www/static/my.html
`);
    process.exit(0);
  }

  try {
    deploy(config.input, { outputName: config.output });
    process.exit(0);
  } catch (err) {
    console.error(`\n❌ 部署失败: ${err.message}`);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { deploy, CDN_REPLACEMENTS };
