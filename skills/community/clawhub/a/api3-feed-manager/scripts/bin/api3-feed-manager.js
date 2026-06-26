#!/usr/bin/env node

const { runCli } = require('../api3-feed-manager');

runCli().catch((error) => {
  console.error(error?.stack || error?.message || String(error));
  process.exit(1);
});
