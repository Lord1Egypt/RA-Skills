#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const workspace = '/home/admin/.openclaw/workspace';
const masterPath = path.join(workspace, 'identity', 'feishu-user-master.json');

function fail(msg) {
  console.error(msg);
  process.exit(1);
}

function loadJson(p) {
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

function saveJson(p, data) {
  fs.writeFileSync(p, JSON.stringify(data, null, 2) + '\n', 'utf8');
}

function normalizeRecord(input) {
  const required = ['source_agent', 'app_context', 'open_id', 'user_id', 'union_id', 'name', 'phone', 'captured_at'];
  for (const key of required) {
    if (!input[key] || typeof input[key] !== 'string') {
      fail(`Missing required field: ${key}`);
    }
  }
  return {
    source_agent: input.source_agent.trim(),
    app_context: input.app_context.trim(),
    open_id: input.open_id.trim(),
    user_id: input.user_id.trim(),
    union_id: input.union_id.trim(),
    name: input.name.trim(),
    phone: input.phone.trim(),
    captured_at: input.captured_at.trim(),
    source_type: input.source_type ? String(input.source_type).trim() : 'agent-reported',
    status: input.status ? String(input.status).trim() : 'confirmed'
  };
}

function findSubject(master, rec) {
  let subject = master.subjects.find(s => s.identifiers?.union_id === rec.union_id);
  if (subject) return { subject, mode: 'union_id' };

  const byUserId = master.subjects.filter(s => Array.isArray(s.identifiers?.user_ids) && s.identifiers.user_ids.includes(rec.user_id));
  if (byUserId.length === 1) return { subject: byUserId[0], mode: 'user_id' };
  if (byUserId.length > 1) return { subject: null, mode: 'ambiguous_user_id' };

  return { subject: null, mode: 'new_subject' };
}

function ensureArrayUnique(arr, value) {
  if (!arr.includes(value)) arr.push(value);
}

function upsertAppIdentity(subject, rec) {
  const existing = subject.app_identities.find(x => x.app_context === rec.app_context && x.open_id === rec.open_id);
  if (existing) {
    Object.assign(existing, rec);
    return 'updated';
  }
  subject.app_identities.push(rec);
  return 'inserted';
}

function createSubjectFromRecord(rec) {
  return {
    subject_id: `feishu:${rec.union_id || rec.user_id}`,
    canonical_name: rec.name,
    aliases: [],
    phones: [rec.phone],
    identifiers: {
      union_id: rec.union_id,
      user_ids: [rec.user_id]
    },
    app_identities: [rec],
    merged_from: [`${rec.app_context}:${rec.open_id}`],
    review: {
      needs_review: false,
      reason: ''
    },
    notes: [
      'Created automatically from agent submission.'
    ]
  };
}

function main() {
  const raw = process.argv[2];
  if (!raw) {
    fail('Usage: node bin/merge_feishu_identity.js \'{"source_agent":"...",...}\'');
  }

  const input = normalizeRecord(JSON.parse(raw));
  const master = loadJson(masterPath);

  const found = findSubject(master, input);
  let action = '';

  if (found.mode === 'ambiguous_user_id') {
    const pending = {
      ...input,
      status: 'needs_review'
    };
    master.pending_reviews = master.pending_reviews || [];
    master.pending_reviews.push({
      type: 'ambiguous_user_id',
      record: pending,
      noted_at: new Date().toISOString()
    });
    action = 'pending_review';
  } else if (found.subject) {
    const subject = found.subject;
    ensureArrayUnique(subject.identifiers.user_ids, input.user_id);
    ensureArrayUnique(subject.phones, input.phone);
    if (subject.canonical_name !== input.name && !subject.aliases.includes(input.name)) {
      subject.aliases.push(input.name);
    }
    const appAction = upsertAppIdentity(subject, input);
    ensureArrayUnique(subject.merged_from, `${input.app_context}:${input.open_id}`);
    action = `${found.mode}_${appAction}`;
  } else {
    master.subjects.push(createSubjectFromRecord(input));
    action = 'new_subject_created';
  }

  master.updated_at = new Date().toISOString();
  saveJson(masterPath, master);
  console.log(JSON.stringify({ ok: true, action, subject_count: master.subjects.length }, null, 2));
}

main();
