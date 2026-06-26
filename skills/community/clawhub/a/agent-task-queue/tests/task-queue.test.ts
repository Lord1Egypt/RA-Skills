import test from "node:test";
import assert from "node:assert/strict";
import { Scheduler } from "../src/Scheduler.js";
import { TaskQueue } from "../src/TaskQueue.js";

test("claims higher priority tasks first", async () => {
  const queue = new TaskQueue();
  const low = await queue.enqueue({ type: "job", payload: { name: "low" }, priority: 1 });
  const high = await queue.enqueue({ type: "job", payload: { name: "high" }, priority: 10 });

  const first = await queue.claimNextReady();
  const second = await queue.claimNextReady();

  assert.equal(first?.id, high.id);
  assert.equal(second?.id, low.id);
});

test("keeps delayed tasks out of the ready queue until due", async () => {
  const queue = new TaskQueue();
  await queue.enqueue({
    type: "job",
    payload: {},
    runAt: new Date(Date.now() + 60_000)
  });

  const snapshot = await queue.getSnapshot();
  assert.equal(snapshot.ready.length, 0);
  assert.equal(snapshot.delayed.length, 1);
});

test("unblocks dependent tasks and passes dependency results", async () => {
  const queue = new TaskQueue();
  const scheduler = new Scheduler(queue, { pollIntervalMs: 5, concurrency: 2 });
  const outputs: string[] = [];

  scheduler.register("producer", async () => "artifact-1");
  scheduler.register("consumer", async (_payload, context) => {
    outputs.push(String(context.dependencies.get("producer-task")));
    return "done";
  });

  await queue.enqueue({ id: "producer-task", type: "producer", payload: {} });
  await queue.enqueue({
    id: "consumer-task",
    type: "consumer",
    payload: {},
    dependencies: ["producer-task"]
  });

  await scheduler.tick();
  await new Promise((resolve) => setTimeout(resolve, 20));
  await scheduler.tick();
  await new Promise((resolve) => setTimeout(resolve, 20));

  const consumer = await queue.get("consumer-task");
  assert.equal(consumer?.status, "completed");
  assert.deepEqual(outputs, ["artifact-1"]);
});

test("moves exhausted retries to dead letter", async () => {
  const queue = new TaskQueue();
  const scheduler = new Scheduler(queue, { pollIntervalMs: 5, concurrency: 1 });
  let attempts = 0;

  scheduler.register("unstable", async () => {
    attempts += 1;
    throw new Error(`boom-${attempts}`);
  });

  await queue.enqueue({
    id: "unstable-task",
    type: "unstable",
    payload: {},
    retryPolicy: { maxAttempts: 2, backoffMs: 0, backoffMultiplier: 1 }
  });

  await scheduler.tick();
  await new Promise((resolve) => setTimeout(resolve, 10));
  const firstFailure = await queue.get("unstable-task");
  assert.equal(firstFailure?.status, "retry_scheduled");

  if (firstFailure) {
    firstFailure.runAt = new Date(Date.now() - 1).toISOString();
    await queue.storage.updateTask(firstFailure);
  }

  await scheduler.tick();
  await new Promise((resolve) => setTimeout(resolve, 10));

  const finalTask = await queue.get("unstable-task");
  assert.equal(finalTask?.status, "dead_letter");
  assert.equal(attempts, 2);
});

test("records timeout failures for long-running tasks", async () => {
  const queue = new TaskQueue();
  const scheduler = new Scheduler(queue, { pollIntervalMs: 5, concurrency: 1 });

  scheduler.register("slow", async (_payload, context) => {
    await new Promise((resolve, reject) => {
      const timer = setTimeout(resolve, 100);
      context.signal.addEventListener("abort", () => {
        clearTimeout(timer);
        reject(context.signal.reason);
      });
    });
    return "unreachable";
  });

  await queue.enqueue({
    id: "slow-task",
    type: "slow",
    payload: {},
    timeoutMs: 20,
    retryPolicy: { maxAttempts: 1 }
  });

  await scheduler.tick();
  await new Promise((resolve) => setTimeout(resolve, 40));

  const task = await queue.get("slow-task");
  assert.equal(task?.status, "dead_letter");
  assert.match(task?.lastError ?? "", /timed out/i);
});
