/**
 * 抖音下载器 - OpenClaw Skill 主入口
 * 
 * 功能：
 * - 解析抖音分享链接
 * - 下载无水印视频
 * - 批量处理
 */

import { parseDouyinVideo, parseMultipleUrls, isDouyinUrl } from './parser.js';
import { downloadDouyinVideo, batchDownload, getDefaultSaveDir } from './downloader.js';
import { getVideoWithPlaywright } from './browser-extract.js';

/**
 * 处理用户请求
 * @param {Object} context - OpenClaw 上下文
 */
export async function handle(context) {
  const { message, config = {} } = context;
  
  // 提取消息中的抖音链接
  const urls = extractDouyinUrls(message);
  
  if (urls.length === 0) {
    return {
      success: false,
      message: '未找到抖音链接。请分享抖音视频链接，例如：https://v.douyin.com/xxxxx'
    };
  }

  // 获取保存目录
  const saveDir = config.saveDir || getDefaultSaveDir();

  try {
    if (urls.length === 1) {
      // 单个视频处理
      let videoInfo = await parseDouyinVideo(urls[0]);
      
      // 如果没有获取到视频 URL，使用 Playwright 浏览器提取
      if (!videoInfo.videoUrl || videoInfo.videoUrl.includes('douyin.com')) {
        console.log('使用 Playwright 获取真实视频地址...');
        const browserResult = await getVideoWithPlaywright(videoInfo.id);
        if (browserResult.success) {
          videoInfo = { ...videoInfo, ...browserResult };
        }
      }
      
      const result = await downloadDouyinVideo(videoInfo, saveDir, {
        saveMetadata: config.saveMetadata !== false
      });

      if (result.success) {
        return {
          success: true,
          message: `✅ 下载成功！\n\n📹 视频：${videoInfo.title}\n👤 作者：${videoInfo.author}\n📁 保存：${result.path}\n💾 大小：${formatSize(result.size)}`,
          data: result
        };
      } else {
        return {
          success: false,
          message: `❌ 下载失败：${result.error}`
        };
      }
    } else {
      // 批量处理
      const parseResults = await parseMultipleUrls(urls);
      
      if (parseResults.results.length === 0) {
        return {
          success: false,
          message: `所有链接解析失败：\n${parseResults.errors.map(e => `- ${e.url}: ${e.error}`).join('\n')}`
        };
      }

      const downloadResults = await batchDownload(parseResults.results, saveDir, {
        saveMetadata: config.saveMetadata !== false
      });

      const successCount = downloadResults.filter(r => r.success).length;
      const failCount = downloadResults.filter(r => !r.success).length;

      return {
        success: true,
        message: `📥 批量下载完成！\n\n✅ 成功：${successCount}\n❌ 失败：${failCount}\n📁 目录：${saveDir}`,
        data: downloadResults
      };
    }
  } catch (error) {
    return {
      success: false,
      message: `❌ 处理失败：${error.message}`
    };
  }
}

/**
 * 从消息中提取抖音链接
 */
function extractDouyinUrls(message) {
  const patterns = [
    /https?:\/\/(?:www\.)?douyin\.com\/[^\s]+/gi,
    /https?:\/\/v\.douyin\.com\/[^\s]+/gi,
    /https?:\/\/m\.douyin\.com\/[^\s]+/gi,
    /https?:\/\/(?:www\.)?iesdouyin\.com\/[^\s]+/gi,
  ];

  const urls = [];
  for (const pattern of patterns) {
    const matches = message.match(pattern);
    if (matches) {
      urls.push(...matches);
    }
  }

  return [...new Set(urls)]; // 去重
}

/**
 * 格式化文件大小
 */
function formatSize(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
}

/**
 * 技能信息
 */
export const skillInfo = {
  name: 'douyin-downloader',
  version: '1.0.0',
  description: '抖音无水印视频下载器',
  triggers: [
    '下载抖音',
    '解析抖音',
    '保存抖音',
    'douyin download',
    '无水印'
  ]
};

// 导出供测试使用
export { parseDouyinVideo, downloadDouyinVideo, getDefaultSaveDir, isDouyinUrl };
