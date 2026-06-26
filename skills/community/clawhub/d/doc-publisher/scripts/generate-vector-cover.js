// 生成向量数据库主题封面
// 创建一个 SVG 图像，展示文本到向量矩阵空间的可视化

const fs = require('fs');
const path = require('path');

// 创建 SVG 封面图
const svgContent = `<?xml version="1.0" encoding="UTF-8"?>
<svg width="900" height="500" xmlns="http://www.w3.org/2000/svg">
  <!-- 背景渐变 -->
  <defs>
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1a1a2e;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#16213e;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="vectorGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0f3460;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#e94560;stop-opacity:1" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>
  
  <!-- 背景 -->
  <rect width="900" height="500" fill="url(#bgGradient)"/>
  
  <!-- 网格线 -->
  <g stroke="#0f3460" stroke-width="1" opacity="0.3">
    <line x1="50" y1="50" x2="850" y2="50"/>
    <line x1="50" y1="150" x2="850" y2="150"/>
    <line x1="50" y1="250" x2="850" y2="250"/>
    <line x1="50" y1="350" x2="850" y2="350"/>
    <line x1="50" y1="450" x2="850" y2="450"/>
    <line x1="50" y1="50" x2="50" y2="450"/>
    <line x1="200" y1="50" x2="200" y2="450"/>
    <line x1="350" y1="50" x2="350" y2="450"/>
    <line x1="500" y1="50" x2="500" y2="450"/>
    <line x1="650" y1="50" x2="650" y2="450"/>
    <line x1="800" y1="50" x2="800" y2="450"/>
  </g>
  
  <!-- 左侧：文本 -->
  <text x="100" y="100" font-family="Arial, sans-serif" font-size="18" fill="#ffffff" text-anchor="middle" font-weight="bold">原始文本</text>
  <rect x="50" y="120" width="100" height="60" rx="8" fill="#16213e" stroke="#e94560" stroke-width="2"/>
  <text x="100" y="155" font-family="Arial, sans-serif" font-size="14" fill="#ffffff" text-anchor="middle">"人工智能"</text>
  
  <!-- 转换箭头 -->
  <path d="M 170 150 L 280 150" stroke="#e94560" stroke-width="3" fill="none" marker-end="url(#arrowhead)"/>
  <text x="225" y="140" font-family="Arial" font-size="12" fill="#e94560">Embedding</text>
  
  <!-- 中间：向量表示 -->
  <text x="450" y="100" font-family="Arial, sans-serif" font-size="18" fill="#ffffff" text-anchor="middle" font-weight="bold">向量表示</text>
  <rect x="320" y="120" width="260" height="60" rx="8" fill="#16213e" stroke="#0f3460" stroke-width="2"/>
  <text x="450" y="155" font-family="Consolas, monospace" font-size="11" fill="#00ff88" text-anchor="middle">[0.82, -0.45, 0.67, ..., 0.23]</text>
  
  <!-- 右侧：向量空间 -->
  <text x="750" y="100" font-family="Arial, sans-serif" font-size="18" fill="#ffffff" text-anchor="middle" font-weight="bold">向量空间</text>
  
  <!-- 向量空间可视化 - 3D 效果 -->
  <g transform="translate(650, 200)" filter="url(#glow)">
    <!-- 坐标轴 -->
    <line x1="0" y1="0" x2="100" y2="0" stroke="#e94560" stroke-width="2"/>
    <line x1="0" y1="0" x2="-50" y2="50" stroke="#00ff88" stroke-width="2"/>
    <line x1="0" y1="0" x2="0" y2="-80" stroke="#00d4ff" stroke-width="2"/>
    
    <!-- 向量点 -->
    <circle cx="30" cy="-20" r="6" fill="#e94560" opacity="0.8"/>
    <circle cx="50" cy="-40" r="6" fill="#00ff88" opacity="0.8"/>
    <circle cx="70" cy="-30" r="6" fill="#00d4ff" opacity="0.8"/>
    <circle cx="40" cy="10" r="6" fill="#ffcc00" opacity="0.8"/>
    <circle cx="60" cy="-10" r="6" fill="#ff66cc" opacity="0.8"/>
    
    <!-- 连接线 -->
    <line x1="30" y1="-20" x2="50" y2="-40" stroke="#ffffff" stroke-width="1" opacity="0.3"/>
    <line x1="50" y1="-40" x2="70" y2="-30" stroke="#ffffff" stroke-width="1" opacity="0.3"/>
    <line x1="70" y1="-30" x2="40" y2="10" stroke="#ffffff" stroke-width="1" opacity="0.3"/>
    <line x1="40" y1="10" x2="60" y2="-10" stroke="#ffffff" stroke-width="1" opacity="0.3"/>
  </g>
  
  <!-- 底部：相似度计算 -->
  <text x="450" y="350" font-family="Arial, sans-serif" font-size="20" fill="#ffffff" text-anchor="middle" font-weight="bold">相似度计算</text>
  
  <!-- 公式 -->
  <rect x="250" y="370" width="400" height="80" rx="8" fill="#16213e" stroke="#0f3460" stroke-width="2"/>
  <text x="450" y="405" font-family="Consolas, monospace" font-size="16" fill="#00d4ff" text-anchor="middle">cos(θ) = A · B / (||A|| × ||B||)</text>
  <text x="450" y="435" font-family="Arial" font-size="12" fill="#888888" text-anchor="middle">余弦相似度：值越接近 1 越相似</text>
  
  <!-- 标题 -->
  <text x="450" y="480" font-family="Arial, sans-serif" font-size="14" fill="#666666" text-anchor="middle">向量数据库技术深度解析</text>
</svg>`;

// 保存 SVG 文件
const outputPath = path.join(__dirname, '..', 'covers', 'vector-db-cover.svg');
const outputDir = path.dirname(outputPath);

if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

fs.writeFileSync(outputPath, svgContent, 'utf8');

console.log('✅ 封面图已生成:', outputPath);
console.log('📐 尺寸：900x500px');
console.log('🎨 主题：向量数据库 - 文本到向量矩阵空间可视化');
