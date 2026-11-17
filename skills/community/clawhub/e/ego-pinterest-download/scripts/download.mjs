#!/usr/bin/env node
// CLI entry. ego-browser nodejs does not receive shell argv, so runCli writes a
// short entry module and loads it with: ego-browser nodejs -e "await import('file://…')"
import { runCli } from "./lib/launch.mjs";

const code = await runCli(process.argv.slice(2));
process.exit(code);
