import { Scheduler, TaskQueue } from "../src/index.js";

async function main(): Promise<void> {
  const queue = new TaskQueue();
  const scheduler = new Scheduler(queue, { concurrency: 2, pollIntervalMs: 50 });

  scheduler.register("fetch-context", async (payload, context) => {
    await context.log("info", "Fetching context", payload as Record<string, unknown>);
    return {
      summary: "Repository state loaded",
      branch: "main"
    };
  });

  scheduler.register("write-report", async (payload, context) => {
    const upstream = context.dependencies.get("task-context") as { summary: string; branch: string } | undefined;
    return {
      message: `Report for ${String((payload as { task: string }).task)}`,
      upstream
    };
  });

  await queue.enqueue({
    id: "task-context",
    type: "fetch-context",
    payload: { repo: "agent-task-queue" },
    priority: 10
  });

  await queue.enqueue({
    id: "task-report",
    type: "write-report",
    payload: { task: "daily-sync" },
    dependencies: ["task-context"]
  });

  await scheduler.tick();
  await new Promise((resolve) => setTimeout(resolve, 25));
  await scheduler.tick();
  await new Promise((resolve) => setTimeout(resolve, 25));

  console.log(await queue.metrics());
  console.log(await queue.get("task-report"));
}

void main();
