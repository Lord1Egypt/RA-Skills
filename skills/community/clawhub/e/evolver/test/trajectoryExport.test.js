'use strict';

const { describe, it } = require('node:test');
const assert = require('node:assert/strict');
const { spawnSync } = require('node:child_process');
const crypto = require('node:crypto');
const fs = require('fs');
const os = require('os');
const path = require('path');

const INDEX_JS = path.join(__dirname, '..', 'index.js');

const {
  buildTrajectories,
  buildTrajectoryFromRows,
  buildTrajectoryFromSessionLog,
  readTraceRowsDetailed,
  writeTrajectories,
} = require('../src/gep/trajectoryExport');

function encryptRowWithKey(row, key, extra = {}) {
  const iv = crypto.randomBytes(12);
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  const ciphertext = Buffer.concat([cipher.update(JSON.stringify(row), 'utf8'), cipher.final()]);
  return {
    encrypted: true,
    algorithm: 'aes-256-gcm',
    payload_schema: 'prism_trace_row',
    iv: iv.toString('base64'),
    tag: cipher.getAuthTag().toString('base64'),
    ciphertext: ciphertext.toString('base64'),
    ...extra,
  };
}

function encryptRowWithNodeSecret(row, nodeSecret, version) {
  const key = crypto.createHash('sha256').update('evomap-proxy-trace-v1:' + nodeSecret, 'utf8').digest();
  return encryptRowWithKey(row, key, version ? { secret_version: version } : {});
}

function encryptRowWithHubKey(row, publicPem) {
  const key = crypto.randomBytes(32);
  const wrapped = crypto.publicEncrypt(
    {
      key: publicPem,
      padding: crypto.constants.RSA_PKCS1_OAEP_PADDING,
      oaepHash: 'sha256',
    },
    key,
  );
  return encryptRowWithKey(row, key, {
    hub_key_envelope: {
      algorithm: 'rsa-oaep-sha256',
      key_id: 'test-key',
      wrapped_key: wrapped.toString('base64'),
    },
  });
}

