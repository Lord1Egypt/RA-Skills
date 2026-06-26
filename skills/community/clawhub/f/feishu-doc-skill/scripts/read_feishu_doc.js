#!/usr/bin/env node

const { resolveReadAccessToken } = require('./lib/auth');
const { requestFeishuJson } = require('./lib/feishu-api');
const { looksLikeWikiToken, resolveWikiNode } = require('./lib/token');

async function getDocumentMetadata(accessToken, docToken) {
  return requestFeishuJson(`/docx/v1/documents/${docToken}`, {
    action: '获取文档元信息',
    headers: { Authorization: `Bearer ${accessToken}` },
  });
}

async function getDocumentBlocks(accessToken, docToken, pageSize = 500) {
  return requestFeishuJson(`/docx/v1/documents/${docToken}/blocks`, {
    action: '获取文档块',
    headers: { Authorization: `Bearer ${accessToken}` },
    query: { page_size: pageSize },
  });
}

async function readFeishuDoc(sourceToken) {
  const { accessToken, tokenSource } = await resolveReadAccessToken();
  let wikiNode = null;
  let docToken = sourceToken;

  if (looksLikeWikiToken(sourceToken)) {
    try {
      wikiNode = await resolveWikiNode(accessToken, sourceToken);
      docToken = wikiNode.data.node.obj_token;
    } catch (error) {
      docToken = sourceToken;
    }
  }

  const metadata = await getDocumentMetadata(accessToken, docToken);
  const blocks = await getDocumentBlocks(accessToken, docToken);

  return {
    token_source: tokenSource,
    input_token: sourceToken,
    resolved_wiki_node: wikiNode,
    metadata,
    blocks,
  };
}

async function main() {
  const sourceToken = process.argv[2];
  if (!sourceToken) {
    console.error('用法: read_feishu_doc.js <doc_or_wiki_token>');
    process.exit(1);
  }

  try {
    const data = await readFeishuDoc(sourceToken);
    console.log(JSON.stringify(data, null, 2));
  } catch (error) {
    if (String(error.message || '').startsWith('缺少 FEISHU_')) {
      console.error(error.message);
      process.exit(2);
    }
    if (String(error.message || '').startsWith('HTTP 请求失败')) {
      console.error(error.message);
      process.exit(3);
    }
    console.error(`读取飞书文档失败: ${error.message}`);
    process.exit(4);
  }
}

if (require.main === module) {
  main();
}

module.exports = {
  readFeishuDoc,
};
