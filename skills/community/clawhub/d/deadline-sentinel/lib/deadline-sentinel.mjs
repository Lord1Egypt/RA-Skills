export class DeadlineSentinel {
    store;
    constructor(store) {
        this.store = store;
    }
    async list() {
        return (await this.store.read()).tasks;
    }
    async add(task) {
        if (!Number.isFinite(Date.parse(task.dueAt)))
            throw new Error("dueAt must be an ISO-8601 date");
        await this.store.update((database) => {
            if (database.tasks.some((existing) => existing.id === task.id))
                throw new Error(`Duplicate task id: ${task.id}`);
            return { tasks: [...database.tasks, task] };
        });
        return task;
    }
    async updateStatus(id, status) {
        let updated;
        await this.store.update((database) => ({
            tasks: database.tasks.map((task) => {
                if (task.id !== id)
                    return task;
                updated = { ...task, status };
                return updated;
            }),
        }));
        if (!updated)
            throw new Error(`Task not found: ${id}`);
        return updated;
    }
    async alerts(now = new Date(), horizonHours = 72) {
        return (await this.list())
            .filter((task) => task.status !== "done")
            .map((task) => ({ task, hoursRemaining: (Date.parse(task.dueAt) - now.getTime()) / 3_600_000 }))
            .filter(({ hoursRemaining }) => hoursRemaining <= horizonHours)
            .map(({ task, hoursRemaining }) => {
            const severity = hoursRemaining < 0 ? "overdue" : hoursRemaining <= 24 ? "urgent" : "soon";
            return { task, hoursRemaining, severity };
        })
            .sort((a, b) => a.hoursRemaining - b.hoursRemaining);
    }
}
