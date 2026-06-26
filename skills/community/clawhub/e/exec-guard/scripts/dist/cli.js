"use strict";
/**
 * CLI 模式
 * 从 stdin 读取 JSON 请求，执行命令，输出 JSON 响应
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.runCLI = runCLI;
exports.printUsage = printUsage;
const executor_1 = require("./executor");
const process_manager_1 = require("./process-manager");
const constants_1 = require("./constants");
/**
 * CLI 执行器
 */
async function runCLI() {
    // 从 stdin 读取 JSON 请求
    const input = await readStdin();
    let req;
    try {
        req = JSON.parse(input);
    }
    catch (err) {
        const response = {
            status: 'failed',
            exitCode: -1,
            stdout: '',
            stderr: '',
            systemMessage: `failed to parse input JSON: ${err.message}`,
        };
        console.log(JSON.stringify(response));
        return;
    }
    // 创建执行器
    const processManager = new process_manager_1.ProcessManager(constants_1.DEFAULT_MAX_PROCESSES);
    const executor = new executor_1.CommandExecutor(processManager);
    // 执行命令
    try {
        const response = await executor.execute(req);
        console.log(JSON.stringify(response));
    }
    catch (err) {
        const response = {
            status: 'failed',
            exitCode: -1,
            stdout: '',
            stderr: '',
            systemMessage: err.message,
        };
        console.log(JSON.stringify(response));
    }
}
/**
 * 从 stdin 读取全部内容
 */
async function readStdin() {
    return new Promise((resolve, reject) => {
        let data = '';
        process.stdin.setEncoding('utf8');
        process.stdin.on('data', (chunk) => {
            data += chunk;
        });
        process.stdin.on('end', () => {
            resolve(data);
        });
        process.stdin.on('error', (err) => {
            reject(err);
        });
    });
}
/**
 * 打印帮助信息
 */
function printUsage() {
    console.log(`
exec-guard - AI Agent Command Execution Tool

Usage:
  exec-guard [options]

Modes:
  CLI Mode (default): Read JSON from stdin, execute command, output JSON result
  Server Mode (--server): Start HTTP server for remote command execution

Options:
  -h, --help       Show this help message
  --server         Run in HTTP server mode
  --port <number>  HTTP server port (default: 8080)
  --max-processes  Maximum number of background processes (default: 100)

Examples:
  # CLI Mode - execute command from stdin
  echo '{"command": "echo hello"}' | exec-guard

  # Server Mode - start HTTP server on port 8080
  exec-guard --server --port 8080

API Endpoints (Server Mode):
  POST   /exec              Execute command
  GET    /process/:pid      Get process status
  GET    /process/:pid/logs Get process logs
  DELETE /process/:pid      Terminate process
  GET    /processes         List all processes
  GET    /health            Health check

Request Format:
  {
    "command": "string, required - system command to execute",
    "workingDir": "string, optional - working directory",
    "timeoutSeconds": "number, optional - timeout in seconds (default: 30)",
    "runInBackground": "boolean, optional - run in background (default: false)",
    "watchDurationSeconds": "number, optional - watch window duration for background mode",
    "env": "object, optional - custom environment variables"
  }

Response Format:
  {
    "status": "success/failed/timeout/killed/running",
    "exitCode": "number - process exit code",
    "stdout": "string - standard output (Head-Tail buffered)",
    "stderr": "string - standard error (Head-Tail buffered)",
    "systemMessage": "string - system message"
  }
`);
}
//# sourceMappingURL=cli.js.map