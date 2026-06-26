/**
 * stdio.ts — MCP Stdio Transport Entry Point
 *
 * Allows agent-comm-hub to run as a stdio MCP server (command-based),
 * in addition to the existing HTTP Streamable HTTP transport.
 *
 * Usage: HUB_AUTH_TOKEN=<token> node dist/stdio.js
 *
 * Auth: Reads HUB_AUTH_TOKEN env var, verifies against auth_tokens table.
 * Logging: All logs go to stderr (stdout is reserved for JSON-RPC).
 */
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { registerTools } from "./tools.js";
import { verifyToken } from "./security.js";
import { logger } from "./logger.js";

async function main(): Promise<void> {
  const token = process.env.HUB_AUTH_TOKEN;
  if (!token) {
    logger.error("stdio_auth_missing", { module: "stdio" });
    process.exit(1);
  }

  // Authenticate (importing security.js triggers db.js initialization)
  const authContext = verifyToken(token);
  if (!authContext) {
    logger.error("stdio_auth_failed", { module: "stdio" });
    process.exit(1);
  }
  logger.info("stdio_authenticated", { module: "stdio", agent_id: authContext.agentId, role: authContext.role });

  // Create MCP server — same config as HTTP transport
  const server = new McpServer({
    name: "agent-comm-hub",
    version: "2.4.0",
  });
  registerTools(server, authContext);

  // Connect stdio transport
  const transport = new StdioServerTransport();
  await server.connect(transport);
  logger.info("stdio_started", { module: "stdio", agent_id: authContext.agentId });
}

main().catch((err) => {
  logger.error("stdio_fatal", { module: "stdio", error: String(err) });
  process.exit(1);
});
