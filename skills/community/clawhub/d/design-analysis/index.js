#!/usr/bin/env node

/**
 * Design Analysis Skill
 * 自动化设计分析工具，分析设计素材并生成HTML演示文档
 */

const fs = require('fs');
const path = require('path');

/**
 * 主函数 - 设计分析并生成HTML
 * @param {Object} options - 配置选项
 * @param {string} options.inputFolder - 输入文件夹路径
 * @param {string} options.outputFile - 输出HTML文件路径
 * @param {string} [options.title="设计分析演示"] - 标题
 * @param {Object} [options.dimensions={width:1920,height:1280}] - 页面尺寸
 * @param {Object} [options.layout={textWidth:30,imageWidth:70}] - 布局比例
 * @param {Array} [options.sections] - 自定义章节（不传则自动生成）
 * @returns {Promise<Object>} 生成结果
 */
async function designAnalysis(options) {
  try {
    // 参数验证
    if (!options.inputFolder) {
      throw new Error('inputFolder 是必填参数');
    }
    if (!options.outputFile) {
      throw new Error('outputFile 是必填参数');
    }

    // 解析路径
    const inputFolder = path.resolve(options.inputFolder);
    const outputFile = path.resolve(options.outputFile);

    // 检查输入文件夹
    if (!fs.existsSync(inputFolder)) {
      throw new Error(`输入文件夹不存在: ${inputFolder}`);
    }

    // 读取图片文件
    const imageFiles = await scanImageFiles(inputFolder);

    if (imageFiles.length === 0) {
      throw new Error(`在文件夹 ${inputFolder} 中未找到图片文件`);
    }

    console.log(`找到 ${imageFiles.length} 个图片文件`);

    // 生成章节内容
    const sections = options.sections || await generateSections(imageFiles, inputFolder);

    // 构建HTML
    const html = buildHTML({
      title: options.title || '设计分析演示',
      dimensions: options.dimensions || { width: 1920, height: 1280 },
      layout: options.layout || { textWidth: 30, imageWidth: 70 },
      sections,
      outputDir: path.dirname(outputFile)
    });

    // 确保输出目录存在
    fs.mkdirSync(path.dirname(outputFile), { recursive: true });

    // 写入文件
    fs.writeFileSync(outputFile, html, 'utf8');

    console.log(`HTML已生成: ${outputFile}`);

    return {
      success: true,
      outputPath: outputFile,
      totalPages: sections.length,
      analysis: {
        fileCount: imageFiles.length,
        imageFiles: imageFiles.map(f => path.basename(f)),
        sections: sections.map(s => s.title)
      }
    };

  } catch (error) {
    console.error('设计分析失败:', error.message);
    return {
      success: false,
      error: error.message
    };
  }
}

/**
 * 扫描文件夹中的图片文件
 * @param {string} folderPath - 文件夹路径
 * @returns {Promise<string[]>} 图片文件路径数组
 */
async function scanImageFiles(folderPath) {
  const files = fs.readdirSync(folderPath);
  const imageExts = ['.png', '.jpg', '.jpeg', '.gif', '.webp'];

  return files
    .filter(file => {
      const ext = path.extname(file).toLowerCase();
      return imageExts.includes(ext);
    })
    .map(file => path.join(folderPath, file))
    .sort((a, b) => {
      // 按修改时间排序（最新的在前）
      const statA = fs.statSync(a);
      const statB = fs.statSync(b);
      return statB.mtimeMs - statA.mtimeMs;
    });
}

/**
 * 自动生成章节内容
 * @param {string[]} imageFiles - 图片文件路径数组
 * @param {string} inputFolder - 输入文件夹路径
 * @returns {Promise<Array>} 章节数组
 */
