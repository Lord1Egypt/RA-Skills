import * as Lark from '@larksuiteoapi/node-sdk';
import fs from 'node:fs';
import os from 'node:os';

function resolve(p) { return p.replace(/^~/, os.homedir()); }

const APP_ID = process.env.FEISHU_APP_ID || '';
const APP_SECRET_PATH = resolve(process.env.FEISHU_APP_SECRET_PATH || '~/.openclaw/secrets/feishu_app_secret');
const RECEIVE_ID = process.argv[2];
const IMAGE_PATH = process.argv[3];

if (!APP_ID) throw new Error('FEISHU_APP_ID missing');
if (!RECEIVE_ID) throw new Error('usage: node send-image.mjs <receive_id> <image_path>');
if (!IMAGE_PATH) throw new Error('usage: node send-image.mjs <receive_id> <image_path>');

const APP_SECRET = fs.readFileSync(APP_SECRET_PATH, 'utf8').trim();
const client = new Lark.Client({
  appId: APP_ID,
  appSecret: APP_SECRET,
  domain: Lark.Domain.Feishu,
  appType: Lark.AppType.SelfBuild,
});

const fileStream = fs.createReadStream(IMAGE_PATH);
const uploadRes = await client.im.v1.image.create({
  data: {
    image_type: 'message',
    image: fileStream,
  },
});
console.log('UPLOAD_RES', JSON.stringify(uploadRes, null, 2));
if ((uploadRes.code ?? uploadRes?.data?.code ?? 0) !== 0) {
  throw new Error(`upload failed: ${uploadRes.msg || uploadRes?.data?.msg || JSON.stringify(uploadRes)}`);
}

const imageKey = uploadRes.data?.image_key || uploadRes.image_key;
if (!imageKey) throw new Error('no image_key returned');

const sendRes = await client.im.v1.message.create({
  params: { receive_id_type: 'open_id' },
  data: {
    receive_id: RECEIVE_ID,
    msg_type: 'image',
    content: JSON.stringify({ image_key: imageKey }),
  },
});

console.log(JSON.stringify({ upload: uploadRes, send: sendRes }, null, 2));
