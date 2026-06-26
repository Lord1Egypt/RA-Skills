#!/usr/bin/env node
import { main } from './scripts/assemblyai.mjs';

main(process.argv.slice(2)).catch((err) => {
  const message = err?.stack ?? err?.message ?? String(err);
  process.stderr.write(`${message}\n`);
  process.exit(1);
});
