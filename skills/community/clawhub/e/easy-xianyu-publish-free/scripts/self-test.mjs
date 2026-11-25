import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const load = async (name) => JSON.parse(await readFile(resolve(root, 'examples', name), 'utf8'));
const success = await load('success.json');
const failure = await load('failure.json');
assert.equal(success.status, 'draft_ready');
assert.equal(success.missingFields.length, 0);
assert.match(success.browserId, /^easybr-/);
assert.equal(failure.status, 'needs_user_action');
assert.ok(failure.errors.length > 0);
console.log('easy-xianyu-publish-free self-test: ok (success + failure samples)');