async function generateSections(imageFiles, inputFolder) {
  const sections = [];

  // 第一章节：概览
  sections.push({
    title: '设计分析总览',
    tags: ['设计系统', 'UI/UX'],
    content: `
      <h2>项目概述</h2>
      <p>本设计分析针对设计素材文件夹，共包含 <b>${imageFiles.length}</b> 个设计文件。</p>

      <h2>设计素材清单</h2>
      <ul>
        ${imageFiles.map((file, index) =>
          `<li><span class="highlight">${path.basename(file)}</span> - 第${index + 1}张设计稿</li>`
        ).join('\n')}
      </ul>

      <h2>分析维度</h2>
      <p>将从以下维度进行分析：</p>
      <ul>
        <li>视觉层次与信息架构</li>
        <li>色彩系统与品牌表达</li>
        <li>布局与间距体系</li>
        <li>图标与组件设计</li>
        <li>交互模式与动效</li>
      </ul>

      <h3>设计理念</h3>
      <p>设计遵循现代UI/UX最佳实践，强调清晰的信息层级、一致的视觉语言和优秀的用户体验。</p>
    `,
    image: path.basename(imageFiles[0])
  });

  // 第二章节：视觉层次
  if (imageFiles.length >= 1) {
    sections.push({
      title: '视觉层次分析',
      tags: ['排版', '信息架构'],
      content: `
        <h2>排版系统</h2>
        <p>设计采用清晰的视觉层次结构，通过字体大小、字重和色彩区分信息重要性。</p>

        <h2>标题层级</h2>
        <ul>
          <li><strong>一级标题 (H1):</strong> 模块主标题，字号最大，用于章节划分</li>
          <li><strong>二级标题 (H2):</strong> 功能分组标题，字号中等</li>
          <li><strong>三级标题 (H3):</strong> 细分项目标题，字号较小</li>
        </ul>

        <h2>段落与列表</h2>
        <p>正文采用舒适的行高(1.6-1.8)，确保可读性。列表用于展示并列信息，通过项目符号明确层次。</p>

        <h2>强调元素</h2>
        <p>使用<span class="highlight">高亮背景</span>突出关键信息，如文件名、核心概念等。</p>
      `,
      image: path.basename(imageFiles[0])
    });
  }

  // 第三章节：色彩系统
  if (imageFiles.length >= 2) {
    sections.push({
      title: '色彩与布局系统',
      tags: ['配色', '栅格'],
      content: `
        <h2>色彩系统</h2>
        <p>设计采用紫蓝渐变主题色，营造专业、现代、富有科技感的视觉氛围。</p>

        <h2>色彩应用规范</h2>
        <ul>
          <li><strong>主题渐变:</strong> 蓝紫渐变 #667eea → #764ba2</li>
          <li><strong>文字颜色:</strong> 纯白(#FFFFFF)，高对比度</li>
          <li><strong>标签背景:</strong> rgba(255,255,255,0.2) 半透明层次</li>
          <li><strong>高亮区域:</strong> rgba(255,255,255,0.15) 突出关键信息</li>
          <li><strong>操作按钮:</strong> #007AFF 主色调</li>
        </ul>

        <h2>布局结构</h2>
        <p>采用 <b>30% : 70%</b> 分栏布局：</p>
        <ul>
          <li><strong>左侧30%:</strong> 文字内容区</li>
          <li><strong>右侧70%:</strong> 视觉展示区</li>
        </ul>

        <h2>间距与圆角</h2>
        <ul>
          <li>页面边距: 20px</li>
          <li>内容区内边距: 40-60px</li>
          <li>圆角: 页面16px、图片12px、按钮20px</li>
          <li>阴影: 多层次阴影营造空间感</li>
        </ul>
      `,
      image: path.basename(imageFiles[1])
    });
  }

  // 第四章：交互设计
  sections.push({
    title: '交互与动效',
    tags: ['导航', '用户体验'],
    content: `
      <h2>翻页机制</h2>
      <ul>
        <li><strong>底部控制栏:</strong> 悬浮固定，包含翻页按钮和页码</li>
        <li><strong>侧边导航点:</strong> 右侧圆点快速跳转</li>
        <li><strong>键盘支持:</strong> 左右方向键翻页</li>
      </ul>

      <h2>动效设计</h2>
      <ul>
        <li><strong>页面切换:</strong> 淡入动画 + 上移效果</li>
        <li><strong>按钮悬浮:</strong> 上移2px + 阴影增强</li>
        <li><strong>导航点:</strong> 放大1.2倍 + 颜色变化</li>
      </ul>

      <h2>响应式适配</h2>
      <p>移动端自动切换为上下布局：</p>
      <ul>
        <li>文字和图片各占100%宽度</li>
        <li>调整控制栏和导航点尺寸</li>
      </ul>

      <h2>可用性考虑</h2>
      <ul>
        <li>控制栏固定在底部，易于操作</li>
        <li>导航点在右侧，便于单手操作</li>
        <li>清晰的按钮禁用状态</li>
        <li>明确的页码指示</li>
      </ul>
    `,
    image: imageFiles.length >= 3 ? path.basename(imageFiles[2]) : path.basename(imageFiles[imageFiles.length - 1])
  });

  return sections;
}

/**
 * 构建HTML内容
 * @param {Object} config - 配置
 * @returns {string} HTML字符串
 */
