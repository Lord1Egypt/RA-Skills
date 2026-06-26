#!/usr/bin/env node

/**
 * bilibit CLI entry point
 * B 站视频下载专家
 */

const cli = require('../src/cli');

// Run CLI with command line arguments
cli.main(process.argv.slice(2)).catch(error => {
  console.error('❌ Unexpected error:', error.message);
  process.exit(1);
});
