#!/usr/bin/env node
import { runCheckCli } from "./lib/launch-check.mjs";

const code = await runCheckCli(process.argv.slice(2));
process.exit(code);
