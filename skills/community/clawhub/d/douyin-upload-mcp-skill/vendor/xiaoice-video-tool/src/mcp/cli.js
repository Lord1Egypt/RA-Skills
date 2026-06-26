#!/usr/bin/env node

const { createMcpServer } = require('./server');

function shutdown(server, signal) {
  try {
    server.close();
    process.stderr.write(`[mcp-server] ${signal} received, shutting down...\n`);
    process.exit(0);
  } catch (error) {
    process.stderr.write(`[mcp-server] failed to shutdown cleanly: ${error.message}\n`);
    process.exit(1);
  }
}

function main() {
  const server = createMcpServer({
    serviceBaseUrl: process.env.XIAOICE_VIDEO_SERVICE_BASE_URL,
    internalToken: process.env.VIDEO_SERVICE_INTERNAL_TOKEN,
    input: process.stdin,
    output: process.stdout,
    logger: console,
  });

  server.start();

  process.on('SIGINT', () => shutdown(server, 'SIGINT'));
  process.on('SIGTERM', () => shutdown(server, 'SIGTERM'));
}

if (require.main === module) {
  try {
    main();
  } catch (error) {
    process.stderr.write(`[mcp-server] startup failed: ${error.message}\n`);
    process.exit(1);
  }
}

module.exports = {
  main,
};
