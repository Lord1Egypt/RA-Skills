#!/usr/bin/env node

const ChangeBrief = require('../src/index.js');
const pkg = require('../package.json');

function parseArgs(argv) {
  const options = { _: [] };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];

    if (!arg.startsWith('-')) {
      options._.push(arg);
      continue;
    }

    const key = arg.replace(/^-+/, '');
    const next = argv[i + 1];
    const hasValue = typeof next !== 'undefined' && !next.startsWith('-');
    options[key] = hasValue ? next : true;
    if (hasValue) {
      i += 1;
    }
  }

  return options;
}

function printHelp() {
  console.log(`ChangeBrief ${pkg.version}

Usage:
  cb brief --before-file last.md --after-file current.md
  cb changes --before-file v1.md --after-file v2.md
  cb invalidations --before-file previous.md --after-file current.md
  cb conflicts --before-file previous.md --after-file current.md
  cb priorities --before-file previous.md --after-file current.md
  cb analyze --before-file previous.md --after-file current.md --json

Commands:
  brief           Generate the full change brief
  changes         Show important additions
  invalidations   Show stale conclusions and what replaced them
  conflicts       Show change-driven conflicts that need a decision
  priorities      Rank the top changes worth immediate action
  analyze         Return the raw structured analysis

Options:
  --before-file <path>   Read the previous snapshot from a file
  --after-file <path>    Read the current snapshot from a file
  --before-text <text>   Read the previous snapshot from inline text
  --after-text <text>    Read the current snapshot from inline text
  --json                 Print JSON output
  --help                 Show this help
  --version              Show version
`);
}

function writeOutput(engine, result, asJson) {
  if (asJson) {
    console.log(JSON.stringify(result, null, 2));
    return;
  }
  console.log(engine.render(result));
}

async function main() {
  const argv = process.argv.slice(2);
  const command = argv[0];

  if (!command || command === '--help' || command === '-h') {
    printHelp();
    return;
  }

  if (command === '--version' || command === '-v') {
    console.log(pkg.version);
    return;
  }

  const options = parseArgs(argv.slice(1));
  const engine = new ChangeBrief();

  try {
    switch (command) {
      case 'brief':
        writeOutput(engine, engine.brief(options), options.json);
        return;
      case 'changes':
        writeOutput(engine, engine.changes(options), options.json);
        return;
      case 'invalidations':
        writeOutput(engine, engine.invalidations(options), options.json);
        return;
      case 'conflicts':
        writeOutput(engine, engine.conflicts(options), options.json);
        return;
      case 'priorities':
        writeOutput(engine, engine.priorities(options), options.json);
        return;
      case 'analyze':
        console.log(JSON.stringify(engine.analyze(options), null, 2));
        return;
      default:
        throw new Error(`Unknown command: ${command}`);
    }
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }
}

main();
