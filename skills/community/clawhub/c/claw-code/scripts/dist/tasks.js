/**
 * Tasks collection management.
 * Supports adding, completing, and querying tasks.
 * Ported from tasks.py
 */
import { PortingTask } from "./task.js";
export class Tasks {
    constructor(tasks) {
        this._tasks = new Map();
        if (tasks) {
            const taskArray = Array.from(tasks);
            for (const task of taskArray) {
                this._tasks.set(task.id, task);
            }
        }
    }
    get size() {
        return this._tasks.size;
    }
    add(task) {
        this._tasks.set(task.id, task);
    }
    addNew(id, description) {
        const task = new PortingTask(id, description);
        this._tasks.set(id, task);
        return task;
    }
    get(id) {
        return this._tasks.get(id);
    }
    has(id) {
        return this._tasks.has(id);
    }
    remove(id) {
        return this._tasks.delete(id);
    }
    complete(id) {
        const task = this._tasks.get(id);
        if (task) {
            task.complete();
            return true;
        }
        return false;
    }
    start(id) {
        const task = this._tasks.get(id);
        if (task) {
            task.start();
            return true;
        }
        return false;
    }
    block(id) {
        const task = this._tasks.get(id);
        if (task) {
            task.block();
            return true;
        }
        return false;
    }
    reset(id) {
        const task = this._tasks.get(id);
        if (task) {
            task.reset();
            return true;
        }
        return false;
    }
    all() {
        return Array.from(this._tasks.values());
    }
    filter(predicate) {
        const result = [];
        for (const task of this._tasks.values()) {
            if (predicate(task)) {
                result.push(task);
            }
        }
        return result;
    }
    byStatus(status) {
        return this.filter((task) => task.status === status);
    }
    pending() {
        return this.byStatus("pending");
    }
    inProgress() {
        return this.byStatus("in_progress");
    }
    completed() {
        return this.byStatus("completed");
    }
    blocked() {
        return this.byStatus("blocked");
    }
    clear() {
        this._tasks.clear();
    }
    *[Symbol.iterator]() {
        yield* Array.from(this._tasks.values());
    }
}
export function defaultTasks() {
    const tasks = new Tasks();
    tasks.add(new PortingTask("root-module-parity", "Mirror the root module surface of the archived snapshot"));
    tasks.add(new PortingTask("directory-parity", "Mirror top-level subsystem names as Python packages"));
    tasks.add(new PortingTask("parity-audit", "Continuously measure parity against the local archive"));
    return tasks;
}
