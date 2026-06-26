"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.FlashMonitorManager = void 0;
const path_1 = __importDefault(require("path"));
const MonitorAnalyzer_1 = require("./MonitorAnalyzer");
const fs_1 = require("../common/fs");
const process_1 = require("../common/process");
class FlashMonitorManager {
    constructor() {
        this.monitorAnalyzer = new MonitorAnalyzer_1.MonitorAnalyzer();
        this.defaultTimeoutMs = 15000;
        this.logTailLines = 16;
    }
    async run(args) {
        const startedAt = Date.now();
        const timeoutMs = args.timeoutMs || this.defaultTimeoutMs;
        const command = ['flash', 'monitor'];
        if (args.port) {
            command.unshift('-p', args.port);
        }
        if (args.baud) {
            command.unshift('-b', String(args.baud));
        }
        if (!await (0, fs_1.pathExists)(path_1.default.join(args.projectPath, 'CMakeLists.txt'))) {
            return {
                status: 'ENV_ERROR',
                command: ['idf.py', ...command],
                port: args.port,
                baud: args.baud,
                timeoutMs,
                durationMs: Date.now() - startedAt,
                stage: 'preflight',
                stageSummary: '预检失败：当前目录不是标准 ESP-IDF 工程。',
                log: '',
                logTail: [],
                reason: '未找到 CMakeLists.txt，请确认当前目录是标准的 ESP-IDF 工程。'
            };
        }
        try {
            const result = await (0, process_1.spawnCombined)('idf.py', command, {
                cwd: args.projectPath,
                env: { ...process.env, FORCE_COLOR: '0' },
                timeoutMs
            });
            const log = result.output;
            const analysis = await this.monitorAnalyzer.analyze({
                chip: args.chip,
                log,
                elfPath: args.elfPath,
                addr2lineBin: args.addr2lineBin
            });
            return {
                status: 'SUCCESS',
                command: ['idf.py', ...command],
                port: args.port,
                baud: args.baud,
                timeoutMs,
                durationMs: Date.now() - startedAt,
                stage: 'analysis',
                stageSummary: analysis.status === 'NO_PANIC'
                    ? 'flash/monitor 完成，未检测到 panic。'
                    : 'flash/monitor 完成，并已分析 monitor 日志。',
                log,
                logTail: this.extractLogTail(log),
                analysis
            };
        }
        catch (error) {
            const log = error.output || error.stdout || error.stderr || error.message || '';
            const analysis = await this.monitorAnalyzer.analyze({
                chip: args.chip,
                log,
                elfPath: args.elfPath,
                addr2lineBin: args.addr2lineBin
            });
            return {
                status: 'FAILED',
                command: ['idf.py', ...command],
                port: args.port,
                baud: args.baud,
                timeoutMs,
                durationMs: Date.now() - startedAt,
                stage: 'flash_monitor',
                stageSummary: this.buildStageSummary(log, analysis, error),
                log,
                logTail: this.extractLogTail(log),
                analysis,
                failureCategory: this.classifyFailure(error, log),
                reason: this.buildFailureReason(error, log)
            };
        }
    }
    extractLogTail(log) {
        return log
            .replace(/\r\n/g, '\n')
            .split('\n')
            .filter((line) => line.trim().length > 0)
            .slice(-this.logTailLines);
    }
    classifyFailure(error, log) {
        const text = `${error?.message || ''}\n${log}`.toLowerCase();
        if (error?.timedOut || text.includes('timed out')) {
            return 'TIMEOUT';
        }
        if (error?.code === 'ENOENT' || text.includes('command not found')) {
            return 'TOOL_NOT_FOUND';
        }
        if (text.includes('permission denied') || text.includes('access is denied')) {
            return 'PORT_PERMISSION';
        }
        if (text.includes('resource busy') || text.includes('device or resource busy') || text.includes('port is busy')) {
            return 'PORT_BUSY';
        }
        if (text.includes('no such file or directory') || text.includes('could not open port') || text.includes('serial port not found')) {
            return 'PORT_NOT_FOUND';
        }
        return 'UNKNOWN';
    }
    buildFailureReason(error, log) {
        const category = this.classifyFailure(error, log);
        switch (category) {
            case 'TIMEOUT':
                return 'flash/monitor 在限定时间内未结束。请检查设备是否卡在烧录、启动或 monitor 输出阶段。';
            case 'TOOL_NOT_FOUND':
                return '未找到可执行的 idf.py 或相关工具。请先导出 ESP-IDF 环境。';
            case 'PORT_PERMISSION':
                return 'flash/monitor 因串口权限不足而失败。请检查当前用户对串口设备的访问权限。';
            case 'PORT_BUSY':
                return 'flash/monitor 因串口被占用而失败。请关闭其他串口监视器或烧录工具后重试。';
            case 'PORT_NOT_FOUND':
                return 'flash/monitor 未找到目标串口。请确认端口号、线缆和板卡连接状态。';
            default:
                return 'flash/monitor 命令执行失败，请检查串口、权限、工具链环境和板卡连接状态。';
        }
    }
    buildStageSummary(log, analysis, error) {
        const category = this.classifyFailure(error, log);
        if (analysis.status === 'PANIC_DECODED') {
            return 'flash/monitor 执行失败，但已检测并解码 panic。';
        }
        if (analysis.status === 'PANIC_DETECTED') {
            return 'flash/monitor 执行失败，日志中检测到 panic/backtrace 特征。';
        }
        if (category === 'TIMEOUT') {
            return 'flash/monitor 因超时中断。';
        }
        return 'flash/monitor 执行失败。';
    }
}
exports.FlashMonitorManager = FlashMonitorManager;
//# sourceMappingURL=FlashMonitorManager.js.map