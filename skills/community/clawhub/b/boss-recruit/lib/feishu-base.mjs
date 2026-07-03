/**
 * 飞书多维表格 base-api 后端 (BaseOpenSDK 等价，纯 HTTP，无依赖)
 * ───────────────────────────────────────────────────────────────────────────
 * 用「授权码(personal_base_token)」直连 base-api.feishu.cn 读写指定 base。
 * 等价于小良知聘后端的 baseopensdk.BaseClient(app_token + personal_base_token)。
 *
 * ⚠️ 授权码只认 /base/ 链接(个人端)，不支持 /wiki/(企业端)。
 * 端点已实测：GET .../records 返回 code:0。
 */
const HOST = 'https://base-api.feishu.cn';

async function bfetch(token, method, urlPath, { body, isForm } = {}) {
  const headers = { Authorization: `Bearer ${token}` };
  let payload;
  if (isForm) { payload = body; }                       // FormData，浏览器/undici 自动设边界
  else if (body !== undefined) { headers['Content-Type'] = 'application/json'; payload = JSON.stringify(body); }
  const res = await fetch(HOST + urlPath, { method, headers, body: payload });
  const json = await res.json().catch(() => ({}));
  if (json.code !== 0) {
    const map = { 99991668: '授权码无效/未带 token', 1254005: '授权码无效或过期', 1254040: '表不存在' };
    throw new Error(`base-api ${json.code}: ${map[json.code] || json.msg || JSON.stringify(json).slice(0, 160)}`);
  }
  return json.data;
}

/** 取某张表的名字（base-api 列表里匹配 table_id）。失败返回 null，不阻塞。 */
export async function getTableName(app, tbl, token) {
  try {
    const d = await bfetch(token, 'GET', `/open-apis/bitable/v1/apps/${app}/tables?page_size=100`);
    return (d.items || []).find((t) => t.table_id === tbl)?.name || null;
  } catch { return null; }
}

/** 列字段名 + 找附件字段(type=17)。 */
export async function listFields(app, tbl, token) {
  const d = await bfetch(token, 'GET', `/open-apis/bitable/v1/apps/${app}/tables/${tbl}/fields?page_size=200`);
  const items = d.items || [];
  const att = items.find((f) => f.type === 17) || items.find((f) => /附件/.test(f.field_name));
  return { fieldNames: items.map((f) => f.field_name), attachmentField: att?.field_name || null };
}

/** 连接测试：能列 1 条即视为授权码+表有效。 */
export async function testConnection(app, tbl, token) {
  const d = await bfetch(token, 'GET', `/open-apis/bitable/v1/apps/${app}/tables/${tbl}/records?page_size=1`);
  return { ok: true, total: d.total ?? (d.items?.length || 0) };
}

/** 创建单条记录，返回 record_id。 */
export async function createRecord(app, tbl, token, fields) {
  const d = await bfetch(token, 'POST', `/open-apis/bitable/v1/apps/${app}/tables/${tbl}/records/batch_create`, {
    body: { records: [{ fields }] },
  });
  const rid = d.records?.[0]?.record_id;
  if (!rid) throw new Error('创建成功但未取到 record_id');
  return rid;
}

/** 更新单条记录。 */
export async function updateRecord(app, tbl, token, recordId, fields) {
  await bfetch(token, 'POST', `/open-apis/bitable/v1/apps/${app}/tables/${tbl}/records/batch_update`, {
    body: { records: [{ record_id: recordId, fields }] },
  });
  return recordId;
}

/** 上传文件到 Drive(parent_type=bitable_file)，返回 file_token。 */
export async function uploadMedia(app, token, fileBuffer, fileName) {
  const form = new FormData();
  form.append('file_name', fileName);
  form.append('parent_type', 'bitable_file');
  form.append('parent_node', app);
  form.append('size', String(fileBuffer.length));
  form.append('file', new Blob([fileBuffer]), fileName);
  const d = await bfetch(token, 'POST', '/open-apis/drive/v1/medias/upload_all', { body: form, isForm: true });
  if (!d.file_token) throw new Error('上传成功但未取到 file_token');
  return d.file_token;
}

/** 上传附件并挂到记录的附件字段。 */
export async function uploadAttachment(app, tbl, token, recordId, attachmentField, fileBuffer, fileName) {
  const fileToken = await uploadMedia(app, token, fileBuffer, fileName);
  await updateRecord(app, tbl, token, recordId, { [attachmentField]: [{ file_token: fileToken }] });
  return fileToken;
}

export default { listFields, testConnection, createRecord, updateRecord, uploadMedia, uploadAttachment };
