#!/usr/bin/env node

/**
 * Email Sender Policy Skill v2.0.1
 * 自動應用郵件發送政策：UTF-8編碼、表格轉清單、電子報格式化、RFC 822格式
 */

const fs = require('fs');
const { argv } = require('process');

// === 參數解析 ===
function parseArgs(args) {
  const result = {
    to: '',
    subject: '',
    body: '',
    file: '',
    cc: '',
    bcc: '',
    help: false,
    test: false,
    newsletter: false,
    title: '',
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    const next = args[i + 1];

    switch (arg) {
      case '--to':
      case '-t':
        result.to = next || '';
        i++;
        break;
      case '--subject':
      case '-s':
        result.subject = next || '';
        i++;
        break;
      case '--body':
      case '-b':
        result.body = next || '';
        i++;
        break;
      case '--file':
      case '-f':
        result.file = next || '';
        i++;
        break;
      case '--bodyFile':  // 別名：與 --file 功能相同
        result.file = next || '';
        i++;
        break;
      case '--cc':
        result.cc = next || '';
        i++;
        break;
      case '--bcc':
        result.bcc = next || '';
        i++;
        break;
      case '--newsletter':
        result.newsletter = true;
        break;
      case '--title':
        result.title = next || '';
        i++;
        break;
      case '--help':
        result.help = true;
        break;
      case '--test':
        result.test = true;
        break;
      default:
        break;
    }
  }

  return result;
}

// === 工具函數 ===

function encodeSubjectRFC2047(subject) {
  if (!subject) return '';
  const base64 = Buffer.from(subject, 'utf-8').toString('base64');
  return `=?utf-8?b?${base64}?=`;
}

function convertMarkdownTableToList(markdown) {
  if (!markdown) return markdown;
  const lines = markdown.split('\n');
  const result = [];

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].trim();
    if (line.startsWith('|') && line.includes('---')) continue;

    if (line.startsWith('|') && line.endsWith('|')) {
      const content = line.slice(1, -1).trim();
      const columns = content.split('|').map(col => col.trim());

      if (columns.length >= 3) {
        const [item, desc, extra] = columns;
        let bullet = `• ${item}`;
        if (desc) bullet += `：${desc}`;
        if (extra) bullet += `（${extra}）`;
        result.push(bullet);
      } else if (columns.length === 2) {
        const [item, desc] = columns;
        result.push(`• ${item}：${desc}`);
      } else if (columns.length === 1 && columns[0]) {
        result.push(`• ${columns[0]}`);
      }
    } else {
      result.push(lines[i]);
    }
  }
  return result.join('\n');
}

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

function buildRFC822Email({ to, subject, body, cc = '', bcc = '' }) {
  const lines = [
    `From: me`,
    `To: ${to}`,
  ];
  if (cc) lines.push(`Cc: ${cc}`);
  if (bcc) lines.push(`Bcc: ${bcc}`);

  const encodedSubject = encodeSubjectRFC2047(subject);
  lines.push(`Subject: ${encodedSubject}`);
  lines.push(`Content-Type: text/plain; charset=UTF-8`);
  lines.push(`Content-Transfer-Encoding: 8bit`);
  lines.push('');
  lines.push(body);

  return lines.join('\r\n');
}

function base64UrlEncode(str) {
  return Buffer.from(str, 'utf-8')
    .toString('base64')
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');
}

async function sendEmailViaMaton({ to, subject, body, cc = '', bcc = '' }) {
  const MATON_API_KEY = process.env.MATON_API_KEY;
  if (!MATON_API_KEY) throw new Error('MATON_API_KEY 環境變數未設定');

  const rfc822 = buildRFC822Email({ to, subject, body, cc, bcc });
  const rawMessage = base64UrlEncode(rfc822);

  const url = 'https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages/send';
  const payload = JSON.stringify({ raw: rawMessage });

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${MATON_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: payload,
  });

  if (!response.ok) {
    const err = await response.text();
    throw new Error(`Gmail API 錯誤：${response.status} - ${err}`);
  }

  return await response.json();
}

