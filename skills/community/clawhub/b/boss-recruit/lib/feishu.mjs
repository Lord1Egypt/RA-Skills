/**
 * 飞书多维表格同步 (feishu sync)
 * ───────────────────────────────────────────────────────────────────────────
 * 把 boss resume 的档案 + boss attachment 的 PDF 写入「人才表」。
 * 幂等：record_id 存在则 update，否则 create（record_id 由 task-memory 持有）。
 */
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import path from 'node:path';
import fs from 'node:fs';
import { POSITION_OPTIONS, STAGE, RESUME_SOURCE } from '../config.mjs';
import { loadTarget } from './target.mjs';
import * as BASE from './feishu-base.mjs';
const pexec = promisify(execFile);

/** 读运行时目标表配置；未配置则报错引导去 setup。 */
function target() {
  const t = loadTarget();
  if (!t) throw new Error('尚未配置飞书目标表。先运行: node scenarios/setup.mjs <飞书表链接> [--token <授权码>]');
  return t;
}
/** 是否走授权码(base-api)后端。 */
function useBaseApi(t) { return t.backend === 'base-api' && t.personal_base_token; }

async function lark(args, opts = {}) {
  const { stdout } = await pexec('lark-cli', args, { maxBuffer: 64 * 1024 * 1024, ...opts });
  // lark-cli 偶尔前置进度行；截取首个 { 起的 JSON
  const i = stdout.indexOf('{');
  const json = i >= 0 ? JSON.parse(stdout.slice(i)) : null;
  if (json && json.ok === false) throw new Error(`lark-cli: ${JSON.stringify(json.error)}`);
  return json;
}

/** 从 "2020-2025  东北大学 · 电子科学与技术 · 本科" 拆出 学校/专业/毕业年份。 */
function parseEducation(edu) {
  if (!edu) return { school: '', major: '', gradYear: '' };
  const line = String(edu).replace(/\\n/g, '\n').split('\n')[0];
  const m = line.match(/(\d{4})\s*[-~]\s*(\d{4})/);
  const gradYear = m ? m[2] : '';
  const parts = line.split('·').map((s) => s.trim());
  const school = parts[0] ? parts[0].replace(/^\s*\d{4}.*?\s/, '').trim() : '';
  const major = parts[1] || '';
  return { school, major, gradYear };
}

/** resume 档案 + recommend 信息 → 人才表字段对象。 */
export function profileToFields(profile, status) {
  const { school, major, gradYear } = parseEducation(profile.education);
  const wh = String(profile.work_history || '').replace(/\\n/g, '\n');
  const edu = String(profile.education || '').replace(/\\n/g, '\n');
  const zaizhi = wh.split('\n')[0].includes('至今') ? '在职' : '离职';
  const f = {
    姓名: profile.name || '',
    性别: profile.gender || '',
    工作年限: profile.experience || '',
    最终工龄: profile.experience || '',
    学历: profile.degree || '',
    学校: school,
    专业: major,
    毕业年份: gradYear,
    在职状态: zaizhi,
    简历解析: `【工作经历】\n${wh}\n\n【教育】\n${edu}\n\n【期望】${profile.expect || ''}　【年龄】${profile.age || ''}`,
    沟通职位: profile.job_name || profile.job_chatting || '',
    简历来源: RESUME_SOURCE,
    当前阶段: STAGE[status] || '新简历',
  };
  const pos = profile.job_name || profile.job_chatting || '';
  if (POSITION_OPTIONS.has(pos)) f['应聘岗位'] = pos;
  // 去空
  for (const k of Object.keys(f)) if (f[k] === '' || f[k] == null) delete f[k];
  // 只保留目标表实际存在的字段（适配不同模板，避免写不存在的列报错）
  const avail = new Set(target().fields || []);
  if (avail.size) for (const k of Object.keys(f)) if (!avail.has(k)) delete f[k];
  return f;
}

/** 创建人才记录，返回 record_id。 */
export async function createRecord(fields) {
  const t = target();
  if (useBaseApi(t)) return BASE.createRecord(t.baseToken, t.talentTable, t.personal_base_token, fields);
  const cols = Object.keys(fields);
  const row = cols.map((k) => fields[k]);
  const res = await lark([
    'base', '+record-batch-create',
    '--base-token', t.baseToken, '--table-id', t.talentTable,
    '--as', t.identity, '--format', 'json',
    '--json', JSON.stringify({ fields: cols, rows: [row] }),
  ]);
  // 返回结构里取 record_id
  const d = res.data || {};
  const rid = d.records?.[0]?.record_id || d.record_id_list?.[0]
    || (Array.isArray(d.records) ? d.records[0]?.id : null)
    || d.record_ids?.[0];
  if (!rid) throw new Error('创建记录成功但未取到 record_id: ' + JSON.stringify(d).slice(0, 200));
  return rid;
}

/** 更新已有记录（同一份 patch 到单条）。 */
export async function updateRecord(recordId, fields) {
  const t = target();
  if (useBaseApi(t)) return BASE.updateRecord(t.baseToken, t.talentTable, t.personal_base_token, recordId, fields);
  await lark([
    'base', '+record-batch-update',
    '--base-token', t.baseToken, '--table-id', t.talentTable,
    '--as', t.identity, '--format', 'json',
    '--json', JSON.stringify({ record_id_list: [recordId], patch: fields }),
  ]);
  return recordId;
}

/** 幂等同步：有 recordId 则更新，否则创建。返回 record_id。 */
export async function syncProfile(profile, status, existingRecordId) {
  const fields = profileToFields(profile, status);
  if (existingRecordId) { await updateRecord(existingRecordId, fields); return existingRecordId; }
  return await createRecord(fields);
}

/** 上传附件 PDF 到「简历附件」字段（处理 lark-cli 相对路径限制：用文件所在目录作 cwd）。 */
export async function uploadAttachment(recordId, pdfPath) {
  const t = target();
  if (!t.attachmentField) throw new Error('目标表没有附件字段，无法同步附件简历');
  if (useBaseApi(t)) {
    const buf = await fs.promises.readFile(pdfPath);
    await BASE.uploadAttachment(t.baseToken, t.talentTable, t.personal_base_token, recordId, t.attachmentField, buf, path.basename(pdfPath));
    return { via: 'base-api' };
  }
  const dir = path.dirname(path.resolve(pdfPath));
  const base = path.basename(pdfPath);
  const res = await lark([
    'base', '+record-upload-attachment',
    '--base-token', t.baseToken, '--table-id', t.talentTable,
    '--record-id', recordId, '--field-id', t.attachmentField,
    '--file', `./${base}`, '--as', t.identity, '--format', 'json',
  ], { cwd: dir });
  return res?.data || {};
}

export default { profileToFields, createRecord, updateRecord, syncProfile, uploadAttachment };
