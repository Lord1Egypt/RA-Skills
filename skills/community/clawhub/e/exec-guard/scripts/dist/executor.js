"use strict";
/**
 * 命令执行器
 * 提供同步和异步两种执行模式，支持超时控制和输出截断
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.CommandExecutor = void 0;
const constants_1 = require("./constants");
const ringbuf_1 = require("./ringbuf");
const platform_1 = require("./platform");
/**
 * 命令执行器
 */
class CommandExecutor {
    processManager;
    constructor(processManager) {
        this.processManager = processManager;
    }
    /**
     * 执行命令（主入口）
     * 根据请求的 runInBackground 字段决定同步或异步执行
     */
    async execute(req) {
        // 验证请求
        this.validateRequest(req);
        // 验证工作目录
        if (req.workingDir) {
            (0, platform_1.validateWorkingDir)(req.workingDir);
        }
        if (req.runInBackground) {
            return this.executeBackground(req);
        }
        return this.executeSync(req);
    }
    /**
     * 验证请求的合法性
     */
    validateRequest(req) {
        if (!req.command || req.command.trim() === '') {
            throw new constants_1.EmptyCommandError();
        }
    }
    /**
     * 获取超时时间（带默认值）
     */
    getTimeout(req) {
        return req.timeoutSeconds && req.timeoutSeconds > 0
            ? req.timeoutSeconds
            : constants_1.DEFAULT_TIMEOUT_SECONDS;
    }
    /**
     * 获取监控窗口时长
     */
    getWatchDuration(req) {
        return req.watchDurationSeconds && req.watchDurationSeconds > 0
            ? req.watchDurationSeconds
            : 0;
    }
    /**
     * 是否启用了监控窗口
     */
    hasWatchWindow(req) {
        return (req.runInBackground ?? false) && this.getWatchDuration(req) > 0;
    }
    /**
     * 同步执行命令
     */
    async executeSync(req) {
        const timeout = this.getTimeout(req);
        const stdoutBuffer = (0, ringbuf_1.createRingBuffer)();
        const stderrBuffer = (0, ringbuf_1.createRingBuffer)();
        const childProcess = (0, platform_1.buildCommand)(req.command, req.workingDir, req.env);
        // 创建超时控制器
        let timeoutId = null;
        let isTimeout = false;
        const timeoutPromise = new Promise((resolve) => {
            timeoutId = setTimeout(async () => {
                isTimeout = true;
                await (0, platform_1.killProcess)(childProcess);
                resolve({
                    status: constants_1.STATUS_TIMEOUT,
                    exitCode: -1,
                    stdout: stdoutBuffer.toString(),
                    stderr: stderrBuffer.toString(),
                    systemMessage: new constants_1.TimeoutExceededError(timeout).message,
                });
            }, timeout * 1000);
        });
        // 捕获输出
        if (childProcess.stdout) {
            childProcess.stdout.on('data', (data) => {
                stdoutBuffer.write(data);
            });
        }
        if (childProcess.stderr) {
            childProcess.stderr.on('data', (data) => {
                stderrBuffer.write(data);
            });
        }
        // 执行完成 Promise
        const executionPromise = new Promise((resolve) => {
            childProcess.on('close', (code) => {
                if (timeoutId) {
                    clearTimeout(timeoutId);
                }
                if (isTimeout) {
                    // 已被超时处理
                    return;
                }
                const exitCode = code ?? -1;
                const status = exitCode === 0 ? constants_1.STATUS_SUCCESS : constants_1.STATUS_FAILED;
                const systemMessage = exitCode === 0
                    ? 'command executed successfully'
                    : `command exited with code ${exitCode}`;
                resolve({
                    status,
                    exitCode,
                    stdout: stdoutBuffer.toString(),
                    stderr: stderrBuffer.toString(),
                    systemMessage,
                });
            });
            childProcess.on('error', (err) => {
                if (timeoutId) {
                    clearTimeout(timeoutId);
                }
                resolve({
                    status: constants_1.STATUS_FAILED,
                    exitCode: -1,
                    stdout: stdoutBuffer.toString(),
                    stderr: stderrBuffer.toString(),
                    systemMessage: `execution error: ${err.message}`,
                });
            });
        });
        // 等待执行完成或超时
        return Promise.race([executionPromise, timeoutPromise]);
    }
    /**
     * 后台执行命令
     * 支持监控窗口模式
     */
    async executeBackground(req) {
        const timeout = this.getTimeout(req);
        const watchDuration = this.getWatchDuration(req);
        const childProcess = (0, platform_1.buildCommand)(req.command, req.workingDir, req.env);
        // 等待进程启动
        await new Promise((resolve, reject) => {
            childProcess.on('spawn', () => resolve());
            childProcess.on('error', (err) => reject(err));
        });
        const pid = childProcess.pid;
        const stdoutBuffer = (0, ringbuf_1.createRingBuffer)();
        const stderrBuffer = (0, ringbuf_1.createRingBuffer)();
        // 创建超时控制器
        let timeoutId = null;
        const cancelCallback = () => {
            if (timeoutId) {
                clearTimeout(timeoutId);
            }
        };
        // 注册进程
        const managedProcess = this.processManager.register(pid, req.command, childProcess, cancelCallback);
        // 捕获输出
        if (childProcess.stdout) {
            childProcess.stdout.on('data', (data) => {
                stdoutBuffer.write(data);
            });
        }
        if (childProcess.stderr) {
            childProcess.stderr.on('data', (data) => {
                stderrBuffer.write(data);
            });
        }
        // 设置超时
        timeoutId = setTimeout(async () => {
            await (0, platform_1.killProcess)(childProcess);
            this.processManager.updateStatus(pid, {
                status: constants_1.PROCESS_STATUS_FAILED,
                endTime: new Date(),
                exitCode: -1,
            });
        }, timeout * 1000);
        // 进程完成处理
        childProcess.on('close', (code) => {
            if (timeoutId) {
                clearTimeout(timeoutId);
            }
            const exitCode = code ?? -1;
            const status = exitCode === 0 ? constants_1.PROCESS_STATUS_COMPLETED : constants_1.PROCESS_STATUS_FAILED;
            this.processManager.updateStatus(pid, {
                status,
                exitCode,
                endTime: new Date(),
            });
        });
        childProcess.on('error', (err) => {
            if (timeoutId) {
                clearTimeout(timeoutId);
            }
            this.processManager.updateStatus(pid, {
                status: constants_1.PROCESS_STATUS_FAILED,
                exitCode: -1,
                endTime: new Date(),
                error: err,
            });
        });
        // 检查是否启用监控窗口
        if (watchDuration > 0) {
            return this.executeWithWatchWindow(pid, watchDuration, stdoutBuffer, stderrBuffer);
        }
        // 无监控窗口：立即返回
        return {
            status: constants_1.STATUS_RUNNING,
            exitCode: -1,
            stdout: '',
            stderr: '',
            systemMessage: `process started with PID ${pid}`,
        };
    }
    /**
     * 带监控窗口的后台执行
     * 等待 watchDuration 秒观察进程状态
     */
    async executeWithWatchWindow(pid, watchDuration, stdoutBuffer, stderrBuffer) {
        const watchPromise = new Promise((resolve) => {
            const watchTimeoutId = setTimeout(() => {
                // 监控窗口超时，进程仍在运行
                this.processManager.updateStatus(pid, {
                    watchCompleted: true,
                    watchDuration,
                });
                resolve({
                    status: constants_1.STATUS_RUNNING,
                    exitCode: -1,
                    stdout: stdoutBuffer.toString(),
                    stderr: stderrBuffer.toString(),
                    systemMessage: `process running with PID ${pid}, watch window (${watchDuration}s) elapsed`,
                });
            }, watchDuration * 1000);
            // 监听进程退出
            const proc = this.processManager.get(pid);
            if (proc?.childProcess) {
                proc.childProcess.on('close', (code) => {
                    clearTimeout(watchTimeoutId);
                    const exitCode = code ?? -1;
                    const status = exitCode === 0 ? constants_1.STATUS_SUCCESS : constants_1.STATUS_FAILED;
                    this.processManager.updateStatus(pid, {
                        status: exitCode === 0 ? constants_1.PROCESS_STATUS_COMPLETED : constants_1.PROCESS_STATUS_FAILED,
                        exitCode,
                        endTime: new Date(),
                        watchCompleted: true,
                    });
                    resolve({
                        status,
                        exitCode,
                        stdout: stdoutBuffer.toString(),
                        stderr: stderrBuffer.toString(),
                        systemMessage: exitCode === 0
                            ? 'process completed during watch window'
                            : `process exited during watch window with code ${exitCode}`,
                    });
                });
            }
        });
        return watchPromise;
    }
    /**
     * 获取后台进程状态
     */
    getProcessStatus(pid) {
        return this.processManager.getStatus(pid);
    }
    /**
     * 获取后台进程完整信息
     */
    getProcessInfo(pid) {
        return this.processManager.getProcessInfo(pid);
    }
    /**
     * 终止后台进程
     */
    async terminateProcess(pid) {
        await this.processManager.terminate(pid);
    }
    /**
     * 列出所有后台进程
     */
    listProcesses() {
        return this.processManager.list();
    }
    /**
     * 清理已完成的进程记录
     */
    cleanupCompletedProcesses() {
        return this.processManager.cleanupCompleted();
    }
}
exports.CommandExecutor = CommandExecutor;
//# sourceMappingURL=executor.js.map