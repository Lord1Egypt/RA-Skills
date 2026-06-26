// export_nodes_raw.js — 导出白板全部节点（raw）
// 用法：node skills/feishu-whiteboard-extract/export_nodes_raw.js <whiteboard_id>

const fs = require('fs');
const os = require('os');
const path = require('path');
const lark = require('@larksuiteoapi/node-sdk');

function parseOpenClawConfig(configPath) {
  const raw = fs.readFileSync(configPath, 'utf8');
  try {
    return JSON.parse(raw);
  } catch (jsonErr) {
    let json5;
    try {
      json5 = require('json5');
    } catch (requireErr) {
      throw new Error(
        `Failed to parse ${configPath} as JSON. The file may be JSON5, but dependency "json5" is not installed.`
      );
    }
    return json5.parse(raw);
  }
}

function loadCredentials() {
  const envAppId = process.env.FEISHU_APP_ID;
  const envAppSecret = process.env.FEISHU_APP_SECRET;
  if (envAppId && envAppSecret) return { appId: envAppId, appSecret: envAppSecret, source: 'env' };

  const configPath = path.join(os.homedir(), '.openclaw', 'openclaw.json');
  const config = parseOpenClawConfig(configPath);
  const cfgAppId = config?.channels?.feishu?.appId;
  const cfgAppSecret = config?.channels?.feishu?.appSecret;
  const appId = envAppId || cfgAppId;
  const appSecret = envAppSecret || cfgAppSecret;
  if (!appId || !appSecret) {
    throw new Error('Missing Feishu credentials in env or ~/.openclaw/openclaw.json (channels.feishu.appId/appSecret)');
  }
  return { appId, appSecret, source: envAppId && envAppSecret ? 'env' : 'openclaw.json' };
}

const args = process.argv.slice(2);
const whiteboardId = args[0];
if (!whiteboardId) {
  console.error(JSON.stringify({ error: 'Usage: node export_nodes_raw.js <whiteboard_id>' }));
  process.exit(1);
}

let credentials;
try {
  credentials = loadCredentials();
} catch (err) {
  console.error(JSON.stringify({ error: err.message }));
  process.exit(1);
}

const client = new lark.Client({ appId: credentials.appId, appSecret: credentials.appSecret });

async function main() {
  const nodes = [];
  let pageToken;
  try {
    do {
      const res = await client.board.v1.whiteboardNode.list({
        path: { whiteboard_id: whiteboardId },
        params: { page_token: pageToken, page_size: 50 },
      });
      if (res.code !== 0) {
        if (res.code === 403 || res.code === 404) {
          console.log(JSON.stringify({ error: `Access Denied (Code ${res.code}): Bot likely needs view permission on the board.` }));
          return;
        }
        throw new Error(`API Error ${res.code}: ${res.msg}`);
      }
      const batch = res?.data?.nodes || [];
      for (const n of batch) nodes.push(n);
      pageToken = res?.data?.page_token;
    } while (pageToken);

    console.log(JSON.stringify({ whiteboard_id: whiteboardId, count: nodes.length, nodes }, null, 2));
  } catch (e) {
    console.error(JSON.stringify({ error: e.message }));
    process.exit(1);
  }
}

main();
