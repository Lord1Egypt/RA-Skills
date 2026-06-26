/**
 * 通用工具函数模块
 */

const fs = require('fs');
const path = require('path');
const axios = require('axios');

/**
 * 格式化数字（如 1285000 -> 128.5万）
 */
function formatNumber(num) {
  if (num === undefined || num === null || isNaN(num)) return '0';
  if (num >= 10000) {
    return (num / 10000).toFixed(1) + '万';
  }
  return num.toLocaleString();
}

/**
 * 格式化时间（毫秒 -> 分:秒）
 */
function formatDuration(ms) {
  if (!ms || isNaN(ms)) return '0:00';
  const totalSeconds = Math.floor(ms / 1000);
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${minutes}:${seconds.toString().padStart(2, '0')}`;
}

/**
 * 打印横幅
 */
function printBanner() {
  console.log('╔════════════════════════════════════════════╗');
  console.log('║    🎬 抖音视频拆解分析器 v2.0.0           ║');
  console.log('║    Douyin Video Analyzer (Playwright)      ║');
  console.log('╚════════════════════════════════════════════╝');
  console.log('');
}

/**
 * 打印普通消息
 */
function printInfo(msg) {
  console.log(`ℹ️  ${msg}`);
}

/**
 * 打印成功消息
 */
function printSuccess(msg) {
  console.log(`✅ ${msg}`);
}

/**
 * 打印错误消息
 */
function printError(msg) {
  console.log(`❌ 错误: ${msg}`);
}

/**
 * 生成基础报告
 */
function generateReport(data) {
  let report = '📊 视频分析报告 (Phase 1)\n';
  report += '━━━━━━━━━━━━━━━━━━━━\n';
  report += `🔗 视频链接: ${data.videoUrl || '未知'}\n`;
  report += `👤 作者: ${data.author || '未知'}\n\n`;
  
  report += '📈 基础数据\n';
  report += `• 点赞: ${formatNumber(data.likes)}\n`;
  report += `• 评论: ${formatNumber(data.comments)}\n`;
  report += `• 视频时长: ${formatDuration(data.duration)}\n\n`;
  
  if (data.title) {
    report += '📝 视频标题\n';
    report += `• ${data.title}\n\n`;
  }
  
  return report;
}

module.exports = {
  formatNumber,
  formatDuration,
  printBanner,
  printInfo,
  printSuccess,
  printError,
  generateReport
};
