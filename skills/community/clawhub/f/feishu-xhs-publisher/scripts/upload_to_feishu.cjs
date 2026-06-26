/**
 * XHS Publisher - 上传图片到飞书文档
 * 
 * 用法：
 *   node upload_to_feishu.cjs <output_dir> <doc_title> <summary_markdown_file>
 * 
 * 环境变量（必须）：
 *   FEISHU_APP_ID      飞书应用 AppId
 *   FEISHU_APP_SECRET  飞书应用 AppSecret
 *   FEISHU_OWNER_ID    文档所有者 open_id（ou_xxx）
 * 
 * 也可以直接修改下方 CONFIG 对象中的值。
 */

const Lark = require('@larksuiteoapi/node-sdk');
const fs = require('fs');
const path = require('path');

// ===== 配置区 =====
const CONFIG = {
  appId:     process.env.FEISHU_APP_ID     || 'cli_a9249001d9f8dcc9',
  appSecret: process.env.FEISHU_APP_SECRET || 'IcxmMHOYNVUGWsuI4Ikp2fjtouXEwDUf',
  ownerId:   process.env.FEISHU_OWNER_ID   || 'ou_966010364ecf08ba373bf29bf198a04a',
};
// ==================

const [,, OUTPUT_DIR, DOC_TITLE, SUMMARY_MD_FILE] = process.argv;

if (!OUTPUT_DIR || !DOC_TITLE) {
  console.error('用法: node upload_to_feishu.cjs <output_dir> <doc_title> [summary_md_file]');
  process.exit(1);
}

const client = new Lark.Client({
  appId: CONFIG.appId,
  appSecret: CONFIG.appSecret,
  domain: Lark.Domain.Feishu,
});

async function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

async function uploadImage(docId, imgPath) {
  const buffer = fs.readFileSync(imgPath);
  const imgName = path.basename(imgPath);
  console.log(`  🖼️  ${imgName} (${(buffer.length/1024).toFixed(0)}KB)...`);

  // Step1: 创建空图片块（parent_block_id = docId）
  const insertRes = await client.docx.documentBlockChildren.create({
    path: { document_id: docId, block_id: docId },
    params: { document_revision_id: -1 },
    data: { children: [{ block_type: 27, image: {} }], index: -1 }
  });
  const imageBlockId = insertRes.data.children[0].block_id;

  // Step2: 用 imageBlockId 作为 parent_node 上传图片（关键！）
  const uploadRes = await client.drive.media.uploadAll({
    data: {
      file_name: imgName,
      parent_type: 'docx_image',
      parent_node: imageBlockId,   // ⚠️ 必须是 blockId，不是 docId
      size: buffer.length,
      file: buffer,
    }
  });

  // Step3: patch 图片块填入 token
  await client.docx.documentBlock.patch({
    path: { document_id: docId, block_id: imageBlockId },
    data: { replace_image: { token: uploadRes.file_token } }
  });
}

async function appendMarkdown(docId, markdown) {
  const convertRes = await client.docx.document.convert({
    data: { content_type: 'markdown', content: markdown }
  });
  await client.docx.documentBlockDescendant.create({
    path: { document_id: docId, block_id: docId },
    data: {
      children_id: convertRes.data.first_level_block_ids,
      descendants: convertRes.data.blocks,
      index: -1
    }
  });
}

async function main() {
  // 1. 创建文档
  console.log(`📄 创建文档：${DOC_TITLE}`);
  const createRes = await client.docx.document.create({
    data: { title: DOC_TITLE, folder_token: '' }
  });
  const docId = createRes.data.document.document_id;
  console.log(`✅ 文档 ID: ${docId}`);

  // 2. 写入简要头部
  const headerMd = `## 图片预览`;
  await appendMarkdown(docId, headerMd);
  await sleep(300);

  // 3. 逐张上传图片（按文件名排序）
  const images = fs.readdirSync(OUTPUT_DIR)
    .filter(f => /\.(png|jpg|jpeg)$/i.test(f))
    .sort();

  console.log(`\n📸 上传 ${images.length} 张图片...`);
  for (const imgName of images) {
    await uploadImage(docId, path.join(OUTPUT_DIR, imgName));
    await sleep(300);
  }

  // 4. 追加正文摘要（如果提供了 md 文件）
  if (SUMMARY_MD_FILE && fs.existsSync(SUMMARY_MD_FILE)) {
    console.log('\n📝 追加正文摘要...');
    const summaryMd = fs.readFileSync(SUMMARY_MD_FILE, 'utf8');
    await appendMarkdown(docId, summaryMd);
    console.log('✅ 摘要写入完成');
  }

  const docUrl = `https://my.feishu.cn/docx/${docId}`;
  console.log(`\n🎉 完成！`);
  console.log(`📎 ${docUrl}`);
  return docUrl;
}

main().catch(e => {
  console.error('❌', e.message);
  if (e.response?.data) console.error(JSON.stringify(e.response.data).slice(0, 400));
  process.exit(1);
});
