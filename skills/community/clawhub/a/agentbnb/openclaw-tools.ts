/**
 * OpenClaw tool factory — bridges AgentBnB MCP tool handlers into
 * OpenClaw's native plugin tool system.
 *
 * Each tool delegates to the existing `handle*()` functions from src/mcp/tools/.
 * Context is lazily constructed and per-agent cached to avoid process.env mutation.
 */

import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { homedir } from 'node:os';
import { ensureIdentity } from '../../src/identity/identity.js';
import type { AgentBnBConfig } from '../../src/cli/config.js';
import type { McpServerContext } from '../../src/mcp/server.js';
import { handleDiscover } from '../../src/mcp/tools/discover.js';
import { handleRequest } from '../../src/mcp/tools/request.js';
import { handleConduct } from '../../src/mcp/tools/conduct.js';
import { handleStatus } from '../../src/mcp/tools/status.js';
import { handlePublish } from '../../src/mcp/tools/publish.js';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

/** Subset of OpenClaw's plugin tool context passed to tool factories. */
export interface OpenClawToolContext {
  workspaceDir?: string;
  agentDir?: string;
}

/** OpenClaw-compatible tool result. */
export interface AgentToolResult {
  content: string;
  details?: unknown;
}

/** OpenClaw-compatible tool shape. */
export interface AgentTool {
  name: string;
  label: string;
  description: string;
  parameters: Record<string, unknown>;
  execute: (toolCallId: string, params: Record<string, unknown>) => Promise<AgentToolResult>;
}

// ---------------------------------------------------------------------------
// Context cache — per-agent isolation keyed by configDir
// ---------------------------------------------------------------------------

const contextCache = new Map<string, McpServerContext>();

/** Clears the per-agent context cache. Useful for tests and daemon restarts. */
export function resetContextCache(): void {
  contextCache.clear();
}

/**
 * Resolves the configDir from OpenClaw tool context.
 *
 * Priority:
 * 1. agentDir (if ends with .agentbnb, use directly; else append .agentbnb)
 * 2. workspaceDir + /.agentbnb
 * 3. Fallback: ~/.agentbnb
 */
export function resolveConfigDir(toolCtx: OpenClawToolContext): string {
  if (toolCtx.agentDir) {
    return toolCtx.agentDir.endsWith('.agentbnb')
      ? toolCtx.agentDir
      : join(toolCtx.agentDir, '.agentbnb');
  }
  if (toolCtx.workspaceDir) {
    return join(toolCtx.workspaceDir, '.agentbnb');
  }
  return join(homedir(), '.agentbnb');
}

/**
 * Constructs an McpServerContext from OpenClaw tool context.
 * Per-agent cached — same configDir reuses the same context.
 *
 * Reads config directly from configDir/config.json instead of mutating
 * process.env.AGENTBNB_DIR, which avoids race conditions in the shared
 * OpenClaw daemon process.
 */
export function buildMcpContext(toolCtx: OpenClawToolContext): McpServerContext {
  const configDir = resolveConfigDir(toolCtx);

  const cached = contextCache.get(configDir);
  if (cached) return cached;

  const configPath = join(configDir, 'config.json');
  if (!existsSync(configPath)) {
    throw new Error(
      `AgentBnB not initialized at ${configDir}. Run \`agentbnb init\` or activate the plugin first.`,
    );
  }

  const config = JSON.parse(readFileSync(configPath, 'utf-8')) as AgentBnBConfig;
  const identity = ensureIdentity(configDir, config.owner);

  const ctx: McpServerContext = { configDir, config, identity };
  contextCache.set(configDir, ctx);
  return ctx;
}

// ---------------------------------------------------------------------------
// Result conversion
// ---------------------------------------------------------------------------

/**
 * Converts MCP result format to OpenClaw AgentToolResult.
 * MCP returns `{ content: [{type:'text', text: '<json>'}] }`.
 * OpenClaw expects `{ content: string, details?: unknown }`.
 */
export function toAgentToolResult(
  mcpResult: { content: Array<{ type: string; text: string }> },
): AgentToolResult {
  const text = mcpResult.content[0]?.text ?? '{}';
  let details: unknown;
  try {
    details = JSON.parse(text);
  } catch {
    details = undefined;
  }
  return { content: text, details };
}

// ---------------------------------------------------------------------------
// Tool creators
// ---------------------------------------------------------------------------

