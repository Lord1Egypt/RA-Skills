"use strict";
/**
 * 后台进程管理器
 * 提供线程安全的进程注册、查询、终止功能
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.ProcessManager = void 0;
const constants_1 = require("./constants");
const ringbuf_1 = require("./ringbuf");
const platform_1 = require("./platform");
/**
 * 进程管理器
 */
class ProcessManager {
    processes = new Map();
    maxProcesses;
    constructor(maxProcesses = constants_1.DEFAULT_MAX_PROCESSES) {
        this.maxProcesses = maxProcesses;
    }
    /**
     * 注册新的后台进程
     */
    register(pid, command, childProcess, cancelCallback) {
        if (this.processes.size >= this.maxProcesses) {
            throw new constants_1.MaxProcessesReachedError(this.maxProcesses);
        }
        if (this.processes.has(pid)) {
            throw new constants_1.ProcessAlreadyExistsError(pid);
        }
        const process = {
            pid,
            command,
            startTime: new Date(),
            status: constants_1.PROCESS_STATUS_RUNNING,
            exitCode: -1,
            watchDuration: 0,
            watchCompleted: false,
            stdoutBuffer: (0, ringbuf_1.createRingBuffer)(),
            stderrBuffer: (0, ringbuf_1.createRingBuffer)(),
            childProcess,
            cancelCallback,
        };
        this.processes.set(pid, process);
        return process;
    }
    /**
     * 获取进程信息
     */
    get(pid) {
        return this.processes.get(pid);
    }
    /**
     * 获取进程状态
     */
    getStatus(pid) {
        const proc = this.processes.get(pid);
        if (!proc) {
            throw new constants_1.ProcessNotFoundError(pid);
        }
        return {
            pid: proc.pid,
            status: proc.status,
            exitCode: proc.exitCode,
            command: proc.command,
            startTime: proc.startTime.toISOString(),
            endTime: proc.endTime?.toISOString(),
            watchDurationSeconds: proc.watchDuration,
            watchCompleted: proc.watchCompleted,
        };
    }
    /**
     * 获取进程完整信息（含输出）
     */
    getProcessInfo(pid) {
        const proc = this.processes.get(pid);
        if (!proc) {
            throw new constants_1.ProcessNotFoundError(pid);
        }
        const status = this.getStatus(pid);
        return {
            ...status,
            stdout: proc.stdoutBuffer.toString(),
            stderr: proc.stderrBuffer.toString(),
        };
    }
    /**
     * 终止进程
     */
    async terminate(pid) {
        const proc = this.processes.get(pid);
        if (!proc) {
            throw new constants_1.ProcessNotFoundError(pid);
        }
        // 调用取消回调（如果设置了超时）
        if (proc.cancelCallback) {
            proc.cancelCallback();
        }
        // 杀死进程
        await (0, platform_1.killProcess)(proc.childProcess);
        // 更新状态
        proc.status = constants_1.PROCESS_STATUS_FAILED;
        proc.endTime = new Date();
        proc.exitCode = -1;
    }
    /**
     * 移除进程记录
     */
    remove(pid) {
        this.processes.delete(pid);
    }
    /**
     * 清理已完成的进程记录
     */
    cleanupCompleted() {
        let count = 0;
        for (const [pid, proc] of this.processes) {
            if (proc.status === constants_1.PROCESS_STATUS_COMPLETED || proc.status === constants_1.PROCESS_STATUS_FAILED) {
                this.processes.delete(pid);
                count++;
            }
        }
        return count;
    }
    /**
     * 列出所有进程
     */
    list() {
        const statuses = [];
        for (const proc of this.processes.values()) {
            statuses.push({
                pid: proc.pid,
                status: proc.status,
                exitCode: proc.exitCode,
                command: proc.command,
                startTime: proc.startTime.toISOString(),
                endTime: proc.endTime?.toISOString(),
                watchDurationSeconds: proc.watchDuration,
                watchCompleted: proc.watchCompleted,
            });
        }
        return statuses;
    }
    /**
     * 获取进程数量
     */
    size() {
        return this.processes.size;
    }
    /**
     * 更新进程状态
     */
    updateStatus(pid, updates) {
        const proc = this.processes.get(pid);
        if (proc) {
            Object.assign(proc, updates);
        }
    }
    /**
     * 获取进程的 stdout Buffer
     */
    getStdoutBuffer(pid) {
        const proc = this.processes.get(pid);
        return proc?.stdoutBuffer;
    }
    /**
     * 获取进程的 stderr Buffer
     */
    getStderrBuffer(pid) {
        const proc = this.processes.get(pid);
        return proc?.stderrBuffer;
    }
}
exports.ProcessManager = ProcessManager;
//# sourceMappingURL=process-manager.js.map