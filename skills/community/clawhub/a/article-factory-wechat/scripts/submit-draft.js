#!/usr/bin/env node

/**
 * 微信公众号草稿提交脚本（使用官方接口）
 * 从环境变量获取 WECHAT_APPID 和 WECHAT_APPSECRET
 * 支持命令行传参 --html 和 --title
 * 流程: 获取access_token → 上传图片 → 发布草稿
 */

const fs = require('fs');
const path = require('path');
const { program } = require('commander');

// 从环境变量获取密钥
let APPID = process.env.WECHAT_APPID?.trim();
let APPSECRET = process.env.WECHAT_APPSECRET?.trim();

// 尝试从 OpenClaw 环境配置文件读取
if (!APPID || !APPSECRET) {
  const envPath = path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'env');
  
  if (fs.existsSync(envPath)) {
    console.log('从 OpenClaw 环境配置文件读取密钥...');
    const envContent = fs.readFileSync(envPath, 'utf-8');
    const appIdMatch = envContent.match(/WECHAT_APPID=(.*)/);
    const appSecretMatch = envContent.match(/WECHAT_APPSECRET=(.*)/);
    
    if (appIdMatch) {
      APPID = appIdMatch[1].trim();
    }
    if (appSecretMatch) {
      APPSECRET = appSecretMatch[1].trim();
    }
  }
}

if (!APPID || !APPSECRET) {
  console.error('错误: 请设置环境变量 WECHAT_APPID 和 WECHAT_APPSECRET');
  console.error('方法1: 在 OpenClaw 环境配置中设置');
  console.error('  编辑 ~/.openclaw/env 文件，添加:');
  console.error('  WECHAT_APPID=your_app_id');
  console.error('  WECHAT_APPSECRET=your_app_secret');
  console.error('方法2: 在系统环境变量中设置');
  console.error('  export WECHAT_APPID=your_app_id');
  console.error('  export WECHAT_APPSECRET=your_app_secret');
  process.exit(1);
}

// 配置命令行参数
program
  .option('--html <path>', 'HTML文件路径')
  .option('--title <title>', '文章标题')
  .option('--author <author>', '作者，默认为"虾看虾说"')
  .option('--digest <digest>', '摘要，若为空则不添加该参数')
  .parse(process.argv);

const options = program.opts();

if (!options.html || !options.title) {
  console.error('错误: 必须提供 --html 和 --title 参数');
  console.error('示例: node scripts/submit-draft-official.js --html output/20260321-test/article.html --title "测试文章"');
  process.exit(1);
}

// 延迟函数
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// 发送HTTP请求
async function request(options) {
  try {
    const response = await fetch(options.url, {
      method: options.method,
      headers: options.headers,
      body: options.body,
    });
    
    const data = await response.text();
    
    if (!data) {
      throw new Error('空响应');
    }
    
    const result = JSON.parse(data);
    if (result.errcode && result.errcode !== 0) {
      throw new Error(`API错误: ${result.errmsg} (code: ${result.errcode})`);
    }
    
    return result;
  } catch (error) {
    console.error('请求错误:', error);
    throw error;
  }
}

// 获取access_token - 使用微信官方接口
async function getAccessToken() {
  console.log('正在获取access_token...');
  const apiUrl = `https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=${APPID}&secret=${APPSECRET}`;
  
  try {
    const response = await fetch(apiUrl, {
      method: 'GET',
    });
    
    const data = await response.text();
    
    if (!data) {
      throw new Error('空响应');
    }
    
    const result = JSON.parse(data);
    if (result.errcode && result.errcode !== 0) {
      throw new Error(`API错误: ${result.errmsg} (code: ${result.errcode})`);
    }
    
    console.log('✓ 获取access_token成功');
    return result.access_token;
  } catch (error) {
    console.error('请求错误:', error);
    throw error;
  }
}

// 测试access_token是否有效 - 使用微信官方接口
async function testAccessToken(accessToken) {
  console.log('测试access_token是否有效...');
  const apiUrl = `https://api.weixin.qq.com/cgi-bin/material/get_materialcount?access_token=${accessToken}`;
  
  try {
    const response = await fetch(apiUrl, {
      method: 'GET',
    });
    
    const data = await response.text();

    if (!data) {
      throw new Error('空响应');
    }
    
    const result = JSON.parse(data);
    if (result.errcode && result.errcode !== 0) {
      throw new Error(`API错误: ${result.errmsg} (code: ${result.errcode})`);
    }
    
    console.log('  素材数量:', JSON.stringify(result, null, 2));
    console.log('✓ access_token有效');
    return result;
  } catch (error) {
    console.error('请求错误:', error);
    throw error;
  }
}

