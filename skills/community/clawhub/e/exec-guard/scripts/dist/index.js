"use strict";
/**
 * exec-guard - AI Agent Command Execution Module
 * 主入口文件
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.printUsage = exports.runCLI = exports.createServer = exports.Server = exports.getPlatform = exports.getShellCommand = exports.killProcess = exports.validateWorkingDir = exports.buildCommand = exports.ProcessManager = exports.CommandExecutor = exports.createRingBuffer = exports.RingBuffer = void 0;
const server_1 = require("./server");
const cli_1 = require("./cli");
const constants_1 = require("./constants");
// 导出核心模块
var ringbuf_1 = require("./ringbuf");
Object.defineProperty(exports, "RingBuffer", { enumerable: true, get: function () { return ringbuf_1.RingBuffer; } });
Object.defineProperty(exports, "createRingBuffer", { enumerable: true, get: function () { return ringbuf_1.createRingBuffer; } });
var executor_1 = require("./executor");
Object.defineProperty(exports, "CommandExecutor", { enumerable: true, get: function () { return executor_1.CommandExecutor; } });
var process_manager_1 = require("./process-manager");
Object.defineProperty(exports, "ProcessManager", { enumerable: true, get: function () { return process_manager_1.ProcessManager; } });
var platform_1 = require("./platform");
Object.defineProperty(exports, "buildCommand", { enumerable: true, get: function () { return platform_1.buildCommand; } });
Object.defineProperty(exports, "validateWorkingDir", { enumerable: true, get: function () { return platform_1.validateWorkingDir; } });
Object.defineProperty(exports, "killProcess", { enumerable: true, get: function () { return platform_1.killProcess; } });
Object.defineProperty(exports, "getShellCommand", { enumerable: true, get: function () { return platform_1.getShellCommand; } });
Object.defineProperty(exports, "getPlatform", { enumerable: true, get: function () { return platform_1.getPlatform; } });
var server_2 = require("./server");
Object.defineProperty(exports, "Server", { enumerable: true, get: function () { return server_2.Server; } });
Object.defineProperty(exports, "createServer", { enumerable: true, get: function () { return server_2.createServer; } });
var cli_2 = require("./cli");
Object.defineProperty(exports, "runCLI", { enumerable: true, get: function () { return cli_2.runCLI; } });
Object.defineProperty(exports, "printUsage", { enumerable: true, get: function () { return cli_2.printUsage; } });
// 导出类型
__exportStar(require("./types"), exports);
// 导出常量
__exportStar(require("./constants"), exports);
/**
 * 解析命令行参数
 */
function parseArgs() {
    const args = process.argv.slice(2);
    let server = false;
    let port = constants_1.DEFAULT_HTTP_PORT;
    let maxProcesses = constants_1.DEFAULT_MAX_PROCESSES;
    let help = false;
    for (let i = 0; i < args.length; i++) {
        const arg = args[i];
        if (arg === '-h' || arg === '--help') {
            help = true;
        }
        else if (arg === '--server') {
            server = true;
        }
        else if (arg === '--port') {
            const nextArg = args[i + 1];
            if (nextArg) {
                port = parseInt(nextArg, 10);
                i++;
            }
        }
        else if (arg === '--max-processes') {
            const nextArg = args[i + 1];
            if (nextArg) {
                maxProcesses = parseInt(nextArg, 10);
                i++;
            }
        }
    }
    return { server, port, maxProcesses, help };
}
/**
 * 主函数
 */
async function main() {
    const { server, port, maxProcesses, help } = parseArgs();
    if (help) {
        (0, cli_1.printUsage)();
        return;
    }
    if (server) {
        // HTTP 服务器模式
        const srv = (0, server_1.createServer)(port, maxProcesses);
        srv.run();
    }
    else {
        // CLI 模式
        await (0, cli_1.runCLI)();
    }
}
// 运行主函数
main().catch((err) => {
    console.error(`Error: ${err.message}`);
    process.exit(1);
});
//# sourceMappingURL=index.js.map