import assert from 'node:assert/strict';
import { execFile } from 'node:child_process';
import { copyFile, mkdir, mkdtemp, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';
import { promisify } from 'node:util';

const exec = promisify(execFile);

test('build watcher restarts only the configured launchd service without provider credentials', async (t) => {
  const root = await mkdtemp(join(tmpdir(), 'amber-watcher-'));
  t.after(() => rm(root, { recursive: true, force: true }));
  await mkdir(join(root, 'scripts'));
  await mkdir(join(root, 'dist'));
  await writeFile(join(root, 'dist', 'index.js'), '');
  const script = join(root, 'scripts', 'dist-watcher.cjs');
  await copyFile(new URL('../scripts/dist-watcher.cjs', import.meta.url), script);

  await exec(process.execPath, ['--input-type=commonjs', '-e', `
    const assert = require('node:assert/strict');
    const childProcess = require('node:child_process');
    const uid = process.getuid?.() ?? 501;
    process.getuid = () => uid;
    const calls = [];
    childProcess.spawnSync = (file, args, options) => {
      assert.deepEqual(options.env, { LC_ALL: 'C' });
      calls.push([file, args]);
      if (file === '/bin/launchctl') {
        return { status: 0, stdout: 'PID Status Label\\n817 0 unrelated-node-app\\n8124 0 com.jarvis.twilio-bridge\\n' };
      }
      assert.equal(file, '/bin/ps');
      return { status: 0, stdout: 'Fri Feb 20 18:00:00 2026' };
    };
    childProcess.execFileSync = (file, args, options) => {
      assert.deepEqual(options.env, { LC_ALL: 'C' });
      calls.push([file, args]);
    };
    global.setInterval = () => {};
    require(process.argv[1]);
    assert.deepEqual(calls, [
      ['/bin/launchctl', ['list']],
      ['/bin/ps', ['-p', '8124', '-o', 'lstart=']],
      ['/bin/launchctl', ['kickstart', '-k', 'gui/' + uid + '/com.jarvis.twilio-bridge']],
    ]);
  `, script]);
});
