const args = process.argv.slice(2);
const portIdx = args.indexOf("--port");
const port = portIdx >= 0 && args[portIdx + 1] ? parseInt(args[portIdx + 1]) : 18800;
async function main() {
  console.log(`[cc-soul] standalone mode \u2014 starting...`);
  try {
    const { ensureDataDir } = require("./persistence.ts");
    ensureDataDir();
  } catch {
  }
  try {
    const { initSQLite } = require("./sqlite-store.ts");
    initSQLite();
  } catch (e) {
    console.error(`[cc-soul] SQLite init failed: ${e.message}`);
  }
  try {
    const { initializeSoul } = require("./init.ts");
    initializeSoul();
  } catch {
  }
  try {
    const { startSoulApi } = require("./soul-api.ts");
    startSoulApi();
  } catch (e) {
    console.error(`[cc-soul] soul-api start failed: ${e.message}`);
    process.exit(1);
  }
  console.log(`[cc-soul] \u2705 standalone API ready \u2014 http://0.0.0.0:${port}`);
  console.log(`[cc-soul] endpoints:`);
  console.log(`  POST /memories  \u2014 store memory`);
  console.log(`  POST /search    \u2014 search memories`);
  console.log(`  GET  /health    \u2014 health check`);
}
main().catch((e) => {
  console.error(`[cc-soul] startup failed: ${e.message}`);
  process.exit(1);
});
