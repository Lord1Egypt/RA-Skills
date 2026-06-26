#!/usr/bin/env node
require("dotenv").config({ path: require("path").resolve(__dirname, "../.env") });

const { runPipeline } = require("../lib/pipeline");

function getArg(flag) {
  const idx = process.argv.indexOf(flag);
  return idx !== -1 ? process.argv[idx + 1] : null;
}

async function main() {
  const imagePath = getArg("--image");
  const date = getArg("--date");

  if (!imagePath) {
    throw new Error("Usage: run_pipeline.js --image <path> [--date YYYY-MM-DD]");
  }

  const result = await runPipeline({ imagePath, date });
  process.stdout.write(JSON.stringify(result));
}

main().catch((err) => {
  process.stderr.write(JSON.stringify({ error: err.message }));
  process.exit(1);
});
