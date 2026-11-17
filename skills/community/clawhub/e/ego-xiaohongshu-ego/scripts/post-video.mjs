#!/usr/bin/env node
import { runCli } from "./lib/launch.mjs";

const code = await runCli("post", process.argv.slice(2));
process.exit(code);