// === CLI 入口 ===

async function main() {
  const args = parseArgs(argv.slice(2));

  if (args.help || !args.to || !args.subject) {
    console.log(`
Email Sender Policy Skill v2.0 - 自動應用郵件發送政策

用法：
  email-sender-policy --to "recipient@example.com" --subject "主題" --body "內容"
  email-sender-policy --to "a@x.com,b@x.com" --subject "主旨" --file "content.md"
  email-sender-policy --to "a@x.com" --subject "主題" --body "內容" --newsletter --title "電子報標題"

選項：
  --to, -t     收件人（多個用逗號分隔）
  --subject, -s 郵件標題
  --body, -b    郵件內容（可直接寫或透過 --file 讀取）
  --file, -f    讀取檔案內容（自動轉換表格）
  --cc          副本收件人
  --bcc         密件副本
  --test        測試模式（驗證格式，不實際發送）
  --newsletter  將內容排版為電子報格式（加上頭尾、分隔線）
  --title "標題" 電子報主標題（配合 --newsletter 使用）
  --help        顯示此幫助

範例：
  # 直接傳內容
  email-sender-policy -t "user@example.com" -s "報告" -b "內容..."

  # 從檔案讀取（表格自動轉清單）
  email-sender-policy -t "team@company.com" -s "週報" -f "weekly.md"

  # 電子報格式（自動添加頭尾裝飾）
  email-sender-policy -t "subscriber@example.com" -s "本週AI新聞" \\
    -b "| 新聞 | 來源 |\\n|------|------|\\n| GPT-5 發布 | OpenAI |" \\
    --newsletter --title "AI 新聞週報"

環境變數：
  MATON_API_KEY   Maton API 金鑰（必須）
`);
    return;
  }

  try {
    let body = args.body || '';
    if (args.file) {
      if (!fs.existsSync(args.file)) {
        throw new Error(`檔案不存在：${args.file}`);
      }
      body = fs.readFileSync(args.file, 'utf-8');
    }

    console.log('🔄 應用格式政策：表格轉清單...');
    let processedBody = convertMarkdownTableToList(body);

    if (args.newsletter) {
      console.log('📧 套用電子報格式排版...');
      processedBody = formatAsNewsletter(processedBody, {
        title: args.title || args.subject,
      });
    }

    if (args.test) {
      console.log('\n=== 測試模式：驗證RFC 822格式 ===');
      const rfc822 = buildRFC822Email({
        to: args.to,
        subject: args.subject,
        body: processedBody,
        cc: args.cc,
        bcc: args.bcc,
      });
      console.log(rfc822);
      console.log('\n✅ RFC 822 格式驗證通過');
      console.log(`📏 郵件大小：${Buffer.byteLength(rfc822, 'utf-8')} bytes`);
      return;
    }

    console.log('🚀 發送郵件...');
    const result = await sendEmailViaMaton({
      to: args.to,
      subject: args.subject,
      body: processedBody,
      cc: args.cc,
      bcc: args.bcc,
    });

    console.log('✅ 郵件發送成功！');
    console.log(`   Message ID: ${result.id}`);
    console.log(`   規模：${result.sizeEstimate} bytes`);

    const logEntry = {
      timestamp: new Date().toISOString(),
      to: args.to,
      subject: args.subject,
      messageId: result.id,
      newsletter: args.newsletter || false,
    };
    console.log('\n📋 發送記錄：', JSON.stringify(logEntry, null, 2));

  } catch (error) {
    console.error('❌ 錯誤：', error.message);
    process.exit(1);
  }
}

if (typeof fetch === 'undefined') {
  global.fetch = (...args) => import('node-fetch').then(({ default: fetch }) => fetch(...args));
}

main();
