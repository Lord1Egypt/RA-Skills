#!/usr/bin/env node

const { extractTokenFromUrl } = require('./lib/token');

function main() {
  const url = process.argv[2];
  if (!url) {
    console.error('用法: extract_feishu_doc_id.js <feishu_url>');
    process.exit(1);
  }

  try {
    console.log(extractTokenFromUrl(url));
  } catch (error) {
    console.error(error.message || String(error));
    process.exit(2);
  }
}

if (require.main === module) {
  main();
}
