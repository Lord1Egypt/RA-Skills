#!/usr/bin/env node

import { runScript } from './vendor/weryai-text/cli.js';
import { createWriteExecutor } from './vendor/weryai-text/write.js';

const HELP = `Usage: node {baseDir}/scripts/write.js [options]

Options:
  --json <data>    Pass parameters as a JSON string (use "-" for stdin)
  --dry-run        Preview the request without calling the API
  --verbose        Print debug info to stderr
  --help           Show this help message

Examples:
  node {baseDir}/scripts/write.js --json '{"prompt":"Write 5 ad copy variations for a productivity app launch","product":"AI productivity app","audience":"busy professionals","format":"paid social ad","cta":"Start free trial"}'
  node {baseDir}/scripts/write.js --json '{"prompt":"Rewrite this ad so it feels sharper and more benefit-driven","sourceText":"...","product":"skincare serum"}' --dry-run
`;

await runScript(process.argv.slice(2), createWriteExecutor('adCopy'), HELP);
