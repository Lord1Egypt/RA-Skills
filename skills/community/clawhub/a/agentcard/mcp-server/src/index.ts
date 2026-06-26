#!/usr/bin/env node

/**
 * @asgcard/mcp-server — Entry point
 *
 * Starts the ASGCard MCP server with stdio transport.
 * Used by Claude Code, Claude Desktop, and Cursor.
 *
 * Required env vars:
 *   STELLAR_PRIVATE_KEY — Stellar secret key (S...) for signing x402 payments
 *
 * Optional env vars:
 *   ASGCARD_API_URL     — API base URL (default: https://api.asgcard.dev)
 *   STELLAR_RPC_URL     — Soroban RPC URL (default: https://mainnet.sorobanrpc.com)
 */

import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { createASGCardServer } from "./server.js";

const privateKey = process.env.STELLAR_PRIVATE_KEY;

if (!privateKey) {
  console.error(
    "❌ STELLAR_PRIVATE_KEY is required.\n" +
      "Set it in your MCP client config or as an environment variable.\n" +
      "This is your Stellar secret key (starts with S...) used to sign x402 payments."
  );
  process.exit(1);
}

const server = createASGCardServer({
  privateKey,
  apiUrl: process.env.ASGCARD_API_URL,
  rpcUrl: process.env.STELLAR_RPC_URL,
});

const transport = new StdioServerTransport();

await server.connect(transport);
