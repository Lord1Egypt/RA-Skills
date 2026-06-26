'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');

const { extractFeatures } = require('../src/proxy/router/features');

describe('extractFeatures', () => {
  it('returns zeroed feature set for empty body', () => {
    const f = extractFeatures({});
    assert.equal(f.last_assistant_tool_call_count, 0);
    assert.equal(f.last_assistant_had_tool_call, false);
    assert.equal(f.last_user_is_tool_result_only, false);
    assert.equal(f.user_requested_planning, false);
    assert.equal(f.user_simple_lookup, false);
    assert.equal(f.last_assistant_output_tokens, 0);
    assert.equal(f.last_assistant_stop_reason, null);
  });

  it('synthesizes stop_reason ToolUse when last assistant emitted tool_use', () => {
    const f = extractFeatures({
      messages: [
        { role: 'user', content: 'go' },
        {
          role: 'assistant',
          content: [{ type: 'tool_use', id: 't1', name: 'a', input: {} }],
        },
      ],
    });
    assert.equal(f.last_assistant_stop_reason, 'ToolUse');
  });

  it('synthesizes stop_reason Stop for text-only assistant tail', () => {
    const f = extractFeatures({
      messages: [
        { role: 'user', content: 'go' },
        { role: 'assistant', content: 'done' },
      ],
    });
    assert.equal(f.last_assistant_stop_reason, 'Stop');
  });

  it('counts tool_use blocks in the last assistant message', () => {
    const body = {
      messages: [
        { role: 'user', content: 'go' },
        {
          role: 'assistant',
          content: [
            { type: 'text', text: 'ok' },
            { type: 'tool_use', id: 't1', name: 'a', input: {} },
            { type: 'tool_use', id: 't2', name: 'b', input: {} },
          ],
        },
        { role: 'user', content: [{ type: 'tool_result', tool_use_id: 't1', content: 'x' }] },
      ],
    };
    const f = extractFeatures(body);
    assert.equal(f.last_assistant_tool_call_count, 2);
    assert.equal(f.last_assistant_had_tool_call, true);
  });

  it('detects tool-result-only tail user message', () => {
    const body = {
      messages: [
        {
          role: 'assistant',
          content: [{ type: 'tool_use', id: 't1', name: 'a', input: {} }],
        },
        {
          role: 'user',
          content: [
            { type: 'tool_result', tool_use_id: 't1', content: 'x' },
            { type: 'tool_result', tool_use_id: 't2', content: 'y' },
          ],
        },
      ],
    };
    const f = extractFeatures(body);
    assert.equal(f.last_user_is_tool_result_only, true);
    assert.equal(f.user_simple_lookup, false, 'tool_result-only tail is not a simple lookup');
  });

  it('rejects tool-result-only when tail also has text blocks', () => {
    const body = {
      messages: [
        {
          role: 'user',
          content: [
            { type: 'tool_result', tool_use_id: 't1', content: 'x' },
            { type: 'text', text: 'also a comment' },
          ],
        },
      ],
    };
    const f = extractFeatures(body);
    assert.equal(f.last_user_is_tool_result_only, false);
  });

  it('flags planning keywords in last user text', () => {
    const cases = [
      'can we plan the migration?',
      'Help me design the schema.',
      "Let's think through this carefully.",
      'Outline the steps please.',
    ];
    for (const text of cases) {
      const f = extractFeatures({ messages: [{ role: 'user', content: text }] });
      assert.equal(f.user_requested_planning, true, `expected planning for: ${text}`);
      assert.equal(f.user_simple_lookup, false, `planning must not also be simple lookup: ${text}`);
    }
  });

  it('flags simple lookup for short queries with no tool_result or planning', () => {
    const f = extractFeatures({ messages: [{ role: 'user', content: 'what is npm install?' }] });
    assert.equal(f.user_simple_lookup, true);
    assert.equal(f.user_requested_planning, false);
  });

  it('does not flag simple lookup for long text', () => {
    const long = 'a'.repeat(200);
    const f = extractFeatures({ messages: [{ role: 'user', content: long }] });
    assert.equal(f.user_simple_lookup, false);
  });

  it('handles string content (not just block arrays)', () => {
    const f = extractFeatures({
      messages: [
        { role: 'user', content: 'hi' },
        { role: 'assistant', content: 'hello back' },
        { role: 'user', content: 'short follow-up' },
      ],
    });
    assert.equal(f.last_assistant_tool_call_count, 0);
    assert.equal(f.last_assistant_had_tool_call, false);
    assert.equal(f.user_simple_lookup, true);
  });
});
