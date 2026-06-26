#!/usr/bin/env node

/**
 * CLI command parser and handler
 * @module cli
 */

const bbdown = require('./downloader/bbdown');
const history = require('./utils/history');

/**
 * Parse command line arguments
 * @param {string[]} args - Command line arguments
 * @returns {Object}
 */
function parseArgs(args) {
  const command = args[0];
  const options = {};
  const positional = [];
  
  for (let i = 1; i < args.length; i++) {
    const arg = args[i];
    
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const value = args[i + 1];
      
      if (value && !value.startsWith('--')) {
        options[key] = value;
        i++;
      } else {
        options[key] = true;
      }
    } else if (arg.startsWith('-')) {
      const key = arg.slice(1);
      const value = args[i + 1];
      
      if (value && !value.startsWith('-')) {
        options[key] = value;
        i++;
      } else {
        options[key] = true;
      }
    } else {
      positional.push(arg);
    }
  }
  
  return { command, options, positional };
}

/**
 * Handle download command
 * @param {string} url - Video URL
 * @param {Object} options - Download options
 */
async function handleDownload(url, options) {
  const cookieFile = options.cookie || options.c;
  const outputDir = options.output || options.o || bbdown.getDefaultDownloadDir();
  
  // Step 1: Fetch video info first
  console.log('🔍 正在获取视频信息...\n');
  
  const infoResult = await bbdown.info(url, { cookieFile });
  
  if (!infoResult.success) {
    console.error('❌ 获取视频信息失败:', infoResult.error);
    process.exit(1);
  }
  
  const { title, duration, quality, size, hasAudio } = infoResult.info;
  
  // Step 2: Display info with pretty formatting
  console.log('════════════════════════════════════════');
  console.log(`📺 【${title || '未知标题'}】`);
  console.log('════════════════════════════════════════');
  console.log(`⏱️  时长：${duration || '未知'} ${quality ? `| 📐 ${quality}` : ''} ${hasAudio ? '| 🔊 音频' : ''}`);
  if (size) {
    console.log(`💾 预计大小：${size}`);
  }
  console.log(`📁 保存到：${outputDir}`);
  console.log('────────────────────────────────────────');
  console.log('⏳ 开始下载...\n');
  
  // Step 3: Download
  const result = await bbdown.download(url, {
    quality: options.quality || options.q,
    danmaku: options.danmaku || options.d,
    cookieFile,
    outputDir
  });
  
  if (result.success) {
    console.log('\n✅ Download completed!');
    console.log(`📁 File: ${result.output}`);
    
    // Add to history
    const videoId = bbdown.extractVideoId(url);
    if (videoId) {
      history.addRecord({
        videoId,
        url,
        title,
        downloadPath: result.output,
        quality: options.quality || options.q,
        danmaku: options.danmaku || options.d
      });
    }
  } else {
    console.error('\n❌ Download failed:', result.error);
    process.exit(1);
  }
}

/**
 * Handle history command
 * @param {Object} options - History options
 */
async function handleHistory(options) {
  const limit = parseInt(options.limit) || 10;
  const records = history.getRecords(limit);
  
  if (records.length === 0) {
    console.log('📭 No download history yet\n');
    return;
  }
  
  console.log('📋 Download History:\n');
  records.forEach((record, index) => {
    console.log(`${index + 1}. ${record.title || 'Unknown'}`);
    console.log(`   🔗 ${record.url}`);
    console.log(`   💾 ${record.downloadPath}`);
    console.log(`   📅 ${new Date(record.downloadAt).toLocaleString()}\n`);
  });
}

/**
 * Show help message
 */
function showHelp() {
  console.log(`
🎬 bilibit - Bilibili Video Downloader

Usage:
  bilibit <url> [options]        Download video
  bilibit history [options]      View download history
  bilibit --help                 Show this help
  bilibit --version              Show version

Download Options:
  -q, --quality <quality>        Video quality (4K, 1080P, etc.)
  -d, --danmaku                  Download danmaku
  -c, --cookie <file>            Cookie file path
  -o, --output <dir>             Output directory

History Options:
  --limit <num>                  Number of records (default: 10)

Examples:
  bilibit https://b23.tv/BV1xx
  bilibit https://b23.tv/BV1xx --quality 4K --danmaku
  bilibit history --limit 20

💡 Tip: Find video URL in browser, then use bilibit to download.
`);
}

/**
 * Show version
 */
function showVersion() {
  const pkg = require('../package.json');
  console.log(`bilibit v${pkg.version}`);
}

/**
 * Main entry point
 */
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    showHelp();
    process.exit(0);
  }
  
  const { command, options, positional } = parseArgs(args);
  
  // Handle commands
  switch (command) {
    case '--help':
    case '-h':
      showHelp();
      break;
      
    case '--version':
    case '-v':
      showVersion();
      break;
      
    case 'history':
      await handleHistory(options);
      break;
      
    default:
      // Assume it's a URL for download
      if (command.startsWith('http') || command.startsWith('BV')) {
        await handleDownload(command, options);
      } else if (positional.length > 0) {
        await handleDownload(positional[0], options);
      } else {
        console.error('❌ Please provide a video URL.\n');
        console.log('Usage: bilibit <url> [options]\n');
        console.log('Examples:');
        console.log('  bilibit https://b23.tv/BV1xx');
        console.log('  bilibit https://www.bilibili.com/video/BV1xx\n');
        process.exit(1);
      }
      break;
  }
}

module.exports = {
  parseArgs,
  handleDownload,
  handleHistory,
  showHelp,
  showVersion,
  main
};

if (require.main === module) {
  main();
}
