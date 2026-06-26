#!/usr/bin/env node

/**
 * 长文章归档脚本 - 支持多图片和分段写入
 * 用于处理包含大量图片的长文章（如 Twitter Article）
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 配置
const FEISHU_CONFIG = {
  space_id: '7527734827164909572',
  parent_node_token: 'NqZvwBqMTiTEtkkMsRoc76rznce',
  app_id: 'cli_a90ecd03bc399bcb',
  app_secret: 'gdEsio0WzDtHEhHFeLS55wBseDpExVtg'
};

// 获取飞书 access token
function getAccessToken() {
  const cmd = `curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \\
    -H "Content-Type: application/json" \\
    -d '{"app_id":"${FEISHU_CONFIG.app_id}","app_secret":"${FEISHU_CONFIG.app_secret}"}'`;
  
  const result = JSON.parse(execSync(cmd, { encoding: 'utf-8' }));
  if (result.code !== 0) {
    throw new Error(`Failed to get access token: ${result.msg}`);
  }
  return result.tenant_access_token;
}

// 解析文章内容，提取图片位置
function parseArticleContent(content) {
  const lines = content.split('\n');
  const segments = [];
  let currentSegment = [];
  let imageIndex = 1;
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    
    // 检测图片标记
    if (line.includes('![图像]') || line.includes('](http')) {
      // 保存当前文本段
      if (currentSegment.length > 0) {
        segments.push({
          type: 'text',
          content: currentSegment.join('\n')
        });
        currentSegment = [];
      }
      
      // 添加图片段
      segments.push({
        type: 'image',
        index: imageIndex++
      });
    } else {
      currentSegment.push(line);
    }
  }
  
  // 保存最后一段文本
  if (currentSegment.length > 0) {
    segments.push({
      type: 'text',
      content: currentSegment.join('\n')
    });
  }
  
  return segments;
}

// 主函数
async function main() {
  const url = process.argv[2];
  if (!url) {
    console.error('Usage: node archive-long-article.js <twitter_url>');
    process.exit(1);
  }
  
  console.log('Step 1: Fetching article content...');
  
  // 抓取文章内容
  const cookieFile = path.join(__dirname, '../config/twitter-cookies.txt');
  const cookie = fs.readFileSync(cookieFile, 'utf-8').trim();
  
  const fetchScript = path.join(__dirname, 'fetch-twitter-article-formatted.js');
  const fetchCmd = `node "${fetchScript}" "${url}" "${cookie}"`;
  const articleJson = execSync(fetchCmd, { encoding: 'utf-8' });
  const article = JSON.parse(articleJson);
  
  if (!article.success) {
    throw new Error('Failed to fetch article');
  }
  
  console.log(`Article title: ${article.title}`);
  console.log(`Content length: ${article.content.split('\n').length} lines`);
  
  // 下载图片
  console.log('\nStep 2: Downloading images...');
  const imageUrls = [];
  const imageRegex = /https:\/\/pbs\.twimg\.com\/media\/[^\)]+/g;
  const matches = article.content.match(imageRegex);
  
  if (matches) {
    matches.forEach(url => {
      const highResUrl = url.replace(/\?format=jpg&name=\w+/, '?format=jpg&name=900x900');
      if (!imageUrls.includes(highResUrl)) {
        imageUrls.push(highResUrl);
      }
    });
  }
  
  console.log(`Found ${imageUrls.length} images`);
  
  const imageDir = '/tmp/article_images';
  execSync(`rm -rf ${imageDir} && mkdir -p ${imageDir}`);
  
  for (let i = 0; i < imageUrls.length; i++) {
    const imagePath = path.join(imageDir, `img${i + 1}.jpg`);
    execSync(`wget -q -O "${imagePath}" "${imageUrls[i]}"`);
    console.log(`Downloaded img${i + 1}.jpg`);
  }
  
  // 解析文章内容，确定图片插入位置
  console.log('\nStep 3: Parsing article structure...');
  const segments = parseArticleContent(article.content);
  console.log(`Parsed into ${segments.length} segments (${segments.filter(s => s.type === 'text').length} text, ${segments.filter(s => s.type === 'image').length} images)`);
  
  // 创建飞书文档
  console.log('\nStep 4: Creating Feishu document...');
  const token = getAccessToken();
  
  const createCmd = `curl -s -X POST "https://open.feishu.cn/open-apis/wiki/v2/spaces/${FEISHU_CONFIG.space_id}/nodes" \\
    -H "Authorization: Bearer ${token}" \\
    -H "Content-Type: application/json" \\
    -d '{"obj_type":"docx","parent_node_token":"${FEISHU_CONFIG.parent_node_token}","node_type":"origin","origin_node_token":"","title":"${article.title.replace(/"/g, '\\"')}"}'`;
  
  const createResult = JSON.parse(execSync(createCmd, { encoding: 'utf-8' }));
  if (createResult.code !== 0) {
    throw new Error(`Failed to create document: ${createResult.msg}`);
  }
  
  const docToken = createResult.data.obj_token;
  const nodeToken = createResult.data.node.node_token;
  console.log(`Document created: ${docToken}`);
  console.log(`Document URL: https://qingzhao.feishu.cn/wiki/${nodeToken}`);
  
  // 写入内容和图片
  console.log('\nStep 5: Writing content and uploading images...');
  
  // 写入元数据
  const metadata = `> **原始链接**：${url}
> 
> **归档时间**：${new Date().toISOString().slice(0, 19).replace('T', ' ')}
> 
> **来源**：x.com (Twitter Article)
> 
> **作者**：${article.author || 'Unknown'}

---

`;
  
  // 第一段：元数据
  const writeCmd = `openclaw feishu-doc write --doc-token "${docToken}" --content "${metadata.replace(/"/g, '\\"').replace(/\n/g, '\\n')}"`;
  execSync(writeCmd, { stdio: 'inherit' });
  
  // 逐段写入内容和图片
  for (let i = 0; i < segments.length; i++) {
    const segment = segments[i];
    
    if (segment.type === 'text') {
      // 写入文本内容
      const content = segment.content.replace(/"/g, '\\"').replace(/\n/g, '\\n');
      const appendCmd = `openclaw feishu-doc append --doc-token "${docToken}" --content "${content}"`;
      execSync(appendCmd, { stdio: 'inherit' });
      console.log(`Appended text segment ${i + 1}/${segments.length}`);
    } else if (segment.type === 'image') {
      // 上传图片
      const imagePath = path.join(imageDir, `img${segment.index}.jpg`);
      if (fs.existsSync(imagePath)) {
        const uploadCmd = `openclaw feishu-doc upload-image --doc-token "${docToken}" --file-path "${imagePath}"`;
        execSync(uploadCmd, { stdio: 'inherit' });
        console.log(`Uploaded image ${segment.index}/${imageUrls.length}`);
      }
    }
  }
  
  console.log('\n✅ Article archived successfully!');
  console.log(`Document URL: https://qingzhao.feishu.cn/wiki/${nodeToken}`);
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
