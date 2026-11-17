import crypto from 'node:crypto';
import fs from 'node:fs/promises';
import path from 'node:path';
import zlib from 'node:zlib';

const fail = (message, code) => { throw Object.assign(new Error(message), { code }); };
const sha = value => crypto.createHash('sha256').update(value).digest('hex');
const u16 = (b, p) => b.readUInt16LE(p);
const u32 = (b, p) => b.readUInt32LE(p);
const canonical = value => {
  if (value === null || typeof value === 'string' || typeof value === 'boolean' || typeof value === 'number') return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(canonical).join(',')}]`;
  if (typeof value === 'object') return `{${Object.keys(value).sort().map(k => `${JSON.stringify(k)}:${canonical(value[k])}`).join(',')}}`;
  fail('案例包含非 JSON 值', 'CASE_JSON_INVALID');
};
function entries(bytes) {
  if (bytes.length < 22 || bytes.subarray(0, 4).toString('hex') !== '504b0304') fail('不是 ZIP/DOCX 文件', 'ZIP_MAGIC_INVALID');
  let eocd = -1;
  for (let i = bytes.length - 22; i >= Math.max(0, bytes.length - 22 - 65535); i--) if (bytes.subarray(i, i + 4).toString('hex') === '504b0506') { eocd = i; break; }
  if (eocd < 0 || eocd + 22 > bytes.length) fail('ZIP 结束目录无效', 'ZIP_EOCD_INVALID');
  const count = u16(bytes, eocd + 10), size = u32(bytes, eocd + 12), start = u32(bytes, eocd + 16);
  if (!count || count > 2048 || start + size > eocd) fail('ZIP 目录范围无效', 'ZIP_EOCD_INVALID');
  let p = start, inflated = 0; const result = new Map();
  for (let i = 0; i < count; i++) {
    if (p + 46 > eocd || bytes.subarray(p, p + 4).toString('hex') !== '504b0102') fail('ZIP 中央目录无效', 'ZIP_EOCD_INVALID');
    const flags = u16(bytes, p + 8), method = u16(bytes, p + 10), packed = u32(bytes, p + 20), raw = u32(bytes, p + 24), nlen = u16(bytes, p + 28), xlen = u16(bytes, p + 30), clen = u16(bytes, p + 32), local = u32(bytes, p + 42);
    if (!nlen || p + 46 + nlen + xlen + clen > eocd) fail('ZIP 中央目录条目越界', 'ZIP_EOCD_INVALID');
    const name = bytes.subarray(p + 46, p + 46 + nlen).toString('utf8');
    if (!name || name.includes('\\') || name.startsWith('/') || /^[A-Za-z]:/.test(name) || name.split('/').includes('..') || result.has(name)) fail('ZIP 内路径不安全', 'ZIP_PATH_UNSAFE');
    if (flags & 1) fail('不接受加密 ZIP', 'ZIP_ENCRYPTED');
    if (![0, 8].includes(method)) fail('ZIP 压缩方式不支持', 'ZIP_METHOD_UNSUPPORTED');
    inflated += raw;
    if (raw > 10 * 1024 * 1024 || inflated > 30 * 1024 * 1024 || (packed && raw / packed > 100) || (!packed && raw > 0)) fail('ZIP 展开超出限制', 'ZIP_EXPANSION_LIMIT');
    if (local + 30 > bytes.length || bytes.subarray(local, local + 4).toString('hex') !== '504b0304') fail('ZIP 本地头无效', 'ZIP_EOCD_INVALID');
    const ln = u16(bytes, local + 26), lx = u16(bytes, local + 28), data = local + 30 + ln + lx;
    if (ln !== nlen || bytes.subarray(local + 30, local + 30 + ln).toString('utf8') !== name || data + packed > bytes.length) fail('ZIP 数据范围无效', 'ZIP_EOCD_INVALID');
    const compressed = bytes.subarray(data, data + packed);
    try { const actual = method === 0 ? compressed : zlib.inflateRawSync(compressed, { maxOutputLength: Math.max(1, raw) }); if (actual.length !== raw) fail('ZIP 展开长度无效', 'ZIP_EXPANSION_LIMIT'); }
    catch (error) { if (error?.code === 'ZIP_EXPANSION_LIMIT') throw error; fail('ZIP 解压失败', 'ZIP_EXPANSION_LIMIT'); }
    result.set(name, { method, packed: compressed }); p += 46 + nlen + xlen + clen;
  }
  return result;
}
function readPart(map, name) {
  const part = map.get(name); if (!part) return null;
  try { return (part.method === 0 ? part.packed : zlib.inflateRawSync(part.packed)).toString('utf8'); } catch { fail('DOCX XML 无法解压', 'PARSER_FAILED'); }
}
function textProjection(xml) {
  return xml.replace(/<w:p\b[^>]*>/g, '\n').replace(/<w:tab\b[^>]*\/>/g, '\t').replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(Number(n))).split(/\n+/).map(x => x.trim()).filter(Boolean);
}
export async function safePreflight(input) {
  let bytes; try { bytes = await fs.readFile(path.resolve(input)); } catch { fail('输入文件不可读取', 'INPUT_READ_FAILED'); }
  const filename = path.basename(input); if (!/\.docx$/i.test(filename)) fail('输入必须是 .docx 文件名', 'FILENAME_INVALID');
  const map = entries(bytes);
  if ([...map.keys()].some(name => /vba|macro|\.bin$/i.test(name))) fail('拒绝含宏或宏相关部件的 DOCX', 'DOCX_MACRO_REJECTED');
  for (const name of ['[Content_Types].xml', '_rels/.rels', 'word/document.xml']) if (!map.has(name)) fail('缺少 DOCX 必需结构', 'DOCX_STRUCTURE_MISSING');
  if (/macroEnabled|vbaProject|vbaData/i.test(readPart(map, '[Content_Types].xml'))) fail('拒绝声明宏类型的 DOCX', 'DOCX_MACRO_REJECTED');
  const paragraphs = textProjection(readPart(map, 'word/document.xml'));
  const project = paragraphs.filter(x => /^项目\s*(?:\d+|[一二三四五六七八九十]+)/u.test(x));
  const brief = paragraphs.filter(x => /^(项目简述|项目说明|任务简述)/.test(x));
  const findings = [];
  if (!project.length) findings.push({ id: 'S1', level: 'advisory', criterion: '至少一个“项目N”结构标题', observed: 0, suggestion: '补充可唯一定位的项目结构标题。' });
  if (!brief.length) findings.push({ id: 'S2', level: 'advisory', criterion: '至少一个项目简述/说明标题', observed: 0, suggestion: '补充可唯一定位的项目简述标题。' });
  const source_sha256 = sha(bytes), criteria_version = 'bookorigin-structure/1.0';
  const candidates = findings.map((finding, ordinal) => ({ candidate_id: `cand_${sha(canonical({ source_sha256, criteria_version, finding_id: finding.id, ordinal: ordinal + 1 })).slice(0, 24)}`, finding_id: finding.id, ordinal: ordinal + 1, level: 'advisory' }));
  const event = { type: 'preflight.completed', at: new Date().toISOString(), detail: { source_sha256, criteria_version, candidate_count: candidates.length }, prev_hash: null }; event.hash = eventHash(event);
  const review_case_template = { spec: 'bookorigin-review-case/1.0', source: { sha256: source_sha256 }, criteria_version, events: [event], event_chain_head: event.hash, candidates, decisions: [] };
  return { input_filename: filename, source_sha256, zip_preflight: { entry_count: map.size, sha256: source_sha256, encrypted: false, macro: false, limits: { max_entries: 2048, max_entry_bytes: 10485760, max_total_bytes: 31457280, max_ratio: 100 } }, observation: { paragraph_count: paragraphs.length, text_projection: '仅统计；不输出原文' }, criteria: { version: criteria_version, checks: ['项目N标题', '项目简述/说明标题'] }, summary: { finding_count: findings.length, status: findings.length ? 'advisory_findings' : 'no_structure_findings' }, findings, review_case_template, boundaries: ['只读本地预检：不保存原件、不上传云端、不调用模型', '仅检查明示的结构信号，不等于教材正确、可印刷或可交付', '不会生成、修改或覆盖 DOCX；不验证身份、授权或人工审批'] };
}
export function eventHash(event) { const { hash, ...rest } = event; return sha(canonical(rest)); }
export function buildReviewPackage(record, source) {
  if (!record || record.spec !== 'bookorigin-review-case/1.0' || !record.source || !Array.isArray(record.events) || !Array.isArray(record.candidates) || !Array.isArray(record.decisions)) fail('案例格式不符合 bookorigin-review-case/1.0', 'CASE_JSON_INVALID');
  const sourceHash = sha(source); if (record.source.sha256 !== sourceHash) fail('源文件哈希与案例不一致', 'SOURCE_HASH_CHANGED');
  let previous = null;
  for (const event of record.events) { if (event.prev_hash !== previous || event.hash !== eventHash(event)) fail('事件链已篡改或不连续', 'EVENT_CHAIN_TAMPERED'); previous = event.hash; }
  if (!previous || record.event_chain_head !== previous) fail('事件链头不匹配', 'EVENT_CHAIN_INVALID');
  const ids = new Set(record.candidates.map(x => x?.candidate_id));
  if (!record.candidates.length || ids.size !== record.candidates.length || [...ids].some(id => typeof id !== 'string' || !/^cand_[A-Za-z0-9_-]{1,96}$/.test(id))) fail('候选列表无效', 'REVIEW_BINDING_INVALID');
  const decided = new Set(record.decisions.map(x => x?.candidate_id));
  if (record.decisions.length !== record.candidates.length || decided.size !== ids.size || [...ids].some(id => !decided.has(id)) || record.decisions.some(x => !ids.has(x.candidate_id) || !['acknowledged', 'deferred', 'rejected'].includes(x.decision))) fail('候选与人工决定必须逐项一一绑定', 'REVIEW_BINDING_INVALID');
  const reviewHash = sha(canonical({ source_sha256: sourceHash, event_chain_head: previous, candidates: record.candidates, decisions: record.decisions }));
  return { manifest: { spec: 'bookorigin-review-package/1.0', source_sha256: sourceHash, event_chain_head: previous, review_hash: reviewHash, candidate_count: record.candidates.length, decision_count: record.decisions.length, output: 'advisory_only_no_modified_docx' }, candidates: record.candidates.map(({ candidate_id, finding_id }, ordinal) => ({ candidate_id, finding_id: typeof finding_id === 'string' ? finding_id.slice(0, 64) : 'unspecified', ordinal: ordinal + 1, level: 'advisory' })), decisions: record.decisions.map(({ candidate_id, decision }) => ({ candidate_id, decision })), boundaries: ['仅复核相对案例记录的哈希与链自洽；不构成签名、身份或防篡改保管链', '输出不含候选自由文本、原文或路径；所有建议均为 advisory-only', 'acknowledged 不等于接受、审批或已修改；本动作未生成已修改 DOCX，也不提供交付资格结论'] };
}
