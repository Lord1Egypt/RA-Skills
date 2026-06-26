import { DependencyManager } from "./DependencyManager.js";
import { InMemoryStorage } from "./storage/InMemoryStorage.js";
import { compareReadyTasks, computeRetryAt, createTaskRecord } from "./utils.js";
import type {
  QueueSnapshot,
  QueueStorage,
  TaskLogEntry,
  TaskMetrics,
  TaskOptions,
  TaskRecord,
  TaskStatus
} from "./types.js";

const TERMINAL_STATUSES: TaskStatus[] = ["completed", "failed", "dead_letter", "cancelled"];

export class TaskQueue {
  readonly storage: QueueStorage;
  readonly dependencies: DependencyManager;

  constructor(storage: QueueStorage = new InMemoryStorage()) {
    this.storage = storage;
    this.dependencies = new DependencyManager(storage);
  }

  async enqueue<TPayload>(options: TaskOptions<TPayload>): Promise<TaskRecord<TPayload>> {
    const task = createTaskRecord(options);
    await this.dependencies.validateTask(task);
    if (task.status === "waiting_dependencies" && (await this.dependencies.areDependenciesSatisfied(task))) {
      await this.dependencies.persistDependencyResults(task);
      task.status = new Date(task.runAt).getTime() <= Date.now() ? "queued" : "retry_scheduled";
    }
    await this.storage.saveTask(task);
    await this.log(task.id, "info", "Task enqueued", {
      priority: task.priority,
      runAt: task.runAt,
      dependencies: task.dependencies
    });
    return task;
  }

  async claimNextReady(): Promise<TaskRecord | undefined> {
    const tasks = await this.storage.listTasks();
    const now = Date.now();
    const ready = tasks
      .filter((task) => ["queued", "retry_scheduled"].includes(task.status))
      .filter((task) => new Date(task.runAt).getTime() <= now)
      .sort(compareReadyTasks);
    const next = ready[0];
    if (!next) {
      return undefined;
    }
    next.status = "running";
    next.attempts += 1;
    next.startedAt = new Date().toISOString();
    next.updatedAt = next.startedAt;
    await this.storage.updateTask(next);
    await this.log(next.id, "info", "Task claimed for execution", { attempt: next.attempts });
    return next;
  }

  async complete(taskId: string, result: unknown): Promise<TaskRecord> {
    const task = await this.mustGet(taskId);
    task.status = "completed";
    task.result = result;
    task.completedAt = new Date().toISOString();
    task.updatedAt = task.completedAt;
    await this.storage.updateTask(task);
    await this.log(taskId, "info", "Task completed", { result });
    await this.dependencies.markBlockedDependents(taskId);
    return task;
  }

  async fail(taskId: string, error: Error | string): Promise<TaskRecord> {
    const task = await this.mustGet(taskId);
    const message = typeof error === "string" ? error : error.message;
    task.lastError = message;
    task.updatedAt = new Date().toISOString();
    if (task.attempts >= task.retryPolicy.maxAttempts) {
      task.status = "dead_letter";
      task.completedAt = task.updatedAt;
    } else {
      task.status = "retry_scheduled";
      task.runAt = computeRetryAt(task).toISOString();
    }
    await this.storage.updateTask(task);
    await this.log(taskId, "error", "Task failed", {
      error: message,
      nextRunAt: task.status === "retry_scheduled" ? task.runAt : undefined
    });
    return task;
  }

  async cancel(taskId: string, reason = "Cancelled"): Promise<TaskRecord> {
    const task = await this.mustGet(taskId);
    if (TERMINAL_STATUSES.includes(task.status)) {
      return task;
    }
    task.status = "cancelled";
    task.lastError = reason;
    task.updatedAt = new Date().toISOString();
    task.completedAt = task.updatedAt;
    await this.storage.updateTask(task);
    await this.log(taskId, "warn", "Task cancelled", { reason });
    return task;
  }

  async get(taskId: string): Promise<TaskRecord | undefined> {
    return this.storage.getTask(taskId);
  }

  async list(status?: TaskStatus): Promise<TaskRecord[]> {
    const tasks = await this.storage.listTasks();
    return tasks
      .filter((task) => !status || task.status === status)
      .sort(compareReadyTasks);
  }

  async getSnapshot(): Promise<QueueSnapshot> {
    const tasks = await this.storage.listTasks();
    const now = Date.now();
    return {
      ready: tasks
        .filter((task) => ["queued", "retry_scheduled"].includes(task.status) && new Date(task.runAt).getTime() <= now)
        .sort(compareReadyTasks),
      delayed: tasks
        .filter((task) => ["queued", "retry_scheduled"].includes(task.status) && new Date(task.runAt).getTime() > now)
        .sort(compareReadyTasks),
      deadLetter: tasks.filter((task) => task.status === "dead_letter").sort(compareReadyTasks)
    };
  }

  async metrics(): Promise<TaskMetrics> {
    const tasks = await this.storage.listTasks();
    const completed = tasks.filter((task) => task.status === "completed");
    const avgDurationMs =
      completed.reduce((sum, task) => {
        if (!task.startedAt || !task.completedAt) {
          return sum;
        }
        return sum + (new Date(task.completedAt).getTime() - new Date(task.startedAt).getTime());
      }, 0) / (completed.length || 1);
    return {
      queued: tasks.filter((task) => task.status === "queued").length,
      running: tasks.filter((task) => task.status === "running").length,
      waitingDependencies: tasks.filter((task) => task.status === "waiting_dependencies").length,
      retryScheduled: tasks.filter((task) => task.status === "retry_scheduled").length,
      completed: completed.length,
      failed: tasks.filter((task) => task.status === "failed").length,
      deadLetter: tasks.filter((task) => task.status === "dead_letter").length,
      avgDurationMs: Number.isFinite(avgDurationMs) ? avgDurationMs : 0
    };
  }

  async logs(taskId?: string): Promise<TaskLogEntry[]> {
    return this.storage.listLogs(taskId);
  }

  async log(taskId: string, level: TaskLogEntry["level"], message: string, context?: Record<string, unknown>): Promise<void> {
    await this.storage.appendLog({
      taskId,
      level,
      message,
      timestamp: new Date().toISOString(),
      context
    });
  }

  private async mustGet(taskId: string): Promise<TaskRecord> {
    const task = await this.storage.getTask(taskId);
    if (!task) {
      throw new Error(`Task ${taskId} not found`);
    }
    return task;
  }
}
