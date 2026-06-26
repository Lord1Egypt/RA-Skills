/**
 * 图片选择器 - 从目录中随机选择图片
 */

const fs = require('fs');
const path = require('path');

/**
 * 扫描目录中的图片文件
 */
function scanImages(dirPath) {
  const imageExts = ['.jpg', '.jpeg', '.png', '.gif', '.webp'];
  const images = [];
  
  if (!fs.existsSync(dirPath)) {
    console.log(`⚠️ 目录不存在：${dirPath}`);
    return images;
  }
  
  const files = fs.readdirSync(dirPath);
  for (const file of files) {
    const ext = path.extname(file).toLowerCase();
    if (imageExts.includes(ext)) {
      images.push({
        filename: file,
        fullPath: path.join(dirPath, file),
        ext: ext
      });
    }
  }
  
  console.log(`🖼️  找到 ${images.length} 张图片`);
  return images;
}

/**
 * 随机选择一张图片
 */
function pickRandomImage(images) {
  if (images.length === 0) return null;
  const index = Math.floor(Math.random() * images.length);
  return images[index];
}

/**
 * 生成图片 HTML（微信公众号格式）
 */
function generateImageHtml(imagePath, caption = '') {
  // 注意：微信公众号需要图片 URL，本地文件需要上传
  // 这里返回占位符，实际需要调用微信 API 上传
  return `
<div style="text-align:center;margin:20px 0;">
  <img src="${imagePath}" alt="${caption}" style="max-width:100%;height:auto;border-radius:8px;" />
  ${caption ? `<p style="text-align:center;color:#999;font-size:13px;margin:8px 0 0;">${caption}</p>` : ''}
</div>
  `.trim();
}

module.exports = {
  scanImages,
  pickRandomImage,
  generateImageHtml
};
