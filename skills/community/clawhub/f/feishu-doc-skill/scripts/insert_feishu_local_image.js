#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { BASE_URL, parseFeishuResponse } = require('./lib/feishu-api');
const { resolveUserAccessTokenForWrite } = require('./lib/auth');
const { resolveDocToken } = require('./lib/token');

function parseArgs(argv) {
  const args = argv.slice(2);
  const positional = [];
  let caption = '';

  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (arg === '--caption') {
      caption = args[i + 1] || '';
      i += 1;
      continue;
    }
    positional.push(arg);
  }

  if (positional.length < 2) {
    throw new Error('用法: insert_feishu_local_image.js <doc> <image_path> [--caption "说明文字"]');
  }

  return {
    doc: positional[0],
    imagePath: positional[1],
    caption,
  };
}

function guessMimeType(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  return (
    {
      '.png': 'image/png',
      '.jpg': 'image/jpeg',
      '.jpeg': 'image/jpeg',
      '.gif': 'image/gif',
      '.webp': 'image/webp',
      '.bmp': 'image/bmp',
      '.svg': 'image/svg+xml',
    }[ext] || 'application/octet-stream'
  );
}

async function createEmptyImageBlock(accessToken, docToken) {
  const response = await fetch(`${BASE_URL}/docx/v1/documents/${docToken}/blocks/${docToken}/children`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      children: [
        {
          block_type: 27,
          image: {},
        },
      ],
    }),
  });
  const data = await parseFeishuResponse(response, '创建空图片块');
  return data.data.children[0].block_id;
}

async function uploadImageMaterial(accessToken, blockId, imagePath) {
  if (!fs.existsSync(imagePath)) {
    throw new Error(`图片不存在: ${imagePath}`);
  }

  const stat = fs.statSync(imagePath);
  const form = new FormData();
  form.set('file_name', path.basename(imagePath));
  form.set('parent_type', 'docx_image');
  form.set('parent_node', blockId);
  form.set('size', String(stat.size));
  form.set(
    'file',
    new File([fs.readFileSync(imagePath)], path.basename(imagePath), {
      type: guessMimeType(imagePath),
    }),
  );

  const response = await fetch(`${BASE_URL}/drive/v1/medias/upload_all`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${accessToken}`,
    },
    body: form,
  });
  const data = await parseFeishuResponse(response, '上传图片素材');
  return data.data.file_token;
}

async function replaceImage(accessToken, docToken, blockId, fileToken) {
  const response = await fetch(`${BASE_URL}/docx/v1/documents/${docToken}/blocks/${blockId}`, {
    method: 'PATCH',
    headers: {
      Authorization: `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      replace_image: {
        token: fileToken,
      },
    }),
  });
  return parseFeishuResponse(response, '更新图片块素材');
}

async function appendCaption(accessToken, docToken, caption) {
  if (!caption) {
    return null;
  }

  const response = await fetch(`${BASE_URL}/docx/v1/documents/${docToken}/blocks/${docToken}/children`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      children: [
        {
          block_type: 2,
          text: {
            elements: [
              {
                text_run: {
                  content: caption,
                },
              },
            ],
          },
        },
      ],
    }),
  });
  return parseFeishuResponse(response, '插入图片说明');
}

async function insertLocalImage(doc, imagePath, caption = '') {
  const accessToken = resolveUserAccessTokenForWrite();
  const { docToken } = await resolveDocToken(accessToken, doc);
  const resolvedImagePath = path.resolve(imagePath.replace(/^~(?=$|\/|\\)/, process.env.HOME || '~'));

  const blockId = await createEmptyImageBlock(accessToken, docToken);
  const fileToken = await uploadImageMaterial(accessToken, blockId, resolvedImagePath);
  const imageResult = await replaceImage(accessToken, docToken, blockId, fileToken);
  const captionResult = caption ? await appendCaption(accessToken, docToken, caption) : null;

  return {
    doc_token: docToken,
    block_id: blockId,
    image_path: resolvedImagePath,
    file_token: fileToken,
    image_result: imageResult,
    caption_result: captionResult,
  };
}

async function main() {
  try {
    const { doc, imagePath, caption } = parseArgs(process.argv);
    const result = await insertLocalImage(doc, imagePath, caption);
    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    const message = error.message || String(error);
    if (message.startsWith('用法:')) {
      console.error(message);
      process.exit(1);
    }
    if (message.startsWith('缺少 FEISHU_')) {
      console.error(message);
      process.exit(3);
    }
    if (message.startsWith('HTTP 请求失败')) {
      console.error(message);
      process.exit(2);
    }
    console.error(`插入图片失败: ${message}`);
    process.exit(3);
  }
}

if (require.main === module) {
  main();
}

module.exports = {
  parseArgs,
  guessMimeType,
  insertLocalImage,
};
