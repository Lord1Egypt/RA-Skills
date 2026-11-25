import assert from 'node:assert/strict';
import { chmodSync, mkdtempSync, readFileSync, rmSync, statSync, symlinkSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';
import { writePrivateFile } from '../write-private-file.js';

test('setup keeps new and existing configuration owner-only, including symlink targets', (t) => {
  const dir = mkdtempSync(join(tmpdir(), 'amber-setup-config-'));
  t.after(() => rmSync(dir, { recursive: true, force: true }));
  const configPath = join(dir, 'settings');
  const envPath = join(dir, '.env');
  writePrivateFile(configPath, 'MODE=old-value\n');
  assert.equal(statSync(configPath).mode & 0o777, 0o600);
  chmodSync(configPath, 0o644);
  symlinkSync(configPath, envPath);
  writePrivateFile(envPath, 'MODE=new\n');
  assert.equal(statSync(configPath).mode & 0o777, 0o600);
  assert.equal(readFileSync(configPath, 'utf8'), 'MODE=new\n');
});
