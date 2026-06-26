#!/usr/bin/env node

/**
 * 发布已有文章到微信公众号草稿箱
 */

const fs = require('fs');
const path = require('path');
const axios = require('axios');
const FormData = require('form-data');

// 配置
const config = {
  appID: 'wx128409576294cb9d',
  appSecret: '3139a3d2a930678209d8ffae5e103005',
  apiBase: 'https://api.weixin.qq.com'
};

// 日志
function log(message, level = 'info') {
  const icons = { info: '📝', success: '✅', error: '❌', process: '🔄' };
  console.log(`${icons[level] || '📝'} ${message}`);
}

// 主函数
async function main() {
  const articlePath = process.argv[2];
  
  if (!articlePath || !fs.existsSync(articlePath)) {
    log('请提供有效的文章路径', 'error');
    process.exit(1);
  }
  
  log(`开始发布文章: ${path.basename(articlePath)}`, 'process');
  
  try {
    // 1. 获取 access token
    log('步骤1: 获取 Access Token...', 'process');
    const tokenUrl = `${config.apiBase}/cgi-bin/token?grant_type=client_credential&appid=${config.appID}&secret=${config.appSecret}`;
    const tokenResponse = await axios.get(tokenUrl, { timeout: 10000 });
    
    if (tokenResponse.data.errcode) {
      throw new Error(`获取Token失败: ${tokenResponse.data.errmsg}`);
    }
    
    const accessToken = tokenResponse.data.access_token;
    log('Access Token 获取成功', 'success');
    
    // 2. 解析文章
    log('步骤2: 解析文章内容...', 'process');
    const articleContent = fs.readFileSync(articlePath, 'utf8');
    const lines = articleContent.split('\n');
    
    let title = '今日分享';
    let digest = '深度内容分享';
    
    // 提取标题（第一个 # 开头的行）
    for (const line of lines) {
      if (line.startsWith('# ')) {
        title = line.replace('# ', '').trim();
        break;
      }
    }
    
    // 提取摘要（第二段非空内容）
    let foundFirst = false;
    for (const line of lines) {
      const trimmed = line.trim();
      if (trimmed && !trimmed.startsWith('#') && !trimmed.startsWith('---') && !trimmed.startsWith('```')) {
        if (!foundFirst) {
          foundFirst = true;
        } else {
          digest = trimmed.substring(0, 100);
          break;
        }
      }
    }
    
    log(`标题: ${title}`, 'info');
    log(`摘要: ${digest.substring(0, 50)}...`, 'info');
    
    // 3. 生成简单封面
    log('步骤3: 生成封面...', 'process');
    const coverPath = '/tmp/wechat-cover.png';
    const svgContent = `<?xml version="1.0" encoding="UTF-8"?>
<svg width="900" height="500" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="#FFFFFF"/>
  <text x="450" y="230" text-anchor="middle" font-size="36" fill="#333333" font-family="Arial, sans-serif">${title.substring(0, 15)}</text>
  <text x="450" y="280" text-anchor="middle" font-size="24" fill="#666666" font-family="Arial, sans-serif">小帽 · AI助手</text>
  <text x="450" y="350" text-anchor="middle" font-size="18" fill="#999999" font-family="Arial, sans-serif">2026-03-19</text>
</svg>`;
    
    const tempSvg = '/tmp/temp-cover.svg';
    fs.writeFileSync(tempSvg, svgContent, 'utf8');
    
    try {
      const { execSync } = require('child_process');
      execSync(`convert ${tempSvg} ${coverPath}`, { stdio: 'ignore' });
      log('封面生成成功', 'success');
    } catch (error) {
      log(`封面生成失败，使用默认封面: ${error.message}`, 'error');
      // 创建一个简单的 PNG
      const { createCanvas } = require('canvas');
      const canvas = createCanvas(900, 500);
      const ctx = canvas.getContext('2d');
      ctx.fillStyle = '#FFFFFF';
      ctx.fillRect(0, 0, 900, 500);
      ctx.fillStyle = '#333333';
      ctx.font = '36px Arial';
      ctx.textAlign = 'center';
      ctx.fillText(title.substring(0, 15), 450, 250);
      fs.writeFileSync(coverPath, canvas.toBuffer('image/png'));
    }
    
    // 4. 上传封面
    log('步骤4: 上传封面到素材库...', 'process');
    const form = new FormData();
    const imageBuffer = fs.readFileSync(coverPath);
    form.append('media', imageBuffer, {
      filename: 'cover.png',
      contentType: 'image/png'
    });
    
    const uploadUrl = `${config.apiBase}/cgi-bin/material/add_material?access_token=${accessToken}&type=image`;
    const uploadResponse = await axios.post(uploadUrl, form, {
      headers: { ...form.getHeaders() },
      maxContentLength: Infinity,
      maxBodyLength: Infinity,
      timeout: 30000
    });
    
    if (uploadResponse.data.errcode) {
      throw new Error(`封面上传失败: ${uploadResponse.data.errmsg}`);
    }
    
    const mediaId = uploadResponse.data.media_id;
    log(`封面上传成功: media_id=${mediaId.substring(0, 20)}...`, 'success');
    
    // 5. 创建草稿
    log('步骤5: 创建草稿...', 'process');
    
    // 转换 Markdown 为简单 HTML（微信公众号支持的格式）
    let htmlContent = articleContent
      .replace(/^# (.+)$/gm, '<h1>$1</h1>')
      .replace(/^## (.+)$/gm, '<h2>$1</h2>')
      .replace(/^### (.+)$/gm, '<h3>$1</h3>')
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.+?)\*/g, '<em>$1</em>')
      .replace(/`(.+?)`/g, '<code>$1</code>')
      .replace(/```(\w+)?\n([\s\S]+?)```/g, '<pre><code>$2</code></pre>')
      .replace(/^- (.+)$/gm, '<li>$1</li>')
      .replace(/\n\n/g, '</p><p>')
      .replace(/\n/g, '<br/>');
    
    htmlContent = `<section><p>${htmlContent}</p></section>`;
    
    const draftData = {
      articles: [{
        title: title,
        author: '小帽',
        digest: digest,
        content: htmlContent,
        content_source_url: '',
        thumb_media_id: mediaId,
        need_open_comment: 0,
        only_fans_can_comment: 0
      }]
    };
    
    const draftUrl = `${config.apiBase}/cgi-bin/draft/add?access_token=${accessToken}`;
    const draftResponse = await axios.post(draftUrl, draftData, {
      headers: { 'Content-Type': 'application/json' },
      timeout: 30000
    });
    
    if (draftResponse.data.errcode) {
      throw new Error(`创建草稿失败: ${draftResponse.data.errmsg}`);
    }
    
    const mediaId2 = draftResponse.data.media_id;
    log('草稿创建成功！', 'success');
    
    console.log('\n' + '='.repeat(50));
    log('发布完成！', 'success');
    log(`标题: ${title}`, 'info');
    log(`草稿 media_id: ${mediaId2}`, 'info');
    log('请登录微信公众号后台查看草稿', 'info');
    console.log('='.repeat(50) + '\n');
    
  } catch (error) {
    log(`发布失败: ${error.message}`, 'error');
    console.error(error);
    process.exit(1);
  }
}

main();
