#!/usr/bin/env node

/**
 * 测试 contentBlocks 逻辑的简化版本
 * 使用模拟的 HTML 结构来验证图片和文本的交替记录
 */

const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  
  // 设置模拟的 HTML 内容
  await page.setContent(`
    <!DOCTYPE html>
    <html>
    <body>
      <div data-testid="twitterArticleRichTextView">
        <p>这是第一段文本。</p>
        <p><strong>这是粗体文本。</strong></p>
        <div>
          <img src="https://pbs.twimg.com/media/image1.jpg" />
        </div>
        <p>这是图片后的文本。</p>
        <div>
          <img src="https://pbs.twimg.com/media/image2.jpg" />
        </div>
        <p>这是第二张图片后的文本。</p>
        <ul>
          <li>列表项 1</li>
          <li>列表项 2</li>
        </ul>
        <div>
          <img src="https://pbs.twimg.com/media/image3.jpg" />
        </div>
        <p>最后一段文本。</p>
      </div>
    </body>
    </html>
  `);

  // 提取 contentBlocks
  const result = await page.evaluate(() => {
    const contentDiv = document.querySelector('[data-testid="twitterArticleRichTextView"]');
    if (!contentDiv) return null;

    const contentBlocks = [];
    let currentText = '';

    function flushText() {
      if (currentText.trim()) {
        contentBlocks.push({
          type: 'text',
          content: currentText.trim()
        });
        currentText = '';
      }
    }

    function processNode(node, inBold = false) {
      if (node.nodeType === Node.TEXT_NODE) {
        currentText += node.textContent;
        return;
      }

      if (node.nodeType === Node.ELEMENT_NODE) {
        const tag = node.tagName.toLowerCase();
        const style = node.getAttribute('style') || '';
        const isBold = style.includes('font-weight: bold') || style.includes('font-weight:bold');

        switch (tag) {
          case 'img':
            const imgSrc = node.getAttribute('src') || node.src;
            if (imgSrc && imgSrc.includes('pbs.twimg.com/media')) {
              flushText();
              const cleanUrl = imgSrc.split('?')[0] + '?format=jpg&name=large';
              contentBlocks.push({
                type: 'image',
                url: cleanUrl
              });
            }
            return;
          
          case 'strong':
          case 'b':
            currentText += '**';
            Array.from(node.childNodes).forEach(child => processNode(child, true));
            currentText += '**';
            return;
          
          case 'p':
          case 'div':
            if (isBold && !inBold) {
              currentText += '**';
              Array.from(node.childNodes).forEach(child => processNode(child, true));
              currentText += '**\n';
            } else {
              Array.from(node.childNodes).forEach(child => processNode(child, inBold || isBold));
              currentText += '\n';
            }
            return;
          
          case 'li':
            currentText += '- ';
            Array.from(node.childNodes).forEach(child => processNode(child, inBold));
            currentText += '\n';
            return;
          
          case 'ul':
          case 'ol':
            currentText += '\n';
            Array.from(node.childNodes).forEach(child => processNode(child, inBold));
            return;
          
          default:
            Array.from(node.childNodes).forEach(child => processNode(child, inBold));
            return;
        }
      }
    }

    processNode(contentDiv);
    flushText();

    return { contentBlocks };
  });

  await browser.close();

  console.log(JSON.stringify(result, null, 2));
})();
