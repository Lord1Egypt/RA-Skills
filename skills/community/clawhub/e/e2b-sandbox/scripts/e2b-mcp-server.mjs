#!/usr/bin/env node
import process from 'node:process';
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import {
  createSandbox,
  listSandboxes,
  getSandboxInfo,
  execInSandbox,
  getSandboxHost,
  setSandboxTimeout,
  snapshotSandbox,
  killSandbox,
  STATE_PATH,
} from './e2b-core.mjs';

function textResult(data) {
  return { content: [{ type: 'text', text: JSON.stringify(data, null, 2) }] };
}

function requireApiKey() {
  if (!process.env.E2B_API_KEY?.trim()) {
    throw new Error('Missing E2B_API_KEY');
  }
}

const tools = [
  {
    name: 'create_sandbox',
    description: 'Create a new E2B sandbox and save its id/label in the local skill state file.',
    inputSchema: {
      type: 'object',
      properties: {
        label: { type: 'string', description: 'Optional human-friendly label for later reuse.' },
        template: { type: 'string', description: 'E2B template name or id. Defaults to base.' },
        timeoutMs: { type: 'number', description: 'Sandbox timeout in milliseconds.' },
        envs: { type: 'object', additionalProperties: { type: 'string' } },
        metadata: { type: 'object', additionalProperties: { type: 'string' } }
      }
    }
  },
  {
    name: 'list_sandboxes',
    description: 'List sandboxes tracked by this skill from the local state file.',
    inputSchema: { type: 'object', properties: {} }
  },
  {
    name: 'get_info',
    description: 'Get live information for a sandbox by id or label.',
    inputSchema: {
      type: 'object',
      required: ['sandbox'],
      properties: { sandbox: { type: 'string', description: 'Sandbox id or saved label.' } }
    }
  },
  {
    name: 'exec',
    description: 'Run a one-shot command inside an E2B sandbox.',
    inputSchema: {
      type: 'object',
      required: ['sandbox', 'cmd'],
      properties: {
        sandbox: { type: 'string' },
        cmd: { type: 'string' },
        cwd: { type: 'string' },
        timeoutMs: { type: 'number' },
        envs: { type: 'object', additionalProperties: { type: 'string' } }
      }
    }
  },
  {
    name: 'host',
    description: 'Get the public E2B host URL for a port exposed by the sandbox.',
    inputSchema: {
      type: 'object',
      required: ['sandbox', 'port'],
      properties: {
        sandbox: { type: 'string' },
        port: { type: 'number' }
      }
    }
  },
  {
    name: 'set_timeout',
    description: 'Update the timeout for a running sandbox.',
    inputSchema: {
      type: 'object',
      required: ['sandbox', 'timeoutMs'],
      properties: {
        sandbox: { type: 'string' },
        timeoutMs: { type: 'number' }
      }
    }
  },
  {
    name: 'snapshot',
    description: 'Create a persistent snapshot from a running sandbox.',
    inputSchema: {
      type: 'object',
      required: ['sandbox'],
      properties: { sandbox: { type: 'string' } }
    }
  },
  {
    name: 'kill',
    description: 'Terminate a sandbox and remove it from the local skill state file.',
    inputSchema: {
      type: 'object',
      required: ['sandbox'],
      properties: { sandbox: { type: 'string' } }
    }
  }
];

const server = new Server(
  { name: 'e2b-sandbox', version: '1.0.0' },
  { capabilities: { tools: {} } },
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({ tools }));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  requireApiKey();
  const name = request.params.name;
  const args = request.params.arguments ?? {};
  switch (name) {
    case 'create_sandbox':
      return textResult(await createSandbox({
        label: typeof args.label === 'string' ? args.label : null,
        template: typeof args.template === 'string' ? args.template : 'base',
        timeoutMs: typeof args.timeoutMs === 'number' ? args.timeoutMs : 3_600_000,
        envs: args.envs && typeof args.envs === 'object' ? args.envs : {},
        metadata: args.metadata && typeof args.metadata === 'object' ? args.metadata : {},
      }));
    case 'list_sandboxes':
      return textResult(await listSandboxes());
    case 'get_info':
      return textResult(await getSandboxInfo({ sandbox: args.sandbox }));
    case 'exec':
      return textResult(await execInSandbox({
        sandbox: args.sandbox,
        cmd: args.cmd,
        cwd: typeof args.cwd === 'string' ? args.cwd : undefined,
        timeoutMs: typeof args.timeoutMs === 'number' ? args.timeoutMs : undefined,
        envs: args.envs && typeof args.envs === 'object' ? args.envs : {},
      }));
    case 'host':
      return textResult(await getSandboxHost({ sandbox: args.sandbox, port: args.port }));
    case 'set_timeout':
      return textResult(await setSandboxTimeout({ sandbox: args.sandbox, timeoutMs: args.timeoutMs }));
    case 'snapshot':
      return textResult(await snapshotSandbox({ sandbox: args.sandbox }));
    case 'kill':
      return textResult(await killSandbox({ sandbox: args.sandbox }));
    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);

process.on('uncaughtException', (error) => {
  console.error('[e2b-sandbox] uncaughtException', error);
});
process.on('unhandledRejection', (error) => {
  console.error('[e2b-sandbox] unhandledRejection', error);
});

console.error(`[e2b-sandbox] MCP server ready. State file: ${STATE_PATH}`);
