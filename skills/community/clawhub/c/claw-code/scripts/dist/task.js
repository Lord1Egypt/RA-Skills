/**
 * Task data class and task status management.
 * Ported from task.py
 */
export class PortingTask {
    constructor(id, description) {
        this._id = id;
        this._description = description;
        this._status = "pending";
        this._createdAt = new Date();
        this._completedAt = null;
    }
    get id() {
        return this._id;
    }
    get description() {
        return this._description;
    }
    get status() {
        return this._status;
    }
    get createdAt() {
        return this._createdAt;
    }
    get completedAt() {
        return this._completedAt;
    }
    isPending() {
        return this._status === "pending";
    }
    isInProgress() {
        return this._status === "in_progress";
    }
    isCompleted() {
        return this._status === "completed";
    }
    isBlocked() {
        return this._status === "blocked";
    }
    start() {
        if (this._status === "pending") {
            this._status = "in_progress";
        }
    }
    block() {
        if (this._status !== "completed") {
            this._status = "blocked";
        }
    }
    complete() {
        if (this._status !== "completed") {
            this._status = "completed";
            this._completedAt = new Date();
        }
    }
    reset() {
        this._status = "pending";
        this._completedAt = null;
    }
    toFields() {
        return {
            id: this._id,
            description: this._description,
            status: this._status,
            createdAt: this._createdAt,
            completedAt: this._completedAt,
        };
    }
}
