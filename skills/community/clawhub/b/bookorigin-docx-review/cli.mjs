#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import { safePreflight as runSafePreflight, buildReviewPackage } from './core.mjs';

const ACTIONS = new Set(['book-docx-safe-preflight', 'book-review-package']);

function args(argv) {
  const [action, ...rest] = argv;
  const out = { action };
  for (let i = 0; i < rest.length; i += 2) {
    if (!rest[i]?.startsWith('--') || rest[i + 1] === undefined) throw Object.assign(new Error('参数必须成对使用：--key value'), { code: 'INPUT_REQUIRED' });
    out[rest[i].slice(2).replaceAll('-', '_')] = rest[i + 1];
  }
  return out;
}
function publicError(action, error) {
  const code = error?.code || 'INTERNAL_ERROR';
  const denied = new Set(['SOURCE_HASH_CHANGED', 'EVENT_CHAIN_INVALID', 'EVENT_CHAIN_TAMPERED', 'REVIEW_BINDING_INVALID']);
  return { body: { ok: false, action_id: action || null, code, message: error?.message || '动作未能完成' }, exit: denied.has(code) ? 3 : code === 'INTERNAL_ERROR' ? 4 : 2 };
}
function finish(body, code = 0) { process.stdout.write(`${JSON.stringify(body)}\n`); process.exitCode = code; }
async function safePreflight(input) {
  if (!input) throw Object.assign(new Error('必须提供 --input 本地 DOCX 路径'), { code: 'INPUT_REQUIRED' });
  return runSafePreflight(input);
}
async function reviewPackage(caseJson, sourcePath, decisionsPath) {
  if (!caseJson || !sourcePath || !decisionsPath) throw Object.assign(new Error('必须同时提供 --case-json、--source 和 --decisions'), { code: 'INPUT_REQUIRED' });
  let record; try { record = JSON.parse(await fs.readFile(path.resolve(caseJson), 'utf8')); } catch (error) { if (error instanceof SyntaxError) throw Object.assign(new Error('case JSON 无法解析'), { code: 'CASE_JSON_INVALID' }); throw Object.assign(new Error('case JSON 不可读取'), { code: 'CASE_JSON_UNREADABLE' }); }
  if (record?.result?.review_case_template) record = record.result.review_case_template;
  try { const decisions = JSON.parse(await fs.readFile(path.resolve(decisionsPath), 'utf8')); record = { ...record, decisions: Array.isArray(decisions) ? decisions : decisions.decisions }; } catch (error) { if (error instanceof SyntaxError) throw Object.assign(new Error('decisions JSON 无法解析'), { code: 'REVIEW_BINDING_INVALID' }); throw Object.assign(new Error('decisions JSON 不可读取'), { code: 'REVIEW_BINDING_INVALID' }); }
  let source; try { source = await fs.readFile(path.resolve(sourcePath)); } catch { throw Object.assign(new Error('源 DOCX 不可读取'), { code: 'SOURCE_COPY_UNREADABLE' }); }
  return buildReviewPackage(record, source);
}
try {
  const parsed = args(process.argv.slice(2));
  if (!ACTIONS.has(parsed.action)) throw Object.assign(new Error('动作必须是 book-docx-safe-preflight 或 book-review-package'), { code: 'INPUT_REQUIRED' });
  const result = parsed.action === 'book-docx-safe-preflight' ? await safePreflight(parsed.input) : await reviewPackage(parsed.case_json, parsed.source, parsed.decisions);
  finish({ ok: true, action_id: parsed.action, result });
} catch (error) {
  const action = process.argv[2]; const { body, exit } = publicError(action, error); finish(body, exit);
}
