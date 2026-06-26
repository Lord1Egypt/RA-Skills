import Database from "better-sqlite3";
import type { QueueStorage, TaskLogEntry, TaskRecord } from "../types.js";

function parseTask(row: Record<string, unknown>): TaskRecord {
  return {
    ...JSON.parse(String(row.data)),
    id: String(row.id)
  } as TaskRecord;
}

export class SQLiteStorage implements QueueStorage {
  private readonly db: Database.Database;

  constructor(filename = "task-queue.sqlite") {
    this.db = new Database(filename);
    this.db.pragma("journal_mode = WAL");
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS tasks (
        id TEXT PRIMARY KEY,
        data TEXT NOT NULL
      );
      CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id TEXT NOT NULL,
        data TEXT NOT NULL
      );
      CREATE TABLE IF NOT EXISTS dependency_results (
        task_id TEXT NOT NULL,
        dependency_id TEXT NOT NULL,
        data TEXT NOT NULL,
        PRIMARY KEY (task_id, dependency_id)
      );
    `);
  }

  async saveTask(task: TaskRecord): Promise<void> {
    this.db.prepare("INSERT OR REPLACE INTO tasks (id, data) VALUES (?, ?)").run(task.id, JSON.stringify(task));
  }

  async getTask(taskId: string): Promise<TaskRecord | undefined> {
    const row = this.db.prepare("SELECT id, data FROM tasks WHERE id = ?").get(taskId) as Record<string, unknown> | undefined;
    return row ? parseTask(row) : undefined;
  }

  async updateTask(task: TaskRecord): Promise<void> {
    await this.saveTask(task);
  }

  async listTasks(): Promise<TaskRecord[]> {
    const rows = this.db.prepare("SELECT id, data FROM tasks").all() as Record<string, unknown>[];
    return rows.map(parseTask);
  }

  async listLogs(taskId?: string): Promise<TaskLogEntry[]> {
    const rows = taskId
      ? this.db.prepare("SELECT data FROM logs WHERE task_id = ? ORDER BY id ASC").all(taskId)
      : this.db.prepare("SELECT data FROM logs ORDER BY id ASC").all();
    return (rows as Array<{ data: string }>).map((row) => JSON.parse(row.data) as TaskLogEntry);
  }

  async appendLog(entry: TaskLogEntry): Promise<void> {
    this.db.prepare("INSERT INTO logs (task_id, data) VALUES (?, ?)").run(entry.taskId, JSON.stringify(entry));
  }

  async saveDependencyResult(taskId: string, dependencyId: string, value: unknown): Promise<void> {
    this.db
      .prepare("INSERT OR REPLACE INTO dependency_results (task_id, dependency_id, data) VALUES (?, ?, ?)")
      .run(taskId, dependencyId, JSON.stringify(value));
  }

  async getDependencyResults(taskId: string): Promise<Map<string, unknown>> {
    const rows = this.db
      .prepare("SELECT dependency_id, data FROM dependency_results WHERE task_id = ?")
      .all(taskId) as Array<{ dependency_id: string; data: string }>;
    return new Map(rows.map((row) => [row.dependency_id, JSON.parse(row.data)]));
  }
}