// 上传图片到微信永久素材（用于正文）- 使用微信官方接口
async function uploadImage(accessToken, imagePath) {
  console.log(`正在上传图片: ${path.basename(imagePath)}`);
  
  // 检查图片文件
  if (!fs.existsSync(imagePath)) {
    throw new Error(`图片不存在: ${imagePath}`);
  }
  
  const stats = fs.statSync(imagePath);
  console.log(`  图片大小: ${(stats.size / 1024).toFixed(2)} KB`);
  
  // 使用微信官方永久素材上传接口
  const apiUrl = `https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=${accessToken}&type=image`;
  
  // 使用FormData上传图片
  const formData = new FormData();
  const imageBuffer = fs.readFileSync(imagePath);
  formData.append('media', new Blob([imageBuffer]), path.basename(imagePath));
  
  console.log('  准备上传图片...');
  
  try {
    const response = await fetch(apiUrl, {
      method: 'POST',
      body: formData,
    });

    const data = await response.text();

    if (!data) {
      throw new Error('空响应');
    }
    
    const result = JSON.parse(data);
    if (result.errcode && result.errcode !== 0) {
      throw new Error(`API错误: ${result.errmsg} (code: ${result.errcode})`);
    }
    
    if (!result.url) {
      throw new Error(`图片上传失败，缺少url: ${JSON.stringify(result)}`);
    }
    
    console.log(`✓ 上传图片成功`);
    return result;
  } catch (error) {
    console.error('请求错误:', error);
    throw error;
  }
}

// 上传封面图片（使用永久素材接口）
async function uploadCover(accessToken, imagePath) {
  console.log(`正在上传封面图片: ${path.basename(imagePath)}`);
  
  // 检查图片文件
  if (!fs.existsSync(imagePath)) {
    throw new Error(`封面图片不存在: ${imagePath}`);
  }
  
  const stats = fs.statSync(imagePath);
  console.log(`  图片大小: ${(stats.size / 1024).toFixed(2)} KB`);
  
  // 使用微信官方永久素材上传接口
  const apiUrl = `https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=${accessToken}&type=image`;
  
  // 使用FormData上传图片
  const formData = new FormData();
  const imageBuffer = fs.readFileSync(imagePath);
  formData.append('media', new Blob([imageBuffer]), path.basename(imagePath));
  
  console.log('  准备上传图片...');
  
  try {
    const response = await fetch(apiUrl, {
      method: 'POST',
      body: formData,
    });

    const data = await response.text();

    if (!data) {
      throw new Error('空响应');
    }
    
    const result = JSON.parse(data);
    if (result.errcode && result.errcode !== 0) {
      throw new Error(`API错误: ${result.errmsg} (code: ${result.errcode})`);
    }
    
    if (!result.media_id) {
      throw new Error(`封面上传失败，缺少media_id: ${JSON.stringify(result)}`);
    }
    
    console.log(`✓ 上传封面成功: media_id=${result.media_id}`);

    return result;
  } catch (error) {
    console.error('请求错误:', error);
    throw error;
  }
}

// 解析HTML提取内容和图片
function parseHtml(htmlPath, outputDir) {
  console.log('正在解析HTML文件...');
  const html = fs.readFileSync(htmlPath, 'utf-8');
  
  // 提取图片 - 找到所有img标签
  const imgRegex = /<img[^>]+src=["']([^"']+)["'][^>]*>/g;
  const images = [];
  let match;
  
  // HTML文件所在目录
  const htmlDir = path.dirname(path.resolve(htmlPath));
  
  while ((match = imgRegex.exec(html)) !== null) {
    let imgSrc = match[1];
    // 如果是相对路径，解析为绝对路径
    if (!imgSrc.startsWith('http')) {
      // 解析为绝对路径
      const absolutePath = path.resolve(htmlDir, imgSrc);
      
      // 检查图片是否存在
      if (fs.existsSync(absolutePath)) {
        images.push(absolutePath);
      }
    }
  }
  
  // 提取<body>标签内的内容，去除完整的HTML结构
  let content = html;
  const bodyMatch = html.match(/<body[^>]*>([\s\S]*)<\/body>/i);
  if (bodyMatch && bodyMatch[1]) {
    content = bodyMatch[1];
    // 去除外层容器div（如果有）
    const containerMatch = content.match(/<div[^>]+class=["']container["'][^>]*>([\s\S]*)<\/div>/i);
    if (containerMatch && containerMatch[1]) {
      content = containerMatch[1];
    }
  }
  
  // 如果没找到本地图片，检查当前目录是否有cover.png
  const defaultCover = path.join(htmlDir, 'cover.png');
  if (images.length === 0 && fs.existsSync(defaultCover)) {
    console.log('⚠️  未在HTML中找到本地图片，使用默认cover.png作为封面');
    images.push(defaultCover);
  }
  
  console.log(`✓ 解析完成，找到 ${images.length} 张本地图片`);

  return {
    content: content,
    images,
  };
}

// 发布草稿 - 使用微信官方接口
async function addDraft(accessToken, title, content, thumbMediaId, author = '虾看虾说', digest = '') {
  console.log('正在发布草稿...');
  
  // 检查content长度
  console.log('  文章内容长度:', content.length);
  
  // 检查thumbMediaId
  console.log('  封面media_id:', thumbMediaId);

  const apiUrl = `https://api.weixin.qq.com/cgi-bin/draft/add?access_token=${accessToken}`;
  
  // 构建请求体 - 使用JSON格式（微信官方接口要求）
  const article = {
    title: title,
    author: author,
    content: content,
    content_source_url: '',
    thumb_media_id: thumbMediaId,
    need_open_comment: 1,
    only_fans_can_comment: 0,
    show_cover_pic: thumbMediaId ? 1 : 0
  };
  
  // 只有当digest不为空时才添加该参数
  if (digest) {
    article.digest = digest;
  }
  
  const requestBody = {
    articles: [article]
  };

  try {
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody),
    });
    
    const data = await response.text();
    
    if (!data) {
      throw new Error('空响应');
    }
    
    const result = JSON.parse(data);
    if (result.errcode && result.errcode !== 0) {
      throw new Error(`API错误: ${result.errmsg} (code: ${result.errcode})`);
    }
    
    console.log('✓ 发布草稿成功');
    console.log(`  draft_id: ${result.media_id}`);
    return result;
  } catch (error) {
    console.error('请求错误:', error);
    throw error;
  }
}

