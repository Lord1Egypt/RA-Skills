import type { QueueStorage, TaskLogEntry, TaskRecord } from "../types.js";

export class InMemoryStorage implements QueueStorage {
  private readonly tasks = new Map<string, TaskRecord>();
  private readonly logs: TaskLogEntry[] = [];
  private readonly dependencyResults = new Map<string, Map<string, unknown>>();

  async saveTask(task: TaskRecord): Promise<void> {
    this.tasks.set(task.id, structuredClone(task));
  }

  async getTask(taskId: string): Promise<TaskRecord | undefined> {
    const task = this.tasks.get(taskId);
    return task ? structuredClone(task) : undefined;
  }

  async updateTask(task: TaskRecord): Promise<void> {
    this.tasks.set(task.id, structuredClone(task));
  }

  async listTasks(): Promise<TaskRecord[]> {
    return [...this.tasks.values()].map((task) => structuredClone(task));
  }

  async listLogs(taskId?: string): Promise<TaskLogEntry[]> {
    return this.logs
      .filter((entry) => !taskId || entry.taskId === taskId)
      .map((entry) => structuredClone(entry));
  }

  async appendLog(entry: TaskLogEntry): Promise<void> {
    this.logs.push(structuredClone(entry));
  }

  async saveDependencyResult(taskId: string, dependencyId: string, value: unknown): Promise<void> {
    const taskResults = this.dependencyResults.get(taskId) ?? new Map<string, unknown>();
    taskResults.set(dependencyId, structuredClone(value));
    this.dependencyResults.set(taskId, taskResults);
  }

  async getDependencyResults(taskId: string): Promise<Map<string, unknown>> {
    const taskResults = this.dependencyResults.get(taskId) ?? new Map<string, unknown>();
    return new Map<string, unknown>([...taskResults.entries()].map(([key, value]) => [key, structuredClone(value)]));
  }
}
