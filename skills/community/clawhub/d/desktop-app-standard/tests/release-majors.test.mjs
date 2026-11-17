import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

// Execute the version checks shipped in the app workflows against package-manager output.
function runGate(stack, targets, dependencies, cargoTree) {
  const workflow = fs.readFileSync(new URL(`../templates/workflows/release-${stack}.yml`, import.meta.url), 'utf8');
  const script = [...workflow.matchAll(/node <<'NODE'\r?\n([\s\S]*?)\r?\n +NODE\b/g)]
    .map(match => match[1]).find(source => source.includes('desktop-version-targets.json'));
  assert.ok(script, 'workflow must check installed dependencies against its target table');
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'desktop-release-'));
  const write = (file, data) => fs.writeFileSync(path.join(root, file), JSON.stringify(data));
  try {
    fs.mkdirSync(path.join(root, '.github'));
    write('.github/desktop-version-targets.json', targets);
    write('npm-tree.json', { dependencies });
    if (cargoTree) write('cargo-tree.json', cargoTree);
    return spawnSync(process.execPath, ['-'], {
      cwd: root, input: script, encoding: 'utf8', env: { ...process.env, RUNNER_TEMP: root },
    });
  } finally {
    fs.rmSync(root, { recursive: true });
  }
}

test('Electron release uses the target table from the application commit', () => {
  const policy = { npm: { electron: 100, 'electron-builder': 26, 'electron-updater': 6 } };
  const packages = { electron: { version: '100.2.3' }, 'electron-builder': { version: '26.1.0' }, 'electron-updater': { version: '6.1.0' } };
  assert.equal(runGate('electron', policy, packages).status, 0);
  for (const version of ['99.9.9', '100.3.0-beta.1']) {
    assert.notEqual(runGate('electron', policy, { ...packages, electron: { version } }).status, 0);
  }
});

test('Tauri release checks the workspace dependency and its JS API minor', () => {
  const policy = { npm: { '@tauri-apps/cli': 2, '@tauri-apps/api': 2 }, cargo: { tauri: 2, 'tauri-build': 2 } };
  const packages = { '@tauri-apps/cli': { version: '2.10.0' }, '@tauri-apps/api': { version: '2.8.0' } };
  const cargo = {
    workspace_members: ['app'],
    resolve: { nodes: [{ id: 'app', deps: [{ pkg: 'core' }, { pkg: 'build' }] }] },
    packages: [{ id: 'core', name: 'tauri', version: '2.8.2' }, { id: 'build', name: 'tauri-build', version: '2.6.0' }],
  };
  assert.equal(runGate('tauri', policy, packages, cargo).status, 0);
  assert.notEqual(runGate('tauri', policy, { ...packages, '@tauri-apps/api': { version: '2.9.0' } }, cargo).status, 0);
  cargo.packages[0].version = '1.8.2';
  assert.notEqual(runGate('tauri', policy, packages, cargo).status, 0);
});
