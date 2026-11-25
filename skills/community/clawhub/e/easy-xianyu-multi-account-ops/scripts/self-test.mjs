import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const load = async (name) => JSON.parse(await readFile(resolve(root, 'examples', name), 'utf8'));
const success = await load('success.json');
const failure = await load('failure.json');
assert.equal(success.accounts.length, 2);
assert.notEqual(success.accounts[0].browserId, success.accounts[1].browserId);
assert.ok(success.accounts.every((account) => account.status === 'completed'));
assert.equal(failure.accounts[0].status, 'needs_user_action');
assert.ok(failure.accounts[0].errors.length > 0);
console.log('easy-xianyu-multi-account-ops self-test: ok (success + failure samples)');
