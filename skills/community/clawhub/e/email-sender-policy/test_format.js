const { execSync } = require('child_process');

// 印出 formatAsNewsletter 的測試
const content = `# AI 新聞週報

• 新聞標題：來源（日期）
• GPT-5 發布：OpenAI（2026-03-15）

## 市場反應
- GPT-5 上线首日突破 100 萬用戶
`;

function formatAsNewsletter(content, options = {}) {
  const {
    title = '',
    issueDate = new Date().toLocaleDateString('zh-TW', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    }),
    editor = 'Shuttle AI 蝦蝦 🦐',
    footer = '感謝您的閱讀！如有任何問題，請回信告知。',
    includeHeader = true,
    includeFooter = true
  } = options;

  let formatted = '';

  if (includeHeader) {
    formatted += `📧 **${title}**\n`;
    formatted += `發行日期：${issueDate}\n`;
    formatted += `編輯：${editor}\n`;
    formatted += '\n---\n\n';
  }

  formatted += content + '\n\n';

  if (includeFooter) {
    formatted += '---\n\n';
    formatted += footer + '\n';
  }

  return formatted;
}

console.log(formatAsNewsletter(content, { title: '🤖 AI 新聞精選｜2026年3月第2週' }));
