const { createServiceSkeleton } = require('./service');
const { createMcpSkeleton } = require('./mcp');
const { createHealthSnapshot } = require('./shared');

function bootstrap() {
  return {
    service: createServiceSkeleton(),
    mcp: createMcpSkeleton(),
    health: createHealthSnapshot(),
  };
}

function main() {
  const app = bootstrap();
  process.stdout.write(`${JSON.stringify(app, null, 2)}\n`);
}

if (require.main === module) {
  main();
}

module.exports = {
  bootstrap,
  main,
};
