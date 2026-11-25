import assert from "node:assert/strict";
import { test } from "node:test";
import { mkdtemp, rm, writeFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { join } from "node:path";
import { tmpdir } from "node:os";

import { TOP_UP_URL as official } from "../scripts/contract.mjs";

const workflow = fileURLToPath(new URL("../scripts/run-workflow.mjs", import.meta.url));
const payload = JSON.stringify({ content: "A candle", duration: 5, resolution: "720p" });

// Runs the real CLI against a mocked API whose balance is `balance` credits.
async function run(args, { balance, topUpUrl }) {
  const directory = await mkdtemp(join(tmpdir(), "aivideo-top-up-"));
  try {
    const mock = join(directory, "mock.mjs");
    const link = topUpUrl === undefined ? {} : { topUpUrl };
    await writeFile(
      mock,
      `
      const balance = ${balance};
      const link = ${JSON.stringify(link)};
      globalThis.fetch = async (url) => {
        const path = new URL(url).pathname;
        if (path === '/api/v1/quote/minimax') {
          const affordable = balance >= 15;
          return Response.json({
            model: 'minimax', credits: 15, listPriceUsd: 0.15, currentBalance: balance,
            affordable, billable: false,
            ...(affordable ? {} : { creditsShort: 15 - balance, ...link }),
          });
        }
        if (path === '/api/v1/generate/minimax') {
          return Response.json(
            { status: 'FAILED', errorCode: 'INSUFFICIENT_CREDITS', message: 'Insufficient credits', ...link },
            { status: 402 },
          );
        }
        throw new Error('unexpected request');
      };`,
    );
    const result = spawnSync(process.execPath, ["--import", mock, workflow, ...args], {
      encoding: "utf8",
      env: { ...process.env, AIVIDEO_API_KEY: "test-only", AIVIDEO_MAX_RETRIES: "0" },
    });
    return { exitCode: result.status, output: JSON.parse(result.stdout) };
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
}

const quote = ["--action", "quote", "--model", "minimax", "--payload", payload];
const generate = ["--model", "minimax", "--maxCredits", "15", "--payload", payload];

test("an unaffordable quote hands the agent the link for adding credits", async () => {
  const { exitCode, output } = await run(quote, { balance: 5, topUpUrl: official });
  assert.equal(exitCode, 0);
  assert.equal(output.data.affordable, false);
  assert.equal(output.topUpUrl, official);
  assert.match(output.nextStep, /submit nothing new until a quote is affordable/);
  // A paid task whose own charge lowered the balance must be resumed, not paid for again.
  assert.match(output.nextStep, /resume or replay it unchanged first/);
});

test("an affordable quote never mentions buying credits", async () => {
  const { output } = await run(quote, { balance: 50, topUpUrl: official });
  assert.equal(output.data.affordable, true);
  assert.ok(!JSON.stringify(output).includes("topUpUrl"));
  assert.equal(output.nextStep, undefined);
});

test("an insufficient-credit failure includes the link and charges nothing", async () => {
  const { exitCode, output } = await run(generate, { balance: 5, topUpUrl: official });
  assert.equal(exitCode, 1);
  assert.equal(output.errorCode, "INSUFFICIENT_CREDITS");
  assert.equal(output.taskId, null);
  assert.equal(output.topUpUrl, official);
  assert.ok(output.suggestions.some((line) => line.includes(official)));
});

for (const [label, topUpUrl] of [
  ["missing", undefined],
  ["foreign", "https://example.test/buy"],
  ["look-alike", "https://aivideomaker.ai.example.test/skill"],
]) {
  test(`a ${label} link from the API falls back to the official page`, async () => {
    for (const args of [quote, generate]) {
      const { output } = await run(args, { balance: 5, topUpUrl });
      assert.match(output.topUpUrl, /^https:\/\/aivideomaker\.ai\/skill\?/);
      assert.ok(!JSON.stringify(output.suggestions ?? []).includes("example.test"));
    }
  });
}
