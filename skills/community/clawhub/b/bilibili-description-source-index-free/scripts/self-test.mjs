#!/usr/bin/env node
import { execFileSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const run = (fixture) => JSON.parse(execFileSync(process.execPath, ['scripts/index-visible-links.mjs', '--input', `fixtures/${fixture}`, '--source-url', 'https://www.bilibili.com/video/BVfixture'], { cwd: root, encoding: 'utf8' }));
const success = run('success.html');
const failure = run('failure.html');
if (success.items.length !== 2 || success.gaps.length !== 0) throw new Error('success fixture was not indexed');
if (failure.items.length !== 0 || !failure.gaps[0]?.reason.includes('不可见')) throw new Error('failure fixture was not recorded');
console.log('self-test passed: success links indexed; restricted description recorded.');
