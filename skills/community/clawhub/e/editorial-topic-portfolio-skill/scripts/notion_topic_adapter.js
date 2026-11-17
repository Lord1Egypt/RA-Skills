const https = require('https');

function requiredEnv(name) {
  const value = process.env[name];
  if (!value) throw new Error(`${name} is required`);
  return value;
}

function request({ token, databaseId, path, method, payload }) {
  return new Promise((resolve, reject) => {
    const body = payload ? JSON.stringify(payload) : '';
    const req = https.request({
      hostname: 'api.notion.com',
      port: 443,
      path,
      method,
      timeout: 30000,
      headers: {
        Authorization: `Bearer ${token}`,
        'Notion-Version': '2022-06-28',
        'Content-Type': 'application/json',
        ...(body ? { 'Content-Length': Buffer.byteLength(body) } : {})
      }
    }, res => {
      let text = '';
      res.on('data', chunk => { text += chunk; });
      res.on('end', () => {
        if (res.statusCode < 200 || res.statusCode >= 300) {
          reject(new Error(`HTTP ${res.statusCode}: ${text.slice(0, 500)}`));
          return;
        }
        try { resolve(JSON.parse(text)); }
        catch (error) { reject(error); }
      });
    });
    req.on('timeout', () => req.destroy(new Error('timeout')));
    req.on('error', reject);
    if (body) req.write(body);
    req.end();
  });
}

function getConfig() {
  return {
    token: requiredEnv('NOTION_TOKEN'),
    databaseId: requiredEnv('NOTION_TOPIC_DATABASE_ID'),
    mapping: JSON.parse(requiredEnv('NOTION_TOPIC_MAPPING_JSON'))
  };
}

function plainText(property) {
  if (!property) return '';
  const list = property.title || property.rich_text || [];
  return list.map(item => item.plain_text || '').join('');
}

function toTopic(page, mapping) {
  const properties = page.properties || {};
  const get = key => properties[mapping[key]];
  return {
    topic_id: page.id,
    title: plainText(get('title')),
    source_date: get('date')?.date?.start || '',
    captured_at: page.last_edited_time || '',
    status: get('lifecycle')?.status?.name || get('lifecycle')?.select?.name || '',
    current_priority: get('priority')?.select?.name || '',
    competition: get('competition')?.select?.name || '',
    originality: get('originality')?.select?.name || '',
    value: plainText(get('value')),
    reason: plainText(get('reason')),
    angle: plainText(get('angle')),
    risk: plainText(get('risk')),
    fit: plainText(get('fit'))
  };
}

async function queryAll() {
  const { token, databaseId, mapping } = getConfig();
  let cursor;
  const pages = [];
  do {
    const result = await request({
      token,
      databaseId,
      path: `/v1/databases/${databaseId}/query`,
      method: 'POST',
      payload: { page_size: 100, ...(cursor ? { start_cursor: cursor } : {}) }
    });
    pages.push(...(result.results || []).map(page => toTopic(page, mapping)));
    cursor = result.has_more ? result.next_cursor : null;
  } while (cursor);
  return pages;
}

async function patchPage(pageId, properties) {
  const { token, databaseId } = getConfig();
  return request({
    token,
    databaseId,
    path: `/v1/pages/${pageId}`,
    method: 'PATCH',
    payload: { properties }
  });
}

async function main() {
  const mode = process.argv[2] || 'read';
  if (mode === 'read') {
    const pages = await queryAll();
    process.stdout.write(JSON.stringify({ pages }, null, 2) + '\n');
    return;
  }
  if (mode === 'write') {
    if (process.env.NOTION_DRY_RUN !== 'false') {
      throw new Error('Refusing to write: set NOTION_DRY_RUN=false only after approved change preview');
    }
    throw new Error('Write mode requires a reviewed adapter implementation and explicit page-level change set');
  }
  throw new Error(`Unknown mode: ${mode}`);
}

main().catch(error => {
  console.error(error.message);
  process.exitCode = 1;
});
