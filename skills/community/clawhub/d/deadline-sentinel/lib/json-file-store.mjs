import { mkdir, readFile, rename, writeFile } from "node:fs/promises";
import { dirname } from "node:path";
import { DatabaseSync } from "node:sqlite";
import { setTimeout as delay } from "node:timers/promises";
export class JsonFileStore {
    path;
    defaultValue;
    writeQueue = Promise.resolve();
    constructor(path, defaultValue) {
        this.path = path;
        this.defaultValue = defaultValue;
    }
    async locked(operation) {
        await mkdir(dirname(this.path), { recursive: true });
        // Local SQLite owns the process-shared lock. Process death releases the
        // transaction; there is no stale lock-file deletion or timeout takeover.
        // Adapted from https://www.sqlite.org/lang_transaction.html#deferred_immediate_and_exclusive_transactions - process-shared transaction locking.
        const lock = new DatabaseSync(`${this.path}.lock.sqlite`);
        lock.exec("PRAGMA busy_timeout=0");
        const deadline = Date.now() + 30_000;
        const statement = async (sql) => {
            while (true) {
                try {
                    lock.exec(sql);
                    return;
                }
                catch (error) {
                    if (!/locked|busy/i.test(String(error)) || Date.now() >= deadline)
                        throw error;
                    await delay(15 + Math.floor(Math.random() * 20));
                }
            }
        };
        try {
            await statement("BEGIN IMMEDIATE");
            try {
                const result = await operation();
                await statement("COMMIT");
                return result;
            }
            catch (error) {
                lock.exec("ROLLBACK");
                throw error;
            }
        }
        finally {
            lock.close();
        }
    }
    async read() {
        try {
            return JSON.parse(await readFile(this.path, "utf8"));
        }
        catch (error) {
            if (error.code === "ENOENT")
                return structuredClone(this.defaultValue);
            throw error;
        }
    }
    async write(value) {
        const operation = async () => {
            await mkdir(dirname(this.path), { recursive: true });
            const temporaryPath = `${this.path}.${process.pid}.${Date.now()}.tmp`;
            await writeFile(temporaryPath, `${JSON.stringify(value, null, 2)}\n`, { encoding: "utf8", mode: 0o600 });
            await rename(temporaryPath, this.path);
        };
        const protectedOperation = () => this.locked(operation);
        this.writeQueue = this.writeQueue.then(protectedOperation, protectedOperation);
        await this.writeQueue;
    }
    async update(mutator) {
        let result;
        const operation = async () => {
            const current = await this.read();
            result = await mutator(current);
            await mkdir(dirname(this.path), { recursive: true });
            const temporaryPath = `${this.path}.${process.pid}.${Date.now()}.tmp`;
            await writeFile(temporaryPath, `${JSON.stringify(result, null, 2)}\n`, { encoding: "utf8", mode: 0o600 });
            await rename(temporaryPath, this.path);
        };
        const protectedOperation = () => this.locked(operation);
        this.writeQueue = this.writeQueue.then(protectedOperation, protectedOperation);
        await this.writeQueue;
        return result;
    }
}
