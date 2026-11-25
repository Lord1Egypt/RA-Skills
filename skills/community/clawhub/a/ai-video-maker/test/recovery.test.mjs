import assert from "node:assert/strict";
import { test } from "node:test";
import { mkdtemp, writeFile, readFile, stat, rm, symlink } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";
import { prepareJobState, readJobState } from "../scripts/job-state.mjs";

const workflow = fileURLToPath(new URL("../scripts/run-workflow.mjs", import.meta.url));

test("private state preserves identity and rejects changed inputs/budget/key and symlinks", async () => {
  const dir = await mkdtemp(join(tmpdir(), "job-state-"));
  try {
    const path = join(dir, "job.json");
    const options = {
      model: "minimax",
      payload: { content: "private prompt", duration: 5 },
      maxCredits: 15,
    };
    const first = await prepareJobState(path, options);
    const reordered = await prepareJobState(path, {
      ...options,
      payload: { duration: 5, content: "private prompt" },
    });
    assert.equal(first.idempotencyKey, reordered.idempotencyKey);
    assert.equal((await stat(path)).mode & 0o777, 0o600);
    assert.doesNotMatch(await readFile(path, "utf8"), /private prompt/);
    for (const change of [
      { maxCredits: 16 },
      { payload: { content: "changed" } },
      { idempotencyKey: "different-key" },
    ])
      await assert.rejects(
        prepareJobState(path, { ...options, ...change }),
        /different request or budget/,
      );
    const link = join(dir, "link.json");
    await symlink(path, link);
    await assert.rejects(readJobState(link));
  } finally {
    await rm(dir, { recursive: true, force: true });
  }
});

test("interrupted submission reuses persisted key; wait never quotes or creates", async () => {
  const dir = await mkdtemp(join(tmpdir(), "job-resume-"));
  try {
    const state = join(dir, "state.json"),
      log = join(dir, "calls.jsonl"),
      mock = join(dir, "fetch.mjs");
    await writeFile(
      mock,
      `
      import {appendFileSync,readFileSync} from 'node:fs';
      globalThis.fetch=async(url,options)=>{
        const path=new URL(url).pathname;
        appendFileSync(${JSON.stringify(log)},JSON.stringify({path,key:options.headers['Idempotency-Key']})+'\\n');
        if(path.includes('/quote/'))return Response.json({credits:15,billable:false});
        if(path.includes('/generate/')){
          const saved=JSON.parse(readFileSync(${JSON.stringify(state)},'utf8'));
          if(saved.idempotencyKey!==options.headers['Idempotency-Key'])throw new Error('not persisted before create');
          if(process.env.SIMULATE_CRASH==='true')process.exit(3);
          return Response.json({status:'SUBMITTED',taskId:'resume-task'});
        }
        if(path.endsWith('/status')) {
          if(process.env.SIMULATE_POLL_ERROR==='true')return Response.json({message:'unavailable'},{status:503});
          return Response.json({status:process.env.SIMULATE_PENDING==='true'?'PROGRESS':'COMPLETED'});
        }
        if(path==='/api/v1/tasks/resume-task')return Response.json({status:'COMPLETED',id:'resume-task',output:{url:'https://example.test/video.mp4'}});
        throw new Error('unexpected request');
      };`,
    );
    const args = [
      "--model",
      "minimax",
      "--payload",
      JSON.stringify({ content: "private prompt", duration: 5 }),
      "--maxCredits",
      "15",
      "--stateFile",
      state,
    ];
    const run = (args, extra = {}) =>
      spawnSync(process.execPath, ["--import", mock, workflow, ...args], {
        encoding: "utf8",
        env: { ...process.env, AIVIDEO_API_KEY: "test-secret", AIVIDEO_MAX_RETRIES: "0", ...extra },
      });
    assert.equal(run(args, { SIMULATE_CRASH: "true" }).status, 3);
    const key = (await readJobState(state)).idempotencyKey;
    const recovered = run([...args, "--autoPoll", "false"]);
    assert.equal(recovered.status, 0, recovered.stdout);
    assert.equal((await readJobState(state)).taskId, "resume-task");
    assert.equal((await readJobState(state)).idempotencyKey, key);
    assert.equal((await stat(state)).mode & 0o777, 0o600);
    const before = (await readFile(log, "utf8")).trim().split("\n").map(JSON.parse);
    assert.ok(before.filter((x) => x.path.includes("/generate/")).every((x) => x.key === key));
    for (const extra of [{}, { SIMULATE_POLL_ERROR: "true" }, { SIMULATE_PENDING: "true" }]) {
      const result = run(
        ["--action", "wait", "--stateFile", state, "--maxWaitMs", "5", "--pollMinMs", "1"],
        extra,
      );
      const output = JSON.parse(result.stdout);
      assert.equal(output.taskId, "resume-task");
      assert.equal(output.idempotencyKey, key);
      assert.equal(
        result.status,
        extra.SIMULATE_PENDING ? 2 : extra.SIMULATE_POLL_ERROR ? 1 : 0,
        result.stdout,
      );
      assert.doesNotMatch(result.stdout, /test-secret|private prompt/);
    }
    const after = (await readFile(log, "utf8"))
      .trim()
      .split("\n")
      .map(JSON.parse)
      .slice(before.length);
    assert.ok(after.every((x) => !x.path.includes("/generate/") && !x.path.includes("/quote/")));
    const mismatch = run(["--action", "wait", "--stateFile", state, "--taskId", "wrong-task"]);
    assert.equal(mismatch.status, 1);
  } finally {
    await rm(dir, { recursive: true, force: true });
  }
});
