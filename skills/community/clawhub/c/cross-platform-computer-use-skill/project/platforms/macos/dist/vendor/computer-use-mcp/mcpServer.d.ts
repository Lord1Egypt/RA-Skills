/**
 * MCP server factory + session-context binder.
 *
 * Two entry points:
 *
 *   `bindSessionContext` — the wrapper closure. Takes a `ComputerUseSessionContext`
 *   (getters + callbacks backed by host session state), returns a dispatcher.
 *   Reusable by both the MCP CallTool handler here AND Cowork's
 *   `InternalServerDefinition.handleToolCall` (which doesn't go through MCP).
 *   This replaces the duplicated wrapper closures in apps/desktop/…/serverDef.ts
 *   and the Claude Code CLI's CU host wrapper — both did the same thing: build `ComputerUseOverrides`
 *   fresh from getters, call `handleToolCall`, stash screenshot, merge permissions.
 *
 *   `createComputerUseMcpServer` — the Server object. When `context` is provided,
 *   the CallTool handler is real (uses `bindSessionContext`). When not, it's the
 *   legacy stub that returns a not-wired error. The tool-schema ListTools handler
 *   is the same either way.
 */
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import type { CuCallToolResult } from "./toolCalls.js";
import type { ComputerUseHostAdapter, ComputerUseSessionContext, CoordinateMode } from "./types.js";
/**
 * Bind session state to a reusable dispatcher. The returned function is the
 * wrapper closure: async lock gate → build overrides fresh → `handleToolCall`
 * → stash screenshot → strip piggybacked fields.
 *
 * The last-screenshot blob is held in a closure cell here (not on `ctx`), so
 * hosts don't need to guarantee `ctx` object identity across calls — they just
 * need to hold onto the returned dispatcher. Cowork caches per
 * `InternalServerContext` in a WeakMap; the CLI host constructs once at server creation.
 */
export declare function bindSessionContext(adapter: ComputerUseHostAdapter, coordinateMode: CoordinateMode, ctx: ComputerUseSessionContext): (name: string, args: unknown) => Promise<CuCallToolResult>;
export declare function createComputerUseMcpServer(adapter: ComputerUseHostAdapter, coordinateMode: CoordinateMode, context?: ComputerUseSessionContext): Server;
