#!/usr/bin/env node
import { runEgoFile } from "./lib/run-ego.mjs";

const code = await runEgoFile(process.argv[2], { command: process.argv[3] || "publish" });
process.exit(code);
