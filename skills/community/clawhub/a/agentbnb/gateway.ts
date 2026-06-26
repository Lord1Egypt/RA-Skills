/**
 * AgentBnB Gateway adapter for OpenClaw skill integration.
 * Delegates to AgentRuntime and createGatewayServer from src/.
 * This is a thin re-export wrapper — no business logic lives here.
 */
import { AgentRuntime } from '../../src/runtime/agent-runtime.js';
import { createGatewayServer } from '../../src/gateway/server.js';
import type { RuntimeOptions } from '../../src/runtime/agent-runtime.js';
import type { GatewayOptions } from '../../src/gateway/server.js';

export { AgentRuntime, createGatewayServer };
export type { RuntimeOptions, GatewayOptions };
