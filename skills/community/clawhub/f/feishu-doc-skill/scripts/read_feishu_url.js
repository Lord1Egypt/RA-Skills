#!/usr/bin/env node

const { extractTokenFromUrl } = require('./lib/token');
const { createReadUrlOutput } = require('./lib/doc-summary');
const { readFeishuDoc } = require('./read_feishu_doc');

async function readFeishuUrl(url) {
  const token = extractTokenFromUrl(url);
  const data = await readFeishuDoc(token);
  return createReadUrlOutput(url, data);
}

async function main() {
  const url = process.argv[2];
  if (!url) {
    console.error('用法: read_feishu_url.js <feishu_url>');
    process.exit(1);
  }

  try {
    const output = await readFeishuUrl(url);
    console.log(JSON.stringify(output, null, 2));
  } catch (error) {
    const message = error.message || String(error);
    if (message.startsWith('用法:')) {
      console.error(message);
      process.exit(1);
    }
    if (message.startsWith('缺少 FEISHU_')) {
      console.error(message);
      process.exit(2);
    }
    if (message.startsWith('读取飞书文档失败:') || message.startsWith('HTTP 请求失败')) {
      console.error(message);
      process.exit(4);
    }
    console.error(`读取飞书链接失败: ${message}`);
    process.exit(3);
  }
}

if (require.main === module) {
  main();
}

module.exports = {
  readFeishuUrl,
};
