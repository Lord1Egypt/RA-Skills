function createMcpSkeleton() {
  return {
    name: 'mcp-server',
    tools: ['xiaoice_video_produce'],
  };
}

const { createMcpServer } = require('./server');
const { createToolHandler } = require('./tool');
const { main } = require('./cli');

module.exports = {
  createMcpSkeleton,
  createMcpServer,
  createToolHandler,
  main,
};
