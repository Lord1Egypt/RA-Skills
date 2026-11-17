const { test } = require('node:test');
const assert = require('node:assert/strict');
const { labelled, socialOf, parseArgs } = require('../lib/cli');

test('a label is optional and a bare number keeps its colons-free value', () => {
  assert.deepEqual(labelled('mobile:+49 176 1'), { label: 'mobile', value: '+49 176 1' });
  assert.deepEqual(labelled('+49 176 1'), { value: '+49 176 1' });
});

test('a numeric social handle is an id, anything else a username', () => {
  assert.deepEqual(socialOf('discord:123456789012345678'), { service: 'discord', userIdentifier: '123456789012345678' });
  assert.deepEqual(socialOf('telegram:@ana'), { service: 'telegram', username: 'ana' });
  assert.equal(parseArgs(['update', 'x', '--phone']).ok, false);
});
