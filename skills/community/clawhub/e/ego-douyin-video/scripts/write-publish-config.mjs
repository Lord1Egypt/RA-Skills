#!/usr/bin/env node
import { writePublishConfigSync } from "./lib/config-file.mjs";

try {
  const { file } = writePublishConfigSync(process.argv.slice(2));
  process.stdout.write(`${file}\n`);
} catch (error) {
  process.stderr.write(`${error.message}\n`);
  process.exit(error.exitCode || 1);
}