/** Creates the agentbnb-discover tool. */
export function createDiscoverTool(toolCtx: OpenClawToolContext): AgentTool {
  return {
    name: 'agentbnb-discover',
    label: 'AgentBnB Discover',
    description:
      'Search for agent capabilities on the AgentBnB network. Returns matching capability cards from both local and remote registries.',
    parameters: {
      type: 'object',
      properties: {
        query: { type: 'string', description: 'Natural language search query' },
        level: {
          type: 'number',
          description: 'Filter by capability level (1=Atomic, 2=Pipeline, 3=Environment)',
        },
        online_only: { type: 'boolean', description: 'Only show online agents' },
      },
      required: ['query'],
    },
    async execute(_toolCallId, params) {
      const ctx = buildMcpContext(toolCtx);
      const result = await handleDiscover(
        params as { query: string; level?: number; online_only?: boolean },
        ctx,
      );
      return toAgentToolResult(result);
    },
  };
}

/** Creates the agentbnb-request tool. */
export function createRequestTool(toolCtx: OpenClawToolContext): AgentTool {
  return {
    name: 'agentbnb-request',
    label: 'AgentBnB Request',
    description:
      'Request execution of a skill from another agent on the AgentBnB network. Handles credit escrow automatically.',
    parameters: {
      type: 'object',
      properties: {
        query: {
          type: 'string',
          description: 'Search query to find a matching capability (auto-request mode)',
        },
        card_id: { type: 'string', description: 'Direct card ID to request (skips search)' },
        skill_id: { type: 'string', description: 'Specific skill within a v2.0 card' },
        params: { type: 'object', description: 'Input parameters for the capability' },
        max_cost: {
          type: 'number',
          description: 'Maximum credits to spend (default: 50)',
        },
      },
      required: [],
    },
    async execute(_toolCallId, params) {
      const ctx = buildMcpContext(toolCtx);
      const result = await handleRequest(
        params as {
          query?: string;
          card_id?: string;
          skill_id?: string;
          params?: Record<string, unknown>;
          max_cost?: number;
        },
        ctx,
      );
      return toAgentToolResult(result);
    },
  };
}

/** Creates the agentbnb-conduct tool. */
export function createConductTool(toolCtx: OpenClawToolContext): AgentTool {
  return {
    name: 'agentbnb-conduct',
    label: 'AgentBnB Conduct',
    description:
      'Orchestrate a complex task across multiple agents on the AgentBnB network. Decomposes the task, matches sub-tasks to agents, and executes the pipeline.',
    parameters: {
      type: 'object',
      properties: {
        task: { type: 'string', description: 'Natural language task description' },
        plan_only: {
          type: 'boolean',
          description: 'If true, return execution plan without executing',
        },
        max_budget: {
          type: 'number',
          description: 'Maximum credits to spend (default: 100)',
        },
      },
      required: ['task'],
    },
    async execute(_toolCallId, params) {
      const ctx = buildMcpContext(toolCtx);
      const result = await handleConduct(
        params as { task: string; plan_only?: boolean; max_budget?: number },
        ctx,
      );
      return toAgentToolResult(result);
    },
  };
}

/** Creates the agentbnb-status tool. */
export function createStatusTool(toolCtx: OpenClawToolContext): AgentTool {
  return {
    name: 'agentbnb-status',
    label: 'AgentBnB Status',
    description:
      'Check your AgentBnB agent status: identity, credit balance, and configuration.',
    parameters: {
      type: 'object',
      properties: {},
      required: [],
    },
    async execute(_toolCallId, _params) {
      const ctx = buildMcpContext(toolCtx);
      const result = await handleStatus(ctx);
      return toAgentToolResult(result);
    },
  };
}

/** Creates the agentbnb-publish tool. */
export function createPublishTool(toolCtx: OpenClawToolContext): AgentTool {
  return {
    name: 'agentbnb-publish',
    label: 'AgentBnB Publish',
    description:
      'Publish a capability card to the AgentBnB network. Stores locally and optionally syncs to remote registry.',
    parameters: {
      type: 'object',
      properties: {
        card_json: {
          type: 'string',
          description: 'JSON string of the capability card to publish',
        },
      },
      required: ['card_json'],
    },
    async execute(_toolCallId, params) {
      const ctx = buildMcpContext(toolCtx);
      const result = await handlePublish(params as { card_json: string }, ctx);
      return toAgentToolResult(result);
    },
  };
}

// ---------------------------------------------------------------------------
// Factory
// ---------------------------------------------------------------------------

/**
 * Creates all 5 AgentBnB tools for an OpenClaw bot.
 * Called by the plugin's `register()` method via `api.registerTool()`.
 */
export function createAllTools(toolCtx: OpenClawToolContext): AgentTool[] {
  return [
    createDiscoverTool(toolCtx),
    createRequestTool(toolCtx),
    createConductTool(toolCtx),
    createStatusTool(toolCtx),
    createPublishTool(toolCtx),
  ];
}
