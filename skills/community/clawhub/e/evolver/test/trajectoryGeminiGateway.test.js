'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');

const { buildTrajectoryFromRows } = require('../src/gep/trajectoryExport');

// FIX-2: Gemini / Vertex gateway tool-call reconstruction. Gemini threads tool calls through
// candidates[].content.parts[].functionCall (camelCase, no `type`), which the type-based scanners
// never recognized. These rows assert both non-streaming and streaming Gemini tool calls surface.

describe('Gemini gateway tool-call reconstruction (FIX-2)', () => {
  it('non-streaming: candidates[].content.parts[].functionCall -> tool_call', () => {
    const trajectory = buildTrajectoryFromRows('sess_gemini', [{
      prism_compatible: true,
      requestId: 'req_gem',
      createdAtIso: '2026-06-24T00:00:00.000Z',
      sessionId: 'sess_gemini',
      path: '/v1beta/models/gemini-3-pro:generateContent',
      upstream: 'gemini',
      model: 'gemini-3-pro',
      status: 200,
      requestBody: JSON.stringify({
        contents: [
          { role: 'user', parts: [{ text: 'List files in the repo root' }] },
        ],
        tools: [{ functionDeclarations: [{ name: 'list_dir' }] }],
      }),
      responseBody: JSON.stringify({
        candidates: [{
          content: {
            role: 'model',
            parts: [
              { text: 'Let me look.' },
              { functionCall: { name: 'list_dir', args: { path: '.' } } },
            ],
          },
          finishReason: 'STOP',
        }],
        usageMetadata: { promptTokenCount: 10, candidatesTokenCount: 5 },
      }),
    }]);

    assert.ok(trajectory);
    assert.equal(trajectory.stats.has_tool_calls, true);
    const calls = trajectory.turns[0].tool_calls.filter((c) => !c.declared && c.name !== 'tool_result');
    const listDir = calls.find((c) => c.name === 'list_dir');
    assert.ok(listDir, 'list_dir functionCall must be reconstructed');
    assert.deepEqual(listDir.input, { path: '.' });
  });

  it('streaming: functionCall in a captured stream chunk + functionResponse pairing', () => {
    const trajectory = buildTrajectoryFromRows('sess_gemini_stream', [{
      prism_compatible: true,
      requestId: 'req_gem_stream',
      createdAtIso: '2026-06-24T00:01:00.000Z',
      sessionId: 'sess_gemini_stream',
      path: '/v1beta/models/gemini-3-pro:streamGenerateContent',
      upstream: 'gemini',
      model: 'gemini-3-pro',
      status: 200,
      isStream: true,
      requestBody: JSON.stringify({
        contents: [
          { role: 'user', parts: [{ text: 'run the tests' }] },
          { role: 'function', parts: [{ functionResponse: { name: 'run_tests', response: { ok: true } } }] },
        ],
      }),
      responseBody: JSON.stringify({
        events: [
          { candidates: [{ content: { role: 'model', parts: [{ text: 'ok' }] } }] },
          { candidates: [{ content: { role: 'model', parts: [{ functionCall: { name: 'run_tests', args: { suite: 'unit' } } }] } }], usageMetadata: { promptTokenCount: 3, candidatesTokenCount: 2 } },
        ],
      }),
    }]);

    assert.ok(trajectory);
    assert.equal(trajectory.stats.has_tool_calls, true);
    const names = trajectory.turns[0].tool_calls.map((c) => c.name);
    assert.ok(names.includes('run_tests'), 'streaming functionCall must surface');
    assert.ok(names.includes('tool_result'), 'request-side functionResponse must surface as a tool_result');
  });
});