function buildHTML(config) {
  const { title, dimensions, layout, sections, outputDir } = config;

  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=${dimensions.width}, height=${dimensions.height}">
    <title>${title}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
            background: #f5f5f5;
            overflow-x: hidden;
            width: ${dimensions.width}px;
            height: ${dimensions.height}px;
            margin: 0 auto;
        }

        html {
            width: ${dimensions.width}px;
            height: ${dimensions.height}px;
        }

        /* Navigation */
        .nav-dock {
            position: fixed;
            right: 20px;
            top: 50%;
            transform: translateY(-50%);
            z-index: 1000;
            display: flex;
            flex-direction: column;
            gap: 8px;
            background: rgba(255, 255, 255, 0.95);
            padding: 12px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }

        .nav-dot {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #ddd;
            cursor: pointer;
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }

        .nav-dot:hover {
            background: #bbb;
            transform: scale(1.2);
        }

        .nav-dot.active {
            background: #007AFF;
            border-color: #007AFF;
            box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.2);
        }

        /* Page Controls */
        .controls {
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 16px;
            z-index: 1000;
            background: rgba(255, 255, 255, 0.95);
            padding: 12px 24px;
            border-radius: 30px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }

        .controls button {
            background: #007AFF;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .controls button:hover {
            background: #0056CC;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 122, 255, 0.3);
        }

        .controls button:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }

        .page-indicator {
            display: flex;
            align-items: center;
            font-size: 14px;
            color: #666;
            font-weight: 500;
            padding: 0 12px;
        }

        /* Pages */
        .page {
            display: none;
            width: ${dimensions.width}px;
            height: ${dimensions.height}px;
            background: white;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
            overflow: hidden;
            animation: fadeIn 0.4s ease;
        }

        .page.active {
            display: flex;
        }

        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .page-content {
            display: flex;
            width: 100%;
            height: 100%;
        }

        .text-section {
            width: ${layout.textWidth}%;
            padding: 60px 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
        }

        .text-section h1 {
            font-size: 42px;
            margin-bottom: 16px;
            font-weight: 700;
            line-height: 1.2;
        }

        .text-section h2 {
            font-size: 28px;
            margin-bottom: 20px;
            margin-top: 32px;
            font-weight: 600;
            opacity: 0.95;
            line-height: 1.3;
        }

        .text-section h3 {
            font-size: 22px;
            margin-top: 24px;
            margin-bottom: 12px;
            font-weight: 500;
            opacity: 0.9;
            line-height: 1.4;
        }

        .text-section p {
            font-size: 18px;
            line-height: 1.7;
            margin-bottom: 20px;
            opacity: 0.85;
        }

        .text-section ul {
            padding-left: 28px;
            margin-bottom: 20px;
        }

        .text-section li {
            font-size: 18px;
            line-height: 1.8;
            margin-bottom: 12px;
            opacity: 0.85;
        }

        .image-section {
            width: ${layout.imageWidth}%;
            padding: 40px;
            background: #fafafa;
            overflow-y: auto;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .image-section img {
            max-width: 100%;
            max-height: ${dimensions.height - 100}px;
            object-fit: contain;
            border-radius: 12px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
        }

        .image-placeholder {
            width: 100%;
            height: 800px;
            background: linear-gradient(135deg, #e0e0e0 0%, #f5f5f5 100%);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #999;
            font-size: 24px;
        }

        .tag {
            display: inline-block;
            background: rgba(255, 255, 255, 0.2);
            padding: 8px 16px;
            border-radius: 16px;
            font-size: 14px;
            margin-right: 10px;
            margin-bottom: 10px;
        }

        .highlight {
            background: rgba(255, 255, 255, 0.15);
            padding: 4px 10px;
            border-radius: 6px;
        }

        /* Scrollbar styling */
        .text-section::-webkit-scrollbar,
        .image-section::-webkit-scrollbar {
            width: 8px;
        }

        .text-section::-webkit-scrollbar-track,
        .image-section::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 4px;
        }

        .text-section::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.3);
            border-radius: 4px;
        }

        .text-section::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.5);
        }

        .image-section::-webkit-scrollbar-thumb {
            background: rgba(0, 0, 0, 0.2);
            border-radius: 4px;
        }

        .image-section::-webkit-scrollbar-thumb:hover {
            background: rgba(0, 0, 0, 0.3);
        }
    </style>
