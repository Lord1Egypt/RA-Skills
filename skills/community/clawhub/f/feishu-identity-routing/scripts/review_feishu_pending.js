#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const workspace = '/home/admin/.openclaw/workspace';
const masterPath = path.join(workspace, 'identity', 'feishu-user-master.json');

function fail(msg) {
  console.error(msg);
  process.exit(1);
}

function load() {
  return JSON.parse(fs.readFileSync(masterPath, 'utf8'));
}

function save(data) {
  fs.writeFileSync(masterPath, JSON.stringify(data, null, 2) + '\n');
}

const action = process.argv[2];
const indexRaw = process.argv[3];
const subjectId = process.argv[4];
const reason = process.argv.slice(5).join(' ') || '';

if (!action || !['list', 'approve', 'reject'].includes(action)) {
  fail('Usage: node bin/review_feishu_pending.js list | approve <index> <subject_id> [reason] | reject <index> [reason]');
}

const data = load();
data.pending_reviews = data.pending_reviews || [];

if (action === 'list') {
  console.log(JSON.stringify({ count: data.pending_reviews.length, pending_reviews: data.pending_reviews }, null, 2));
  process.exit(0);
}

const index = Number(indexRaw);
if (!Number.isInteger(index) || index < 0 || index >= data.pending_reviews.length) {
  fail('Invalid pending review index');
}

const pending = data.pending_reviews[index];
const rec = pending.record;

if (action === 'approve') {
  if (!subjectId) fail('approve requires <subject_id>');
  const subject = data.subjects.find(s => s.subject_id === subjectId);
  if (!subject) fail(`Subject not found: ${subjectId}`);

  subject.app_identities = subject.app_identities || [];
  subject.merged_from = subject.merged_from || [];
  subject.notes = subject.notes || [];
  subject.identifiers = subject.identifiers || { user_ids: [] };
  subject.phones = subject.phones || [];
  subject.aliases = subject.aliases || [];

  if (!subject.app_identities.find(x => x.app_context === rec.app_context && x.open_id === rec.open_id)) {
    subject.app_identities.push({ ...rec, status: 'confirmed' });
  }
  if (!subject.merged_from.includes(`${rec.app_context}:${rec.open_id}`)) {
    subject.merged_from.push(`${rec.app_context}:${rec.open_id}`);
  }
  if (rec.user_id && !subject.identifiers.user_ids.includes(rec.user_id)) {
    subject.identifiers.user_ids.push(rec.user_id);
  }
  if (rec.phone && !subject.phones.includes(rec.phone)) {
    subject.phones.push(rec.phone);
  }
  if (rec.name && rec.name !== subject.canonical_name && !subject.aliases.includes(rec.name)) {
    subject.aliases.push(rec.name);
  }
  subject.notes.push(`Review approved at ${new Date().toISOString()} by main-agent. Reason: ${reason || 'n/a'}`);

  data.pending_reviews.splice(index, 1);
  data.updated_at = new Date().toISOString();
  save(data);
  console.log(JSON.stringify({ ok: true, action: 'approved', subject_id: subjectId }, null, 2));
  process.exit(0);
}

if (action === 'reject') {
  data.rejected_reviews = data.rejected_reviews || [];
  data.rejected_reviews.push({
    ...pending,
    reviewed_at: new Date().toISOString(),
    reviewed_by: 'main-agent',
    decision: 'rejected',
    reason
  });
  data.pending_reviews.splice(index, 1);
  data.updated_at = new Date().toISOString();
  save(data);
  console.log(JSON.stringify({ ok: true, action: 'rejected', index }, null, 2));
}
