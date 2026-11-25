import assert from 'node:assert/strict';
import { execFile } from 'node:child_process';
import { mkdtemp, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';
import { fileURLToPath } from 'node:url';
import { promisify } from 'node:util';

const exec = promisify(execFile);

test('CRM preserves notes on null and lets the operator intentionally clear them', async (t) => {
  const temp = await mkdtemp(join(tmpdir(), 'amber-crm-notes-'));
  t.after(() => rm(temp, { recursive: true, force: true }));
  await exec(process.execPath, ['--input-type=commonjs', '-e', `
    const assert = require('node:assert/strict');
    const crm = require(process.argv[1]);
    async function main() {
      const phone = '+12025550142';
      const context = {};
      const update = (fields) => crm({ action: 'upsert_contact', phone, ...fields }, context);
      const notes = 'Operator follow-up';
      assert.equal((await update({context_notes: notes})).result.context_notes, notes);
      assert.equal((await update({name: 'Alex', context_notes: null})).result.context_notes, notes);
      assert.equal((await update({context_notes: ''})).result.context_notes, null);
    }
    main().catch(error => { console.error(error); process.exitCode = 1; });
  `, fileURLToPath(new URL('../../amber-skills/crm/handler.js', import.meta.url))], {
    env: { ...process.env, AMBER_CRM_DB_PATH: join(temp, 'crm.sqlite') },
  });
});

test('voice CRM is scoped to the call number while local MCP keeps cross-contact access', async (t) => {
  const { Client } = await import('@modelcontextprotocol/sdk/client/index.js');
  const { StdioClientTransport } = await import('@modelcontextprotocol/sdk/client/stdio.js');
  const { handleSkillCall, registerSkills } = await import('../dist/skills/router.js');

  const temp = await mkdtemp(join(tmpdir(), 'amber-crm-scope-'));
  const client = new Client({ name: 'amber-crm-test', version: '1.0.0' });
  t.after(async () => {
    await client.close();
    await rm(temp, { recursive: true, force: true });
  });
  const caller = '+12025550141';
  const otherContact = '+12025550142';
  const handlerCalls = [];
  registerSkills([{
    manifest: {
      name: 'crm',
      amber: {
        function_schema: { name: 'crm' },
        capabilities: ['query'],
        permissions: [],
        timeout_ms: 25,
      },
    },
    handler: async (args) => {
      handlerCalls.push(args);
      return { success: true };
    },
  }]);
  async function voiceCrm(args, callerId = caller) {
    let result;
    await handleSkillCall('crm', JSON.stringify(args), null, 'tool-call', {
      clawdClient: null,
      operatorName: 'Test Operator',
      callId: 'test-call',
      callerId,
      transcript: '',
      writeJsonl() {},
      sendFunctionCallOutput(_ws, _callId, output) { result = JSON.parse(output); },
    });
    return result;
  }
  assert.equal((await voiceCrm({ action: 'search_contacts', query: 'Other Contact' })).success, false);
  assert.equal((await voiceCrm({ action: 'lookup_contact', phone: otherContact })).success, false);
  assert.equal((await voiceCrm({ action: 'upsert_contact', phone: otherContact, name: 'Changed' })).success, false);
  assert.equal((await voiceCrm({ action: 'get_history' }, '')).success, false);
  assert.deepEqual(handlerCalls, []);
  assert.equal((await voiceCrm({ action: 'lookup_contact' })).success, true);
  assert.deepEqual(handlerCalls, [{ action: 'lookup_contact', phone: caller }]);

  await client.connect(new StdioClientTransport({
    command: process.execPath,
    args: [fileURLToPath(new URL('../dist/mcp-server.js', import.meta.url))],
    env: { AMBER_CRM_ENABLED: 'true', AMBER_CRM_DB_PATH: join(temp, 'crm.sqlite') },
  }));
  const operatorCrm = (args) => client.callTool({ name: 'crm', arguments: args });
  const created = await operatorCrm({ action: 'create', phone: otherContact, name: 'Other Contact' });
  assert.equal(created.isError, false, JSON.stringify(created));
  const search = await operatorCrm({ action: 'search', identifier: 'Other Contact' });
  assert.equal(search.isError, false, JSON.stringify(search));
  assert.match(search.content[0].text, /Other Contact/);
});
