import assert from 'node:assert/strict';
import { access, cp, mkdir, mkdtemp, rm, symlink, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import { loadSkills } from '../dist/skills/loader.js';

test('the local MCP server lists and invokes only operator-approved Calendar and CRM skills', async (t) => {
  const root = await mkdtemp(join(tmpdir(), 'amber-mcp-policy-'));
  t.after(() => rm(root, { recursive: true, force: true }));
  const runtime = join(root, 'runtime');
  const skills = join(root, 'amber-skills');
  await mkdir(runtime);
  await cp(new URL('../dist/', import.meta.url), join(runtime, 'dist'), { recursive: true });
  await symlink(new URL('../node_modules/', import.meta.url), join(runtime, 'node_modules'), 'dir');
  for (const file of ['package.json', 'bridge-credential.cjs', 'realtime-models.cjs']) {
    await cp(new URL(`../${file}`, import.meta.url), join(runtime, file));
  }
  for (const name of ['calendar', 'crm']) {
    const folder = join(skills, name);
    await mkdir(folder, { recursive: true });
    await writeFile(join(folder, 'handler.js'), `
      module.exports = async ({ action }) => ({ success: true, message: '${name}: ' + action });
    `);
  }
  const manifest = join(skills, 'SKILL_MANIFEST.json');
  async function check(approved) {
    await writeFile(manifest, JSON.stringify({ approvedSkills: approved }));
    const client = new Client({ name: 'amber-operator-policy-test', version: '1.0.0' });
    try {
      await client.connect(new StdioClientTransport({
        command: process.execPath,
        args: [join(runtime, 'dist', 'mcp-server.js')],
        env: { AMBER_CRM_ENABLED: 'true', BRIDGE_API_TOKEN: 'test-bridge' },
      }));
      const names = (await client.listTools()).tools.map((tool) => tool.name);
      assert(names.includes('contacts_lookup'));
      for (const [skill, tool] of [['calendar', 'calendar_query'], ['crm', 'crm']]) {
        const allowed = approved.includes(skill);
        assert.equal(names.includes(tool), allowed);
        const result = await client.callTool({ name: tool, arguments: { action: 'lookup' } });
        assert.equal(result.isError, !allowed);
        if (allowed) {
          assert.match(result.content[0].text, new RegExp(`^${skill}:`));
        } else {
          assert.match(result.content[0].text, /disabled by the operator's approved skill list/);
        }
      }
    } finally {
      await client.close();
    }
  }
  await check(['calendar', 'crm']);
  await check([]);
});

test('a disabled voice skill is never loaded even when the operator allowlists its directory', async (t) => {
  const root = await mkdtemp(join(tmpdir(), 'amber-voice-policy-'));
  t.after(() => rm(root, { recursive: true, force: true }));
  const crm = join(root, 'crm');
  const loadedMarker = join(root, 'handler-imported');
  await mkdir(crm);
  await writeFile(join(root, 'SKILL_MANIFEST.json'), JSON.stringify({ approvedSkills: ['crm'] }));
  await writeFile(join(crm, 'SKILL.md'), [
    '---',
    'name: crm',
    'metadata: {"amber":{"capabilities":["read"],"function_schema":{"name":"crm"}}}',
    '---',
  ].join('\n'));
  await writeFile(join(crm, 'handler.js'), `
    require('node:fs').writeFileSync(${JSON.stringify(loadedMarker)}, 'loaded');
    module.exports = async () => ({ success: true });
  `);

  assert.deepEqual(loadSkills(root, (manifest) => manifest.name !== 'crm'), []);
  await assert.rejects(access(loadedMarker), { code: 'ENOENT' });
  assert.deepEqual(loadSkills(root).map((skill) => skill.manifest.name), ['crm']);
  await access(loadedMarker);
});