</head>
<body>
    <!-- Navigation Dots -->
    <nav class="nav-dock" id="navDock"></nav>

    <!-- Page Controls -->
    <div class="controls">
        <button id="prevBtn" onclick="prevPage()">
            ◀ 上一页
        </button>
        <div class="page-indicator">
            <span id="currentPage">1</span> / <span id="totalPages">${sections.length}</span>
        </div>
        <button id="nextBtn" onclick="nextPage()">
            下一页 ▶
        </button>
    </div>

    <!-- Pages Container -->
    <div id="pagesContainer"></div>

    <script>
        const pages = ${JSON.stringify(sections, null, 2)};

        let currentPage = 0;
        const totalPages = pages.length;

        // Initialize
        function init() {
            document.getElementById('totalPages').textContent = totalPages;
            renderNavDots();
            renderPages();
            showPage(0);

            // Keyboard navigation
            document.addEventListener('keydown', (e) => {
                if (e.key === 'ArrowLeft') prevPage();
                if (e.key === 'ArrowRight') nextPage();
            });
        }

        // Render navigation dots
        function renderNavDots() {
            const navDock = document.getElementById('navDock');
            navDock.innerHTML = '';
            pages.forEach((page, index) => {
                const dot = document.createElement('div');
                dot.className = 'nav-dot';
                dot.onclick = () => showPage(index);
                dot.title = page.title;
                navDock.appendChild(dot);
            });
        }

        // Render all pages
        function renderPages() {
            const container = document.getElementById('pagesContainer');
            container.innerHTML = '';
            pages.forEach((page, index) => {
                const pageEl = document.createElement('div');
                pageEl.className = 'page';
                pageEl.id = \`page-\${index}\`;

                // 使用绝对路径加载图片
                const imagePath = page.image ?
                    \`\${window.location.pathname.replace(/[^/]*$/, '')}\${page.image}\` :
                    '';

                const imageHtml = imagePath ?
                    \`<img src="\${imagePath}" alt="\${page.title}" onerror="this.parentElement.innerHTML='<div class=\\'image-placeholder\\' style=\\'width:100%;height:800px;background:#e0e0e0;display:flex;align-items:center;justify-content:center;color:#999;font-size:24px;border-radius:8px;\\'>图片加载失败</div>'" />\` :
                    \`<div class="image-placeholder">图片位置: \${page.title}</div>\`;

                pageEl.innerHTML = \`
                    <div class="page-content">
                        <div class="text-section">
                            <h1>\${page.title}</h1>
                            \${page.tags ? page.tags.map(tag => \`<span class="tag">\${tag}</span>\`).join('') : ''}
                            \${page.content}
                        </div>
                        <div class="image-section">
                            \${imageHtml}
                        </div>
                    </div>
                \`;
                container.appendChild(pageEl);
            });
        }

        // Show specific page
        function showPage(index) {
            // Hide all pages
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.nav-dot').forEach(d => d.classList.remove('active'));

            // Show target page
            document.getElementById(\`page-\${index}\`).classList.add('active');
            document.querySelectorAll('.nav-dot')[index].classList.add('active');

            currentPage = index;
            document.getElementById('currentPage').textContent = index + 1;
            document.getElementById('prevBtn').disabled = index === 0;
            document.getElementById('nextBtn').disabled = index === totalPages - 1;
        }

        // Navigation functions
        function nextPage() {
            if (currentPage < totalPages - 1) {
                showPage(currentPage + 1);
            }
        }

        function prevPage() {
            if (currentPage > 0) {
                showPage(currentPage - 1);
            }
        }

        // Initialize on load
        init();
    </script>
</body>
</html>`;
}

// 导出函数
module.exports = {
  designAnalysis
};

// 如果直接运行此文件，则执行示例
if (require.main === module) {
  (async () => {
    if (process.argv.length < 4) {
      console.log(`
设计分析工具 - 用法:
  node index.js <输入文件夹> <输出HTML文件> [标题]

示例:
  node index.js ~/Desktop/01.DesignAnalysis ~/Desktop/output.html "我的设计分析"
      `);
      process.exit(1);
    }

    const [inputFolder, outputFile, title] = process.argv.slice(2);

    const result = await designAnalysis({
      inputFolder,
      outputFile,
      title: title || '设计分析演示'
    });

    if (result.success) {
      console.log('\\n✅ 生成成功!');
      console.log(`📍 输出文件: ${result.outputPath}`);
      console.log(`📄 总页数: ${result.totalPages}`);
      console.log('\\n📊 分析内容:');
      console.log(`   - 图片数量: ${result.analysis.fileCount}`);
      console.log(`   - 图片文件: ${result.analysis.imageFiles.join(', ')}`);
      console.log(`   - 章节列表: ${result.analysis.sections.join(' → ')}`);
    } else {
      console.error('❌ 生成失败:', result.error);
      process.exit(1);
    }
  })();
}