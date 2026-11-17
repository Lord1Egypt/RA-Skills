#!/usr/bin/env node
import { runCli } from "./lib/launch.mjs";

const code = await runCli("edit", process.argv.slice(2));
process.exit(code);
