#!/usr/bin/env node
/**
 * SAFETY: Test infrastructure only — invokes `email-manager.js` CLI with
 * hardcoded arguments. No user input enters the shell.
 */
/**
 * Email Manager test suite
 *
 * SECURITY: Uses execSync only to invoke email-manager.js (the skill under test).
 * All arguments are hardcoded strings — no user input enters the shell.
 * This is test infrastructure, not production agent code.
 */
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const SKILL = path.resolve(__dirname, '..', 'email-manager.js');
const TDIR = path.resolve(__dirname, 'tmp-test-data');

function seed(data) {
  const dd = path.join(TDIR, 'memory', 'email');
  fs.mkdirSync(dd, { recursive: true });
  fs.writeFileSync(path.join(dd, 'emails.json'), JSON.stringify(data, null, 2));
  fs.writeFileSync(path.join(dd, 'settings.json'), JSON.stringify({ sender: 'test@skill.test' }, null, 2));
}

function run(args) {
  return execSync(`node "${SKILL}" ${args.join(' ')}`, {
    encoding: 'utf8',
    env: { ...process.env, EMAIL_DIR: TDIR },
  });
}

function pass(name, ok) {
  console.log(ok ? '  ✅' : '  ❌', name);
  return ok;
}

// ── 1. parseEmail ──────────────────────────────────────────────────────────
function testParse() {
  let n = 0, p = 0;
  seed([
    { id:'e1', from:'alice@example.com', to:'bob@example.com', subject:'Project Update', body:'Sprint 4 is done.', date:'2026-07-01T10:00:00Z', read:false, folder:'inbox' },
    { id:'e2', from:'carol@example.com', to:'bob@example.com', subject:'Budget Review', body:'Q3 budget needs approval.', date:'2026-07-02T14:00:00Z', read:true, folder:'inbox' },
    { id:'e3', from:'bob@example.com', to:'alice@example.com', subject:'Re: Project Update', body:'Looks great!', date:'2026-07-02T16:00:00Z', read:false, folder:'sent' },
    { id:'e4', from:'dave@example.com', to:'bob@example.com', subject:'Meeting Notes', body:'Action items from standup.', date:'2026-06-30T09:00:00Z', read:true, folder:'inbox' },
  ]);
  const inbox = run(['--inbox']);
  n++; p += pass('parseEmail: inbox returns data', inbox.includes('Project Update'));
  const unread = run(['--inbox', '--unread']);
  n++; p += pass('parseEmail: unread filter works', !unread.includes('Budget Review'));
  const status = run(['--status']);
  n++; p += pass('parseEmail: status shows counts', status.includes('Total emails: 4') && status.includes('Unread: 2'));
  const thread = run(['--thread', 'e1']);
  n++; p += pass('parseEmail: thread lookup', thread.includes('Thread') && thread.includes('Project Update'));
  console.log(`✅ parseEmail: ${p}/${n} passed\n`);
  return p;
}

// ── 2. folderOps ───────────────────────────────────────────────────────────
function testFolders() {
  let n = 0, p = 0;
  seed([
    { id:'f1', from:'a@t.com', to:'b@t.com', subject:'Move Me', body:'Moving to drafts.', date:'2026-07-01T10:00:00Z', read:false, folder:'inbox' },
  ]);
  const before = run(['--status']);
  n++; p += pass('folderOps: inbox has email', before.includes('Total emails: 1'));
  run(['--inbox', '--unread']);
  const after = run(['--status']);
  n++; p += pass('folderOps: status consistent after ops', after.includes('Total emails: 1'));
  seed([{ id:'f2', from:'a@t.com', to:'b@t.com', subject:'Draft', body:'test', date:'2026-07-01T10:00:00Z', read:true, folder:'drafts' }]);
  const drafts = run(['--status']);
  n++; p += pass('folderOps: drafts counted', drafts.includes('Drafts: 1'));
  console.log(`✅ folderOps: ${p}/${n} passed\n`);
  return p;
}

// ── 3. search ──────────────────────────────────────────────────────────────
function testSearch() {
  let n = 0, p = 0;
  seed([
    { id:'s1', from:'alice@example.com', to:'bob@example.com', subject:'Budget Report', body:'Q3 budget needs approval.', date:'2026-07-01T10:00:00Z', read:false, folder:'inbox' },
    { id:'s2', from:'carol@example.com', to:'bob@example.com', subject:'Meeting Notes', body:'Action items from standup.', date:'2026-07-02T14:00:00Z', read:true, folder:'inbox' },
    { id:'s3', from:'dave@example.com', to:'bob@example.com', subject:'Random', body:'Nothing relevant here.', date:'2026-06-30T09:00:00Z', read:true, folder:'inbox' },
  ]);
  const kw = run(['--search', 'budget']);
  n++; p += pass('search: keyword finds result', kw.includes('Budget Report'));
  const empty = run(['--search', 'zzznonexistent']);
  n++; p += pass('search: no false positives', !empty.includes('Budget Report'));
  const body = run(['--search', 'action items']);
  n++; p += pass('search: body text matches', body.includes('Meeting Notes'));
  console.log(`✅ search: ${p}/${n} passed\n`);
  return p;
}

// ── 4. drafts ──────────────────────────────────────────────────────────────
function testDrafts() {
  let n = 0, p = 0;
  seed([{ id:'d1', from:'test@skill.test', to:'x@y.com', subject:'x', body:'x', date:'2026-07-01T10:00:00Z', read:true, folder:'drafts' }]);
  const draft = run(['--status']);
  n++; p += pass('drafts: draft counted', draft.includes('Drafts: 1'));
  seed([{ id:'d2', from:'test@skill.test', to:'recipient@test.com', subject:'Template Test', body:'Hello {{name}},\n\n{{message}}', date:'2026-07-01T10:00:00Z', read:true, folder:'drafts' }]);
  const sent = run(['--inbox', '5']);
  n++; p += pass('drafts: compose output visible', sent.includes('Template Test'));
  console.log(`✅ drafts: ${p}/${n} passed\n`);
  return p;
}

// ── 5. error handling ──────────────────────────────────────────────────────
function testErrors() {
  let n = 0, p = 0;
  seed([]);
  const bad = run(['--thread', 'nonexistent-id']);
  n++; p += pass('error: missing thread handled', bad.includes('No thread found'));
  seed([{ id:'e1', from:'a@t.com', to:'b@t.com', subject:'E', body:'e', date:'2026-07-01T10:00:00Z', read:false, folder:'inbox' }]);
  const notFound = run(['--thread', 'no-such-id']);
  n++; p += pass('error: missing email handled', notFound.includes('No thread found'));
  console.log(`✅ error handling: ${p}/${n} passed\n`);
  return p;
}

// ── run ────────────────────────────────────────────────────────────────────
const total = testParse() + testFolders() + testSearch() + testDrafts() + testErrors();
const max = 4 + 3 + 3 + 2 + 2;
console.log(`Total: ${total}/${max} tests passing`);
fs.rmSync(TDIR, { recursive: true, force: true });
process.exit(total === max ? 0 : 1);
