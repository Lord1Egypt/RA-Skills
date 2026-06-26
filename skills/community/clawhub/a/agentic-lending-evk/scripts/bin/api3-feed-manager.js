#!/usr/bin/env node

const { runCli } = require('../lib/api3-feed-manager');

runCli().catch((error) => {
  console.error(error.message || error);
  process.exit(1);
});
