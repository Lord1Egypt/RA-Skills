/**
 * MCP Server Tests - ANFSF v2.0
 * 
 * @module asf-v4/mcp/__tests__/server.test.ts
 */

import { describe, test, expect, beforeEach } from '@jest/globals';
import { ANFSFMCPUserver, createANFSFMCPUserver } from '../mcp-server';

describe('MCP Server Tests', () => {
  let server: ANFSFMCPUserver;

 beforeEach(() => {
    server = createANFSFMCPUserver();
  });

  test('should create MCP server', () => {
    expect(server).toBeDefined();
    expect(server.name).toBe('anfsf-v2');
    expect(server.version).toBe('2.0.0');
  });

  test('should have correct capabilities', () => {
    expect(server.capabilities).toBeDefined();
    expect(server.capabilities.tools).toBe(true);
    expect(server.capabilities.resources).toBe(true);
    expect(server.capabilities.prompts).toBe(true);
  });

  test('should have initialized tools', () => {
    const toolNames = Object.keys(server.tools);
    expect(toolNames.length).toBeGreaterThan(0);
    expect(toolNames).toContain('veto-check');
    expect(toolNames).toContain('ownership-proof');
    expect(toolNames).toContain('risk-predict');
    expect(toolNames).toContain('ui-synthesize');
    expect(toolNames).toContain('layout-generate');
  });

  test('should connect successfully', async () => {
    await expect(server.connect()).resolves.toBeUndefined();
  });

  test('should disconnect successfully', async () => {
    await expect(server.disconnect()).resolves.toBeUndefined();
  });

  test('should get resource', async () => {
    const result = await server.getResource('anfsf://config/main');
    expect(result).toBeDefined();
    expect(result.success).toBe(true);
  });

  test('should get prompt', async () => {
    const result = await server.getPrompt('review-security');
    expect(result).toBeDefined();
    expect(result.success).toBe(true);
  });

  test('should execute veto-check tool', async () => {
    const tool = server.tools['veto-check'];
    expect(tool).toBeDefined();
    const result = await tool.execute({
      changes: [{ resourceType: 'config', resourcePath: '/app', action: 'update' }],
    });
    expect(result.success).toBe(true);
  });

  test('should execute ownership-proof tool', async () => {
    const tool = server.tools['ownership-proof'];
    expect(tool).toBeDefined();
    const result = await tool.execute({
      resources: [{ type: 'file', path: '/app.ts' }],
    });
    expect(result.success).toBe(true);
  });

  test('should execute risk-predict tool', async () => {
    const tool = server.tools['risk-predict'];
    expect(tool).toBeDefined();
    const result = await tool.execute({
      tasks: [{ id: 'task-1', complexity: 5, teamSize: 3 }],
    });
    expect(result.success).toBe(true);
  });
});