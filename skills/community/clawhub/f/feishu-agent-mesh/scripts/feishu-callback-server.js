// Minimal Feishu callback handler.
// Requires: npm i express body-parser node-fetch crypto

import express from 'express';
import bodyParser from 'body-parser';
import crypto from 'crypto';
import fetch from 'node-fetch';

const {
  APP_ID,
  APP_SECRET,
  ENCRYPT_KEY,
  VERIFICATION_TOKEN,
  BITABLE_APP_TOKEN,
  BITABLE_TABLE_ID,
  LOG_FIELDS_CHAT = 'chat_id',
  LOG_FIELDS_TASK = 'task_id',
  LOG_FIELDS_ACTOR = 'actor',
  LOG_FIELDS_TARGET = 'target',
  LOG_FIELDS_ACTION = 'action',
  LOG_FIELDS_CONTENT = 'content',
  LOG_FIELDS_TS = 'timestamp',
  LOG_FIELDS_STATUS = 'status'
} = process.env;

let tenantTokenCache = { token: null, expire: 0 };

async function getTenantToken() {
  const now = Date.now();
  if (tenantTokenCache.token && now < tenantTokenCache.expire) {
    return tenantTokenCache.token;
  }
  const resp = await fetch('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ app_id: APP_ID, app_secret: APP_SECRET })
  });
  const data = await resp.json();
  if (data.code !== 0) throw new Error(`get tenant token failed: ${resp.status} ${data.msg}`);
  tenantTokenCache = { token: data.tenant_access_token, expire: now + (data.expire * 1000 - 60 * 1000) };
  return tenantTokenCache.token;
}

function decryptEvent(encryptText) {
  const key = Buffer.from(ENCRYPT_KEY, 'utf8');
  const iv = key.slice(0, 16);
  const decipher = crypto.createDecipheriv('aes-256-cbc', key, iv);
  decipher.setAutoPadding(true);
  let decoded = decipher.update(encryptText, 'base64', 'utf8');
  decoded += decipher.final('utf8');
  return JSON.parse(decoded);
}

async function appendLog(record) {
  const token = await getTenantToken();
  await fetch(`https://open.feishu.cn/open-apis/bitable/v1/apps/${BITABLE_APP_TOKEN}/tables/${BITABLE_TABLE_ID}/records`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ records: [{ fields: record }] })
  });
}

const app = express();
app.use(bodyParser.json({ type: '*/*' }));

app.post('/feishu/callback', async (req, res) => {
  try {
    const raw = req.body;
    if (raw.type === 'url_verification') {
      return res.json({ challenge: raw.challenge });
    }

    let eventBody = raw;
    if (raw.encrypt) {
      eventBody = decryptEvent(raw.encrypt);
    }
    if (eventBody.token !== VERIFICATION_TOKEN) {
      return res.status(403).end('invalid token');
    }

    const event = eventBody.event || {};
    if (event.type === 'message') {
      const openId = event.sender?.sender_id?.open_id || '';
      const chatId = event.chat_id || '';
      const msgId = event.message?.message_id || '';
      const msgType = event.message?.message_type || '';
      const msgContent = event.message?.content || '';
      const ts = event.message?.create_time || Date.now();
      const record = {
        [LOG_FIELDS_CHAT]: chatId,
        [LOG_FIELDS_TASK]: msgId,
        [LOG_FIELDS_ACTOR]: openId,
        [LOG_FIELDS_TARGET]: eventBody.header?.event_id || '',
        [LOG_FIELDS_ACTION]: msgType,
        [LOG_FIELDS_CONTENT]: msgContent,
        [LOG_FIELDS_TS]: new Date(Number(ts)).toISOString(),
        [LOG_FIELDS_STATUS]: 'received'
      };
      await appendLog(record);
    }

    res.json({ code: 0, msg: 'ok' });
  } catch (err) {
    console.error(err);
    res.status(500).send('error');
  }
});

const port = process.env.PORT || 8787;
app.listen(port, () => {
  console.log(`Feishu callback listening on ${port}`);
});
```} Comment we added? yes. Need to ensure node-fetch import style? Since Node 18? we can mention to run with `node --experimental-modules`? But sample is enough. We included sample in skill earlier? but now TOT ensures zipped? Good enough though we need to mention to run with `