describe('trajectoryExport', () => {
  it('groups proxy traces into session-level coding trajectories', () => {
    const rows = [
      {
        prism_compatible: true,
        requestId: 'req_a',
        createdAtIso: '2026-06-23T01:00:00.000Z',
        sessionId: 'sess_1',
        path: '/v1/messages',
        upstream: 'anthropic',
        model: 'claude-test',
        status: 200,
        durationMs: 10,
        input_tokens: 11,
        output_tokens: 7,
        requestBody: JSON.stringify({
          model: 'claude-test',
          messages: [
            { role: 'user', content: 'Fix the TypeScript parser test' },
            {
              role: 'assistant',
              content: [{ type: 'tool_use', id: 'tool_1', name: 'exec_command', input: { cmd: 'pnpm test' } }],
            },
          ],
        }),
        responseBody: JSON.stringify({
          id: 'msg_1',
          stop_reason: 'end_turn',
          content: [{ type: 'tool_use', id: 'tool_1', name: 'exec_command', input: { cmd: 'pnpm test' } }],
        }),
      },
      {
        prism_compatible: true,
        requestId: 'req_b',
        createdAtIso: '2026-06-23T01:01:00.000Z',
        sessionId: 'sess_2',
        path: '/v1/responses',
        upstream: 'openai',
        model: 'gpt-test',
        status: 200,
        durationMs: 12,
        input_tokens: 5,
        output_tokens: 6,
        responseId: 'resp_1',
        requestBody: JSON.stringify({ model: 'gpt-test', instructions: 'Review Python code' }),
        responseBody: JSON.stringify({ id: 'resp_1', status: 'completed' }),
      },
    ];

    const trajectories = buildTrajectories(rows);
    assert.equal(trajectories.length, 2);
    const first = trajectories.find((t) => t.session_id === 'sess_1');
    assert.ok(first);
    assert.equal(first.schema, 'evomap.coding_trajectory.v1');
    assert.equal(first.task, 'Fix the TypeScript parser test');
    assert.equal(first.stats.turns, 1);
    assert.equal(first.stats.input_tokens, 11);
    assert.equal(first.stats.output_tokens, 7);
    assert.equal(first.stats.has_tool_calls, true);
    assert.equal(first.stats.tool_types.exec_command, 1);
    assert.ok(first.languages.includes('typescript'));

    const second = trajectories.find((t) => t.session_id === 'sess_2');
    assert.ok(second);
    assert.deepEqual(second.providers, ['openai']);
    assert.deepEqual(second.endpoints, ['/v1/responses']);
    assert.equal(second.task, 'Review Python code');
    assert.equal(second.turns[0].response_id, 'resp_1');
    assert.ok(second.languages.includes('python'));
  });

  it('marks failed turns as failure-correction candidates', () => {
    const trajectory = buildTrajectoryFromRows('sess_fail', [{
      prism_compatible: true,
      requestId: 'req_fail',
      createdAtIso: '2026-06-23T01:00:00.000Z',
      sessionId: 'sess_fail',
      path: '/v1/chat/completions',
      upstream: 'openai',
      model: 'gpt-test',
      status: 429,
      errorMessage: 'rate_limit_exceeded',
      requestBody: JSON.stringify({ model: 'gpt-test', messages: [{ role: 'user', content: 'hello' }] }),
      responseBody: JSON.stringify({ error: { type: 'rate_limit_exceeded' } }),
    }]);

    assert.equal(trajectory.stats.has_failure_correction, true);
    assert.equal(trajectory.turns[0].provider, 'openai');
    assert.equal(trajectory.turns[0].endpoint, '/v1/chat/completions');
  });

  it('normalizes Bedrock provider aliases to the Anthropic Bedrock taxonomy', () => {
    const trajectory = buildTrajectoryFromRows('sess_bedrock', [
      {
        prism_compatible: true,
        requestId: 'req_bedrock_upstream',
        createdAtIso: '2026-06-23T01:00:00.000Z',
        sessionId: 'sess_bedrock',
        path: '/v1/messages',
        upstream: 'aws-bedrock',
        model: 'claude-test',
        status: 200,
        requestBody: JSON.stringify({ model: 'claude-test', messages: [{ role: 'user', content: 'Summarize Bedrock output' }] }),
        responseBody: JSON.stringify({ content: [{ type: 'text', text: 'done' }] }),
      },
      {
        prism_compatible: true,
        requestId: 'req_bedrock_provider',
        createdAtIso: '2026-06-23T01:01:00.000Z',
        sessionId: 'sess_bedrock',
        path: '/v1/messages',
        provider: 'aws-bedrock',
        model: 'claude-test',
        status: 200,
        requestBody: JSON.stringify({ model: 'claude-test', messages: [{ role: 'user', content: 'Continue Bedrock output' }] }),
        responseBody: JSON.stringify({ content: [{ type: 'text', text: 'done' }] }),
      },
    ]);

    assert.deepEqual(trajectory.providers, ['aws-bedrock-anthropic']);
    assert.deepEqual(trajectory.turns.map((turn) => turn.provider), [
      'aws-bedrock-anthropic',
      'aws-bedrock-anthropic',
    ]);
  });

  it('extracts task and tool calls from OpenAI Responses shapes', () => {
    const trajectory = buildTrajectoryFromRows('sess_openai', [{
      prism_compatible: true,
      requestId: 'req_openai',
      createdAtIso: '2026-06-23T01:00:00.000Z',
      sessionId: 'sess_openai',
      path: '/v1/responses',
      upstream: 'openai',
      model: 'gpt-test',
      status: 200,
      responseId: 'resp_tool',
      previousResponseId: 'resp_prev',
      requestBody: JSON.stringify({
        model: 'gpt-test',
        input: 'Patch the Go parser',
        previous_response_id: 'resp_prev',
        tools: [{ type: 'function', name: 'exec_command' }],
      }),
      responseBody: JSON.stringify({
        id: 'resp_tool',
        output: [{ type: 'function_call', call_id: 'call_1', name: 'exec_command' }],
      }),
    }]);

    assert.equal(trajectory.task, 'Patch the Go parser');
    assert.equal(trajectory.stats.has_tool_calls, true);
    assert.equal(trajectory.stats.tool_types.exec_command, 1);
    assert.equal(trajectory.turns[0].tool_calls.length, 2);
    assert.equal(trajectory.turns[0].response_id, 'resp_tool');
    assert.equal(trajectory.turns[0].previous_response_id, 'resp_prev');
    assert.ok(trajectory.languages.includes('go'));
  });

  it('extracts OpenAI Responses request input tool calls and failed tool outputs', () => {
    const trajectory = buildTrajectoryFromRows('sess_openai_input_tools', [{
      prism_compatible: true,
      requestId: 'req_openai_input_tools',
      createdAtIso: '2026-06-23T01:00:00.000Z',
      sessionId: 'sess_openai_input_tools',
      path: '/v1/responses',
      upstream: 'openai',
      model: 'gpt-test',
      status: 200,
      requestBody: JSON.stringify({
        model: 'gpt-test',
        input: [
          { role: 'user', content: 'Run the pytest suite and fix failures' },
          {
            type: 'function_call',
            call_id: 'call_pytest_fake',
            name: 'exec_command',
            arguments: '{"cmd":"pytest test_fake.py"}',
          },
          {
            type: 'function_call_output',
            call_id: 'call_pytest_fake',
            output: 'pytest failed: 1 failed; command exited with code 1',
          },
        ],
      }),
      responseBody: JSON.stringify({ id: 'resp_after_input_tools', status: 'completed' }),
    }]);

    assert.equal(trajectory.stats.has_tool_calls, true);
    assert.equal(trajectory.stats.tool_call_count, 2);
    assert.equal(trajectory.stats.tool_types.exec_command, 1);
    assert.equal(trajectory.stats.tool_types.tool_result, 1);
    assert.equal(trajectory.stats.has_failure_correction, true);
    assert.equal(trajectory.turns[0].tool_calls.length, 2);
    assert.equal(trajectory.turns[0].tool_calls[0].name, 'exec_command');
    assert.equal(trajectory.turns[0].tool_calls[0].id, 'call_pytest_fake');
    assert.equal(trajectory.turns[0].tool_calls[1].name, 'tool_result');
    assert.equal(trajectory.turns[0].tool_calls[1].id, 'call_pytest_fake');
    assert.equal(trajectory.turns[0].tool_calls[1].arguments, 'pytest failed: 1 failed; command exited with code 1');
    assert.equal(Object.prototype.hasOwnProperty.call(trajectory.turns[0].tool_calls[1], 'content'), false);
    assert.equal(Object.prototype.hasOwnProperty.call(trajectory.turns[0].tool_calls[1], 'output'), false);
  });

  it('accepts v2 llm_turn rows and normalizes trajectory fields', () => {
    const trajectory = buildTrajectoryFromRows('', [{
      event: 'llm_turn',
      ts: '2026-06-23T01:00:00.000Z',
      request_id: 'req_v2',
      session_id: 'sess_v2',
      response_id: 'resp_v2',
      previous_response_id: 'resp_prev_v2',
      route: 'POST /v1/responses',
      provider: 'openai',
      chosen_model: 'gpt-chosen',
      original_model: 'gpt-original',
      latency_ms: 123,
      stream: true,
      stop_reason: 'completed',
      usage: { input_tokens: 31, output_tokens: 17 },
      request_body: JSON.stringify({
        model: 'gpt-original',
        input: 'Normalize v2 trace rows',
        previous_response_id: 'resp_prev_v2',
      }),
      response_body: JSON.stringify({ id: 'resp_v2', status: 'completed' }),
    }]);

    assert.equal(trajectory.session_id, 'sess_v2');
    assert.deepEqual(trajectory.providers, ['openai']);
    assert.deepEqual(trajectory.endpoints, ['/v1/responses']);
    assert.equal(trajectory.task, 'Normalize v2 trace rows');
    assert.equal(trajectory.stats.input_tokens, 31);
    assert.equal(trajectory.stats.output_tokens, 17);

    const turn = trajectory.turns[0];
    assert.equal(turn.request_id, 'req_v2');
    assert.equal(turn.timestamp, '2026-06-23T01:00:00.000Z');
    assert.equal(turn.provider, 'openai');
    assert.equal(turn.endpoint, '/v1/responses');
    assert.equal(turn.model, 'gpt-chosen');
    assert.equal(turn.chosen_model, 'gpt-chosen');
    assert.equal(turn.original_model, 'gpt-original');
    assert.equal(turn.duration_ms, 123);
    assert.equal(turn.is_stream, true);
    assert.equal(turn.finish_reason, 'completed');
    assert.equal(turn.response_id, 'resp_v2');
    assert.equal(turn.previous_response_id, 'resp_prev_v2');
    assert.equal(turn.input_tokens, 31);
    assert.equal(turn.output_tokens, 17);
    assert.equal(Object.prototype.hasOwnProperty.call(turn, 'error'), false);
  });

  it('preserves row error fields and treats row.error as a failure signal', () => {
    const trajectory = buildTrajectoryFromRows('sess_v2_error', [
      {
        event: 'llm_turn',
        ts: '2026-06-23T01:00:00.000Z',
        request_id: 'req_error',
        session_id: 'sess_v2_error',
        route: '/v1/responses',
        provider: 'openai',
        error: 'upstream stream error: synthetic failure',
        errorMessage: 'legacy error should not win',
        stream: true,
        request_body: JSON.stringify({ model: 'gpt-test', input: 'stream failed' }),
        response_body: JSON.stringify({ reconstructed_stream: true, events: [] }),
      },
      {
        event: 'llm_turn',
        ts: '2026-06-23T01:01:00.000Z',
        request_id: 'req_error_message',
        session_id: 'sess_v2_error',
        route: '/v1/responses',
        provider: 'openai',
        errorMessage: 'fallback error message',
        request_body: JSON.stringify({ model: 'gpt-test', input: 'request failed' }),
        response_body: JSON.stringify({ id: 'resp_after_error' }),
      },
    ]);

    assert.equal(trajectory.stats.has_failure_correction, true);
    assert.equal(trajectory.stats.has_incomplete_turns, true);
    assert.equal(trajectory.turns[0].error, 'upstream stream error: synthetic failure');
    assert.deepEqual(trajectory.turns[0].incomplete_reasons, ['stream_error']);
    assert.equal(trajectory.turns[1].error, 'fallback error message');
  });

  it('preserves row-level trajectory parity fields and row-level tool calls', () => {
    const reasoning = { summary: 'selected edit then validation' };
    const diff = 'diff --git a/file.js b/file.js';
    const validation = { commands: ['pnpm test'] };
    const trajectory = buildTrajectoryFromRows('sess_row_parity', [{
      prism_compatible: true,
      requestId: 'req_row_parity',
      createdAtIso: '2026-06-23T01:00:00.000Z',
      sessionId: 'sess_row_parity',
      path: '/v1/responses',
      upstream: 'openai',
      model: 'gpt-test',
      status: 200,
      body_truncated: true,
      redaction: 'evolver-redact-v2',
      reasoning,
      diff,
      validation,
      tool_calls: [
        { id: 'call_patch', name: 'apply_patch', arguments: '{"patch":"*** Begin Patch"}', bytes: 50 },
        { id: 'call_test', name: 'exec_command', input: { cmd: 'pnpm test' }, bytes: 30 },
      ],
      requestBody: JSON.stringify({
        model: 'gpt-test',
        input: 'Patch and validate',
        tools: [{ type: 'function', function: { name: 'apply_patch' } }],
      }),
      responseBody: JSON.stringify({
        output: [
          { type: 'function_call', call_id: 'call_patch', name: 'apply_patch', arguments: '{"patch":"*** Begin Patch"}' },
        ],
      }),
    }]);

    const turn = trajectory.turns[0];
    assert.equal(turn.reasoning, reasoning);
    assert.equal(turn.diff, diff);
    assert.equal(turn.validation, validation);
    assert.equal(turn.redaction, 'evolver-redact-v2');
    assert.equal(turn.body_truncated, true);
    assert.equal(turn.response_events_truncated, true);
    assert.deepEqual(turn.incomplete_reasons, ['body_truncated']);
    assert.equal(turn.tool_calls.filter((call) => call.id === 'call_patch' && !call.declared).length, 1);
    assert.ok(turn.tool_calls.some((call) => (
      call.id === 'call_test'
      && call.name === 'exec_command'
      && call.input.cmd === 'pnpm test'
    )));
    assert.equal(trajectory.stats.tool_call_count, 2);
    assert.deepEqual(trajectory.stats.tool_types, { apply_patch: 1, exec_command: 1 });
    assert.equal(trajectory.stats.has_code_edit, true);
    assert.equal(trajectory.stats.has_test_execution, true);
    assert.deepEqual(trajectory.stats.test_commands, ['pnpm test']);
    assert.equal(trajectory.stats.has_truncated_stream, true);
    assert.equal(trajectory.stats.has_incomplete_turns, true);
  });

  it('extracts OpenAI Chat Completions tool calls', () => {
    const trajectory = buildTrajectoryFromRows('sess_chat', [{
      prism_compatible: true,
      requestId: 'req_chat',
      createdAtIso: '2026-06-23T01:00:00.000Z',
      sessionId: 'sess_chat',
      path: '/v1/chat/completions',
      upstream: 'openai',
      model: 'gpt-test',
      status: 200,
      requestBody: JSON.stringify({
        model: 'gpt-test',
        messages: [{ role: 'user', content: 'Run the Python test' }],
        tools: [{ type: 'function', function: { name: 'exec_command' } }],
      }),
      responseBody: JSON.stringify({
        choices: [{
          message: {
            tool_calls: [{
              id: 'call_1',
              type: 'function',
              function: { name: 'exec_command', arguments: '{}' },
            }],
          },
        }],
      }),
    }]);

    assert.equal(trajectory.task, 'Run the Python test');
    assert.equal(trajectory.stats.tool_types.exec_command, 1);
    assert.equal(trajectory.turns[0].endpoint, '/v1/chat/completions');
    assert.ok(trajectory.languages.includes('python'));
  });

  it('does not count declared tools as actual tool calls', () => {
    const trajectory = buildTrajectoryFromRows('sess_declared_only', [{
      prism_compatible: true,
      requestId: 'req_declared_only',
      createdAtIso: '2026-06-23T01:00:00.000Z',
      sessionId: 'sess_declared_only',
      path: '/v1/responses',
      upstream: 'openai',
      model: 'gpt-test',
      status: 200,
      requestBody: JSON.stringify({
        model: 'gpt-test',
        input: 'Say hello',
        tools: [{ type: 'function', name: 'exec_command' }],
      }),
      responseBody: JSON.stringify({
        id: 'resp_plain',
        status: 'completed',
        output: [{ type: 'message', content: [{ type: 'output_text', text: 'hello' }] }],
      }),
    }]);

    assert.equal(trajectory.stats.has_tool_calls, false);
    assert.equal(trajectory.stats.tool_call_count, 0);
    assert.deepEqual(trajectory.stats.tool_types, {});
    assert.equal(trajectory.turns[0].tool_calls.length, 1);
    assert.equal(trajectory.turns[0].tool_calls[0].declared, true);
    assert.equal(trajectory.turns[0].request_body.model, 'gpt-test');
    assert.equal(trajectory.turns[0].response_body.id, 'resp_plain');
  });

  it('detects code edits and test execution from tool call arguments', () => {
    const trajectory = buildTrajectoryFromRows('sess_edit_test', [{
      prism_compatible: true,
      requestId: 'req_edit_test',
      createdAtIso: '2026-06-23T01:00:00.000Z',
      sessionId: 'sess_edit_test',
      path: '/v1/messages',
      upstream: 'anthropic',
      model: 'claude-test',
      status: 200,
      requestBody: JSON.stringify({ model: 'claude-test', messages: [{ role: 'user', content: 'Patch and test' }] }),
      responseBody: JSON.stringify({
        id: 'msg_1',
        stop_reason: 'end_turn',
        content: [
          { type: 'tool_use', id: 'tool_patch', name: 'apply_patch', input: { patch: '*** Begin Patch\n*** End Patch' } },
          { type: 'tool_use', id: 'tool_test', name: 'exec_command', input: { cmd: 'pnpm test' } },
        ],
      }),
    }]);

    assert.equal(trajectory.stats.has_code_edit, true);
    assert.equal(trajectory.stats.has_test_execution, true);
    assert.deepEqual(trajectory.stats.test_commands, ['pnpm test']);
  });

  it('does not mark ordinary tool calls as code edits or tests', () => {
    const trajectory = buildTrajectoryFromRows('sess_read_only', [{
      prism_compatible: true,
      requestId: 'req_read_only',
      createdAtIso: '2026-06-23T01:00:00.000Z',
      sessionId: 'sess_read_only',
      path: '/v1/messages',
      upstream: 'anthropic',
      model: 'claude-test',
      status: 200,
      requestBody: JSON.stringify({
        model: 'claude-test',
        messages: [{
          role: 'assistant',
          content: [
            { type: 'tool_use', id: 'tool_read', name: 'Read', input: { file_path: 'src/index.js' } },
            { type: 'tool_use', id: 'tool_ls', name: 'List', input: { path: 'src' } },
            { type: 'tool_use', id: 'tool_shell', name: 'exec_command', input: { cmd: 'node scripts/inspect.js' } },
          ],
        }],
      }),
      responseBody: JSON.stringify({ id: 'msg_1', stop_reason: 'end_turn' }),
    }]);

    assert.equal(trajectory.stats.has_code_edit, false);
    assert.equal(trajectory.stats.has_test_execution, false);
    assert.deepEqual(trajectory.stats.test_commands, []);
  });

  it('exports native stream events as response bodies and extracts streamed tool calls', () => {
    const trajectory = buildTrajectoryFromRows('sess_stream', [{
      prism_compatible: true,
      requestId: 'req_stream',
      createdAtIso: '2026-06-23T01:00:00.000Z',
      sessionId: 'sess_stream',
      path: '/v1/messages',
      upstream: 'anthropic',
      model: 'claude-test',
      status: 200,
      isStream: true,
      requestBody: JSON.stringify({ model: 'claude-test', messages: [{ role: 'user', content: 'Patch and test' }] }),
      responseBody: JSON.stringify({
        reconstructed_stream: true,
        events: [
          { type: 'content_block_delta', delta: { type: 'text_delta', text: 'working' } },
          { type: 'content_block_start', content_block: { type: 'tool_use', id: 'tool_patch', name: 'apply_patch', input: { patch: '*** Begin Patch' } } },
          { type: 'response.output_item.done', item: { type: 'function_call', call_id: 'call_test', name: 'exec_command', arguments: JSON.stringify({ cmd: 'node --test test/trajectoryExport.test.js' }) } },
        ],
      }),
    }]);

    assert.equal(trajectory.turns[0].is_stream, true);
    assert.equal(trajectory.turns[0].response_body.reconstructed_stream, true);
    assert.equal(trajectory.stats.has_code_edit, true);
    assert.equal(trajectory.stats.has_test_execution, true);
    assert.deepEqual(trajectory.stats.test_commands, ['node --test test/trajectoryExport.test.js']);
  });

  it('reconstructs streamed Anthropic tool input_json_delta arguments', () => {
    const trajectory = buildTrajectoryFromRows('sess_stream_delta', [{
      prism_compatible: true,
      requestId: 'req_stream_delta',
      createdAtIso: '2026-06-23T01:00:00.000Z',
      sessionId: 'sess_stream_delta',
      path: '/v1/messages',
      upstream: 'anthropic',
      model: 'claude-test',
      status: 200,
      isStream: true,
      requestBody: JSON.stringify({ model: 'claude-test', messages: [{ role: 'user', content: 'Patch and test' }] }),
      responseBody: JSON.stringify({
        reconstructed_stream: true,
        events: [
          { type: 'content_block_start', index: 1, content_block: { type: 'tool_use', id: 'tool_bash', name: 'Bash', input: {} } },
          { type: 'content_block_delta', index: 1, delta: { type: 'input_json_delta', partial_json: '{"command":"apply_patch <<PATCH\\n*** Begin Patch\\nPATCH' } },
          { type: 'content_block_delta', index: 1, delta: { type: 'input_json_delta', partial_json: ' && node --test test/trajectoryExport.test.js"}' } },
          { type: 'content_block_stop', index: 1 },
        ],
      }),
    }]);

    assert.equal(trajectory.stats.has_code_edit, true);
    assert.equal(trajectory.stats.has_test_execution, true);
    assert.deepEqual(trajectory.stats.test_commands, ['apply_patch <<PATCH\n*** Begin Patch\nPATCH && node --test test/trajectoryExport.test.js']);
    assert.equal(trajectory.turns[0].tool_calls.length, 1);
    assert.equal(trajectory.turns[0].tool_calls[0].name, 'Bash');
    assert.equal(trajectory.turns[0].tool_calls[0].input.command, 'apply_patch <<PATCH\n*** Begin Patch\nPATCH && node --test test/trajectoryExport.test.js');
  });

  it('reconstructs streamed OpenAI Chat tool call argument deltas', () => {
    const trajectory = buildTrajectoryFromRows('sess_chat_stream_delta', [{
      prism_compatible: true,
      requestId: 'req_chat_stream_delta',
      createdAtIso: '2026-06-23T01:00:00.000Z',
      sessionId: 'sess_chat_stream_delta',
      path: '/v1/chat/completions',
      upstream: 'openai',
      model: 'gpt-test',
      status: 200,
      isStream: true,
      requestBody: JSON.stringify({ model: 'gpt-test', messages: [{ role: 'user', content: 'Run the test' }] }),
      responseBody: JSON.stringify({
        reconstructed_stream: true,
        events: [
          {
            choices: [{
              index: 0,
              delta: {
                tool_calls: [{
                  index: 0,
                  id: 'call_test',
                  type: 'function',
                  function: { name: 'exec_command', arguments: '{"cmd":"pnpm ' },
                }],
              },
            }],
          },
          {
            choices: [{
              index: 0,
              delta: {
                tool_calls: [{
                  index: 0,
                  function: { arguments: 'test"}' },
                }],
              },
            }],
          },
        ],
      }),
    }]);

    assert.equal(trajectory.stats.has_tool_calls, true);
    assert.equal(trajectory.stats.has_test_execution, true);
    assert.deepEqual(trajectory.stats.test_commands, ['pnpm test']);
    assert.equal(trajectory.turns[0].tool_calls.length, 1);
    assert.equal(trajectory.turns[0].tool_calls[0].function.name, 'exec_command');
    assert.equal(trajectory.turns[0].tool_calls[0].function.arguments, '{"cmd":"pnpm test"}');
  });

  it('does not append duplicate OpenAI Chat streamed full tool call snapshots', () => {
    const responseBody = {
      reconstructed_stream: true,
      events: [
        {
          choices: [{
            index: 0,
            delta: {
              tool_calls: [{
                index: 0,
                id: 'call_test',
                type: 'function',
                function: { name: 'exec_command', arguments: '{"cmd":"pnpm ' },
              }],
            },
          }],
        },
        {
          choices: [{
            index: 0,
            delta: {
              tool_calls: [{
                index: 0,
                function: { arguments: '{"cmd":"pnpm test"}' },
              }],
            },
          }],
        },
      ],
    };
    const trajectory = buildTrajectoryFromRows('sess_chat_stream_snapshot', [{
      prism_compatible: true,
      requestId: 'req_chat_stream_snapshot',
      createdAtIso: '2026-06-23T01:00:00.000Z',
      sessionId: 'sess_chat_stream_snapshot',
      path: '/v1/chat/completions',
      upstream: 'openai',
      model: 'gpt-test',
      status: 200,
      isStream: true,
      requestBody: JSON.stringify({ model: 'gpt-test', messages: [{ role: 'user', content: 'Run the test' }] }),
      responseBody: JSON.stringify(responseBody),
    }]);

    assert.deepEqual(trajectory.turns[0].response_body, responseBody);
    assert.equal(trajectory.stats.has_test_execution, true);
    assert.deepEqual(trajectory.stats.test_commands, ['pnpm test']);
    assert.equal(trajectory.turns[0].tool_calls.length, 1);
    assert.equal(trajectory.turns[0].tool_calls[0].function.arguments, '{"cmd":"pnpm test"}');
  });

  it('reconstructs streamed OpenAI Responses function call argument deltas', () => {
    const trajectory = buildTrajectoryFromRows('sess_responses_stream_delta', [{
      prism_compatible: true,
      requestId: 'req_responses_stream_delta',
      createdAtIso: '2026-06-23T01:00:00.000Z',
      sessionId: 'sess_responses_stream_delta',
      path: '/v1/responses',
      upstream: 'openai',
      model: 'gpt-test',
      status: 200,
      isStream: true,
      requestBody: JSON.stringify({ model: 'gpt-test', input: 'Run the test' }),
      responseBody: JSON.stringify({
        reconstructed_stream: true,
        events: [
          {
            type: 'response.output_item.added',
            output_index: 0,
            item: {
              id: 'fc_1',
              type: 'function_call',
              call_id: 'call_test',
              name: 'exec_command',
              arguments: '',
            },
          },
          {
            type: 'response.function_call_arguments.delta',
            output_index: 0,
            item_id: 'fc_1',
            delta: '{"cmd":"pnpm ',
          },
          {
            type: 'response.function_call_arguments.delta',
            output_index: 0,
            item_id: 'fc_1',
            delta: 'test"}',
          },
          {
            type: 'response.function_call_arguments.done',
            output_index: 0,
            item_id: 'fc_1',
            arguments: '{"cmd":"pnpm test"}',
          },
          {
            type: 'response.output_item.done',
            output_index: 0,
            item: {
              id: 'fc_1',
              type: 'function_call',
              call_id: 'call_test',
              name: 'exec_command',
              arguments: '',
            },
          },
        ],
      }),
    }]);

    assert.equal(trajectory.stats.has_tool_calls, true);
    assert.equal(trajectory.stats.has_test_execution, true);
    assert.deepEqual(trajectory.stats.test_commands, ['pnpm test']);
    assert.equal(trajectory.turns[0].tool_calls.length, 1);
    assert.equal(trajectory.turns[0].tool_calls[0].name, 'exec_command');
    assert.equal(trajectory.turns[0].tool_calls[0].arguments, '{"cmd":"pnpm test"}');
  });

  it('surfaces truncated reconstructed stream markers', () => {
    const trajectory = buildTrajectoryFromRows('sess_stream_truncated', [{
      prism_compatible: true,
      requestId: 'req_stream_truncated',
      createdAtIso: '2026-06-23T01:00:00.000Z',
      sessionId: 'sess_stream_truncated',
      path: '/v1/responses',
      upstream: 'openai',
      model: 'gpt-test',
      status: 200,
      isStream: true,
      requestBody: JSON.stringify({ model: 'gpt-test', input: 'Long task' }),
      responseBody: JSON.stringify({
        reconstructed_stream: true,
        events_truncated: true,
        events_limit: 1000,
        events: [{ type: 'response.output_text.delta', delta: 'partial' }],
      }),
    }]);

    assert.equal(trajectory.stats.has_truncated_stream, true);
    assert.equal(trajectory.turns[0].response_events_truncated, true);
    assert.equal(trajectory.turns[0].response_body.events_truncated, true);
  });

  it('marks raw stream capture truncation as an incomplete streamed turn', () => {
    const trajectory = buildTrajectoryFromRows('sess_raw_stream_truncated', [{
      prism_compatible: true,
      requestId: 'req_raw_stream_truncated',
      createdAtIso: '2026-06-23T01:00:00.000Z',
      sessionId: 'sess_raw_stream_truncated',
      path: '/v1/responses',
      upstream: 'openai',
      model: 'gpt-test',
      status: 200,
      isStream: true,
      requestBody: JSON.stringify({ model: 'gpt-test', input: 'Long task' }),
      responseBody: JSON.stringify({
        reconstructed: true,
        raw_stream_truncated: true,
        raw_stream_body: 'partial',
      }),
    }]);

    const turn = trajectory.turns[0];
    assert.equal(turn.complete, false);
    assert.equal(turn.response_events_truncated, true);
    assert.deepEqual(turn.incomplete_reasons, ['response_body_truncated']);
    assert.equal(trajectory.stats.has_truncated_stream, true);
    assert.equal(trajectory.stats.has_incomplete_turns, true);
  });

  it('exports retry attempts with parsed snake_case bodies without adding turns', () => {
    const trajectory = buildTrajectoryFromRows('sess_attempts', [{
      prism_compatible: true,
      requestId: 'req_attempts',
      createdAtIso: '2026-06-23T01:00:00.000Z',
      sessionId: 'sess_attempts',
      path: '/v1/messages',
      upstream: 'anthropic',
      model: 'claude-opus-4-1',
      status: 200,
      requestBody: JSON.stringify({ model: 'claude-opus-4-1', messages: [] }),
      responseBody: JSON.stringify({ id: 'msg_retry' }),
      attempts: [
        {
          attempt_index: 0,
          model: 'claude-haiku-4-7',
          status: 503,
          upstreamMode: 'anthropic',
          requestBody: JSON.stringify({ model: 'claude-haiku-4-7', messages: [] }),
          responseBody: JSON.stringify({ error: { type: 'upstream_unavailable' } }),
        },
        {
          attempt_index: 1,
          model: 'claude-opus-4-1',
          status: 200,
          upstreamMode: 'anthropic',
          requestBody: JSON.stringify({ model: 'claude-opus-4-1', messages: [] }),
          responseBody: JSON.stringify({ id: 'msg_retry' }),
        },
      ],
    }]);

    const turn = trajectory.turns[0];
    assert.equal(trajectory.stats.turns, 1);
    assert.equal(turn.attempts.length, 2);
    assert.equal(turn.attempts[0].upstream_mode, 'anthropic');
    assert.deepEqual(turn.attempts[0].request_body, { model: 'claude-haiku-4-7', messages: [] });
    assert.deepEqual(turn.attempts[0].response_body, { error: { type: 'upstream_unavailable' } });
    assert.deepEqual(turn.attempts[1].request_body, { model: 'claude-opus-4-1', messages: [] });
    assert.deepEqual(turn.attempts[1].response_body, { id: 'msg_retry' });
  });

  it('extracts tool calls from semantic stream tail events after event capture truncates', () => {
    const trajectory = buildTrajectoryFromRows('sess_stream_tail', [{
      prism_compatible: true,
      requestId: 'req_stream_tail',
      createdAtIso: '2026-06-23T01:00:00.000Z',
      sessionId: 'sess_stream_tail',
      path: '/v1/responses',
      upstream: 'openai',
      model: 'gpt-test',
      status: 200,
      isStream: true,
      requestBody: JSON.stringify({ model: 'gpt-test', input: 'Run the test' }),
      responseBody: JSON.stringify({
        reconstructed_stream: true,
        events: [{ type: 'response.output_text.delta', delta: 'working' }],
        semantic_tail_events: [
          { type: 'response.output_item.done', item: { type: 'function_call', call_id: 'call_tail', name: 'exec_command', arguments: JSON.stringify({ cmd: 'node --test test/trajectoryExport.test.js' }) } },
          { type: 'response.completed', response: { id: 'resp_tail', status: 'completed', usage: { input_tokens: 5, output_tokens: 7 } } },
        ],
        events_truncated: true,
        events_limit: 1000,
      }),
    }]);

    assert.equal(trajectory.stats.has_test_execution, true);
    assert.deepEqual(trajectory.stats.test_commands, ['node --test test/trajectoryExport.test.js']);
    assert.equal(trajectory.turns[0].response_events_truncated, true);
  });

  it('groups OpenAI Responses chains when session and cwd are absent', () => {
    const trajectories = buildTrajectories([
      {
        prism_compatible: true,
        requestId: 'req_1',
        createdAtIso: '2026-06-23T01:00:00.000Z',
        path: '/v1/responses',
        upstream: 'openai',
        responseId: 'resp_1',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'Start task' }),
        responseBody: JSON.stringify({ id: 'resp_1', status: 'completed' }),
      },
      {
        prism_compatible: true,
        requestId: 'req_2',
        createdAtIso: '2026-06-23T01:01:00.000Z',
        path: '/v1/responses',
        upstream: 'openai',
        previousResponseId: 'resp_1',
        responseId: 'resp_2',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'Continue task', previous_response_id: 'resp_1' }),
        responseBody: JSON.stringify({ id: 'resp_2', status: 'completed' }),
      },
    ]);

    assert.equal(trajectories.length, 1);
    assert.equal(trajectories[0].turns.length, 2);
    assert.equal(trajectories[0].turns[0].response_id, 'resp_1');
    assert.equal(trajectories[0].turns[1].previous_response_id, 'resp_1');
  });

  it('does not merge previousResponseId through ambiguous duplicate response owners', () => {
    const trajectories = buildTrajectories([
      {
        prism_compatible: true,
        requestId: 'req_owner_a',
        createdAtIso: '2026-06-23T01:00:00.000Z',
        path: '/v1/responses',
        upstream: 'openai',
        responseId: 'resp_duplicate',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'Task A' }),
        responseBody: JSON.stringify({ id: 'resp_duplicate', status: 'completed' }),
      },
      {
        prism_compatible: true,
        requestId: 'req_owner_b',
        createdAtIso: '2026-06-23T01:01:00.000Z',
        path: '/v1/responses',
        upstream: 'openai',
        responseId: 'resp_duplicate',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'Task B' }),
        responseBody: JSON.stringify({ id: 'resp_duplicate', status: 'completed' }),
      },
      {
        prism_compatible: true,
        requestId: 'req_child',
        createdAtIso: '2026-06-23T01:02:00.000Z',
        path: '/v1/responses',
        upstream: 'openai',
        previousResponseId: 'resp_duplicate',
        responseId: 'resp_child',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'Continue task', previous_response_id: 'resp_duplicate' }),
        responseBody: JSON.stringify({ id: 'resp_child', status: 'completed' }),
      },
    ]);

    assert.equal(trajectories.length, 3);
    assert.ok(trajectories.every((trajectory) => trajectory.turns.length === 1));
  });

  it('merges duplicate response owners only when the child has one compatible session owner', () => {
    const trajectories = buildTrajectories([
      {
        prism_compatible: true,
        requestId: 'req_owner_a',
        createdAtIso: '2026-06-23T01:00:00.000Z',
        sessionId: 'sess_a',
        path: '/v1/responses',
        upstream: 'openai',
        responseId: 'resp_duplicate_session_filter',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'Task A' }),
        responseBody: JSON.stringify({ id: 'resp_duplicate_session_filter', status: 'completed' }),
      },
      {
        prism_compatible: true,
        requestId: 'req_owner_b',
        createdAtIso: '2026-06-23T01:01:00.000Z',
        sessionId: 'sess_b',
        path: '/v1/responses',
        upstream: 'openai',
        responseId: 'resp_duplicate_session_filter',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'Task B' }),
        responseBody: JSON.stringify({ id: 'resp_duplicate_session_filter', status: 'completed' }),
      },
      {
        prism_compatible: true,
        requestId: 'req_child_a',
        createdAtIso: '2026-06-23T01:02:00.000Z',
        sessionId: 'sess_a',
        path: '/v1/responses',
        upstream: 'openai',
        previousResponseId: 'resp_duplicate_session_filter',
        responseId: 'resp_child_a',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'Continue task A', previous_response_id: 'resp_duplicate_session_filter' }),
        responseBody: JSON.stringify({ id: 'resp_child_a', status: 'completed' }),
      },
    ]);

    assert.equal(trajectories.length, 2);
    const sessA = trajectories.find((trajectory) => trajectory.session_id === 'sess_a');
    assert.ok(sessA);
    assert.equal(sessA.turns.length, 2);
    assert.deepEqual(trajectories.map((trajectory) => trajectory.session_id).sort(), ['sess_a', 'sess_b']);
  });

  it('merges duplicate response owners only after they resolve to one explicit session root', () => {
    const trajectories = buildTrajectories([
      {
        prism_compatible: true,
        requestId: 'req_same_session_a',
        createdAtIso: '2026-06-23T01:00:00.000Z',
        sessionId: 'sess_duplicate_owner',
        path: '/v1/responses',
        upstream: 'openai',
        responseId: 'resp_duplicate_session',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'Task A' }),
        responseBody: JSON.stringify({ id: 'resp_duplicate_session', status: 'completed' }),
      },
      {
        prism_compatible: true,
        requestId: 'req_same_session_b',
        createdAtIso: '2026-06-23T01:01:00.000Z',
        sessionId: 'sess_duplicate_owner',
        path: '/v1/responses',
        upstream: 'openai',
        responseId: 'resp_duplicate_session',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'Task B' }),
        responseBody: JSON.stringify({ id: 'resp_duplicate_session', status: 'completed' }),
      },
      {
        prism_compatible: true,
        requestId: 'req_same_session_child',
        createdAtIso: '2026-06-23T01:02:00.000Z',
        path: '/v1/responses',
        upstream: 'openai',
        previousResponseId: 'resp_duplicate_session',
        responseId: 'resp_child',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'Continue task', previous_response_id: 'resp_duplicate_session' }),
        responseBody: JSON.stringify({ id: 'resp_child', status: 'completed' }),
      },
    ]);

    assert.equal(trajectories.length, 1);
    assert.equal(trajectories[0].session_id, 'sess_duplicate_owner');
    assert.equal(trajectories[0].turns.length, 3);
  });

  it('does not merge response chains across different explicit sessions', () => {
    const trajectories = buildTrajectories([
      {
        prism_compatible: true,
        requestId: 'req_session_a',
        createdAtIso: '2026-06-23T01:00:00.000Z',
        sessionId: 'sess_a',
        path: '/v1/responses',
        upstream: 'openai',
        responseId: 'resp_session_a',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'Task A' }),
        responseBody: JSON.stringify({ id: 'resp_session_a', status: 'completed' }),
      },
      {
        prism_compatible: true,
        requestId: 'req_session_b',
        createdAtIso: '2026-06-23T01:01:00.000Z',
        sessionId: 'sess_b',
        path: '/v1/responses',
        upstream: 'openai',
        previousResponseId: 'resp_session_a',
        responseId: 'resp_session_b',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'Task B', previous_response_id: 'resp_session_a' }),
        responseBody: JSON.stringify({ id: 'resp_session_b', status: 'completed' }),
      },
    ]);

    assert.equal(trajectories.length, 2);
    assert.deepEqual(trajectories.map((t) => t.session_id).sort(), ['sess_a', 'sess_b']);
  });

  it('uses explicit child sessionId for response chains rooted at unlabeled turns', () => {
    const trajectories = buildTrajectories([
      {
        prism_compatible: true,
        requestId: 'req_root',
        createdAtIso: '2026-06-23T01:00:00.000Z',
        path: '/v1/responses',
        upstream: 'openai',
        responseId: 'resp_root',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'Start task' }),
        responseBody: JSON.stringify({ id: 'resp_root', status: 'completed' }),
      },
      {
        prism_compatible: true,
        requestId: 'req_child',
        createdAtIso: '2026-06-23T01:01:00.000Z',
        sessionId: 'sess_child',
        path: '/v1/responses',
        upstream: 'openai',
        previousResponseId: 'resp_root',
        responseId: 'resp_child',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'Continue task', previous_response_id: 'resp_root' }),
        responseBody: JSON.stringify({ id: 'resp_child', status: 'completed' }),
      },
    ]);

    assert.equal(trajectories.length, 1);
    assert.equal(trajectories[0].session_id, 'sess_child');
    assert.equal(trajectories[0].turns.length, 2);
  });

  it('does not merge different child sessions through an unlabeled response root', () => {
    const trajectories = buildTrajectories([
      {
        prism_compatible: true,
        requestId: 'req_root',
        createdAtIso: '2026-06-23T01:00:00.000Z',
        path: '/v1/responses',
        upstream: 'openai',
        responseId: 'resp_root',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'Start task' }),
        responseBody: JSON.stringify({ id: 'resp_root', status: 'completed' }),
      },
      {
        prism_compatible: true,
        requestId: 'req_child_a',
        createdAtIso: '2026-06-23T01:01:00.000Z',
        sessionId: 'sess_a',
        path: '/v1/responses',
        upstream: 'openai',
        previousResponseId: 'resp_root',
        responseId: 'resp_child_a',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'Continue task A', previous_response_id: 'resp_root' }),
        responseBody: JSON.stringify({ id: 'resp_child_a', status: 'completed' }),
      },
      {
        prism_compatible: true,
        requestId: 'req_child_b',
        createdAtIso: '2026-06-23T01:02:00.000Z',
        sessionId: 'sess_b',
        path: '/v1/responses',
        upstream: 'openai',
        previousResponseId: 'resp_root',
        responseId: 'resp_child_b',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'Continue task B', previous_response_id: 'resp_root' }),
        responseBody: JSON.stringify({ id: 'resp_child_b', status: 'completed' }),
      },
    ]);

    assert.equal(trajectories.length, 2);
    assert.deepEqual(trajectories.map((t) => t.session_id).sort(), ['sess_a', 'sess_b']);
  });

  it('keeps unrelated unlabeled components separate even when fallback ids collide', () => {
    const trajectories = buildTrajectories([
      {
        prism_compatible: true,
        requestId: 'shared-request',
        createdAtIso: '2026-06-23T01:00:00.000Z',
        path: '/v1/responses',
        upstream: 'openai',
        responseId: 'resp_a',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'Task A' }),
        responseBody: JSON.stringify({ id: 'resp_a', status: 'completed' }),
      },
      {
        prism_compatible: true,
        requestId: 'shared-request',
        createdAtIso: '2026-06-23T01:01:00.000Z',
        path: '/v1/responses',
        upstream: 'openai',
        responseId: 'resp_b',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'Task B' }),
        responseBody: JSON.stringify({ id: 'resp_b', status: 'completed' }),
      },
    ]);

    assert.equal(trajectories.length, 2);
    assert.ok(trajectories.every((trajectory) => trajectory.turns.length === 1));
    assert.equal(new Set(trajectories.map((trajectory) => trajectory.session_id)).size, 2);
  });

  it('keeps unrelated unlabeled components separate when response ids collide', () => {
    const trajectories = buildTrajectories([
      {
        prism_compatible: true,
        requestId: 'req_a',
        createdAtIso: '2026-06-23T01:00:00.000Z',
        path: '/v1/responses',
        upstream: 'openai',
        responseId: 'shared-response',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'Task A' }),
        responseBody: JSON.stringify({ id: 'shared-response', status: 'completed' }),
      },
      {
        prism_compatible: true,
        requestId: 'req_b',
        createdAtIso: '2026-06-23T01:01:00.000Z',
        path: '/v1/responses',
        upstream: 'openai',
        responseId: 'shared-response',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'Task B' }),
        responseBody: JSON.stringify({ id: 'shared-response', status: 'completed' }),
      },
    ]);

    assert.equal(trajectories.length, 2);
    assert.ok(trajectories.every((trajectory) => trajectory.turns.length === 1));
    assert.equal(new Set(trajectories.map((trajectory) => trajectory.session_id)).size, 2);
  });

  it('does not merge independent runs only because they share a cwd', () => {
    const trajectories = buildTrajectories([
      {
        prism_compatible: true,
        requestId: 'req_cwd_a',
        createdAtIso: '2026-06-23T01:00:00.000Z',
        cwd: '/repo/app',
        path: '/v1/responses',
        upstream: 'openai',
        responseId: 'resp_cwd_a',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'Task A' }),
        responseBody: JSON.stringify({ id: 'resp_cwd_a', status: 'completed' }),
      },
      {
        prism_compatible: true,
        requestId: 'req_cwd_b',
        createdAtIso: '2026-06-23T01:01:00.000Z',
        cwd: '/repo/app',
        path: '/v1/responses',
        upstream: 'openai',
        responseId: 'resp_cwd_b',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'Task B' }),
        responseBody: JSON.stringify({ id: 'resp_cwd_b', status: 'completed' }),
      },
    ]);

    assert.equal(trajectories.length, 2);
    assert.deepEqual(trajectories.map((t) => t.task).sort(), ['Task A', 'Task B']);
  });

  it('does not use raw cwd as a fallback session id', () => {
    const trajectories = buildTrajectories([{
      prism_compatible: true,
      createdAtIso: '2026-06-23T01:00:00.000Z',
      cwd: '/Users/alice/private-repo',
      path: '/v1/responses',
      upstream: 'openai',
      requestBody: JSON.stringify({ model: 'gpt-test', input: 'Task without ids' }),
      responseBody: JSON.stringify({ id: 'resp_body_only', status: 'completed' }),
    }]);

    assert.equal(trajectories.length, 1);
    assert.equal(trajectories[0].session_id, 'unknown#0');
    assert.doesNotMatch(JSON.stringify(trajectories[0]), /\/Users\/alice\/private-repo/);
  });

  it('reads sorted top-level llm trace files when input is a directory', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-dir-'));
    try {
      fs.mkdirSync(path.join(dir, 'nested'));
      fs.writeFileSync(path.join(dir, 'ignore.jsonl'), JSON.stringify({
        prism_compatible: true,
        requestId: 'ignored',
      }) + '\n', 'utf8');
      fs.writeFileSync(path.join(dir, 'nested', 'llm-trace-000.jsonl'), JSON.stringify({
        prism_compatible: true,
        requestId: 'ignored_nested',
      }) + '\n', 'utf8');
      fs.writeFileSync(path.join(dir, 'llm-trace-002.jsonl'), JSON.stringify({
        prism_compatible: true,
        requestId: 'req_b',
        sessionId: 'sess_b',
        path: '/v1/responses',
        upstream: 'openai',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'second sorted row' }),
        responseBody: JSON.stringify({ id: 'resp_b' }),
      }) + '\n', 'utf8');
      fs.writeFileSync(path.join(dir, 'llm-trace-001.jsonl'), JSON.stringify({
        prism_compatible: true,
        requestId: 'req_a',
        sessionId: 'sess_a',
        path: '/v1/responses',
        upstream: 'openai',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'first sorted row' }),
        responseBody: JSON.stringify({ id: 'resp_a' }),
      }) + '\n', 'utf8');

      const { rows, stats } = readTraceRowsDetailed(dir);

      assert.deepEqual(rows.map((row) => row.requestId), ['req_a', 'req_b']);
      assert.equal(stats.filesScanned, 2);
      assert.equal(stats.rowsScanned, 2);
      assert.equal(stats.rowsRead, 2);
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('reads v2 llm_turn trace rows from jsonl input', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-v2-input-'));
    try {
      const input = path.join(dir, 'traces.jsonl');
      fs.writeFileSync(input, [
        JSON.stringify({
          event: 'llm_turn',
          ts: '2026-06-23T01:00:00.000Z',
          request_id: 'req_v2_file',
          session_id: 'sess_v2_file',
          response_id: 'resp_v2_file',
          route: '/v1/responses',
          provider: 'openai',
          chosen_model: 'gpt-test',
          latency_ms: 25,
          usage: { input_tokens: 3, output_tokens: 4 },
          request_body: JSON.stringify({ model: 'gpt-test', input: 'v2 file row' }),
          response_body: JSON.stringify({ id: 'resp_v2_file' }),
        }),
        JSON.stringify({ event: 'not_llm_turn', request_id: 'skip_v2_file' }),
      ].join('\n') + '\n', 'utf8');

      const { rows, stats } = readTraceRowsDetailed(input);

      assert.equal(rows.length, 1);
      assert.equal(rows[0].requestId, 'req_v2_file');
      assert.equal(rows[0].sessionId, 'sess_v2_file');
      assert.equal(rows[0].responseId, 'resp_v2_file');
      assert.equal(rows[0].path, '/v1/responses');
      assert.equal(rows[0].durationMs, 25);
      assert.equal(rows[0].input_tokens, 3);
      assert.equal(rows[0].output_tokens, 4);
      assert.equal(stats.rowsScanned, 2);
      assert.equal(stats.rowsRead, 1);
      assert.equal(stats.nonPrismSkipped, 1);
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('CLI accepts split --input/--output args for directory exports', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-cli-dir-'));
    try {
      const traceDir = path.join(dir, 'traces');
      const output = path.join(dir, 'trajectories.jsonl');
      fs.mkdirSync(traceDir);
      fs.writeFileSync(path.join(traceDir, 'llm-trace-001.jsonl'), JSON.stringify({
        prism_compatible: true,
        requestId: 'req_cli_dir',
        sessionId: 'sess_cli_dir',
        path: '/v1/responses',
        upstream: 'openai',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'split arg directory input' }),
        responseBody: JSON.stringify({ id: 'resp_cli_dir' }),
      }) + '\n', 'utf8');

      const res = spawnSync(process.execPath, [
        INDEX_JS,
        'trajectory-export',
        '--input',
        traceDir,
        '--output',
        output,
      ], {
        cwd: dir,
        env: {
          ...process.env,
          A2A_NODE_SECRET: '',
          EVOMAP_NODE_SECRET: '',
          EVOLVER_HOME: dir,
          HOME: dir,
        },
        encoding: 'utf8',
      });

      assert.equal(res.status, 0, res.stderr);
      const exported = fs.readFileSync(output, 'utf8').trim().split('\n').map((line) => JSON.parse(line));
      assert.equal(exported.length, 1);
      assert.equal(exported[0].session_id, 'sess_cli_dir');
      assert.equal(exported[0].task, 'split arg directory input');
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('CLI exports a Codex rollout session JSONL as a runtime session trajectory', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-codex-session-'));
    try {
      const inputDir = path.join(dir, '.codex', 'sessions', '2026', '06', '24');
      const input = path.join(inputDir, 'rollout-2026-06-24T01-02-03-test.jsonl');
      const output = path.join(dir, 'coding-trajectories.jsonl');
      fs.mkdirSync(inputDir, { recursive: true });
      fs.writeFileSync(input, [
        {
          timestamp: '2026-06-24T01:02:03.000Z',
          type: 'session_meta',
          payload: { id: 'codex-session-1', cwd: '/tmp/work' },
        },
        {
          timestamp: '2026-06-24T01:02:04.000Z',
          type: 'response_item',
          payload: {
            type: 'message',
            role: 'user',
            content: [{ type: 'input_text', text: 'Fix the TypeScript test and run pnpm test.' }],
          },
        },
        {
          timestamp: '2026-06-24T01:02:05.000Z',
          type: 'response_item',
          payload: {
            type: 'reasoning',
            model: 'gpt-5-codex',
            usage: { input_tokens: 13, output_tokens: 2 },
            summary: [{ text: 'Need inspect then test.' }],
            encrypted_content: 'codex-encrypted-content',
          },
        },
        {
          timestamp: '2026-06-24T01:02:06.000Z',
          type: 'response_item',
          payload: {
            type: 'function_call',
            name: 'shell_command',
            call_id: 'call_test',
            arguments: '{"command":"pnpm test"}',
          },
        },
        {
          timestamp: '2026-06-24T01:02:07.000Z',
          type: 'response_item',
          payload: {
            type: 'function_call_output',
            call_id: 'call_test',
            output: 'Exit code: 1\nOutput:\n1 failed',
          },
        },
        {
          timestamp: '2026-06-24T01:02:08.000Z',
          type: 'response_item',
          payload: {
            type: 'custom_tool_call',
            name: 'apply_patch',
            call_id: 'call_patch',
            input: '*** Begin Patch\n*** End Patch',
          },
        },
        {
          timestamp: '2026-06-24T01:02:09.000Z',
          type: 'response_item',
          payload: {
            type: 'tool_search_call',
            id: 'call_search',
            query: 'confirmed high jsonl',
            filters: { repo: 'evolver' },
          },
        },
        {
          timestamp: '2026-06-24T01:02:10.000Z',
          type: 'response_item',
          payload: {
            type: 'tool_search_output',
            call_id: 'call_search',
            results: [{ title: 'Keep native tool events' }],
          },
        },
      ].map((row) => JSON.stringify(row)).join('\n') + '\n', 'utf8');

      const res = spawnSync(process.execPath, [
        INDEX_JS,
        'trajectory-export',
        '--input',
        dir,
        '--output',
        output,
      ], {
        cwd: dir,
        env: {
          ...process.env,
          A2A_NODE_SECRET: '',
          EVOMAP_NODE_SECRET: '',
          EVOLVER_HOME: dir,
          HOME: dir,
        },
        encoding: 'utf8',
      });

      assert.equal(res.status, 0, res.stderr);
      const [trajectory] = fs.readFileSync(output, 'utf8').trim().split('\n').map((line) => JSON.parse(line));
      assert.equal(trajectory.session_id, 'codex-session-1');
      assert.equal(trajectory.source_kind, 'runtime_session');
      assert.equal(trajectory.source_agent, 'codex');
      assert.equal(trajectory.source_path, input);
      assert.match(trajectory.task, /Fix the TypeScript test/);
      assert.equal(trajectory.stats.has_test_execution, true);
      assert.equal(trajectory.stats.has_code_edit, true);
      assert.equal(trajectory.stats.has_failure_correction, true);
      assert.equal(trajectory.stats.input_tokens, 13);
      assert.equal(trajectory.stats.output_tokens, 2);
      assert.equal(trajectory.stats.tool_types.shell_command, 1);
      assert.equal(trajectory.stats.tool_types.apply_patch, 1);
      assert.equal(trajectory.stats.tool_types.tool_search_call, 1);
      const reasoningTurn = trajectory.turns.find((turn) => turn.reasoning === 'Need inspect then test.');
      assert.ok(reasoningTurn);
      assert.equal(reasoningTurn.model, 'gpt-5-codex');
      assert.equal(reasoningTurn.input_tokens, 13);
      assert.equal(reasoningTurn.output_tokens, 2);
      assert.equal(reasoningTurn.encrypted_content, 'codex-encrypted-content');
      assert.ok(trajectory.turns.some((turn) => String(turn.error || '').includes('1 failed')));
      assert.ok(trajectory.turns.some((turn) => turn.tool_calls.some((call) => (
        call.name === 'shell_command' && call.input === '{"command":"pnpm test"}'
      ))));
      assert.ok(trajectory.turns.some((turn) => turn.tool_calls.some((call) => (
        call.name === 'tool_search_call'
        && call.id === 'call_search'
        && call.input.query === 'confirmed high jsonl'
      ))));
      const toolOutputTurn = trajectory.turns.find((turn) => (
        turn.response_body
        && turn.response_body.tool_name === 'tool_search_output'
        && turn.response_body.tool_use_id === 'call_search'
      ));
      assert.ok(toolOutputTurn);
      assert.deepEqual(JSON.parse(toolOutputTurn.response_body.tool_result).results, [{ title: 'Keep native tool events' }]);
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('writes the export atomically with mode 0o600 and does not follow a pre-placed symlink (PR #294 C4)', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-c4-'));
    try {
      const inputDir = path.join(dir, '.codex', 'sessions');
      const input = path.join(inputDir, 'rollout.jsonl');
      fs.mkdirSync(inputDir, { recursive: true });
      fs.writeFileSync(input, [
        JSON.stringify({ timestamp: '2026-06-24T01:02:03.000Z', type: 'session_meta', payload: { id: 'c4-session' } }),
        JSON.stringify({
          timestamp: '2026-06-24T01:02:04.000Z',
          type: 'response_item',
          payload: { type: 'message', role: 'user', content: [{ type: 'input_text', text: 'hello' }] },
        }),
      ].join('\n') + '\n', 'utf8');

      const sensitiveTarget = path.join(dir, 'sensitive-target.txt');
      fs.writeFileSync(sensitiveTarget, 'ORIGINAL', { mode: 0o644 });
      const output = path.join(dir, 'out.jsonl');
      fs.symlinkSync(sensitiveTarget, output);

      writeTrajectories({ input, output });

      // The pre-placed symlink must not be followed: the sensitive target stays untouched.
      assert.equal(fs.readFileSync(sensitiveTarget, 'utf8'), 'ORIGINAL');
      // The output is now a real regular file (symlink replaced), owner-only 0o600.
      const st = fs.lstatSync(output);
      assert.ok(!st.isSymbolicLink());
      if (process.platform === 'win32') {
        assert.equal((st.mode & fs.constants.S_IFMT), fs.constants.S_IFREG);
      } else {
        assert.equal(st.mode & 0o777, 0o600);
      }
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('marks Codex rollout session trajectories incomplete when JSONL contains invalid rows', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-codex-invalid-json-'));
    try {
      const inputDir = path.join(dir, '.codex', 'sessions');
      const input = path.join(inputDir, 'rollout-invalid.jsonl');
      const output = path.join(dir, 'coding-trajectories.jsonl');
      fs.mkdirSync(inputDir, { recursive: true });
      fs.writeFileSync(input, [
        JSON.stringify({
          timestamp: '2026-06-24T01:02:03.000Z',
          type: 'session_meta',
          payload: { id: 'codex-invalid-json' },
        }),
        '{bad json',
        JSON.stringify({
          timestamp: '2026-06-24T01:02:04.000Z',
          type: 'response_item',
          payload: {
            type: 'message',
            role: 'user',
            content: [{ type: 'input_text', text: 'Fix incomplete export.' }],
          },
        }),
      ].join('\n') + '\n', 'utf8');

      const result = writeTrajectories({ input, output });
      const [trajectory] = fs.readFileSync(output, 'utf8').trim().split('\n').map((line) => JSON.parse(line));

      assert.equal(result.stats.invalidJson, 1);
      assert.equal(result.stats.sessionInvalidJson, 1);
      assert.equal(trajectory.stats.has_incomplete_turns, true);
      assert.ok(trajectory.turns.every((turn) => turn.complete === false));
      assert.ok(trajectory.turns.every((turn) => turn.incomplete_reasons.includes('runtime_session_invalid_json')));
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('discovers current-workspace Codex and Claude Code session JSONL with runtimeSessions', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-runtime-discovery-'));
    const prevTraceFile = process.env.EVOMAP_PROXY_TRACE_FILE;
    const prevEvolverHome = process.env.EVOLVER_HOME;
    const prevHome = process.env.HOME;
    try {
      const home = path.join(dir, 'home');
      const workspace = path.join(dir, 'workspace');
      const codexDir = path.join(home, '.codex', 'sessions', '2026', '06', '26');
      const claudeDir = path.join(home, '.claude', 'projects', 'workspace');
      const output = path.join(dir, 'coding-trajectories.jsonl');
      fs.mkdirSync(codexDir, { recursive: true });
      fs.mkdirSync(claudeDir, { recursive: true });
      fs.mkdirSync(workspace, { recursive: true });
      fs.writeFileSync(path.join(codexDir, 'rollout-2026-06-26T01-02-03-test.jsonl'), [
        { timestamp: '2026-06-26T01:02:03.000Z', type: 'session_meta', payload: { id: 'codex-runtime-1', cwd: workspace } },
        { timestamp: '2026-06-26T01:02:04.000Z', type: 'response_item', payload: { type: 'message', role: 'user', content: [{ type: 'input_text', text: 'Patch the Codex runtime path.' }] } },
        { timestamp: '2026-06-26T01:02:05.000Z', type: 'response_item', payload: { type: 'message', role: 'assistant', content: [{ type: 'output_text', text: 'Patched.' }] } },
      ].map((row) => JSON.stringify(row)).join('\n') + '\n', 'utf8');
      fs.writeFileSync(path.join(claudeDir, 'claude-runtime-1.jsonl'), [
        { timestamp: '2026-06-26T02:00:00.000Z', cwd: workspace, type: 'user', message: { content: [{ type: 'text', text: 'Patch the Claude runtime path.' }] } },
        { timestamp: '2026-06-26T02:00:01.000Z', cwd: workspace, type: 'assistant', message: { content: [{ type: 'text', text: 'Done.' }] } },
      ].map((row) => JSON.stringify(row)).join('\n') + '\n', 'utf8');
      process.env.EVOMAP_PROXY_TRACE_FILE = path.join(dir, 'missing-proxy-traces.jsonl');
      process.env.EVOLVER_HOME = path.join(dir, '.evomap');
      process.env.HOME = home;

      // Strict marking gate (default): both runtime sessions must be in the
      // evolver-marked registry to be collected. The session-start hook writes
      // codex's session_meta.payload.id ('codex-runtime-1') and Claude Code's
      // session uuid (the transcript basename 'claude-runtime-1').
      const markedFile = path.join(dir, 'marked-sessions.jsonl');
      fs.writeFileSync(markedFile, [
        { session_id: 'codex-runtime-1', marked_at: '2026-06-26T01:02:03.000Z' },
        { session_id: 'claude-runtime-1', marked_at: '2026-06-26T02:00:00.000Z' },
      ].map((row) => JSON.stringify(row)).join('\n') + '\n', 'utf8');

      const result = writeTrajectories({
        output,
        runtimeSessions: true,
        homedir: home,
        workspaceRoot: workspace,
        markedSessionsFile: markedFile,
      });
      const trajectories = fs.readFileSync(output, 'utf8').trim().split('\n').map((line) => JSON.parse(line));

      assert.deepEqual(trajectories.map((item) => item.source_agent).sort(), ['claude-code', 'codex']);
      assert.ok(trajectories.every((item) => item.source_kind === 'runtime_session'));
      assert.ok(trajectories.some((item) => String(item.task || '').includes('Codex runtime path')));
      assert.ok(trajectories.some((item) => String(item.task || '').includes('Claude runtime path')));
      assert.equal(result.runtimeSessionDiscovery.enabled, true);
      assert.equal(result.runtimeSessionDiscovery.dirsScanned, 2);
      assert.equal(result.runtimeSessionDiscovery.filesMatched, 2);
    } finally {
      if (prevTraceFile === undefined) delete process.env.EVOMAP_PROXY_TRACE_FILE;
      else process.env.EVOMAP_PROXY_TRACE_FILE = prevTraceFile;
      if (prevEvolverHome === undefined) delete process.env.EVOLVER_HOME;
      else process.env.EVOLVER_HOME = prevEvolverHome;
      if (prevHome === undefined) delete process.env.HOME;
      else process.env.HOME = prevHome;
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('CLI exports a Claude Code transcript JSONL as a runtime session trajectory', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-claude-session-'));
    try {
      const inputDir = path.join(dir, '.claude', 'projects', 'demo');
      const input = path.join(inputDir, 'claude-session-1.transcript.jsonl');
      const output = path.join(dir, 'coding-trajectories.jsonl');
      fs.mkdirSync(inputDir, { recursive: true });
      fs.writeFileSync(input, [
        {
          timestamp: '2026-06-24T02:00:00.000Z',
          type: 'user',
          message: { content: [{ type: 'text', text: 'Patch foo.py and run pytest.' }] },
        },
        {
          timestamp: '2026-06-24T02:00:01.000Z',
          type: 'assistant',
          message: {
            model: 'claude-opus-4-20250514',
            usage: { input_tokens: 17, output_tokens: 23 },
            content: [
              {
                type: 'thinking',
                thinking: 'Need inspect first.',
                signature: 'claude-thinking-signature',
                encrypted_signature: 'claude-encrypted-signature',
              },
              { type: 'tool_use', id: 'tu_1', name: 'Bash', input: { command: 'pytest' } },
            ],
          },
        },
        {
          timestamp: '2026-06-24T02:00:02.000Z',
          type: 'user',
          message: {
            content: [{ type: 'tool_result', tool_use_id: 'tu_1', content: 'Exit code: 1\npytest failed', is_error: true }],
          },
        },
      ].map((row) => JSON.stringify(row)).join('\n') + '\n', 'utf8');

      const res = spawnSync(process.execPath, [
        INDEX_JS,
        'trajectory-export',
        '--input',
        input,
        '--output',
        output,
      ], {
        cwd: dir,
        env: {
          ...process.env,
          A2A_NODE_SECRET: '',
          EVOMAP_NODE_SECRET: '',
          EVOLVER_HOME: dir,
          HOME: dir,
        },
        encoding: 'utf8',
      });

      assert.equal(res.status, 0, res.stderr);
      const [trajectory] = fs.readFileSync(output, 'utf8').trim().split('\n').map((line) => JSON.parse(line));
      assert.equal(trajectory.session_id, 'claude-session-1.transcript');
      assert.equal(trajectory.source_kind, 'runtime_session');
      assert.equal(trajectory.source_agent, 'claude-code');
      assert.equal(trajectory.source_path, input);
      assert.equal(trajectory.stats.has_test_execution, true);
      assert.equal(trajectory.stats.has_failure_correction, true);
      assert.equal(trajectory.stats.input_tokens, 17);
      assert.equal(trajectory.stats.output_tokens, 23);
      assert.equal(trajectory.stats.total_tokens, 40);
      assert.equal(trajectory.stats.tool_types.Bash, 1);
      const reasoningTurn = trajectory.turns.find((turn) => turn.reasoning === 'Need inspect first.');
      assert.ok(reasoningTurn);
      assert.equal(reasoningTurn.model, 'claude-opus-4-20250514');
      assert.equal(reasoningTurn.input_tokens, 17);
      assert.equal(reasoningTurn.output_tokens, 23);
      assert.equal(reasoningTurn.reasoning_signature, 'claude-thinking-signature');
      assert.equal(reasoningTurn.encrypted_signature, 'claude-encrypted-signature');
      assert.doesNotMatch(reasoningTurn.reasoning, /claude-thinking-signature|claude-encrypted-signature/);
      assert.ok(trajectory.turns.some((turn) => (
        turn.response_body
        && turn.response_body.tool_name === 'Bash'
        && String(turn.error || '').includes('pytest failed')
      )));
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('redacts runtime session bodies, tool inputs, errors, and summaries before export', () => {
    const auth = 'Bearer local-redaction-fixture-value';
    const apiKey = 'api_key=local-redaction-fixture-value';
    const trajectory = buildTrajectoryFromSessionLog({
      sourceAgent: 'generic-chat',
      sourcePath: 'sample.messages.jsonl',
      sessionId: 'runtime-redaction',
      turns: [
        {
          role: 'user',
          text: `Fix login with Authorization: ${auth}`,
          isMeta: false,
        },
        {
          role: 'assistant',
          text: `Need shell with ${apiKey}`,
          reasoning: true,
          isMeta: false,
        },
        {
          role: 'assistant',
          text: '',
          toolName: 'shell_command',
          toolUseId: 'call_secret',
          toolInput: { command: `curl -H "Authorization: ${auth}" https://example.invalid` },
          isMeta: false,
        },
        {
          role: 'tool',
          text: '',
          toolUseId: 'call_secret',
          toolResult: `Exit code: 1\nOutput:\n${apiKey}`,
          errorMessage: `failed with ${apiKey}`,
          isMeta: false,
        },
      ],
    });

    const serialized = JSON.stringify(trajectory);
    assert.ok(trajectory);
    assert.doesNotMatch(serialized, new RegExp(auth.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')));
    assert.doesNotMatch(serialized, new RegExp(apiKey.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')));
    assert.match(trajectory.task, /\[redacted\]/i);
    assert.match(trajectory.turns[1].reasoning, /\[redacted\]/i);
    assert.equal(trajectory.turns[2].redaction, 'evolver-redact-v2');
    assert.match(JSON.stringify(trajectory.turns[2].tool_calls[0].input), /\[redacted\]/i);
    assert.match(trajectory.turns[3].error, /\[redacted\]/i);
  });

  it('preserves runtime session system prompts and session envelope metadata', () => {
    const trajectory = buildTrajectoryFromSessionLog({
      sourceAgent: 'generic-chat',
      sourcePath: 'sample.messages.jsonl',
      sessionId: 'runtime-envelope-session',
      provider: 'openai',
      model: 'gpt-5.5',
      tools: [{ type: 'function', function: { name: 'exec_command', parameters: { type: 'object' } } }],
      turns: [
        {
          role: 'system',
          text: 'SYSTEM_PROMPT_MUST_SURVIVE',
          isMeta: true,
        },
        {
          role: 'user',
          text: 'Use the declared tool.',
          isMeta: false,
        },
        {
          role: 'assistant',
          text: '',
          toolName: 'exec_command',
          toolUseId: 'call_test',
          toolInput: { cmd: 'node --test' },
          isMeta: false,
        },
      ],
    });

    assert.match(JSON.stringify(trajectory), /SYSTEM_PROMPT_MUST_SURVIVE/);
    assert.deepEqual(trajectory.providers, ['openai']);
    assert.equal(trajectory.session_model, 'gpt-5.5');
    assert.deepEqual(trajectory.session_tools, [{ type: 'function', function: { name: 'exec_command', parameters: { type: 'object' } } }]);
    assert.deepEqual(trajectory.turns[0].request_body, {
      source: 'runtime_session',
      role: 'system',
      model: 'gpt-5.5',
      tools_ref: 'session_tools',
      text: 'SYSTEM_PROMPT_MUST_SURVIVE',
    });
    assert.ok(trajectory.turns[1].tool_calls.some((call) => call.name === 'exec_command' && call.declared === true));
    assert.equal(trajectory.stats.tool_call_count, 1);
  });

  it('exports generic OpenAI messages JSONL and preserves tool call arguments', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-generic-chat-'));
    try {
      const input = path.join(dir, 'session.messages.jsonl');
      const output = path.join(dir, 'coding-trajectories.jsonl');
      const toolArguments = '{"cmd":"pnpm test"}';
      fs.writeFileSync(input, [
        { role: 'system', content: 'You are a careful coding assistant.' },
        { role: 'user', content: 'Fix the TypeScript test and run pnpm test.' },
        {
          role: 'assistant',
          model: 'gpt-generic-runtime',
          usage: { prompt_tokens: 5, completion_tokens: 7 },
          content: [{ type: 'thinking', thinking: 'Need run tests.', signature: 'generic-thinking-signature' }],
        },
        {
          role: 'assistant',
          content: null,
          tool_calls: [{
            id: 'call_run_tests',
            type: 'function',
            function: {
              name: 'exec_command',
              arguments: toolArguments,
            },
          }],
        },
        {
          role: 'tool',
          tool_call_id: 'call_run_tests',
          content: 'Exit code: 0\nTests passed',
        },
      ].map((row) => JSON.stringify(row)).join('\n') + '\n', 'utf8');

      const result = writeTrajectories({ input, output });
      const [trajectory] = fs.readFileSync(output, 'utf8').trim().split('\n').map((line) => JSON.parse(line));

      assert.equal(result.trajectories.length, 1);
      assert.equal(result.rowsRead, 0);
      assert.equal(result.sessionFilesRead, 1);
      assert.equal(trajectory.source_kind, 'runtime_session');
      assert.equal(trajectory.source_agent, 'generic-chat');
      assert.equal(trajectory.source_path, input);
      assert.equal(trajectory.task, 'Fix the TypeScript test and run pnpm test.');
      assert.equal(trajectory.stats.has_tool_calls, true);
      assert.equal(trajectory.stats.tool_types.exec_command, 1);
      assert.equal(trajectory.stats.has_test_execution, true);
      assert.equal(trajectory.stats.input_tokens, 5);
      assert.equal(trajectory.stats.output_tokens, 7);
      assert.deepEqual(trajectory.stats.test_commands, ['pnpm test']);
      const reasoningTurn = trajectory.turns.find((turn) => turn.reasoning === 'Need run tests.');
      assert.ok(reasoningTurn);
      assert.equal(reasoningTurn.model, 'gpt-generic-runtime');
      assert.equal(reasoningTurn.reasoning_signature, 'generic-thinking-signature');
      assert.doesNotMatch(reasoningTurn.reasoning, /generic-thinking-signature/);

      const callTurn = trajectory.turns.find((turn) => (
        Array.isArray(turn.tool_calls)
        && turn.tool_calls.some((call) => call.id === 'call_run_tests')
      ));
      assert.ok(callTurn);
      assert.equal(callTurn.response_body.tool_input, toolArguments);
      assert.equal(callTurn.tool_calls[0].name, 'exec_command');
      assert.equal(callTurn.tool_calls[0].input, toolArguments);

      const resultTurn = trajectory.turns.find((turn) => (
        turn.response_body
        && turn.response_body.tool_result === 'Exit code: 0\nTests passed'
      ));
      assert.ok(resultTurn);
      assert.equal(resultTurn.response_body.tool_name, 'exec_command');
      assert.equal(resultTurn.response_body.tool_use_id, 'call_run_tests');
      assert.match(JSON.stringify(trajectory), /careful coding assistant/);
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('exports generic chat wrapper system prompt and top-level envelope metadata', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-generic-wrapper-'));
    try {
      const input = path.join(dir, 'sample.messages.json');
      const output = path.join(dir, 'coding-trajectories.jsonl');
      fs.writeFileSync(input, JSON.stringify({
        session_id: 'wrapper-session-1',
        provider: 'openai',
        model: 'gpt-5.5',
        tools: [{ type: 'function', function: { name: 'exec_command', parameters: { type: 'object' } } }],
        messages: [
          { role: 'system', content: 'SYSTEM_PROMPT_MUST_SURVIVE' },
          { role: 'user', content: 'Run the declared tool.' },
          { role: 'assistant', tool_calls: [{ id: 'call_test', type: 'function', function: { name: 'exec_command', arguments: '{"cmd":"node --test"}' } }] },
        ],
      }), 'utf8');

      const result = writeTrajectories({ input, output });
      const [trajectory] = fs.readFileSync(output, 'utf8').trim().split('\n').map((line) => JSON.parse(line));

      assert.equal(result.trajectories.length, 1);
      assert.equal(trajectory.session_id, 'wrapper-session-1');
      assert.deepEqual(trajectory.providers, ['openai']);
      assert.equal(trajectory.session_model, 'gpt-5.5');
      assert.match(JSON.stringify(trajectory.session_tools), /exec_command/);
      assert.match(JSON.stringify(trajectory), /SYSTEM_PROMPT_MUST_SURVIVE/);
      assert.deepEqual(trajectory.turns[0].request_body, {
      source: 'runtime_session',
      role: 'system',
      model: 'gpt-5.5',
      tools_ref: 'session_tools',
      text: 'SYSTEM_PROMPT_MUST_SURVIVE',
    });
      assert.ok(trajectory.turns[1].tool_calls.some((call) => call.name === 'exec_command' && call.declared === true));
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('exports one trajectory per generic JSONL session wrapper row', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-generic-multi-session-'));
    try {
      const input = path.join(dir, 'sample.messages.jsonl');
      const output = path.join(dir, 'coding-trajectories.jsonl');
      fs.writeFileSync(input, [
        { session_id: 's1', model: 'gpt-test', messages: [{ role: 'user', content: 'Patch parser one.' }, { role: 'assistant', content: 'Done one.' }] },
        { session_id: 's2', model: 'gpt-test', messages: [{ role: 'user', content: 'Patch parser two.' }, { role: 'assistant', content: 'Done two.' }] },
      ].map((row) => JSON.stringify(row)).join('\n') + '\n', 'utf8');

      const result = writeTrajectories({ input, output });
      const trajectories = fs.readFileSync(output, 'utf8').trim().split('\n').map((line) => JSON.parse(line));

      assert.equal(result.trajectories.length, 2);
      assert.deepEqual(trajectories.map((trajectory) => trajectory.session_id), ['s1', 's2']);
      assert.deepEqual(trajectories.map((trajectory) => trajectory.task), ['Patch parser one.', 'Patch parser two.']);
      assert.deepEqual(trajectories.map((trajectory) => trajectory.turns.length), [2, 2]);
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('exports OpenAI card prompt/candidates/tools/meta with reasoning_content', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-card-envelope-'));
    try {
      const input = path.join(dir, 'baidu-card.jsonl');
      const output = path.join(dir, 'coding-trajectories.jsonl');
      fs.writeFileSync(input, JSON.stringify({
        task_id: 'card-task-1',
        prompt: [
          { role: 'system', content: [{ type: 'text', text: 'SYSTEM_PROMPT_MUST_SURVIVE' }] },
          { role: 'user', content: [{ type: 'text', text: 'Run the declared command.' }] },
        ],
        candidates: [[{
          role: 'assistant',
          reasoning_content: 'Need inspect before command.',
          content: [{ type: 'text', text: 'I will call the command.' }],
          tool_calls: [{ id: 'call_exec', type: 'function', function: { name: 'exec_command', arguments: '{"cmd":"node --test"}' } }],
        }]],
        tools: [{ type: 'function', function: { name: 'exec_command' } }],
        meta: { model: 'claude-opus-4.5', create_time: '2026-06-23T00:00:00Z' },
      }) + '\n', 'utf8');

      const result = writeTrajectories({ input, output });
      const [trajectory] = fs.readFileSync(output, 'utf8').trim().split('\n').map((line) => JSON.parse(line));

      assert.equal(result.trajectories.length, 1);
      assert.equal(trajectory.session_id, 'card-task-1');
      assert.equal(trajectory.session_model, 'claude-opus-4.5');
      assert.match(JSON.stringify(trajectory.session_tools), /exec_command/);
      assert.ok(trajectory.turns.some((turn) => turn.reasoning === 'Need inspect before command.'));
      assert.ok(trajectory.turns.some((turn) => turn.response_body?.reasoning === true && turn.response_body.text === 'Need inspect before command.'));
      assert.ok(trajectory.turns.some((turn) => turn.tool_calls?.some((call) => call.name === 'exec_command' && call.declared !== true)));
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('exports native call-level request plus response.response_data JSON', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-native-call-'));
    try {
      const input = path.join(dir, 'native-call.json');
      const output = path.join(dir, 'coding-trajectories.jsonl');
      fs.writeFileSync(input, JSON.stringify({
        session_id: 'native-call-1',
        timestamp: '2026-06-23T01:02:03Z',
        request: {
          model: 'claude-sonnet-4-6',
          max_tokens: 4096,
          metadata: { trace_label: 'native-user-1' },
          tools: [{ name: 'Bash', input_schema: { type: 'object' } }],
          messages: [{ role: 'user', content: [{ type: 'text', text: 'Run node --test.' }] }],
        },
        response: {
          response_data: {
            id: 'msg_native_1',
            role: 'assistant',
            model: 'claude-sonnet-4-6',
            stop_reason: 'tool_use',
            usage: { input_tokens: 10, output_tokens: 4 },
            content: [
              { type: 'thinking', thinking: 'Need test result first.', signature: 'thinking-sig-native-1' },
              { type: 'tool_use', id: 'tu_1', name: 'Bash', input: { command: 'node --test' } },
            ],
          },
        },
      }), 'utf8');

      const result = writeTrajectories({ input, output });
      const [trajectory] = fs.readFileSync(output, 'utf8').trim().split('\n').map((line) => JSON.parse(line));

      assert.equal(result.trajectories.length, 1);
      assert.equal(trajectory.session_id, 'native-call-1');
      assert.equal(trajectory.session_model, 'claude-sonnet-4-6');
      assert.equal(trajectory.stats.input_tokens, 10);
      assert.equal(trajectory.stats.output_tokens, 4);
      assert.equal(trajectory.stats.tool_types.Bash, 1);
      assert.equal(trajectory.native_calls[0].request_body.max_tokens, 4096);
      assert.deepEqual(trajectory.native_calls[0].request_body.metadata, { trace_label: 'native-user-1' });
      assert.equal(trajectory.native_calls[0].response_body.response_data.id, 'msg_native_1');
      assert.equal(trajectory.native_calls[0].response_body.response_data.stop_reason, 'tool_use');
      assert.deepEqual(trajectory.native_calls[0].response_body.response_data.usage, { input_tokens: 10, output_tokens: 4 });
      assert.equal(trajectory.native_calls[0].response_body.response_data.content[0].signature, 'thinking-sig-native-1');
      assert.ok(trajectory.turns.some((turn) => turn.reasoning === 'Need test result first.' && turn.reasoning_signature === 'thinking-sig-native-1'));
      assert.ok(trajectory.turns.some((turn) => turn.tool_calls?.some((call) => (
        call.name === 'Bash'
        && call.input !== undefined
        && JSON.stringify(call.input).includes('node --test')
      ))));
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('exports OpenAI native response_body choices and usage without losing normalized text', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-openai-native-call-'));
    try {
      const input = path.join(dir, 'native-openai.messages.json');
      const output = path.join(dir, 'coding-trajectories.jsonl');
      fs.writeFileSync(input, JSON.stringify({
        session_id: 'openai-native-call-1',
        provider: 'openai',
        timestamp: '2026-06-23T02:03:04Z',
        request_body: {
          model: 'gpt-5.5',
          messages: [{ role: 'user', content: 'Summarize the failure.' }],
        },
        response_body: {
          id: 'chatcmpl_native_1',
          model: 'gpt-5.5',
          choices: [{
            index: 0,
            finish_reason: 'stop',
            message: { role: 'assistant', content: 'Tests failed because timeout was too low.' },
          }],
          usage: { prompt_tokens: 7, completion_tokens: 9, total_tokens: 16 },
        },
      }), 'utf8');

      const result = writeTrajectories({ input, output });
      const [trajectory] = fs.readFileSync(output, 'utf8').trim().split('\n').map((line) => JSON.parse(line));

      assert.equal(result.trajectories.length, 1);
      assert.equal(trajectory.session_id, 'openai-native-call-1');
      assert.deepEqual(trajectory.providers, ['openai']);
      assert.deepEqual(trajectory.stats, {
        turns: 2,
        input_tokens: 7,
        output_tokens: 9,
        total_tokens: 16,
        tool_call_count: 0,
        tool_types: {},
        has_tool_calls: false,
        has_code_edit: false,
        has_test_execution: false,
        test_commands: [],
        has_failure_correction: false,
        has_truncated_stream: false,
        has_incomplete_turns: false,
      });
      assert.equal(trajectory.native_calls[0].response_body.id, 'chatcmpl_native_1');
      assert.equal(trajectory.native_calls[0].response_body.choices[0].finish_reason, 'stop');
      assert.deepEqual(trajectory.native_calls[0].response_body.usage, { prompt_tokens: 7, completion_tokens: 9, total_tokens: 16 });
      assert.ok(trajectory.turns.some((turn) => turn.response_body?.text === 'Tests failed because timeout was too low.'));
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('accepts generic chat arrays, wrappers, and single pretty JSON messages', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-generic-formats-'));
    try {
      const cases = [
        {
          name: 'array.chat.json',
          body: [
            { role: 'system', content: 'Hidden setup.' },
            { role: 'user', content: 'Patch the Python parser.' },
          ],
          task: 'Patch the Python parser.',
        },
        {
          name: 'wrapped.messages.json',
          body: { messages: [{ role: 'user', content: 'Run go test.' }] },
          task: 'Run go test.',
        },
        {
          name: 'wrapped.transcript.json',
          body: { turns: [{ role: 'user', content: 'Review TypeScript code.' }] },
          task: 'Review TypeScript code.',
        },
        {
          name: 'single.messages.json',
          body: { role: 'user', content: 'Summarize the Java failure.' },
          task: 'Summarize the Java failure.',
        },
      ];

      for (const item of cases) {
        const input = path.join(dir, item.name);
        const output = path.join(dir, `${item.name}.out.jsonl`);
        fs.writeFileSync(input, JSON.stringify(item.body, null, 2), 'utf8');

        const result = writeTrajectories({ input, output });
        const [trajectory] = fs.readFileSync(output, 'utf8').trim().split('\n').map((line) => JSON.parse(line));

        assert.equal(result.trajectories.length, 1);
        assert.equal(result.rowsRead, 0);
        assert.equal(result.sessionFilesRead, 1);
        assert.equal(trajectory.source_agent, 'generic-chat');
        assert.equal(trajectory.task, item.task);
      }
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('classifies an explicitly named generic session JSONL by content', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-content-session-'));
    try {
      const input = path.join(dir, 'session.jsonl');
      const output = path.join(dir, 'coding-trajectories.jsonl');
      fs.writeFileSync(input, [
        { role: 'user', content: 'Patch the parser and run node --test.' },
        { role: 'assistant', content: 'I will inspect the parser first.' },
      ].map((row) => JSON.stringify(row)).join('\n') + '\n', 'utf8');

      const result = writeTrajectories({ input, output });
      const [trajectory] = fs.readFileSync(output, 'utf8').trim().split('\n').map((line) => JSON.parse(line));

      assert.equal(result.trajectories.length, 1);
      assert.equal(result.rowsRead, 0);
      assert.equal(result.sessionFilesRead, 1);
      assert.equal(trajectory.source_kind, 'runtime_session');
      assert.equal(trajectory.source_agent, 'generic-chat');
      assert.equal(trajectory.task, 'Patch the parser and run node --test.');
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('skips unrelated JSON files while content-classifying an explicit directory', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-content-dir-'));
    try {
      const output = path.join(dir, 'coding-trajectories.jsonl');
      fs.writeFileSync(path.join(dir, 'package.json'), JSON.stringify({ name: 'not-a-session' }), 'utf8');
      fs.writeFileSync(path.join(dir, 'session.jsonl'), [
        { role: 'user', content: 'Fix the JSONL directory parser.' },
        { role: 'assistant', content: 'I will keep unrelated JSON out.' },
      ].map((row) => JSON.stringify(row)).join('\n') + '\n', 'utf8');

      const result = writeTrajectories({ input: dir, output });
      const [trajectory] = fs.readFileSync(output, 'utf8').trim().split('\n').map((line) => JSON.parse(line));

      assert.equal(result.trajectories.length, 1);
      assert.equal(trajectory.task, 'Fix the JSONL directory parser.');
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('fails closed when an explicit JSONL input is not a supported trace or session', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-unknown-jsonl-'));
    try {
      const input = path.join(dir, 'session.jsonl');
      const output = path.join(dir, 'coding-trajectories.jsonl');
      fs.writeFileSync(input, [
        { payload: { message: 'missing role and trace event' } },
        { payload: { message: 'still unsupported' } },
      ].map((row) => JSON.stringify(row)).join('\n') + '\n', 'utf8');

      assert.throws(
        () => writeTrajectories({ input, output }),
        /trajectory input format is not recognized/,
      );
      assert.equal(fs.existsSync(output), false);
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('fails closed when an explicit hidden .jsonl file is not a supported trace or session', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-hidden-jsonl-'));
    try {
      const input = path.join(dir, '.jsonl');
      const output = path.join(dir, 'coding-trajectories.jsonl');
      fs.writeFileSync(input, JSON.stringify({ payload: { message: 'unsupported hidden jsonl' } }) + '\n', 'utf8');

      assert.throws(
        () => writeTrajectories({ input, output }),
        /trajectory input format is not recognized/,
      );
      assert.equal(fs.existsSync(output), false);
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('fails closed when an explicitly named Codex JSONL file has no runtime turns', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-codex-unknown-jsonl-'));
    try {
      const input = path.join(dir, 'codex-unknown.jsonl');
      const output = path.join(dir, 'coding-trajectories.jsonl');
      fs.writeFileSync(input, JSON.stringify({ task_id: 'unsupported', canonical_solution: 'return 1' }) + '\n', 'utf8');

      assert.throws(
        () => writeTrajectories({ input, output }),
        /trajectory input format is not recognized/,
      );
      assert.equal(fs.existsSync(output), false);
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('fails closed when encrypted trace rows cannot be decrypted', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-encrypted-'));
    try {
      const input = path.join(dir, 'traces.jsonl');
      fs.writeFileSync(input, JSON.stringify({
        encrypted: true,
        algorithm: 'aes-256-gcm',
        payload_schema: 'prism_trace_row',
        iv: 'bad',
        tag: 'bad',
        ciphertext: 'bad',
      }) + '\n', 'utf8');

      assert.throws(() => readTraceRowsDetailed(input, { nodeSecret: '' }), /encrypted trace row cannot be exported without node secret/);
      assert.throws(() => readTraceRowsDetailed(input, { nodeSecret: '0'.repeat(64) }), /failed to decrypt encrypted trace row/);
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('decrypts hub_key_envelope rows with a hub private key and fails closed on bad keys', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-hub-key-'));
    try {
      const input = path.join(dir, 'traces.jsonl');
      const { publicKey, privateKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
      const { privateKey: wrongPrivateKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
      const publicPem = publicKey.export({ type: 'spki', format: 'pem' });
      const privatePem = privateKey.export({ type: 'pkcs8', format: 'pem' });
      const wrongPrivatePem = wrongPrivateKey.export({ type: 'pkcs8', format: 'pem' });
      fs.writeFileSync(input, JSON.stringify(encryptRowWithHubKey({
        prism_compatible: true,
        requestId: 'req_hub_key',
        sessionId: 'sess_hub_key',
        path: '/v1/responses',
        upstream: 'openai',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'hub private key decrypts this row' }),
        responseBody: JSON.stringify({ id: 'resp_hub_key' }),
      }, publicPem)) + '\n', 'utf8');

      const result = readTraceRowsDetailed(input, { hubPrivateKey: privatePem });

      assert.equal(result.rows.length, 1);
      assert.equal(result.rows[0].requestId, 'req_hub_key');
      assert.equal(result.stats.encryptedRows, 1);
      assert.equal(result.stats.decryptFailures, 0);
      assert.throws(
        () => readTraceRowsDetailed(input, { hubPrivateKey: wrongPrivatePem }),
        /failed to decrypt encrypted trace row with hub private key/,
      );
      const partial = readTraceRowsDetailed(input, { hubPrivateKey: wrongPrivatePem, allowPartial: true });
      assert.equal(partial.rows.length, 0);
      assert.equal(partial.stats.decryptFailures, 1);
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('falls back to node secret when hub private key cannot decrypt the row', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-hub-node-fallback-'));
    const nodeSecret = 'c'.repeat(64);
    try {
      const input = path.join(dir, 'traces.jsonl');
      const { publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
      const { privateKey: wrongPrivateKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
      const publicPem = publicKey.export({ type: 'spki', format: 'pem' });
      const wrongPrivatePem = wrongPrivateKey.export({ type: 'pkcs8', format: 'pem' });
      const nodeEncrypted = encryptRowWithNodeSecret({
        prism_compatible: true,
        requestId: 'req_hub_fallback',
        sessionId: 'sess_hub_fallback',
        path: '/v1/responses',
        upstream: 'openai',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'node secret fallback row' }),
        responseBody: JSON.stringify({ id: 'resp_hub_fallback' }),
      }, nodeSecret, 7);
      const hubEnvelope = encryptRowWithHubKey({ prism_compatible: true }, publicPem).hub_key_envelope;
      fs.writeFileSync(input, JSON.stringify({ ...nodeEncrypted, hub_key_envelope: hubEnvelope }) + '\n', 'utf8');

      const result = readTraceRowsDetailed(input, {
        hubPrivateKey: wrongPrivatePem,
        nodeSecret,
        nodeSecretKeyring: { 7: nodeSecret },
      });

      assert.equal(result.rows.length, 1);
      assert.equal(result.rows[0].requestId, 'req_hub_fallback');
      assert.equal(result.stats.decryptFailures, 0);
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('CLI accepts split --hub-private-key for hub envelope rows', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-cli-hub-key-'));
    try {
      const input = path.join(dir, 'traces.jsonl');
      const output = path.join(dir, 'trajectories.jsonl');
      const privateKeyFile = path.join(dir, 'hub_private.pem');
      const { publicKey, privateKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
      const publicPem = publicKey.export({ type: 'spki', format: 'pem' });
      const privatePem = privateKey.export({ type: 'pkcs8', format: 'pem' });
      fs.writeFileSync(privateKeyFile, privatePem, { encoding: 'utf8', mode: 0o600 });
      fs.writeFileSync(input, JSON.stringify(encryptRowWithHubKey({
        prism_compatible: true,
        requestId: 'req_cli_hub_key',
        sessionId: 'sess_cli_hub_key',
        path: '/v1/responses',
        upstream: 'openai',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'split hub private key row' }),
        responseBody: JSON.stringify({ id: 'resp_cli_hub_key' }),
      }, publicPem)) + '\n', 'utf8');

      const res = spawnSync(process.execPath, [
        INDEX_JS,
        'trajectory-export',
        '--input',
        input,
        '--output',
        output,
        '--hub-private-key',
        privateKeyFile,
      ], {
        cwd: dir,
        env: {
          ...process.env,
          A2A_NODE_SECRET: '',
          EVOMAP_NODE_SECRET: '',
          EVOLVER_HOME: dir,
          HOME: dir,
        },
        encoding: 'utf8',
      });

      assert.equal(res.status, 0, res.stderr);
      assert.doesNotMatch(`${res.stdout}\n${res.stderr}`, /BEGIN PRIVATE KEY/);
      const exported = fs.readFileSync(output, 'utf8').trim().split('\n').map((line) => JSON.parse(line));
      assert.equal(exported.length, 1);
      assert.equal(exported[0].session_id, 'sess_cli_hub_key');
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('uses row secret_version to select a node secret keyring entry before fallback secret', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-keyring-'));
    const fallbackSecret = 'a'.repeat(64);
    const rotatedSecret = 'b'.repeat(64);
    try {
      const input = path.join(dir, 'traces.jsonl');
      fs.writeFileSync(input, [
        JSON.stringify(encryptRowWithNodeSecret({
          prism_compatible: true,
          requestId: 'req_rotated',
          sessionId: 'sess_rotated',
          path: '/v1/responses',
          upstream: 'openai',
          requestBody: JSON.stringify({ model: 'gpt-test', input: 'rotated secret row' }),
          responseBody: JSON.stringify({ id: 'resp_rotated' }),
        }, rotatedSecret, 2)),
        JSON.stringify(encryptRowWithNodeSecret({
          prism_compatible: true,
          requestId: 'req_fallback',
          sessionId: 'sess_fallback',
          path: '/v1/responses',
          upstream: 'openai',
          requestBody: JSON.stringify({ model: 'gpt-test', input: 'fallback secret row' }),
          responseBody: JSON.stringify({ id: 'resp_fallback' }),
        }, fallbackSecret)),
      ].join('\n') + '\n', 'utf8');

      const result = readTraceRowsDetailed(input, {
        nodeSecret: fallbackSecret,
        nodeSecretKeyring: { 2: rotatedSecret },
      });

      assert.deepEqual(result.rows.map((row) => row.requestId), ['req_rotated', 'req_fallback']);
      assert.equal(result.stats.encryptedRows, 2);
      assert.equal(result.stats.decryptFailures, 0);
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('falls back to nodeSecret when a keyring entry cannot decrypt the row', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-keyring-fallback-'));
    const staleSecret = 'a'.repeat(64);
    const currentSecret = 'b'.repeat(64);
    try {
      const input = path.join(dir, 'traces.jsonl');
      fs.writeFileSync(input, JSON.stringify(encryptRowWithNodeSecret({
        prism_compatible: true,
        requestId: 'req_current_fallback',
        sessionId: 'sess_current_fallback',
        path: '/v1/responses',
        upstream: 'openai',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'current secret row' }),
        responseBody: JSON.stringify({ id: 'resp_current_fallback' }),
      }, currentSecret, 4)) + '\n', 'utf8');

      const result = readTraceRowsDetailed(input, {
        nodeSecret: currentSecret,
        nodeSecretKeyring: { 4: staleSecret },
      });

      assert.equal(result.rows.length, 1);
      assert.equal(result.rows[0].requestId, 'req_current_fallback');
      assert.equal(result.stats.decryptFailures, 0);
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('CLI accepts split --node-secret-keyring and array keyring JSON', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-cli-keyring-'));
    const rotatedSecret = 'c'.repeat(64);
    try {
      const input = path.join(dir, 'traces.jsonl');
      const output = path.join(dir, 'trajectories.jsonl');
      const keyringFile = path.join(dir, 'keyring.json');
      fs.writeFileSync(keyringFile, JSON.stringify([{ version: 3, nodeSecret: rotatedSecret }]), 'utf8');
      fs.writeFileSync(input, JSON.stringify(encryptRowWithNodeSecret({
        prism_compatible: true,
        requestId: 'req_cli_keyring',
        sessionId: 'sess_cli_keyring',
        path: '/v1/responses',
        upstream: 'openai',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'array keyring row' }),
        responseBody: JSON.stringify({ id: 'resp_cli_keyring' }),
      }, rotatedSecret, 3)) + '\n', 'utf8');

      const res = spawnSync(process.execPath, [
        INDEX_JS,
        'trajectory-export',
        '--input',
        input,
        '--output',
        output,
        '--node-secret-keyring',
        keyringFile,
      ], {
        cwd: dir,
        env: {
          ...process.env,
          A2A_NODE_SECRET: '',
          EVOMAP_NODE_SECRET: '',
          EVOLVER_HOME: dir,
          HOME: dir,
        },
        encoding: 'utf8',
      });

      assert.equal(res.status, 0, res.stderr);
      assert.doesNotMatch(`${res.stdout}\n${res.stderr}`, new RegExp(rotatedSecret));
      const exported = fs.readFileSync(output, 'utf8').trim().split('\n').map((line) => JSON.parse(line));
      assert.equal(exported.length, 1);
      assert.equal(exported[0].session_id, 'sess_cli_keyring');
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('CLI accepts literal --node-secret for encrypted rows', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-cli-node-secret-literal-'));
    const secret = 'd'.repeat(64);
    try {
      const input = path.join(dir, 'traces.jsonl');
      const output = path.join(dir, 'trajectories.jsonl');
      fs.writeFileSync(input, JSON.stringify(encryptRowWithNodeSecret({
        prism_compatible: true,
        requestId: 'req_cli_node_secret_literal',
        sessionId: 'sess_cli_node_secret_literal',
        path: '/v1/responses',
        upstream: 'openai',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'literal node secret row' }),
        responseBody: JSON.stringify({ id: 'resp_cli_node_secret_literal' }),
      }, secret)) + '\n', 'utf8');

      const res = spawnSync(process.execPath, [
        INDEX_JS,
        'trajectory-export',
        `--input=${input}`,
        `--output=${output}`,
        `--node-secret=${secret}`,
      ], {
        cwd: dir,
        env: {
          ...process.env,
          A2A_NODE_SECRET: '',
          EVOMAP_NODE_SECRET: '',
          EVOLVER_HOME: dir,
          HOME: dir,
        },
        encoding: 'utf8',
      });

      assert.equal(res.status, 0, res.stderr);
      assert.doesNotMatch(`${res.stdout}\n${res.stderr}`, new RegExp(secret));
      const exported = fs.readFileSync(output, 'utf8').trim().split('\n').map((line) => JSON.parse(line));
      assert.equal(exported.length, 1);
      assert.equal(exported[0].session_id, 'sess_cli_node_secret_literal');
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('CLI reads --node-secret from an existing file path', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-cli-node-secret-file-path-'));
    const secret = 'e'.repeat(64);
    try {
      const input = path.join(dir, 'traces.jsonl');
      const output = path.join(dir, 'trajectories.jsonl');
      const secretFile = path.join(dir, 'node_secret');
      fs.writeFileSync(secretFile, secret + '\n', { encoding: 'utf8', mode: 0o600 });
      fs.writeFileSync(input, JSON.stringify(encryptRowWithNodeSecret({
        prism_compatible: true,
        requestId: 'req_cli_node_secret_path',
        sessionId: 'sess_cli_node_secret_path',
        path: '/v1/responses',
        upstream: 'openai',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'file path node secret row' }),
        responseBody: JSON.stringify({ id: 'resp_cli_node_secret_path' }),
      }, secret)) + '\n', 'utf8');

      const res = spawnSync(process.execPath, [
        INDEX_JS,
        'trajectory-export',
        '--input',
        input,
        '--output',
        output,
        '--node-secret',
        secretFile,
      ], {
        cwd: dir,
        env: {
          ...process.env,
          A2A_NODE_SECRET: '',
          EVOMAP_NODE_SECRET: '',
          EVOLVER_HOME: dir,
          HOME: dir,
        },
        encoding: 'utf8',
      });

      assert.equal(res.status, 0, res.stderr);
      assert.doesNotMatch(`${res.stdout}\n${res.stderr}`, new RegExp(secret));
      const exported = fs.readFileSync(output, 'utf8').trim().split('\n').map((line) => JSON.parse(line));
      assert.equal(exported.length, 1);
      assert.equal(exported[0].session_id, 'sess_cli_node_secret_path');
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('CLI --allow-partial exports plaintext rows when encrypted rows fail decrypt', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-cli-partial-'));
    try {
      const input = path.join(dir, 'traces.jsonl');
      const output = path.join(dir, 'trajectories.jsonl');
      const secretFile = path.join(dir, 'node_secret');
      fs.writeFileSync(secretFile, 'a'.repeat(64) + '\n', { encoding: 'utf8', mode: 0o600 });
      fs.writeFileSync(input, [
        JSON.stringify({
          prism_compatible: true,
          requestId: 'req_plain_cli',
          sessionId: 'sess_plain_cli',
          path: '/v1/responses',
          upstream: 'openai',
          requestBody: JSON.stringify({ model: 'gpt-test', input: 'keep plaintext row' }),
          responseBody: JSON.stringify({ id: 'resp_plain_cli', status: 'completed' }),
        }),
        JSON.stringify({
          encrypted: true,
          algorithm: 'aes-256-gcm',
          payload_schema: 'prism_trace_row',
          iv: 'bad',
          tag: 'bad',
          ciphertext: 'bad',
        }),
      ].join('\n') + '\n', 'utf8');

      const res = spawnSync(process.execPath, [
        INDEX_JS,
        'trajectory-export',
        `--input=${input}`,
        `--output=${output}`,
        `--node-secret-file=${secretFile}`,
        '--allow-partial',
      ], {
        cwd: dir,
        env: {
          ...process.env,
          A2A_NODE_SECRET: '',
          EVOMAP_NODE_SECRET: '',
          EVOLVER_HOME: dir,
          HOME: dir,
        },
        encoding: 'utf8',
      });

      assert.equal(res.status, 0, res.stderr);
      assert.match(res.stdout, /decrypt_failures=1/);
      const exported = fs.readFileSync(output, 'utf8').trim().split('\n').map((line) => JSON.parse(line));
      assert.equal(exported.length, 1);
      assert.equal(exported[0].session_id, 'sess_plain_cli');
      assert.equal(exported[0].task, 'keep plaintext row');
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('CLI node secret env input is not echoed when decrypt fails', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-cli-secret-'));
    const secret = 'a'.repeat(64);
    try {
      const input = path.join(dir, 'traces.jsonl');
      const output = path.join(dir, 'trajectories.jsonl');
      fs.writeFileSync(input, JSON.stringify({
        encrypted: true,
        algorithm: 'aes-256-gcm',
        payload_schema: 'prism_trace_row',
        iv: 'bad',
        tag: 'bad',
        ciphertext: 'bad',
      }) + '\n', 'utf8');

      const res = spawnSync(process.execPath, [
        INDEX_JS,
        'trajectory-export',
        `--input=${input}`,
        `--output=${output}`,
        '--node-secret-env=TRAJECTORY_EXPORT_TEST_SECRET',
      ], {
        cwd: dir,
        env: {
          ...process.env,
          A2A_NODE_SECRET: '',
          EVOMAP_NODE_SECRET: '',
          EVOLVER_HOME: dir,
          HOME: dir,
          TRAJECTORY_EXPORT_TEST_SECRET: secret,
        },
        encoding: 'utf8',
      });

      assert.equal(res.status, 1);
      assert.match(res.stderr, /failed to decrypt encrypted trace row/);
      assert.doesNotMatch(`${res.stdout}\n${res.stderr}`, new RegExp(secret));
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('fails closed when an explicit trace input is missing', () => {
    const missing = path.join(os.tmpdir(), `missing-trajectory-${Date.now()}.jsonl`);

    assert.throws(() => readTraceRowsDetailed(missing), /trace input is not readable/);
    assert.throws(() => writeTrajectories({ input: missing, output: path.join(os.tmpdir(), 'unused-trajectories.jsonl') }), /trace input is not readable/);
    assert.throws(() => writeTrajectories({ input: '', output: path.join(os.tmpdir(), 'unused-trajectories.jsonl') }), /trace input is not readable/);
  });

  it('fails closed when default trace rows cannot be decrypted', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-default-encrypted-'));
    const prevTraceFile = process.env.EVOMAP_PROXY_TRACE_FILE;
    const prevEvolverHome = process.env.EVOLVER_HOME;
    const prevHome = process.env.HOME;
    const prevEvomapSecret = process.env.EVOMAP_NODE_SECRET;
    const prevA2aSecret = process.env.A2A_NODE_SECRET;
    try {
      const input = path.join(dir, 'proxy-traces.jsonl');
      const output = path.join(dir, 'trajectories.jsonl');
      fs.writeFileSync(input, JSON.stringify({
        encrypted: true,
        algorithm: 'aes-256-gcm',
        payload_schema: 'prism_trace_row',
        iv: 'bad',
        tag: 'bad',
        ciphertext: 'bad',
      }) + '\n', 'utf8');
      process.env.EVOMAP_PROXY_TRACE_FILE = input;
      process.env.EVOLVER_HOME = dir;
      process.env.HOME = dir;
      delete process.env.EVOMAP_NODE_SECRET;
      delete process.env.A2A_NODE_SECRET;

      assert.throws(() => writeTrajectories({ output }), /encrypted trace row cannot be exported without node secret or hub private key/);
      assert.equal(fs.existsSync(output), false);
    } finally {
      if (prevTraceFile === undefined) delete process.env.EVOMAP_PROXY_TRACE_FILE;
      else process.env.EVOMAP_PROXY_TRACE_FILE = prevTraceFile;
      if (prevEvolverHome === undefined) delete process.env.EVOLVER_HOME;
      else process.env.EVOLVER_HOME = prevEvolverHome;
      if (prevHome === undefined) delete process.env.HOME;
      else process.env.HOME = prevHome;
      if (prevEvomapSecret === undefined) delete process.env.EVOMAP_NODE_SECRET;
      else process.env.EVOMAP_NODE_SECRET = prevEvomapSecret;
      if (prevA2aSecret === undefined) delete process.env.A2A_NODE_SECRET;
      else process.env.A2A_NODE_SECRET = prevA2aSecret;
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('treats undefined nodeSecret as default secret resolution', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-secret-'));
    const prevSecret = process.env.EVOMAP_NODE_SECRET;
    try {
      const input = path.join(dir, 'traces.jsonl');
      fs.writeFileSync(input, JSON.stringify({
        encrypted: true,
        algorithm: 'aes-256-gcm',
        payload_schema: 'prism_trace_row',
        iv: 'bad',
        tag: 'bad',
        ciphertext: 'bad',
      }) + '\n', 'utf8');
      process.env.EVOMAP_NODE_SECRET = '0'.repeat(64);

      assert.throws(() => readTraceRowsDetailed(input, { nodeSecret: undefined }), /failed to decrypt encrypted trace row/);
    } finally {
      if (prevSecret === undefined) delete process.env.EVOMAP_NODE_SECRET;
      else process.env.EVOMAP_NODE_SECRET = prevSecret;
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('deduplicates request history tool calls already counted from prior responses', () => {
    const trajectory = buildTrajectoryFromRows('sess_history', [
      {
        prism_compatible: true,
        requestId: 'req_first',
        createdAtIso: '2026-06-23T01:00:00.000Z',
        sessionId: 'sess_history',
        path: '/v1/chat/completions',
        upstream: 'openai',
        status: 200,
        requestBody: JSON.stringify({ messages: [{ role: 'user', content: 'Run the JavaScript test' }] }),
        responseBody: JSON.stringify({
          choices: [{ message: { tool_calls: [{ id: 'call_1', function: { name: 'exec_command' } }] } }],
        }),
      },
      {
        prism_compatible: true,
        requestId: 'req_second',
        createdAtIso: '2026-06-23T01:01:00.000Z',
        sessionId: 'sess_history',
        path: '/v1/chat/completions',
        upstream: 'openai',
        status: 200,
        requestBody: JSON.stringify({
          messages: [
            { role: 'user', content: 'Run the JavaScript test' },
            { role: 'assistant', tool_calls: [{ id: 'call_1', function: { name: 'exec_command' } }] },
            { role: 'tool', tool_call_id: 'call_1', content: 'ok' },
            { role: 'user', content: 'continue without tools' },
          ],
        }),
        responseBody: JSON.stringify({ choices: [{ message: { content: 'done' } }] }),
      },
    ]);

    assert.equal(trajectory.stats.tool_call_count, 2);
    assert.equal(trajectory.stats.tool_types.exec_command, 1);
    assert.equal(trajectory.stats.tool_types.tool_result, 1);
    assert.equal(trajectory.turns[1].tool_calls.length, 2);
  });

  it('marks tool output failures as failure-correction candidates', () => {
    const trajectory = buildTrajectoryFromRows('sess_tool_fail', [{
      prism_compatible: true,
      requestId: 'req_tool_fail',
      createdAtIso: '2026-06-23T01:00:00.000Z',
      sessionId: 'sess_tool_fail',
      path: '/v1/responses',
      upstream: 'openai',
      status: 200,
      requestBody: JSON.stringify({ model: 'gpt-test', input: 'Run tests and fix failures' }),
      responseBody: JSON.stringify({
        id: 'resp_tool_fail',
        output: [{ type: 'function_call_output', call_id: 'call_1', output: 'pytest failed: 2 failed; command exited with code 1' }],
      }),
    }]);

    assert.equal(trajectory.stats.has_failure_correction, true);
  });

  it('does not treat ordinary assistant prose about failed tests as failure correction', () => {
    const trajectory = buildTrajectoryFromRows('sess_assistant_prose', [{
      prism_compatible: true,
      requestId: 'req_assistant_prose',
      createdAtIso: '2026-06-23T01:00:00.000Z',
      sessionId: 'sess_assistant_prose',
      path: '/v1/chat/completions',
      upstream: 'openai',
      status: 200,
      requestBody: JSON.stringify({ model: 'gpt-test', messages: [{ role: 'user', content: 'Summarize the build' }] }),
      responseBody: JSON.stringify({
        choices: [{ message: { role: 'assistant', content: 'The report says tests failed yesterday, but this response is only prose.' } }],
      }),
    }]);

    assert.equal(trajectory.stats.has_failure_correction, false);
  });

  it('marks failed request-side tool history as failure-correction candidates', () => {
    const trajectory = buildTrajectoryFromRows('sess_request_tool_fail', [{
      prism_compatible: true,
      requestId: 'req_request_tool_fail',
      createdAtIso: '2026-06-23T01:00:00.000Z',
      sessionId: 'sess_request_tool_fail',
      path: '/v1/chat/completions',
      upstream: 'openai',
      status: 200,
      requestBody: JSON.stringify({
        messages: [
          { role: 'user', content: 'Run tests' },
          { role: 'assistant', tool_calls: [{ id: 'call_fail', function: { name: 'exec_command', arguments: '{"cmd":"pytest"}' } }] },
          { role: 'tool', tool_call_id: 'call_fail', content: 'pytest failed: 1 failed; exit code 1' },
          { role: 'user', content: 'Fix the failure' },
        ],
        tools: [{ type: 'function', function: { name: 'exec_command' } }],
      }),
      responseBody: JSON.stringify({ choices: [{ message: { content: 'I will fix it.' } }] }),
    }]);

    assert.equal(trajectory.stats.has_failure_correction, true);
    assert.equal(trajectory.stats.has_tool_calls, true);
    assert.equal(trajectory.stats.tool_types.exec_command, 1);
    assert.equal(trajectory.stats.tool_types.tool_result, 1);
    assert.equal(trajectory.stats.tool_call_count, 2);
    assert.equal(trajectory.turns[0].tool_calls.filter((call) => call.declared).length, 1);
  });

  it('marks streamed turns without captured response bodies as incomplete', () => {
    const trajectory = buildTrajectoryFromRows('sess_stream_missing', [{
      prism_compatible: true,
      requestId: 'req_stream_missing',
      createdAtIso: '2026-06-23T01:00:00.000Z',
      sessionId: 'sess_stream_missing',
      path: '/v1/responses',
      upstream: 'openai',
      status: 200,
      isStream: true,
      finished: true,
      requestBody: JSON.stringify({ model: 'gpt-test', input: 'stream a response' }),
      responseBody: '',
      responseId: 'resp_stream_missing',
      input_tokens: 10,
      output_tokens: 20,
    }]);

    assert.equal(trajectory.stats.has_incomplete_turns, true);
    assert.equal(trajectory.turns[0].complete, false);
    assert.deepEqual(trajectory.turns[0].incomplete_reasons, ['stream_response_body_missing']);
  });

  it('marks streamed turns with partial bodies as incomplete when transport did not complete', () => {
    const partialResponseBody = {
      reconstructed_stream: true,
      events: [{ type: 'response.output_text.delta', delta: 'partial text' }],
    };
    const rows = [
      {
        prism_compatible: true,
        requestId: 'req_stream_unfinished',
        createdAtIso: '2026-06-23T01:00:00.000Z',
        sessionId: 'sess_stream_transport',
        path: '/v1/responses',
        upstream: 'openai',
        status: 200,
        isStream: true,
        finished: false,
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'stream unfinished' }),
        responseBody: JSON.stringify(partialResponseBody),
      },
      {
        prism_compatible: true,
        requestId: 'req_stream_unobserved',
        createdAtIso: '2026-06-23T01:01:00.000Z',
        sessionId: 'sess_stream_transport',
        path: '/v1/responses',
        upstream: 'openai',
        status: 200,
        isStream: true,
        finished: true,
        finishReason: 'stream_forwarded_unobserved',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'stream forwarded' }),
        responseBody: JSON.stringify(partialResponseBody),
      },
      {
        prism_compatible: true,
        requestId: 'req_stream_cancelled',
        createdAtIso: '2026-06-23T01:02:00.000Z',
        sessionId: 'sess_stream_transport',
        path: '/v1/responses',
        upstream: 'openai',
        status: 499,
        isStream: true,
        finished: false,
        errorMessage: 'client cancelled stream',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'stream cancelled' }),
        responseBody: JSON.stringify(partialResponseBody),
      },
      {
        prism_compatible: true,
        requestId: 'req_stream_error',
        createdAtIso: '2026-06-23T01:03:00.000Z',
        sessionId: 'sess_stream_transport',
        path: '/v1/responses',
        upstream: 'openai',
        status: 502,
        isStream: true,
        finished: true,
        errorMessage: 'upstream stream error: ECONNRESET',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'stream error' }),
        responseBody: JSON.stringify(partialResponseBody),
      },
    ];
    const trajectory = buildTrajectoryFromRows('sess_stream_transport', rows);

    assert.equal(trajectory.stats.has_incomplete_turns, true);
    assert.deepEqual(trajectory.turns.map((turn) => turn.complete), [false, false, false, false]);
    assert.deepEqual(trajectory.turns.map((turn) => turn.incomplete_reasons), [
      ['stream_unfinished'],
      ['stream_forwarded_unobserved'],
      ['stream_cancelled'],
      ['stream_error'],
    ]);
  });

  it('exports explicit stream error and cancellation details', () => {
    const partialResponseBody = {
      reconstructed_stream: true,
      events: [{ type: 'response.output_text.delta', delta: 'partial text' }],
    };
    const trajectory = buildTrajectoryFromRows('sess_stream_details', [
      {
        prism_compatible: true,
        requestId: 'req_stream_error_detail',
        createdAtIso: '2026-06-23T01:00:00.000Z',
        sessionId: 'sess_stream_details',
        path: '/v1/responses',
        upstream: 'openai',
        status: 502,
        isStream: true,
        finished: false,
        stream_error: 'upstream stream error ECONNRESET',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'stream error' }),
        responseBody: JSON.stringify(partialResponseBody),
      },
      {
        prism_compatible: true,
        requestId: 'req_stream_cancel_detail',
        createdAtIso: '2026-06-23T01:01:00.000Z',
        sessionId: 'sess_stream_details',
        path: '/v1/responses',
        upstream: 'openai',
        status: 499,
        isStream: true,
        finished: false,
        stream_cancelled: 'client cancelled stream',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'stream cancel' }),
        responseBody: JSON.stringify(partialResponseBody),
      },
    ]);

    assert.equal(trajectory.turns[0].stream_error, 'upstream stream error ECONNRESET');
    assert.equal(trajectory.turns[1].stream_cancelled, 'client cancelled stream');
    assert.deepEqual(trajectory.turns.map((turn) => turn.incomplete_reasons), [
      ['stream_error'],
      ['stream_cancelled'],
    ]);
  });

  it('marks missing, invalid, empty, and truncated native bodies as incomplete', () => {
    const trajectory = buildTrajectoryFromRows('sess_incomplete', [
      {
        prism_compatible: true,
        requestId: 'req_metadata_only',
        createdAtIso: '2026-06-23T01:00:00.000Z',
        sessionId: 'sess_incomplete',
        path: '/v1/messages',
        upstream: 'anthropic',
        status: 200,
      },
      {
        prism_compatible: true,
        requestId: 'req_invalid_request',
        createdAtIso: '2026-06-23T01:01:00.000Z',
        sessionId: 'sess_incomplete',
        path: '/v1/messages',
        upstream: 'anthropic',
        status: 200,
        requestBody: '{bad json',
        responseBody: JSON.stringify({ id: 'msg_valid' }),
      },
      {
        prism_compatible: true,
        requestId: 'req_empty_response',
        createdAtIso: '2026-06-23T01:02:00.000Z',
        sessionId: 'sess_incomplete',
        path: '/v1/messages',
        upstream: 'anthropic',
        status: 200,
        requestBody: JSON.stringify({ model: 'claude-test' }),
        responseBody: '{}',
      },
      {
        prism_compatible: true,
        requestId: 'req_truncated',
        createdAtIso: '2026-06-23T01:03:00.000Z',
        sessionId: 'sess_incomplete',
        path: '/v1/chat/completions',
        upstream: 'openai',
        status: 200,
        body_truncated: true,
        requestBody: JSON.stringify({ model: 'gpt-test', messages: [{ role: 'user', content: 'hello' }] }),
        responseBody: JSON.stringify({ content_truncated: true }),
      },
    ]);

    assert.equal(trajectory.stats.has_incomplete_turns, true);
    assert.equal(trajectory.stats.has_truncated_stream, true);
    assert.deepEqual(trajectory.turns.map((turn) => turn.complete), [false, false, false, false]);
    assert.deepEqual(trajectory.turns[0].incomplete_reasons, ['request_body_missing', 'response_body_missing']);
    assert.deepEqual(trajectory.turns[1].incomplete_reasons, ['request_body_invalid_json']);
    assert.deepEqual(trajectory.turns[2].incomplete_reasons, ['response_body_empty']);
    assert.deepEqual(trajectory.turns[3].incomplete_reasons, ['body_truncated', 'response_body_truncated']);
    assert.equal(trajectory.turns[3].response_events_truncated, true);
  });

  it('exports Trial Pack trajectory_id, string meta JSON, system prompt, thinking, and raw source records', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-trial-pack-'));
    try {
      const input = path.join(dir, 'trial.messages.jsonl');
      const output = path.join(dir, 'coding-trajectories.jsonl');
      fs.writeFileSync(input, JSON.stringify({
        trajectory_id: 'trial-pack-trajectory-1',
        meta: JSON.stringify({
          model_name: 'claude-trial-pack',
          risk: { level: 'low' },
          fidelity: { source: 'trial-pack', complete: true },
          confidentiality: { tier: 'internal' },
        }),
        system_prompt: 'TRIAL_SYSTEM_PROMPT',
        messages: [
          { role: 'user', content: 'Patch Trial Pack export.' },
          {
            role: 'assistant',
            thinking: 'Need preserve top-level thinking.',
            content: 'Done.',
            usage: { input_tokens: 3, output_tokens: 4 },
          },
        ],
      }) + '\n', 'utf8');

      const result = writeTrajectories({ input, output });
      const [trajectory] = fs.readFileSync(output, 'utf8').trim().split('\n').map((line) => JSON.parse(line));

      assert.equal(result.trajectories.length, 1);
      assert.equal(trajectory.session_id, 'trial-pack-trajectory-1');
      assert.equal(trajectory.session_model, 'claude-trial-pack');
      assert.deepEqual(trajectory.risk, { level: 'low' });
      assert.deepEqual(trajectory.fidelity, { source: 'trial-pack', complete: true });
      assert.deepEqual(trajectory.confidentiality, { tier: 'internal' });
      assert.match(JSON.stringify(trajectory), /TRIAL_SYSTEM_PROMPT/);
      assert.equal(trajectory.stats.input_tokens, 3);
      assert.equal(trajectory.stats.output_tokens, 4);
      const reasoningTurn = trajectory.turns.find((turn) => turn.reasoning === 'Need preserve top-level thinking.');
      assert.ok(reasoningTurn);
      assert.equal(reasoningTurn.model, 'claude-trial-pack');
      assert.equal(trajectory.metadata.model_name, 'claude-trial-pack');
      assert.equal(reasoningTurn.source_record_index, 0);
      assert.equal(reasoningTurn.raw_row_index, 0);
      assert.equal(trajectory.source_records[0].trajectory_id, 'trial-pack-trajectory-1');
      assert.equal(trajectory.raw_rows[0].trajectory_id, 'trial-pack-trajectory-1');
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('exports normalized showcase metadata, usage, risk, fidelity, confidentiality, headers, ttfb, and raw passthrough', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-showcase-'));
    try {
      const input = path.join(dir, 'normalized.messages.json');
      const output = path.join(dir, 'coding-trajectories.jsonl');
      fs.writeFileSync(input, JSON.stringify({
        metadata: {
          model: 'gpt-showcase',
          system_prompt: 'SHOWCASE_SYSTEM_PROMPT',
          client_source: 'showcase-client',
          authorization: 'placeholder',
        },
        usage: { prompt_tokens: 11, completion_tokens: 12 },
        risk: { score: 0.1 },
        fidelity: { transcript: 'raw-plus-normalized' },
        confidentiality: { pii: false },
        headers: { 'set-cookie': 'placeholder', 'x-trace-id': 'trace-1' },
        ttfb_ms: 42,
        messages: [
          { role: 'user', content: 'Build normalized showcase.' },
          { role: 'assistant', content: 'ok' },
        ],
      }), 'utf8');

      const result = writeTrajectories({ input, output });
      const [trajectory] = fs.readFileSync(output, 'utf8').trim().split('\n').map((line) => JSON.parse(line));

      assert.equal(result.trajectories.length, 1);
      assert.equal(trajectory.session_model, 'gpt-showcase');
      assert.equal(trajectory.client_source, 'showcase-client');
      assert.equal(trajectory.metadata.model, 'gpt-showcase');
      assert.equal(trajectory.metadata.authorization, '[redacted]');
      assert.deepEqual(trajectory.usage, { prompt_tokens: 11, completion_tokens: 12 });
      assert.deepEqual(trajectory.risk, { score: 0.1 });
      assert.deepEqual(trajectory.fidelity, { transcript: 'raw-plus-normalized' });
      assert.deepEqual(trajectory.confidentiality, { pii: false });
      assert.equal(trajectory.stats.input_tokens, 11);
      assert.equal(trajectory.stats.output_tokens, 12);
      assert.match(JSON.stringify(trajectory), /SHOWCASE_SYSTEM_PROMPT/);
      const firstTurn = trajectory.turns[0];
      assert.equal(firstTurn.client_source, 'showcase-client');
      assert.equal(firstTurn.headers['set-cookie'], '[redacted]');
      assert.equal(firstTurn.headers['x-trace-id'], 'trace-1');
      assert.equal(firstTurn.ttfb_ms, 42);
      assert.equal(firstTurn.source_record_index, 0);
      assert.equal(firstTurn.raw_row_index, 0);
      assert.equal(trajectory.source_records[0].metadata.authorization, '[redacted]');
      assert.equal(trajectory.raw_rows[0].metadata.authorization, '[redacted]');
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('exports proxy trace raw passthrough, metadata, headers, ttfb, and degraded body-stripped reasons', () => {
    const trajectory = buildTrajectoryFromRows('sess_passthrough', [{
      prism_compatible: true,
      requestId: 'req_passthrough',
      createdAtIso: '2026-06-23T01:00:00.000Z',
      sessionId: 'sess_passthrough',
      path: '/v1/responses',
      upstream: 'openai',
      status: 200,
      requestBody: JSON.stringify({ model: 'gpt-test', input: 'hello' }),
      responseBody: JSON.stringify({ id: 'resp_passthrough', status: 'completed' }),
      metadata: { source: 'raw-fixture', authorization: 'placeholder' },
      usage: { input_tokens: 5, output_tokens: 6 },
      risk: { level: 'low' },
      fidelity: { normalized: true },
      confidentiality: { pii: false },
      source_record: { authorization: 'placeholder', raw: 'source' },
      raw_row: { cookie: 'placeholder', raw: 'row' },
      headers: { 'set-cookie': 'placeholder', 'x-upstream': 'ok' },
      ttfb_ms: 123,
      trace_degraded: true,
      trace_degraded_reason: 'missing_node_secret',
      body_stripped: true,
      body_stripped_reason: 'missing_node_secret',
    }]);

    const turn = trajectory.turns[0];
    assert.equal(turn.metadata.authorization, '[redacted]');
    assert.equal(turn.source_record_index, 0);
    assert.equal(turn.raw_row_index, 0);
    assert.equal(trajectory.source_records[0].authorization, '[redacted]');
    assert.equal(trajectory.raw_rows[0].cookie, '[redacted]');
    assert.equal(turn.headers['set-cookie'], '[redacted]');
    assert.equal(turn.headers['x-upstream'], 'ok');
    assert.equal(turn.ttfb_ms, 123);
    assert.equal(turn.trace_degraded, true);
    assert.equal(turn.trace_degraded_reason, 'missing_node_secret');
    assert.equal(turn.body_stripped, true);
    assert.equal(turn.body_stripped_reason, 'missing_node_secret');
    assert.deepEqual(turn.usage, { input_tokens: 5, output_tokens: 6 });
    assert.deepEqual(turn.risk, { level: 'low' });
    assert.equal(turn.complete, false);
    assert.ok(turn.incomplete_reasons.includes('trace_degraded'));
    assert.ok(turn.incomplete_reasons.includes('body_stripped'));
  });

  it('marks oversized runtime transcript fields as truncated and incomplete with omitted bytes', () => {
    const oversized = 'x'.repeat(1024 * 1024 + 2048);
    const trajectory = buildTrajectoryFromSessionLog({
      sourceAgent: 'generic-chat',
      sourcePath: 'oversized.messages.jsonl',
      sessionId: 'runtime-oversized',
      turns: [{ role: 'user', text: oversized, isMeta: false }],
    });

    const turn = trajectory.turns[0];
    assert.equal(turn.complete, false);
    assert.equal(turn.body_truncated, true);
    assert.ok(turn.omitted_bytes > 0);
    assert.deepEqual(turn.incomplete_reasons, ['body_truncated']);
    assert.equal(turn.request_body.body_truncated, true);
    assert.equal(turn.request_body.incomplete_reasons.includes('body_truncated'), true);
    assert.ok(turn.request_body.omitted_bytes > 0);
  });

  it('writes exported trajectories with owner-only permissions', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-'));
    try {
      const input = path.join(dir, 'traces.jsonl');
      const output = path.join(dir, 'trajectories.jsonl');
      fs.writeFileSync(input, JSON.stringify({
        prism_compatible: true,
        requestId: 'req_perm',
        sessionId: 'sess_perm',
        path: '/v1/responses',
        upstream: 'openai',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'hello' }),
      }) + '\n', 'utf8');

      const result = writeTrajectories({ input, output });
      assert.equal(result.trajectories.length, 1);
      if (process.platform !== 'win32') {
        assert.equal(fs.statSync(output).mode & 0o777, 0o600);
      }
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });

  it('tightens permissions when overwriting an existing export file', () => {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'trajectory-export-'));
    try {
      const input = path.join(dir, 'traces.jsonl');
      const output = path.join(dir, 'trajectories.jsonl');
      fs.writeFileSync(input, JSON.stringify({
        prism_compatible: true,
        requestId: 'req_perm_existing',
        sessionId: 'sess_perm_existing',
        path: '/v1/responses',
        upstream: 'openai',
        requestBody: JSON.stringify({ model: 'gpt-test', input: 'hello' }),
      }) + '\n', 'utf8');
      fs.writeFileSync(output, 'old\n', { encoding: 'utf8', mode: 0o644 });
      try {
        fs.chmodSync(output, 0o644);
      } catch {
        // Best effort on filesystems that do not support POSIX modes.
      }

      writeTrajectories({ input, output });
      if (process.platform !== 'win32') {
        assert.equal(fs.statSync(output).mode & 0o777, 0o600);
      }
    } finally {
      fs.rmSync(dir, { recursive: true, force: true });
    }
  });
});
