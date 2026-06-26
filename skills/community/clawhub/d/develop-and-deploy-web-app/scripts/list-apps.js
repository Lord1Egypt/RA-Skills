"use strict";

const { parseArgs, readUserIndex, readWorkspaceRegistry } = require("./common");

function main() {
  const args = parseArgs(process.argv);
  if (args.userName) {
    process.stdout.write(`${JSON.stringify(readUserIndex(args.userName), null, 2)}\n`);
    return;
  }
  const registry = readWorkspaceRegistry();
  process.stdout.write(`${JSON.stringify(registry, null, 2)}\n`);
}

main();
