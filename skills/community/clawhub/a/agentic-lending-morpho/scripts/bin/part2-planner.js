#!/usr/bin/env node

const { runCli } = require('../lib/part2-planner');

runCli().catch((error) => {
  console.error(error.message || error);
  process.exit(1);
});
