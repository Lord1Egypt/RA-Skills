#!/usr/bin/env node

/**
 * 抖音视频拆解分析器 - 核心稳定版 (v3.2.1)
 * 流程：Playwright 解析 -> 高性能下载 -> 自动 50 帧抽帧 -> GLM-4.6V 视觉拆解
 */

require('dotenv').config();

const scraper = require('../lib/scraper');
const playwrightScraper = require('../lib/playwright-scraper');
const videoDownloader = require('../lib/video-downloader');
const frameExtractor = require('../lib/frame-extractor');
const aiAnalyzer = require('../lib/ai-analyzer');
const audioProcessor = require('../lib/audio-processor');
const utils = require('../lib/utils');
const path = require('path');
const fs = require('fs');

const TEMP_DIR = process.env.TEMP_DIR || path.join(__dirname, '../temp');
const ZHIPU_API_KEY = process.env.ZHIPU_API_KEY;
const GLM_MODEL = process.env.GLM_MODEL || aiAnalyzer.DEFAULT_MODEL;

// 硬编码最大帧数限制，符合 GLM-4.6V 模型规格
const MAX_SPEC_FRAMES = 50;

function parseArgs() {
  const args = process.argv.slice(2);
  const result = { videoUrl: null, localFile: null, model: GLM_MODEL, fps: 2 };
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--model' && i + 1 < args.length) result.model = args[++i];
    else if (arg === '--fps' && i + 1 < args.length) result.fps = parseFloat(args[++i]);
    else if (!arg.startsWith('--')) {
      if (arg.startsWith('http')) result.videoUrl = arg;
      else if (fs.existsSync(arg)) result.localFile = arg;
    }
  }
  return result;
}

function printHelp() {
  console.log('用法: node scripts/analyze.js <链接/本地路径> [选项]');
  console.log('');
  console.log('选项:');
  console.log('  --model <model>        AI 模型 (默认: glm-4.6v)');
  console.log('  --fps <number>         每秒抽帧数量 (默认: 2, 最大限制: 5)');
  console.log('');
  console.log('💡 采用分段处理模式：每次处理 30 帧，自动汇总最终分析结果。');
}

function attachAIData(report, phase2Data) {
  if (phase2Data) {
    report += '\n🎨 AI 视觉深度拆解\n';
    report += '━━━━━━━━━━━━━━━━━━━━\n';
    if (phase2Data.visualStyle) report += `• 视觉风格: ${phase2Data.visualStyle}\n`;
    if (phase2Data.colorScheme) report += `• 配色方案: ${phase2Data.colorScheme}\n`;
    if (phase2Data.textFrequency) report += `• 文字频率: ${phase2Data.textFrequency}\n`;
    if (phase2Data.hooks) {
      report += '\n🎯 视觉钩子:\n';
      phase2Data.hooks.forEach((h, i) => report += `  ${i + 1}. ${h}\n`);
    }
    if (phase2Data.recommendations) {
      report += '\n💡 可复制元素:\n';
      phase2Data.recommendations.forEach((r, i) => report += `  ${i + 1}. ${r}\n`);
    }
  }
  return report + '\n━━━━━━━━━━━━━━━━━━━━\n';
}

async function main() {
  const args = parseArgs();
  if (!args.videoUrl && !args.localFile) return printHelp();

  utils.printBanner();
  
  try {
    let videoFilePath = '';
    let videoId = 'temp_' + Date.now();
    let reportBase = '';

    if (args.localFile) {
      videoFilePath = args.localFile;
      videoId = path.basename(args.localFile, path.extname(args.localFile));
      utils.printInfo(`本地模式: ${videoFilePath}`);
      reportBase = `📊 本地视频深度拆解报告\n━━━━━━━━━━━━━━━━━━━━\n📁 文件: ${videoFilePath}\n`;
    } else {
      utils.printInfo('步骤 1/3: 浏览器解析中...');
      const pwData = await playwrightScraper.fetchWithPlaywright(args.videoUrl);
      if (!pwData.downloadUrl) throw new Error('未能解析到下载地址，请检查链接或稍后再试');

      const res = await require('../lib/url-resolver').resolveDouyinUrl(args.videoUrl);
      videoId = res.videoId;
      
      utils.printInfo('步骤 2/3: 自动下载视频...');
      const dl = await videoDownloader.downloadVideo(pwData.downloadUrl, path.join(TEMP_DIR, 'downloads', videoId), videoId);
      if (!dl.success) throw new Error('下载失败: ' + (dl.error || '未知原因'));
      videoFilePath = dl.filePath;
      reportBase = utils.generateReport({ ...pwData, videoId, duration: 0 });
    }

    const effectiveFps = Math.min(5, Math.max(0.1, args.fps));
    utils.printInfo(`步骤 3/3: 正在提取 ${effectiveFps}fps 关键帧 (分段处理模式) 并进行 AI 视觉拆解...`);
    const framesDir = path.join(TEMP_DIR, 'frames', videoId);
    const { frames } = await frameExtractor.extractKeyframes(videoFilePath, framesDir, { 
        interval: 1 / effectiveFps
    });
    
    if (frames.length === 0) throw new Error('关键帧提取失败');
    
    // Phase 4: 音频提取与 ASR 识别
    utils.printInfo('步骤 4/4: 正在提取音频并进行智能 ASR 识别...');
    const audioPathRaw = path.join(TEMP_DIR, 'audio', `${videoId}`);
    fs.mkdirSync(path.dirname(audioPathRaw), { recursive: true });
    
    // 自动适配后缀
    const actualAudioPath = await audioProcessor.extractAudio(videoFilePath, audioPathRaw);
    const scriptText = await audioProcessor.recognizeSpeech(actualAudioPath, ZHIPU_API_KEY);
    
    // 执行视觉分析
    const aiResult = await aiAnalyzer.analyzeFrames(frames, ZHIPU_API_KEY, args.model);

    // 组装最终报告
    let finalReport = reportBase;
    if (scriptText) {
      finalReport += '\n🎙️ 语音转文字 (ASR)\n';
      finalReport += '━━━━━━━━━━━━━━━━━━━━\n';
      finalReport += `${scriptText}\n\n`;
    }
    finalReport = attachAIData(finalReport, aiResult);

    console.log(finalReport);
    
    // 清理临时文件
    frameExtractor.cleanupFrames(framesDir);
    if (fs.existsSync(actualAudioPath)) fs.unlinkSync(actualAudioPath);

  } catch (error) {
    utils.printError(error.message);
  }
}

main();
