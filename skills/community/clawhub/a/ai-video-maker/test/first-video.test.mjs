import assert from "node:assert/strict";
import { test } from "node:test";
import { mkdtemp, writeFile, rm, readFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";
import { firstVideoPayload } from "../scripts/first-video.mjs";

const workflow = fileURLToPath(new URL("../scripts/run-workflow.mjs", import.meta.url));
const flow = "38bfe3d9-b03e-45c3-9e05-88cb5a7f7ad7";

test("product guide accepts canonical URL/data URI, rejects missing, invalid and legacy image fields", () => {
  for (const imageUrl of ["https://example.test/lamp.png", "data:image/png;base64,aGVsbG8="])
    assert.equal(
      firstVideoPayload("product", { content: "Show lamp", imageUrl }).imageUrl,
      imageUrl,
    );
  for (const imageUrl of [undefined, null, "", [], "./lamp.png"])
    assert.throws(() => firstVideoPayload("product", { content: "Show lamp", imageUrl }));
  assert.throws(
    () =>
      firstVideoPayload("product", {
        content: "Show lamp",
        image: "https://example.test/lamp.png",
      }),
    /imageUrl, not image/,
  );
  assert.equal(firstVideoPayload("social", { content: "My idea" }).aspectRatio, "9:16");
});

test("product CLI sends the same image to quote/create and enforces approval, budget and stable retry", async () => {
  const dir = await mkdtemp(join(tmpdir(), "product-guide-"));
  try {
    const log = join(dir, "calls.jsonl");
    const mock = join(dir, "fetch.mjs");
    await writeFile(
      mock,
      `
      import {appendFileSync} from 'node:fs';
      globalThis.fetch=async(url,options)=>{
        const path=new URL(url).pathname;
        const payload=JSON.parse(options.body);
        if(payload.imageUrl!=='https://example.test/lamp.png'||payload.image!==undefined) throw new Error('image lost');
        appendFileSync(${JSON.stringify(log)},JSON.stringify({path,key:options.headers['Idempotency-Key'],payload})+'\\n');
        if(path.includes('/quote/')) return Response.json({credits:15,affordable:true,billable:false});
        if(path.includes('/generate/')) return Response.json({taskId:'product-task',status:'SUBMITTED'});
        throw new Error('unexpected request');
      };`,
    );
    const base = [
      "--firstVideoFlow",
      flow,
      "--scenario",
      "product",
      "--payload",
      JSON.stringify({ content: "Show lamp", imageUrl: "https://example.test/lamp.png" }),
    ];
    const run = (args) =>
      spawnSync(process.execPath, ["--import", mock, workflow, ...base, ...args], {
        encoding: "utf8",
        env: { ...process.env, AIVIDEO_API_KEY: "test-only", AIVIDEO_MAX_RETRIES: "0" },
      });
    assert.equal(run(["--action", "quote"]).status, 0);
    assert.equal(run(["--maxCredits", "15"]).status, 1);
    assert.equal(run(["--approved", "true", "--maxCredits", "14"]).status, 1);
    for (let i = 0; i < 2; i++) {
      const result = run(["--approved", "true", "--maxCredits", "15", "--autoPoll", "false"]);
      assert.equal(result.status, 0, result.stdout);
      assert.equal(JSON.parse(result.stdout).idempotencyKey, `first-video:${flow}`);
    }
    const creates = (await readFile(log, "utf8"))
      .trim()
      .split("\n")
      .map(JSON.parse)
      .filter((x) => x.path.includes("/generate/"));
    assert.equal(creates.length, 2);
    assert.ok(creates.every((x) => x.key === `first-video:${flow}`));
  } finally {
    await rm(dir, { recursive: true, force: true });
  }
});
