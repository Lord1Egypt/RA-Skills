/**
 * Unit tests for openclaw-tools.ts — OpenClaw tool factory.
 *
 * Tests verify:
 *   - Tool factory returns 5 tools with correct shape
 *   - Tool names are kebab-case with agentbnb- prefix
 *   - Parameter schemas are valid JSON Schema
 *   - Result conversion from MCP format to AgentToolResult
 *   - Context caching and multi-agent isolation
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { mkdtempSync, writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

import {
  createAllTools,
  createDiscoverTool,
  createRequestTool,
  createConductTool,
  createStatusTool,
  createPublishTool,
  toAgentToolResult,
  buildMcpContext,
  resolveConfigDir,
  resetContextCache,
} from './openclaw-tools.js';
import type { AgentTool, OpenClawToolContext } from './openclaw-tools.js';

// ---------------------------------------------------------------------------
// Mocks
// ---------------------------------------------------------------------------

vi.mock('../../src/identity/identity.js', () => ({
  ensureIdentity: vi.fn((_dir: string, owner: string) => ({
    agent_id: 'mock-agent-id',
    owner,
    public_key: 'deadbeef'.repeat(8),
    created_at: '2026-01-01T00:00:00.000Z',
  })),
}));

vi.mock('../../src/mcp/tools/discover.js', () => ({
  handleDiscover: vi.fn(async () => ({
    content: [{ type: 'text', text: JSON.stringify({ results: [], count: 0 }) }],
  })),
}));

vi.mock('../../src/mcp/tools/request.js', () => ({
  handleRequest: vi.fn(async () => ({
    content: [{ type: 'text', text: JSON.stringify({ success: true }) }],
  })),
}));

vi.mock('../../src/mcp/tools/conduct.js', () => ({
  handleConduct: vi.fn(async () => ({
    content: [{ type: 'text', text: JSON.stringify({ success: true, plan: [] }) }],
  })),
}));

vi.mock('../../src/mcp/tools/status.js', () => ({
  handleStatus: vi.fn(async () => ({
    content: [{ type: 'text', text: JSON.stringify({ agent_id: 'mock', balance: 50 }) }],
  })),
}));

vi.mock('../../src/mcp/tools/publish.js', () => ({
  handlePublish: vi.fn(async () => ({
    content: [{ type: 'text', text: JSON.stringify({ success: true, card_id: 'abc' }) }],
  })),
}));

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/**
 * Creates a temp dir ending with `.agentbnb` containing config.json.
 * resolveConfigDir() uses the dir as-is when it ends with `.agentbnb`.
 */
