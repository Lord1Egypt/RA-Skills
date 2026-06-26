import type { QueueStorage, TaskRecord } from "./types.js";

export class DependencyManager {
  constructor(private readonly storage: QueueStorage) {}

  async validateTask(task: TaskRecord): Promise<void> {
    if (task.dependencies.includes(task.id)) {
      throw new Error(`Task ${task.id} cannot depend on itself`);
    }

    for (const dependencyId of task.dependencies) {
      const dependency = await this.storage.getTask(dependencyId);
      if (!dependency) {
        throw new Error(`Task ${task.id} depends on missing task ${dependencyId}`);
      }
    }

    const allTasks = await this.storage.listTasks();
    const graph = new Map<string, string[]>();
    for (const item of allTasks) {
      graph.set(item.id, [...item.dependencies]);
    }
    graph.set(task.id, [...task.dependencies]);
    this.assertNoCycle(graph, task.id);
  }

  async areDependenciesSatisfied(task: TaskRecord): Promise<boolean> {
    for (const dependencyId of task.dependencies) {
      const dependency = await this.storage.getTask(dependencyId);
      if (!dependency || dependency.status !== "completed") {
        return false;
      }
    }
    return true;
  }

  async persistDependencyResults(task: TaskRecord): Promise<void> {
    for (const dependencyId of task.dependencies) {
      const dependency = await this.storage.getTask(dependencyId);
      if (dependency?.status === "completed") {
        await this.storage.saveDependencyResult(task.id, dependencyId, dependency.result);
      }
    }
  }

  async markBlockedDependents(completedTaskId: string): Promise<void> {
    const tasks = await this.storage.listTasks();
    for (const task of tasks) {
      if (!task.dependencies.includes(completedTaskId)) {
        continue;
      }
      if (task.status !== "waiting_dependencies") {
        continue;
      }
      if (!(await this.areDependenciesSatisfied(task))) {
        continue;
      }
      await this.persistDependencyResults(task);
      task.status = new Date(task.runAt).getTime() <= Date.now() ? "queued" : "retry_scheduled";
      task.updatedAt = new Date().toISOString();
      await this.storage.updateTask(task);
      await this.storage.appendLog({
        taskId: task.id,
        level: "info",
        message: "All dependencies satisfied",
        timestamp: task.updatedAt,
        context: { completedTaskId }
      });
    }
  }

  private assertNoCycle(graph: Map<string, string[]>, start: string): void {
    const visited = new Set<string>();
    const path = new Set<string>();
    const visit = (node: string): void => {
      if (path.has(node)) {
        throw new Error(`Dependency cycle detected at task ${node}`);
      }
      if (visited.has(node)) {
        return;
      }
      visited.add(node);
      path.add(node);
      for (const dependency of graph.get(node) ?? []) {
        visit(dependency);
      }
      path.delete(node);
    };
    visit(start);
  }
}
