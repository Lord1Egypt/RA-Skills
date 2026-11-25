import assert from "node:assert/strict";
import { mkdtemp, writeFile, readFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";
import { test } from "node:test";

const workflow = fileURLToPath(new URL("../scripts/run-workflow.mjs", import.meta.url));
const flow = "38bfe3d9-b03e-45c3-9e05-88cb5a7f7ad7";
const newFlow = "48bfe3d9-b03e-45c3-9e05-88cb5a7f7ad7";

async function isolatedMock(run) {
  const directory = await mkdtemp(join(tmpdir(), "skill-review-"));
  try {
    const ledger = join(directory, "ledger.json");
    const mock = join(directory, "fetch.mjs");
    await writeFile(
      ledger,
      JSON.stringify({ balance: 50, tasks: {}, posts: 0, charges: 0, queries: 0 }),
    );
    await writeFile(
      mock,
      `
      import {readFileSync,writeFileSync} from 'node:fs';
      const ledgerPath=${JSON.stringify(ledger)};
      globalThis.fetch=async(url,options)=>{
        const path=new URL(url).pathname;
        const ledger=JSON.parse(readFileSync(ledgerPath,'utf8'));
        const save=()=>writeFileSync(ledgerPath,JSON.stringify(ledger));
        if(path==='/api/v1/quote/minimax') {
          return Response.json({credits:45,currentBalance:ledger.balance,affordable:ledger.balance>=45,billable:false});
        }
        if(path==='/api/v1/generate/minimax') {
          ledger.posts++;
          const key=options.headers['Idempotency-Key'];
          if(options.headers['X-Max-Credits']!=='45') throw new Error('missing credit cap');
          if(ledger.tasks[key]) {save();return Response.json({taskId:ledger.tasks[key],status:'SUBMITTED',idempotentReplay:true});}
          if(ledger.balance<45) {save();return Response.json({status:'FAILED',errorCode:'INSUFFICIENT_CREDITS',message:'Insufficient credits'},{status:402});}
          ledger.balance-=45;ledger.charges++;
          ledger.tasks[key]='paid-task';save();
          if(process.env.CRASH_AFTER_DEBIT==='true')process.exit(3);
          return Response.json({taskId:'paid-task',status:'SUBMITTED',creditsCharged:45});
        }
        if(path==='/api/v1/tasks/paid-task/status') {
          ledger.queries++;save();
          if(process.env.QUERY_MODE==='transport-failed')return Response.json({status:'FAILED',message:'Query unavailable'},{status:503});
          return Response.json({status:process.env.QUERY_MODE||'COMPLETED'});
        }
        if(path==='/api/v1/tasks/paid-task')return Response.json({id:'paid-task',status:'COMPLETED',output:{url:'https://example.test/video.mp4'}});
        throw new Error('unexpected request');
      };`,
    );
    const cli = (args, extra = {}) => {
      const result = spawnSync(process.execPath, ["--import", mock, workflow, ...args], {
        encoding: "utf8",
        env: { ...process.env, AIVIDEO_API_KEY: "test-only", AIVIDEO_MAX_RETRIES: "0", ...extra },
      });
      return { ...result, output: result.stdout.trim() ? JSON.parse(result.stdout) : null };
    };
    await run({
      cli,
      stateFile: join(directory, "state.json"),
      readLedger: async () => JSON.parse(await readFile(ledger, "utf8")),
    });
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
}

function createArgs(flowId = flow) {
  return [
    "--firstVideoFlow",
    flowId,
    "--scenario",
    "product",
    "--payload",
    JSON.stringify({
      content: "Show lamp",
      imageUrl: "https://example.test/lamp.png",
      duration: 15,
    }),
    "--approved",
    "true",
    "--maxCredits",
    "45",
    "--autoPoll",
    "false",
  ];
}

for (const recovery of ["same-key", "saved-task", "interrupted-submission"]) {
  test(`45-credit first-video ${recovery} recovers after balance drops from 50 to 5`, async () => {
    await isolatedMock(async ({ cli, stateFile, readLedger }) => {
      const args = [
        ...createArgs(),
        ...(recovery === "same-key" ? [] : ["--stateFile", stateFile]),
      ];
      const initial = cli(
        args,
        recovery === "interrupted-submission" ? { CRASH_AFTER_DEBIT: "true" } : {},
      );
      assert.equal(initial.status, recovery === "interrupted-submission" ? 3 : 0, initial.stdout);
      assert.equal((await readLedger()).balance, 5);
      const replay = cli(args);
      assert.equal(replay.status, 0, replay.stdout);
      assert.equal(replay.output.taskId, "paid-task");
      assert.equal(replay.output.idempotencyKey, `first-video:${flow}`);
      let ledger = await readLedger();
      assert.equal(ledger.charges, 1);
      assert.equal(Object.keys(ledger.tasks).length, 1);
      assert.equal(ledger.balance, 5);
      const fresh = cli(createArgs(newFlow));
      assert.equal(fresh.status, 1);
      assert.equal(fresh.output.errorCode, "INSUFFICIENT_CREDITS");
      ledger = await readLedger();
      assert.equal(ledger.charges, 1, "a new unaffordable task must not charge");
      assert.equal(
        Object.keys(ledger.tasks).length,
        1,
        "a new unaffordable task must not be created",
      );
      const posts = ledger.posts;
      const capped = createArgs(newFlow);
      capped[capped.indexOf("--maxCredits") + 1] = "44";
      const overBudget = cli(capped);
      assert.equal(overBudget.output.errorCode, "BUDGET_EXCEEDED");
      assert.equal((await readLedger()).posts, posts, "the approved cap must block POST locally");
    });
  });
}

for (const status of ["FAILED", "CANCEL", "transport-failed", "PROGRESS"]) {
  test(`wait distinguishes ${status} from other task/query states`, async () => {
    await isolatedMock(async ({ cli, readLedger }) => {
      const result = cli(
        ["--action", "wait", "--taskId", "paid-task", "--maxWaitMs", "10", "--pollMinMs", "1"],
        { QUERY_MODE: status },
      );
      assert.equal(result.status, status === "PROGRESS" ? 2 : 1, result.stdout);
      assert.equal(result.output.taskId, "paid-task");
      const suggestions = result.output.suggestions.join(" ");
      if (status === "FAILED" || status === "CANCEL") {
        assert.equal(result.output.status, status);
        assert.match(suggestions, /new.*quote|separately quoted/i);
        assert.doesNotMatch(suggestions, /--action wait|resume|continue waiting/i);
        assert.equal((await readLedger()).queries, 1);
      } else {
        assert.match(suggestions, /--action wait/);
        if (status === "PROGRESS") assert.equal(result.output.errorCode, "POLL_TIMEOUT");
      }
      assert.equal((await readLedger()).posts, 0, "waiting must never submit a generation");
    });
  });
}
