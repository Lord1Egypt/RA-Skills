#!/usr/bin/env node
const base = process.env.ACTION_GATE_URL || "http://localhost:8787";

const input = {
  source: process.argv[2] || "communications",
  actionType: process.argv[3],
  target: process.argv[4],
  summary: process.argv[5],
  payloadSummary: process.argv[6] || "",
  program: process.argv[7] || "",
};

async function main() {
  if (!input.actionType || !input.target || !input.summary) {
    throw new Error(
      "Usage: propose-action.js <source> <actionType> <target> <summary> [payloadSummary] [program]",
    );
  }

  const res = await fetch(`${base}/v1/proposals`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(input),
  });
  console.log(JSON.stringify(await res.json(), null, 2));
}

main().catch((err) => {
  console.error(err.stack || String(err));
  process.exit(1);
});