function createTempConfigDir(): string {
  const parent = mkdtempSync(join(tmpdir(), 'agentbnb-test-'));
  const configDir = join(parent, '.agentbnb');
  mkdirSync(configDir, { recursive: true });
  writeFileSync(
    join(configDir, 'config.json'),
    JSON.stringify({
      owner: 'test-agent',
      gateway_url: 'http://localhost:7700',
      gateway_port: 7700,
      db_path: ':memory:',
      credit_db_path: ':memory:',
      token: 'test-token',
      registry: 'https://hub.agentbnb.dev',
    }),
  );
  return configDir;
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

describe('openclaw-tools', () => {
  beforeEach(() => {
    resetContextCache();
  });

  afterEach(() => {
    resetContextCache();
  });

  // -------------------------------------------------------------------------
  // 1. Tool factory shape
  // -------------------------------------------------------------------------
  describe('createAllTools()', () => {
    it('returns array of 5 tools', () => {
      const configDir = createTempConfigDir();
      const tools = createAllTools({ agentDir: configDir });
      expect(tools).toHaveLength(5);
    });

    it('each tool has required properties', () => {
      const configDir = createTempConfigDir();
      const tools = createAllTools({ agentDir: configDir });
      for (const tool of tools) {
        expect(tool).toHaveProperty('name');
        expect(tool).toHaveProperty('label');
        expect(tool).toHaveProperty('description');
        expect(tool).toHaveProperty('parameters');
        expect(tool).toHaveProperty('execute');
        expect(typeof tool.name).toBe('string');
        expect(typeof tool.label).toBe('string');
        expect(typeof tool.description).toBe('string');
        expect(typeof tool.parameters).toBe('object');
        expect(typeof tool.execute).toBe('function');
      }
    });
  });

  // -------------------------------------------------------------------------
  // 2. Tool names — kebab-case with agentbnb- prefix
  // -------------------------------------------------------------------------
  describe('tool names', () => {
    it('all names follow agentbnb-<action> pattern', () => {
      const configDir = createTempConfigDir();
      const tools = createAllTools({ agentDir: configDir });
      const names = tools.map((t) => t.name);

      expect(names).toEqual([
        'agentbnb-discover',
        'agentbnb-request',
        'agentbnb-conduct',
        'agentbnb-status',
        'agentbnb-publish',
      ]);

      for (const name of names) {
        expect(name).toMatch(/^agentbnb-[a-z]+$/);
      }
    });
  });

  // -------------------------------------------------------------------------
  // 3. Parameter schemas
  // -------------------------------------------------------------------------
  describe('parameter schemas', () => {
    it('discover requires query', () => {
      const configDir = createTempConfigDir();
      const tool = createDiscoverTool({ agentDir: configDir });
      const schema = tool.parameters as { required: string[]; properties: Record<string, unknown> };
      expect(schema.required).toContain('query');
      expect(schema.properties).toHaveProperty('query');
      expect(schema.properties).toHaveProperty('level');
      expect(schema.properties).toHaveProperty('online_only');
    });

    it('request has no required fields', () => {
      const configDir = createTempConfigDir();
      const tool = createRequestTool({ agentDir: configDir });
      const schema = tool.parameters as { required: string[] };
      expect(schema.required).toEqual([]);
    });

    it('conduct requires task', () => {
      const configDir = createTempConfigDir();
      const tool = createConductTool({ agentDir: configDir });
      const schema = tool.parameters as { required: string[] };
      expect(schema.required).toContain('task');
    });

    it('status has no required fields', () => {
      const configDir = createTempConfigDir();
      const tool = createStatusTool({ agentDir: configDir });
      const schema = tool.parameters as { required: string[]; properties: Record<string, unknown> };
      expect(schema.required).toEqual([]);
      expect(Object.keys(schema.properties)).toHaveLength(0);
    });

    it('publish requires card_json', () => {
      const configDir = createTempConfigDir();
      const tool = createPublishTool({ agentDir: configDir });
      const schema = tool.parameters as { required: string[] };
      expect(schema.required).toContain('card_json');
    });
  });

  // -------------------------------------------------------------------------
  // 4. Result conversion
  // -------------------------------------------------------------------------
  describe('toAgentToolResult()', () => {
    it('converts MCP format to AgentToolResult with parsed details', () => {
      const mcpResult = {
        content: [{ type: 'text' as const, text: '{"results":[],"count":0}' }],
      };
      const result = toAgentToolResult(mcpResult);
      expect(result.content).toBe('{"results":[],"count":0}');
      expect(result.details).toEqual({ results: [], count: 0 });
    });

    it('handles non-JSON text gracefully', () => {
      const mcpResult = {
        content: [{ type: 'text' as const, text: 'not json' }],
      };
      const result = toAgentToolResult(mcpResult);
      expect(result.content).toBe('not json');
      expect(result.details).toBeUndefined();
    });

    it('handles empty content array', () => {
      const mcpResult = { content: [] as Array<{ type: string; text: string }> };
      const result = toAgentToolResult(mcpResult);
      expect(result.content).toBe('{}');
    });
  });

  // -------------------------------------------------------------------------
  // 5. Context caching
  // -------------------------------------------------------------------------
  describe('context caching', () => {
    it('same configDir reuses cached context', () => {
      const configDir = createTempConfigDir();
      const ctx1 = buildMcpContext({ agentDir: configDir });
      const ctx2 = buildMcpContext({ agentDir: configDir });
      expect(ctx1).toBe(ctx2); // same reference
    });

    it('resetContextCache() clears the cache', () => {
      const configDir = createTempConfigDir();
      const ctx1 = buildMcpContext({ agentDir: configDir });
      resetContextCache();
      const ctx2 = buildMcpContext({ agentDir: configDir });
      expect(ctx1).not.toBe(ctx2); // different reference
    });
  });

  // -------------------------------------------------------------------------
  // 6. Multi-agent isolation
  // -------------------------------------------------------------------------
  describe('multi-agent isolation', () => {
    it('different workspaceDir values produce different contexts', () => {
      const dir1 = createTempConfigDir();
      const dir2 = createTempConfigDir();

      const ctx1 = buildMcpContext({ agentDir: dir1 });
      const ctx2 = buildMcpContext({ agentDir: dir2 });

      expect(ctx1).not.toBe(ctx2);
      expect(ctx1.configDir).not.toBe(ctx2.configDir);
    });
  });

  // -------------------------------------------------------------------------
  // 7. resolveConfigDir
  // -------------------------------------------------------------------------
  describe('resolveConfigDir()', () => {
    it('uses agentDir directly if it ends with .agentbnb', () => {
      const dir = resolveConfigDir({ agentDir: '/tmp/test/.agentbnb' });
      expect(dir).toBe('/tmp/test/.agentbnb');
    });

    it('appends .agentbnb to agentDir if it does not end with .agentbnb', () => {
      const dir = resolveConfigDir({ agentDir: '/tmp/test-agent' });
      expect(dir).toBe('/tmp/test-agent/.agentbnb');
    });

    it('derives from workspaceDir when agentDir is not set', () => {
      const dir = resolveConfigDir({ workspaceDir: '/tmp/workspace' });
      expect(dir).toBe('/tmp/workspace/.agentbnb');
    });

    it('falls back to ~/.agentbnb when neither is set', () => {
      const dir = resolveConfigDir({});
      expect(dir).toMatch(/\.agentbnb$/);
    });
  });

  // -------------------------------------------------------------------------
  // 8. buildMcpContext error on missing config
  // -------------------------------------------------------------------------
  describe('buildMcpContext()', () => {
    it('throws when config.json does not exist', () => {
      const dir = mkdtempSync(join(tmpdir(), 'agentbnb-noconfig-'));
      expect(() => buildMcpContext({ agentDir: dir })).toThrow(/not initialized/);
    });
  });

  // -------------------------------------------------------------------------
  // 9. Tool execution delegates to MCP handlers
  // -------------------------------------------------------------------------
  describe('tool execution', () => {
    it('discover tool delegates to handleDiscover', async () => {
      const configDir = createTempConfigDir();
      const tool = createDiscoverTool({ agentDir: configDir });
      const result = await tool.execute('call-1', { query: 'stock analysis' });
      expect(result.content).toBeTruthy();
      expect(result.details).toEqual({ results: [], count: 0 });
    });

    it('status tool delegates to handleStatus', async () => {
      const configDir = createTempConfigDir();
      const tool = createStatusTool({ agentDir: configDir });
      const result = await tool.execute('call-2', {});
      expect(result.details).toEqual({ agent_id: 'mock', balance: 50 });
    });
  });
});
