import * as Lark from '@larksuiteoapi/node-sdk';
import fs from 'node:fs';
import os from 'node:os';

function resolve(p) { return p.replace(/^~/, os.homedir()); }

const APP_ID = process.env.FEISHU_APP_ID || '';
const APP_SECRET_PATH = resolve(process.env.FEISHU_APP_SECRET_PATH || '~/.openclaw/secrets/feishu_app_secret');
const RECEIVE_ID = process.argv[2];
const FILE_PATH = process.argv[3];
const FILE_TYPE = process.argv[4] || 'stream';
const DURATION_MS = process.argv[5] || '';

if (!APP_ID) throw new Error('FEISHU_APP_ID missing');
if (!RECEIVE_ID || !FILE_PATH) throw new Error('usage: node send-file.mjs <receive_id> <file_path> [file_type] [duration_ms]');

const APP_SECRET = fs.readFileSync(APP_SECRET_PATH, 'utf8').trim();
const client = new Lark.Client({
  appId: APP_ID,
  appSecret: APP_SECRET,
  domain: Lark.Domain.Feishu,
  appType: Lark.AppType.SelfBuild,
});

const fileStream = fs.createReadStream(FILE_PATH);
const fileName = FILE_PATH.split('/').pop();
const data = {
  file_type: FILE_TYPE,
  file_name: fileName,
  file: fileStream,
};
if (DURATION_MS) data.duration = Number(DURATION_MS);

const uploadRes = await client.im.v1.file.create({ data });
console.log('UPLOAD_RES', JSON.stringify(uploadRes, null, 2));
const fileKey = uploadRes.data?.file_key || uploadRes.file_key;
if (!fileKey) throw new Error('no file_key returned');

const sendRes = await client.im.v1.message.create({
  params: { receive_id_type: 'open_id' },
  data: {
    receive_id: RECEIVE_ID,
    msg_type: 'media',
    content: JSON.stringify({ file_key: fileKey }),
  },
});

console.log(JSON.stringify({ upload: uploadRes, send: sendRes }, null, 2));
