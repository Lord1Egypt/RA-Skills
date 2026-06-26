#!/usr/bin/env node
'use strict';

const { createHermesAdapter } = require('./index');

function print(value) {
  process.stdout.write(JSON.stringify(value, null, 2) + '\n');
}

function fail(message, extra) {
  const payload = Object.assign({ status: 'ERROR', message }, extra || {});
  process.stderr.write(JSON.stringify(payload, null, 2) + '\n');
  process.exit(1);
}

function parseInput(rawInput) {
  if (!rawInput) return {};
  try {
    return JSON.parse(rawInput);
  } catch (error) {
    fail('Invalid JSON input', { input: rawInput, error: error.message });
  }
}

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  const adapter = createHermesAdapter();

  if (!command || command === 'help' || command === '--help') {
    process.stdout.write([
      'Hermes adapter CLI',
      '  node hermes/cli.js tools',
      '  node hermes/cli.js manifest',
      '  node hermes/cli.js schema <tool>',
      '  node hermes/cli.js openai-tools',
      '  node hermes/cli.js mcp-tools',
      '  node hermes/cli.js smoke',
      '  node hermes/cli.js verify',
      '  node hermes/cli.js call <tool> [json-input]',
      'Examples:',
      '  node hermes/cli.js call env',
      '  node hermes/cli.js call owned',
      '  node hermes/cli.js call boot {"sessionId":"demo"}',
      '  node hermes/cli.js call status {"tokenId":1}',
      '  node hermes/cli.js schema status',
      '  node hermes/cli.js openai-tools',
      '  node hermes/cli.js mcp-tools',
      '  node hermes/cli.js call raw {"command":"wallet","expectJson":false}'
    ].join('\n') + '\n');
    return;
  }

  if (command === 'tools') {
    print({
      status: 'OK',
      tools: Object.keys(adapter.tools).map(function(name) {
        return { name, description: adapter.tools[name].description };
      })
    });
    return;
  }

  if (command === 'manifest') {
    print({ status: 'OK', manifest: adapter.manifest });
    return;
  }

  if (command === 'schema') {
    const toolName = args[1];
    if (!toolName) {
      fail('Missing tool name');
    }
    const schema = adapter.toolSchemas[toolName];
    if (!schema) {
      fail('Unknown tool', { tool: toolName, availableTools: Object.keys(adapter.toolSchemas) });
    }
    print({ status: 'OK', tool: toolName, schema });
    return;
  }

  if (command === 'openai-tools') {
    print({ status: 'OK', tools: adapter.openAiTools });
    return;
  }

  if (command === 'mcp-tools') {
    print({ status: 'OK', tools: adapter.mcpTools });
    return;
  }

  if (command === 'smoke') {
    const env = await adapter.tools.env.execute({});
    const owned = await adapter.tools.owned.execute({});
    const boot = await adapter.tools.boot.execute({ sessionId: 'smoke' });
    print({
      status: 'OK',
      checks: {
        env: {
          status: env.status,
          hasWallet: Object.prototype.hasOwnProperty.call(env, 'hasWallet'),
          commands: env.commands || null
        },
        owned: {
          status: owned.status,
          scope: owned.scope || null,
          count: owned.count || 0
        },
        boot: {
          status: boot.status,
          hasOwnedNFAs: Array.isArray(boot.ownedNFAs),
          selectRequired: Object.prototype.hasOwnProperty.call(boot, 'selectRequired'),
          emotionTrigger: Object.prototype.hasOwnProperty.call(boot, 'emotionTrigger')
        }
      }
    });
    return;
  }

  if (command === 'verify') {
    const checks = {};
    checks.env = await adapter.tools.env.execute({});
    checks.owned = await adapter.tools.owned.execute({});
    checks.boot = await adapter.tools.boot.execute({ sessionId: 'verify' });
    checks.wallet = await adapter.tools.wallet.execute({});
    checks.world = await adapter.tools.world.execute({});
    checks.supply = await adapter.tools.supply.execute({});
    checks.market_search = await adapter.tools.market_search.execute({});
    checks.pk_search = await adapter.tools.pk_search.execute({});
    checks.raw_wallet = await adapter.tools.raw.execute({ command: 'wallet', expectJson: false });

    print({
      status: 'OK',
      verification: {
        envStatus: checks.env.status,
        ownedStatus: checks.owned.status,
        bootStatus: checks.boot.status,
        walletLines: checks.wallet.lines,
        worldKeys: Object.keys(checks.world),
        supplyKeys: Object.keys(checks.supply),
        marketSearchType: Array.isArray(checks.market_search) ? 'array' : typeof checks.market_search,
        pkSearchType: Array.isArray(checks.pk_search) ? 'array' : typeof checks.pk_search,
        rawWalletLines: checks.raw_wallet.lines,
        manifestTools: adapter.manifest.tools.length,
        openAiTools: adapter.openAiTools.length,
        mcpTools: adapter.mcpTools.length
      }
    });
    return;
  }

  if (command === 'call') {
    const toolName = args[1];
    if (!toolName) {
      fail('Missing tool name');
    }
    const tool = adapter.tools[toolName];
    if (!tool) {
      fail('Unknown tool', { tool: toolName, availableTools: Object.keys(adapter.tools) });
    }
    const rawInput = args.slice(2).join(' ').trim();
    const input = parseInput(rawInput);
    const result = await tool.execute(input);
    print({ status: 'OK', tool: toolName, result });
    return;
  }

  fail('Unknown command', { command });
}

main().catch(function(error) {
  fail(error && error.message ? error.message : String(error), {
    code: error && error.code ? error.code : null,
    command: error && error.command ? error.command : null,
    args: error && error.args ? error.args : null,
    exitCode: error && typeof error.exitCode === 'number' ? error.exitCode : null,
    stdout: error && typeof error.stdout === 'string' ? error.stdout : null,
    stderr: error && typeof error.stderr === 'string' ? error.stderr : null
  });
});
