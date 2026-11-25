import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const load = async (name) => JSON.parse(await readFile(resolve(root, 'examples', name), 'utf8'));
const success = await load('success.json');
const failure = await load('failure.json');
assert.equal(success.status, 'completed');
assert.ok(success.titleVariants.length > 0);
assert.equal(failure.status, 'needs_user_input');
assert.ok(failure.missingFacts.length >= 2);
console.log('easy-xianyu-title-copy-free self-test: ok (success + failure samples)');
