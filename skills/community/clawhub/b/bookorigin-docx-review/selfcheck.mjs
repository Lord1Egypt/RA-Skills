#!/usr/bin/env node
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import zlib from 'node:zlib';
import { fileURLToPath } from 'node:url';
import { eventHash } from './core.mjs';
let passed = 0;
const u16 = n => { const b = Buffer.alloc(2); b.writeUInt16LE(n); return b; };
const u32 = n => { const b = Buffer.alloc(4); b.writeUInt32LE(n); return b; };
function crc32(b) { let c = 0xffffffff; for (const x of b) { c ^= x; for (let i = 0; i < 8; i++) c = (c >>> 1) ^ (0xedb88320 & -(c & 1)); } return (c ^ 0xffffffff) >>> 0; }
function zip(parts) { let at = 0; const local = [], cd = []; for (const p of parts) { const n = Buffer.from(p.name), raw = Buffer.from(p.data), packed = zlib.deflateRawSync(raw), crc = crc32(raw); const l = Buffer.concat([Buffer.from('504b0304', 'hex'),u16(20),u16(0),u16(8),u16(0),u16(0),u32(crc),u32(packed.length),u32(raw.length),u16(n.length),u16(0),n,packed]); local.push(l); cd.push(Buffer.concat([Buffer.from('504b0102','hex'),u16(20),u16(20),u16(0),u16(8),u16(0),u16(0),u32(crc),u32(packed.length),u32(raw.length),u16(n.length),u16(0),u16(0),u16(0),u16(0),u32(0),u32(at),n])); at += l.length; } const body=Buffer.concat(local), central=Buffer.concat(cd); return Buffer.concat([body,central,Buffer.from('504b0506','hex'),u16(0),u16(0),u16(parts.length),u16(parts.length),u32(central.length),u32(body.length),u16(0)]); }
const docx = () => zip([{name:'[Content_Types].xml',data:'<Types/>'},{name:'_rels/.rels',data:'<Relationships/>'},{name:'word/document.xml',data:'<w:document><w:body><w:p>合成教材</w:p><w:p>项目1</w:p><w:p>项目简述</w:p></w:body></w:document>'}]);
const here = path.dirname(fileURLToPath(import.meta.url)), cli = path.join(here, 'cli.mjs');
const call = argv => spawnSync(process.execPath, [cli, ...argv], { encoding: 'utf8' });
const tmp = await fs.mkdtemp(path.join(os.tmpdir(), 'bookorigin-skill-'));
try {
  const source = path.join(tmp, 'fixture.docx'), bytes = docx(); await fs.writeFile(source, bytes);
  let out = call(['book-docx-safe-preflight','--input',source]); assert.equal(out.status,0); const preflightResult = JSON.parse(out.stdout); assert.equal(preflightResult.result.summary.finding_count,0); assert.equal(preflightResult.result.review_case_template.source.sha256, crypto.createHash('sha256').update(bytes).digest('hex')); passed++;
  out = call(['book-docx-safe-preflight','--input',path.join(tmp,'missing.docx')]); assert.equal(out.status,2); assert.equal(JSON.parse(out.stdout).code,'INPUT_READ_FAILED'); passed++;
  const macro = path.join(tmp, 'macro.docx'); await fs.writeFile(macro, zip([{name:'[Content_Types].xml',data:'<Types/>'},{name:'_rels/.rels',data:'<Relationships/>'},{name:'word/document.xml',data:'<w:document/>'},{name:'word/vbaProject.bin',data:'not-a-macro-to-execute'}]));
  out = call(['book-docx-safe-preflight','--input',macro]); assert.equal(out.status,2); assert.equal(JSON.parse(out.stdout).code,'DOCX_MACRO_REJECTED'); passed++;
  const hash = crypto.createHash('sha256').update(bytes).digest('hex');
  const event = { type:'observed', at:'2026-09-02T00:00:00.000Z', detail:{ source_sha256:hash }, prev_hash:null }; event.hash = eventHash(event);
  const record = { spec:'bookorigin-review-case/1.0', source:{sha256:hash}, events:[event], event_chain_head:event.hash, candidates:[{candidate_id:'cand_1',finding_id:'S1',location:'paragraph:1',suggestion:'补标题'}], decisions:[{candidate_id:'cand_1',decision:'acknowledged'}] };
  const caseFile = path.join(tmp,'case.json'); await fs.writeFile(caseFile,JSON.stringify(record));
  const decisionsFile = path.join(tmp,'decisions.json'); await fs.writeFile(decisionsFile,JSON.stringify(record.decisions));
  out = call(['book-review-package','--case-json',caseFile,'--source',source,'--decisions',decisionsFile]); assert.equal(out.status,0); assert.equal(JSON.parse(out.stdout).result.manifest.output,'advisory_only_no_modified_docx'); passed++;
  await fs.writeFile(decisionsFile,JSON.stringify([])); out=call(['book-review-package','--case-json',caseFile,'--source',source,'--decisions',decisionsFile]); assert.equal(out.status,3); assert.equal(JSON.parse(out.stdout).code,'REVIEW_BINDING_INVALID'); passed++;
  await fs.writeFile(decisionsFile,JSON.stringify([{candidate_id:'missing',decision:'acknowledged'}])); out=call(['book-review-package','--case-json',caseFile,'--source',source,'--decisions',decisionsFile]); assert.equal(out.status,3); assert.equal(JSON.parse(out.stdout).code,'REVIEW_BINDING_INVALID'); passed++;
  record.events[0].detail.source_sha256='0'.repeat(64); await fs.writeFile(caseFile,JSON.stringify(record)); await fs.writeFile(decisionsFile,JSON.stringify(record.decisions)); out=call(['book-review-package','--case-json',caseFile,'--source',source,'--decisions',decisionsFile]); assert.equal(out.status,3); assert.equal(JSON.parse(out.stdout).code,'EVENT_CHAIN_TAMPERED'); passed++;
} finally { await fs.rm(tmp,{recursive:true,force:true}); }
console.log(`BookOrigin standalone skill selfcheck: ${passed}/7 passed`);
