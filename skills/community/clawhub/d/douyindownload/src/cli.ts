#!/usr/bin/env node
// CLI 客户端：命令行直接调用视频解析服务
import { parseVideo } from './parser.js';
import { checkAndRecord, activateKey, getStatus } from './license.js';
import * as readline from 'readline';

const args = process.argv.slice(2);

// 彩色输出
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  red: '\x1b[31m',
  cyan: '\x1b[36m',
};

function log(msg: string, color = 'reset') {
  console.log(`${(colors as any)[color]}${msg}${colors.reset}`);
}

function printBanner() {
  log(`
╔═══════════════════════════════════════════╗
║     抖音 视频解析 CLI        ║
║     v1.0.0  |  去水印 · 免费使用         ║
╚═══════════════════════════════════════════╝
`, 'cyan');
}

function printHelp() {
  printBanner();
  console.log(`
用法：
  douyin-mcp <命令> [参数]

命令：
  parse <url>        解析视频链接（去水印）
  activate <key>     激活授权码
  status             查看当前额度状态
  reset              重置用量（仅调试）

示例：
  douyin-mcp parse "https://v.douyin.com/xxx"
  douyin-mcp activate DEMO-PRO-2026
  douyin-mcp status

免费版：每月 10 次
💎 基础版：9.9元/月 = 500次
🚀 Pro版：29.9元/月 = 无限次
`);
}

async function cmdParse(url: string) {
  // 先检查额度
  const check = checkAndRecord();
  if (!check.allowed) {
    log(`\n⚠️  免费次数已用完\n`, 'yellow');
    log(check.upgradeMessage || '', 'yellow');
    log(`\n当前状态：免费版剩余 0 次\n`, 'yellow');
    return;
  }

  log(`\n🔍 正在解析...`);
  const result = await parseVideo(url);

  if (!result.success) {
    log(`\n❌ 解析失败：${result.error}\n`, 'red');
    process.exit(1);
  }

  const platformIcons: Record<string, string> = {
    douyin: '🎵 抖音',
    kuaishou: '📺 快手',
  };

  log(`\n✅ 解析成功！`, 'green');
  console.log(`
${platformIcons[result.platform] || '📱'} 平台：${result.platform}
👤 作者：${result.author || '未知'}
📌 标题：${result.title || '未知'}
🎬 无水印地址：
${result.videoUrl}
${check.isPaid ? '' : `\n📊 剩余免费次数：${check.remaining}（免费版）`}
`);
}

async function cmdActivate(key: string) {
  const result = await activateKey('', key);
  if (result.isPaid) {
    log(`\n✅ ${result.reason}\n`, 'green');
  } else {
    log(`\n❌ ${result.reason}\n`, 'red');
    process.exit(1);
  }
}

function cmdStatus() {
  const result = getStatus();
  const remaining = result.remaining === Infinity ? '无限' : `${result.remaining} 次`;
  log(`\n📊 当前状态\n`, 'cyan');
  console.log(`  套餐：${result.plan}`);
  console.log(`  剩余：${remaining}`);
  console.log(`  付费：${result.isPaid ? '✅ 是' : '❌ 否'}`);
  if (!result.isPaid) {
    log(`\n💎 升级：9.9元/月 = 500次 | 29.9元/月 = 无限次\n`, 'yellow');
  }
}

function cmdReset() {
  const { resetUsage } = require('./license.js');
  resetUsage();
  log(`\n✅ 用量已重置\n`, 'green');
}

// 主入口
async function main() {
  if (args.length === 0 || args[0] === '-h' || args[0] === '--help') {
    printHelp();
    return;
  }

  const [cmd, ...rest] = args;
  const subargs = rest.join(' ').trim();

  switch (cmd) {
    case 'parse':
      if (!subargs) {
        log(`\n❌ 请提供视频链接\n`, 'red');
        log(`例如：douyin-mcp parse "https://v.douyin.com/xxx"\n`, 'yellow');
        return;
      }
      await cmdParse(subargs);
      break;

    case 'activate':
      if (!subargs) {
        log(`\n❌ 请提供授权码\n`, 'red');
        return;
      }
      await cmdActivate(subargs);
      break;

    case 'status':
      cmdStatus();
      break;

    case 'reset':
      cmdReset();
      break;

    default:
      log(`\n❌ 未知命令：${cmd}\n`, 'red');
      printHelp();
  }
}

main().catch((error) => {
  log(`\n❌ 错误：${error.message}\n`, 'red');
  process.exit(1);
});