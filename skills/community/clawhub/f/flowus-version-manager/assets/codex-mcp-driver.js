// Optional Codex host driver. Python performs policy, journaling, and byte verification.
// The host executes native MCP tools; credentials and signed responses are never saved here.
function relayReplyContainsTransaction(value) {
  if (typeof value === 'string') return /[?&](?:amp;)?(?:token|access_token|refresh_token|signature|credential|auth_key|api_key|apikey|authorization|policy|awsaccesskeyid|expires|x-amz-[a-z-]+|x-oss-[a-z-]+|q-sign-[a-z-]+|x-cos-security-token)=/i.test(value)
    || (value.match(/https?:\/\/[^\s<>"\\]+/ig) || []).some(url => /\?/.test(url)
      && /^https?:\/\/(?:[^/?]+\.)?(?:flowus\.cn|flowus\.app|myqcloud\.com|aliyuncs\.com)(?:\/|\?)/i.test(url));
  if (Array.isArray(value)) return value.some(relayReplyContainsTransaction);
  if (value && typeof value === 'object') return Object.entries(value).some(([key, item]) =>
    /^(?:access_token|refresh_token|authorization|cookie|upload_url|headers)$/i.test(key) || relayReplyContainsTransaction(item));
  return false;
}

function projectRelayResult(tool, data) {
  if (tool === 'flowus_help') {
    return {results: (data.results || [data]).map(item => ({callable: item.callable,
      operation: {path: item.operation?.path, method: item.operation?.method}})),
      _cva_projection: 'named_operation_declarations'};
  }
  // This adapter uses Markdown export only to find actual attachment links.
  // Database property/frontmatter text is already read through the page/query tools.
  if (tool === 'flowus_get_page_markdown' && typeof data.markdown === 'string') {
    return {markdown: (data.markdown.match(/https:\/\/[^\s<>"\\]+/g) || []).join('\n'),
      _cva_projection: 'official_export_link_candidates'};
  }
  return data;
}

async function runMcpRelay({tools, job, onProgress = () => {}}) {
  const quote = value => "'" + String(value).replace(/'/g, "'\\''") + "'";
  const allowed = new Set([
    'flowus_help', 'flowus_get_current_user', 'flowus_get_page', 'flowus_create_page',
    'flowus_update_page', 'flowus_get_database', 'flowus_create_database', 'flowus_query_database',
    'flowus_get_block', 'flowus_get_block_children', 'flowus_append_block_children',
    'flowus_update_block', 'flowus_create_file_upload', 'flowus_get_page_markdown', 'flowus_move_page'
  ]);
  const helped = new Set(['flowus_help']);
  const failed = result => {
    const description = (result.content || []).filter(item => item.type === 'text').map(item => item.text).join('\n');
    return {code: /Transport send error|error sending request|http\/request failed/.test(description) ? 'mcp_transport_error' : 'mcp_tool_error'};
  };
  async function invokeNative(tool, args) {
    const invoke = tools['mcp__flowus__' + tool];
    if (typeof invoke !== 'function') throw new Error('Native MCP tool unavailable');
    const safe = tool === 'flowus_help' || tool.startsWith('flowus_get_') || tool === 'flowus_query_database'
      || (tool === 'flowus_create_page' && Boolean(args.idempotency_key));
    for (let attempt = 0; ; attempt++) {
      const result = await invoke(args);
      if (!safe || attempt === 2 || !result.isError) return result;
      await onProgress({retry: attempt + 1, tool, reason: failed(result).code});
      await new Promise(resolve => setTimeout(resolve, (attempt + 1) * 1000));
    }
  }
  const unwrap = result => {
    if (result.structuredContent) return result.structuredContent;
    for (const content of result.content || []) {
      if (content.type === 'text') {
        try { return JSON.parse(content.text); } catch (_) {}
      }
    }
    throw new Error('Native MCP returned no JSON object');
  };
  async function readJson(path, chars) {
    if (chars === undefined) {
      const stat = await tools.exec_command({cmd: 'python3 -c ' + quote('import pathlib,sys; print(len(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")))') + ' ' + quote(path), max_output_tokens: 200});
      if (stat.exit_code !== 0) throw new Error('Cannot read private relay result');
      chars = Number(stat.output.trim());
    }
    if (!Number.isInteger(chars) || chars < 0 || chars > 16 * 1024 * 1024) throw new Error('Invalid relay JSON size');
    const offsets = Array.from({length: Math.ceil(chars / 4000)}, (_, index) => index * 4000);
    const pieces = [];
    for (let start = 0; start < offsets.length; start += 8) {
      const results = await Promise.allSettled(offsets.slice(start, start + 8).map(async offset => {
        const code = 'import json,pathlib,sys; s=pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"); n=int(sys.argv[2]); print(json.dumps({"part":s[n:n+4000]},ensure_ascii=False))';
        const result = await tools.exec_command({cmd: 'python3 -c ' + quote(code) + ' ' + quote(path) + ' ' + offset, max_output_tokens: 10000});
        if (result.exit_code !== 0) throw new Error('Cannot read relay request');
        return JSON.parse(result.output).part;
      }));
      for (const result of results) {
        if (result.status !== 'fulfilled') throw result.reason;
        pieces.push(result.value);
      }
    }
    return JSON.parse(pieces.join(''));
  }
  const command = ['python3', '-u', job.program, '--config', job.config, '--result-file', job.resultFile, ...job.args].map(quote).join(' ');
  let response = await tools.exec_command({cmd: command, workdir: job.cwd, tty: true,
    yield_time_ms: 1000, max_output_tokens: 2500, sandbox_permissions: 'require_escalated', justification: job.justification});
  let session = response.session_id;
  let buffer = '';
  let requests = 0;
  let lastProgress = Date.now();
  try {
  while (true) {
    buffer += response.output.replace(/\r/g, '');
    let request = null;
    while (buffer.includes('\n')) {
      const index = buffer.indexOf('\n');
      const line = buffer.slice(0, index);
      buffer = buffer.slice(index + 1);
      if (line.startsWith('CVA_MCP_REQUEST ')) {
        if (request) throw new Error('Concurrent requests on one relay stream');
        request = JSON.parse(line.slice('CVA_MCP_REQUEST '.length));
      }
    }
    if (request) {
      if (++requests > 4000) throw new Error('Relay request limit reached');
      if (!allowed.has(request.tool) || !/\/cva-mcp-request-[A-Za-z0-9_-]+\/request\.json$/.test(request.request_file)) throw new Error('Unexpected relay request');
      const call = await readJson(request.request_file, request.request_chars);
      if (call.id !== request.id || call.tool !== request.tool) throw new Error('Relay request changed');
      let reply;
      try {
        if (!helped.has(call.tool)) {
          const help = await invokeNative('flowus_help', {query: [call.tool], detail: 'input'});
          if (help.isError) throw failed(help);
          helped.add(call.tool);
        }
        const result = await invokeNative(call.tool, call.arguments);
        if (result.isError && !result.structuredContent) {
          let data;
          try { data = unwrap(result); } catch (_) { data = failed(result); }
          reply = {id: call.id, ok: false, error: data};
        } else {
          const data = unwrap(result);
          reply = result.isError || data.object === 'error' ? {id: call.id, ok: false, error: data}
            : {id: call.id, ok: true, data: projectRelayResult(call.tool, data)};
        }
      } catch (error) {
        reply = {id: call.id, ok: false, error: {code: error.code || 'mcp_tool_error'}};
      }
      if (requests === 1 || Date.now() - lastProgress > 20000) {
        await onProgress({requests, tool: call.tool});
        lastProgress = Date.now();
      }
      let serialized;
      const plain = JSON.stringify(reply);
      if (plain.length > 1000 && !relayReplyContainsTransaction(reply)) {
        const path = request.request_file.replace(/request\.json$/, 'response.json');
        await tools.apply_patch('*** Begin Patch\n*** Add File: ' + path + '\n+' + plain + '\n*** End Patch');
        serialized = JSON.stringify({id: reply.id, response_file: path}) + '\n';
      } else {
        serialized = plain + '\n';
        if (serialized.length > 16000) throw new Error('Sensitive MCP response exceeds the reviewed plain-JSON transport bound; no encoded fallback');
      }
      response = await tools.write_stdin({session_id: session, chars: serialized, yield_time_ms: 250, max_output_tokens: 2500});
      continue;
    }
    if (response.exit_code !== undefined) {
      const result = await readJson(job.resultFile);
      return {exit_code: response.exit_code, requests, result};
    }
    if (!session) throw new Error('Relay process ended before completion');
    response = await tools.write_stdin({session_id: session, chars: '', yield_time_ms: 250, max_output_tokens: 2500});
  }
  } catch (error) {
    if (session) {
      try { await tools.write_stdin({session_id: session, chars: '\u0003', yield_time_ms: 1000, max_output_tokens: 200}); } catch (_) {}
    }
    throw error;
  }
}
