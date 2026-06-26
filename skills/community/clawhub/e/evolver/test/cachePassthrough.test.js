'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');

const { rewriteModel } = require('../src/proxy/router/cache_passthrough');

describe('rewriteModel', () => {
  it('returns a clone with model rewritten', () => {
    const body = { model: 'claude-opus-4-7', messages: [{ role: 'user', content: 'hi' }] };
    const out = rewriteModel(body, 'claude-haiku-4-5');
    assert.equal(out.model, 'claude-haiku-4-5');
    assert.equal(body.model, 'claude-opus-4-7', 'input must not mutate');
    assert.notEqual(out, body, 'must return a fresh object');
  });

  it('preserves cache_control breakpoints on messages array', () => {
    const breakpoint = { type: 'ephemeral' };
    const body = {
      model: 'claude-opus-4-7',
      messages: [
        {
          role: 'user',
          content: [
            { type: 'text', text: 'long context...', cache_control: breakpoint },
            { type: 'text', text: 'question' },
          ],
        },
      ],
    };
    const out = rewriteModel(body, 'claude-sonnet-4-6');
    assert.equal(out.messages, body.messages, 'messages array identity preserved');
    assert.equal(out.messages[0].content[0].cache_control, breakpoint);
  });

  it('returns input when newModel is missing or same', () => {
    const body = { model: 'x' };
    assert.equal(rewriteModel(body, null), body);
    assert.equal(rewriteModel(body, undefined), body);
    assert.equal(rewriteModel(body, 'x'), body, 'same model -> no clone');
  });

  it('returns input when body is not an object', () => {
    assert.equal(rewriteModel(null, 'x'), null);
    assert.equal(rewriteModel(undefined, 'x'), undefined);
    assert.equal(rewriteModel('raw', 'x'), 'raw');
  });
});