// 主流程
async function main() {
  try {
    const accessToken = await getAccessToken();
    
    // 测试access_token是否有效
    // await testAccessToken(accessToken);
    
    const htmlPath = path.resolve(options.html);
    const outputDir = path.dirname(htmlPath);
    
    // 解析HTML
    const { content, images } = parseHtml(htmlPath, outputDir);
    
    // 上传所有图片并替换HTML中的图片URL
    let processedContent = content;
    const uploadedImages = [];
    let thumbMediaId = null;
    
    // 优先使用 HTML文件同一目录下的 images/cover.png 作为封面图片
    const htmlDir = path.dirname(path.resolve(options.html));
    const defaultCover = path.join(htmlDir, 'images', 'cover.png');
    const fallbackCover = path.join(htmlDir, 'cover.png');
    let coverImage = null;
    
    // 检查是否存在默认封面图片
    if (fs.existsSync(defaultCover)) {
      coverImage = defaultCover;
      console.log('✓ 使用默认封面图片: images/cover.png');
    } else if (fs.existsSync(fallbackCover)) {
      coverImage = fallbackCover;
      console.log('✓ 使用默认封面图片: cover.png');
    } else if (images.length > 0) {
      // 如果没有默认封面，使用第一张图片
      coverImage = images[0];
      console.log('⚠️  未找到默认封面图片，使用第一张图片作为封面');
    } else {
      console.error('错误: 没有找到图片，请至少包含一张封面图片');
      process.exit(1);
    }
    
    // 上传封面图片
    const coverResult = await uploadCover(accessToken, coverImage);
    thumbMediaId = coverResult.media_id;
    
    // 上传所有文章内图片作为临时素材（封面仅需要上传一次作为thumb，不需要重复上传到内容）
    const allImages = new Set([...images]);
    for (const image of allImages) {
      const uploadResult = await uploadImage(accessToken, image);
      uploadedImages.push(uploadResult);
      
      // 替换HTML中的本地图片URL为微信服务器URL
      const localImagePath = image;
      const localImageName = path.basename(localImagePath);
      const wechatImageUrl = uploadResult.url;
      
      // 替换相对路径的图片 (如 images/api-summary.png)
      const htmlDir = path.dirname(path.resolve(options.html));
      const relativePath = path.relative(htmlDir, localImagePath);
      
      // 替换带 ./ 前缀的相对路径
      const withDotSlashPattern = new RegExp('\\./' + relativePath.replace(/\//g, '\\/'), 'g');
      let tempContent = processedContent;
      tempContent = tempContent.replace(withDotSlashPattern, wechatImageUrl);
      
      // 替换标准相对路径
      const normalPattern = new RegExp(relativePath.replace(/\//g, '\\/'), 'g');
      tempContent = tempContent.replace(normalPattern, wechatImageUrl);
      
      // 替换纯文件名的图片
      const namePattern = new RegExp(localImageName, 'g');
      tempContent = tempContent.replace(namePattern, wechatImageUrl);
      
      // 替换绝对路径的图片
      const absolutePattern = new RegExp(localImagePath.replace(/\//g, '\\/'), 'g');
      tempContent = tempContent.replace(absolutePattern, wechatImageUrl);
      
      processedContent = tempContent;
    }
    
    // 获取命令行参数
    const author = options.author || '虾看虾说';
    const digest = options.digest || '';
    
    // 发布草稿
    const result = await addDraft(accessToken, options.title, processedContent, thumbMediaId, author, digest);
    
    // 保存草稿信息到输出目录
    const draftInfo = {
      title: options.title,
      htmlPath: options.html,
      accessToken: accessToken,
      media_id: result.media_id,
      draft_id: result.media_id,
      uploadedImages: uploadedImages,
      createTime: new Date().toISOString(),
    };
    
    const draftPath = path.join(outputDir, 'draft.json');
    fs.writeFileSync(draftPath, JSON.stringify(draftInfo, null, 2));
    
    console.log('\n🎉 提交成功！');
    console.log(`草稿ID: ${result.media_id}`);
    console.log(`草稿信息已保存到: ${draftPath}`);
    console.log(`请登录微信公众号后台查看草稿`);
    
  } catch (error) {
    console.error('❌ 错误:', error.message);
    process.exit(1);
  }
}

// 运行主函数
main();