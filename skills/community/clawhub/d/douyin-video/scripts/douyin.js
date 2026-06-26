#!/usr/bin/env node

/**
 * 抖音无水印视频下载器
 * 
 * 功能:
 * 1. 解析抖音分享链接
 * 2. 提取视频信息（标题、作者、点赞等）
 * 3. 下载无水印视频
 * 4. 返回本地文件路径
 * 
 * 使用示例:
 *   node douyin.js "https://v.douyin.com/FSfWiKriBuY/"
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

// 配置
const HEADERS = {
  'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'zh-CN,zh;q=0.9'
};

// 工具函数：HTTP 请求
function httpRequest(url) {
  return new Promise((resolve, reject) => {
    const client = url.startsWith('https') ? https : http;
    const req = client.get(url, { headers: HEADERS }, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        httpRequest(res.headers.location).then(resolve).catch(reject);
        return;
      }
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    });
    req.on('error', reject);
    req.setTimeout(30000, () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });
  });
}

// 从 HTML 中提取 JSON 数据
function extractVideoInfo(html) {
  // 提取 videoInfoRes
  const match = html.match(/"videoInfoRes":(\{.*?\}),"itemId"/);
  if (!match) {
    throw new Error('无法解析视频信息');
  }
  
  const videoInfo = JSON.parse(match[1]);
  const item = videoInfo.item_list[0];
  
  if (!item) {
    throw new Error('视频信息为空');
  }
  
  // 提取视频播放地址
  const playUrl = item.video.play_addr.url_list[0];
  
  return {
    video_id: item.aweme_id,
    title: item.desc,
    author: item.author.nickname,
    digg_count: item.statistics.digg_count,
    share_count: item.statistics.share_count,
    collect_count: item.statistics.collect_count,
    play_url: playUrl
  };
}

// 下载视频
async function downloadVideo(url, outputPath) {
  return new Promise((resolve, reject) => {
    const client = url.startsWith('https') ? https : http;
    const file = fs.createWriteStream(outputPath);
    
    const req = client.get(url, { headers: HEADERS }, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        downloadVideo(res.headers.location, outputPath).then(resolve).catch(reject);
        return;
      }
      
      res.pipe(file);
      file.on('finish', () => {
        file.close();
        resolve();
      });
    });
    
    req.on('error', (e) => {
      fs.unlink(outputPath, () => {});
      reject(e);
    });
    
    req.setTimeout(60000, () => {
      req.destroy();
      fs.unlink(outputPath, () => {});
      reject(new Error('Download timeout'));
    });
  });
}

// 主函数
async function main() {
  const shareUrl = process.argv[2];
  
  if (!shareUrl) {
    console.error('用法：node douyin.js <抖音分享链接>');
    process.exit(1);
  }
  
  console.log('🔍 正在解析抖音视频...');
  
  try {
    // 1. 获取 HTML 页面
    const html = await httpRequest(shareUrl);
    
    // 2. 提取视频信息
    const info = extractVideoInfo(html);
    
    console.log(`📹 找到视频：${info.title}`);
    console.log(`👤 作者：${info.author}`);
    console.log(`👍 点赞：${info.digg_count}`);
    
    // 3. 下载视频
    const workspaceDir = path.join(process.env.HOME || '/root', '.openclaw/workspace/douyin-downloads');
    // 确保目录存在
    if (!fs.existsSync(workspaceDir)) {
      fs.mkdirSync(workspaceDir, { recursive: true });
    }
    
    // 清理上一个下载的视频（如果有）
    const lastVideoFile = path.join(workspaceDir, 'douyin_last.mp4');
    if (fs.existsSync(lastVideoFile)) {
      fs.unlinkSync(lastVideoFile);
      console.log('🧹 已清理上一个视频');
    }
    
    const outputPath = lastVideoFile; // 统一使用 douyin_last.mp4
    console.log(`📥 正在下载视频...`);
    
    await downloadVideo(info.play_url, outputPath);
    
    // 4. 获取文件大小
    const stats = fs.statSync(outputPath);
    const size = (stats.size / 1024 / 1024).toFixed(2) + 'MB';
    
    console.log(`✅ 下载完成！`);
    console.log(`📊 大小：${size}`);
    console.log(`📁 路径：${outputPath}`);
    
    // 输出 JSON 结果
    const result = {
      success: true,
      video_id: info.video_id,
      title: info.title,
      author: info.author,
      statistics: {
        digg_count: info.digg_count,
        share_count: info.share_count,
        collect_count: info.collect_count
      },
      file_path: outputPath,
      file_size: size
    };
    
    console.log('\n---JSON RESULT---');
    console.log(JSON.stringify(result, null, 2));
    
  } catch (error) {
    console.error('❌ 错误:', error.message);
    process.exit(1);
  }
}

main();
