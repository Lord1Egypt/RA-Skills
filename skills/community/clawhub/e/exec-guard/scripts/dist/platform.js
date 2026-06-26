"use strict";
/**
 * 跨平台命令构建
 * 根据不同操作系统包装命令，确保跨平台兼容性
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
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.buildCommand = buildCommand;
exports.validateWorkingDir = validateWorkingDir;
exports.killProcess = killProcess;
exports.getShellCommand = getShellCommand;
exports.getPlatform = getPlatform;
const child_process_1 = require("child_process");
const fs = __importStar(require("fs"));
const os = __importStar(require("os"));
const tree_kill_1 = __importDefault(require("tree-kill"));
const constants_1 = require("./constants");
/**
 * 构建跨平台命令
 * Windows: 使用 cmd.exe /c <command>
 * Linux/macOS: 使用 bash -c "<command>"
 */
function buildCommand(command, workingDir, env) {
    const platform = os.platform();
    let shell;
    let shellArgs;
    if (platform === 'win32') {
        shell = 'cmd.exe';
        shellArgs = ['/c', command];
    }
    else {
        shell = 'bash';
        shellArgs = ['-c', command];
    }
    // 合并环境变量（继承宿主机 + 自定义覆盖）
    const mergedEnv = { ...process.env, ...env };
    // 确定工作目录
    const cwd = workingDir || process.cwd();
    // 创建子进程
    const childProcess = (0, child_process_1.spawn)(shell, shellArgs, {
        cwd,
        env: mergedEnv,
        // Windows 和 Unix 都需要设置进程组以便统一杀死
        windowsHide: true,
        detached: platform !== 'win32', // Unix 上创建独立进程组
    });
    return childProcess;
}
/**
 * 验证工作目录
 */
function validateWorkingDir(dir) {
    if (!fs.existsSync(dir)) {
        throw new constants_1.InvalidWorkingDirError(dir);
    }
    const stats = fs.statSync(dir);
    if (!stats.isDirectory()) {
        throw new constants_1.InvalidWorkingDirError(`${dir} is not a directory`);
    }
}
/**
 * 杀死进程及其所有子进程
 * 使用 tree-kill 实现跨平台进程终止
 */
function killProcess(childProcess) {
    if (!childProcess || !childProcess.pid) {
        return Promise.resolve();
    }
    return new Promise((resolve, reject) => {
        (0, tree_kill_1.default)(childProcess.pid, 'SIGKILL', (err) => {
            if (err) {
                // 尝试直接杀死进程
                try {
                    childProcess.kill('SIGKILL');
                    resolve();
                }
                catch (killErr) {
                    reject(killErr);
                }
            }
            else {
                resolve();
            }
        });
    });
}
/**
 * 获取当前平台的 shell 命令格式
 */
function getShellCommand() {
    const platform = os.platform();
    if (platform === 'win32') {
        return 'cmd.exe /c';
    }
    return 'bash -c';
}
/**
 * 获取平台名称
 */
function getPlatform() {
    const platform = os.platform();
    if (platform === 'win32')
        return 'windows';
    if (platform === 'linux')
        return 'linux';
    if (platform === 'darwin')
        return 'macos';
    return 'other';
}
//# sourceMappingURL=platform.js.map