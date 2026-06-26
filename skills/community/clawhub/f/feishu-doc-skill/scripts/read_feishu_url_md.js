#!/usr/bin/env node

const { renderMarkdownDocument } = require('./lib/doc-summary');
const { readFeishuUrl } = require('./read_feishu_url');

async function readFeishuUrlMarkdown(url) {
  const data = await readFeishuUrl(url);
  return renderMarkdownDocument(data);
}

async function main() {
  const url = process.argv[2];
  if (!url) {
    console.error('用法: read_feishu_url_md.js <feishu_url>');
    process.exit(1);
  }

  try {
    const markdown = await readFeishuUrlMarkdown(url);
    console.log(markdown);
  } catch (error) {
    const message = error.message || String(error);
    if (message.startsWith('缺少 FEISHU_')) {
      console.error(message);
      process.exit(2);
    }
    console.error(`生成 Markdown 失败: ${message}`);
    process.exit(3);
  }
}

if (require.main === module) {
  main();
}

module.exports = {
  readFeishuUrlMarkdown,
};
