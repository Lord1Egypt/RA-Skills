'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');

const { extractThinkingEffort } = require('../src/proxy/trace/extractor');

describe('extractThinkingEffort (FIX-9 normalized reasoning effort)', () => {
  it('OpenAI reasoning.effort', () => {
    assert.equal(extractThinkingEffort({ reasoning: { effort: 'high' } }), 'high');
  });
  it('OpenAI flat reasoning_effort', () => {
    assert.equal(extractThinkingEffort({ reasoning_effort: 'minimal' }), 'minimal');
  });
  it('Anthropic thinking budget_tokens', () => {
    assert.equal(extractThinkingEffort({ thinking: { type: 'enabled', budget_tokens: 8000 } }), 'budget:8000');
  });
  it('Anthropic thinking type only', () => {
    assert.equal(extractThinkingEffort({ thinking: { type: 'enabled' } }), 'enabled');
  });
  it('output_config.effort', () => {
    assert.equal(extractThinkingEffort({ output_config: { effort: 'low' } }), 'low');
  });
  it('Gemini generationConfig.thinkingConfig.thinkingBudget', () => {
    assert.equal(extractThinkingEffort({ generationConfig: { thinkingConfig: { thinkingBudget: 1024 } } }), 'budget:1024');
  });
  it('metadata.thinking_effort fallback', () => {
    assert.equal(extractThinkingEffort({ metadata: { thinking_effort: 'medium' } }), 'medium');
  });
  it('empty when not requested', () => {
    assert.equal(extractThinkingEffort({ model: 'x', messages: [] }), '');
    assert.equal(extractThinkingEffort({}), '');
  });
});
