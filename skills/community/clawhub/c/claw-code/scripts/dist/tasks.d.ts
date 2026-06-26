/**
 * Tasks collection management.
 * Supports adding, completing, and querying tasks.
 * Ported from tasks.py
 */
import { PortingTask, TaskStatus } from "./task.js";
export declare class Tasks {
    private readonly _tasks;
    constructor(tasks?: Iterable<PortingTask>);
    get size(): number;
    add(task: PortingTask): void;
    addNew(id: string, description: string): PortingTask;
    get(id: string): PortingTask | undefined;
    has(id: string): boolean;
    remove(id: string): boolean;
    complete(id: string): boolean;
    start(id: string): boolean;
    block(id: string): boolean;
    reset(id: string): boolean;
    all(): PortingTask[];
    filter(predicate: (task: PortingTask) => boolean): PortingTask[];
    byStatus(status: TaskStatus): PortingTask[];
    pending(): PortingTask[];
    inProgress(): PortingTask[];
    completed(): PortingTask[];
    blocked(): PortingTask[];
    clear(): void;
    [Symbol.iterator](): Iterator<PortingTask>;
}
export declare function defaultTasks(): Tasks;
