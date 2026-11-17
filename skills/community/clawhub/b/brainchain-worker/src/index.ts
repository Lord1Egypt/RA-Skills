#!/usr/bin/env node
// Checked before anything else loads: a dependency of the Solana client needs
// require() of ES modules, which Node.js has run unflagged only since 22.12.
const [major = 0, minor = 0] = process.versions.node.split(".").map(Number);
if (major < 22 || (major === 22 && minor < 12)) {
  console.error(`brainchain-worker needs Node.js 22.12 or later; this is ${process.version}.`);
  process.exit(1);
}
const { reason } = await import("./chain.js");
const { main, UsageError } = await import("./cli.js");

main(process.argv.slice(2)).catch((error: unknown) => {
  console.error(error instanceof UsageError ? error.message : `brainchain-worker: ${reason(error)}`);
  process.exit(1);
});
