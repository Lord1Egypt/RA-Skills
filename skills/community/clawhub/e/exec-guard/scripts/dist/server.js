"use strict";
/**
 * HTTP 服务器
 * 提供 RESTful API 用于远程命令执行
 */
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.Server = void 0;
exports.createServer = createServer;
const express_1 = __importDefault(require("express"));
const executor_1 = require("./executor");
const process_manager_1 = require("./process-manager");
const constants_1 = require("./constants");
/**
 * HTTP 服务器
 */
class Server {
    app;
    executor;
    port;
    constructor(port = constants_1.DEFAULT_HTTP_PORT, maxProcesses = constants_1.DEFAULT_MAX_PROCESSES) {
        this.port = port;
        this.app = (0, express_1.default)();
        const processManager = new process_manager_1.ProcessManager(maxProcesses);
        this.executor = new executor_1.CommandExecutor(processManager);
        this.setupMiddleware();
        this.setupRoutes();
    }
    /**
     * 设置中间件
     */
    setupMiddleware() {
        this.app.use(express_1.default.json());
        this.app.use(express_1.default.urlencoded({ extended: true }));
    }
    /**
     * 设置路由
     */
    setupRoutes() {
        // 执行命令
        this.app.post('/exec', this.handleExec.bind(this));
        // 进程管理
        this.app.get('/process/:pid', this.handleGetProcessStatus.bind(this));
        this.app.get('/process/:pid/logs', this.handleGetProcessLogs.bind(this));
        this.app.delete('/process/:pid', this.handleDeleteProcess.bind(this));
        // 健康检查
        this.app.get('/health', this.handleHealth.bind(this));
        // 列出所有进程
        this.app.get('/processes', this.handleListProcesses.bind(this));
    }
    /**
     * 处理命令执行请求
     */
    async handleExec(req, res) {
        try {
            const execReq = req.body;
            if (!execReq.command) {
                res.status(400).json({ error: 'command is required' });
                return;
            }
            const response = await this.executor.execute(execReq);
            res.json(response);
        }
        catch (err) {
            const error = err;
            res.status(400).json({ error: error.message });
        }
    }
    /**
     * 获取进程状态
     */
    handleGetProcessStatus(req, res) {
        try {
            const pid = parseInt(req.params.pid, 10);
            if (isNaN(pid)) {
                res.status(400).json({ error: 'invalid PID' });
                return;
            }
            const status = this.executor.getProcessStatus(pid);
            res.json(status);
        }
        catch (err) {
            const error = err;
            if (error instanceof constants_1.ProcessNotFoundError) {
                res.status(404).json({ error: error.message });
            }
            else {
                res.status(500).json({ error: error.message });
            }
        }
    }
    /**
     * 获取进程日志
     */
    handleGetProcessLogs(req, res) {
        try {
            const pid = parseInt(req.params.pid, 10);
            if (isNaN(pid)) {
                res.status(400).json({ error: 'invalid PID' });
                return;
            }
            const info = this.executor.getProcessInfo(pid);
            res.json(info);
        }
        catch (err) {
            const error = err;
            if (error instanceof constants_1.ProcessNotFoundError) {
                res.status(404).json({ error: error.message });
            }
            else {
                res.status(500).json({ error: error.message });
            }
        }
    }
    /**
     * 终止进程
     */
    async handleDeleteProcess(req, res) {
        try {
            const pid = parseInt(req.params.pid, 10);
            if (isNaN(pid)) {
                res.status(400).json({ error: 'invalid PID' });
                return;
            }
            await this.executor.terminateProcess(pid);
            res.json({
                status: 'success',
                message: `process ${pid} terminated`,
            });
        }
        catch (err) {
            const error = err;
            if (error instanceof constants_1.ProcessNotFoundError) {
                res.status(404).json({ error: error.message });
            }
            else {
                res.status(500).json({ error: error.message });
            }
        }
    }
    /**
     * 健康检查
     */
    handleHealth(req, res) {
        const response = { status: 'healthy' };
        res.json(response);
    }
    /**
     * 列出所有进程
     */
    handleListProcesses(req, res) {
        const processes = this.executor.listProcesses();
        res.json(processes);
    }
    /**
     * 启动服务器
     */
    run() {
        this.app.listen(this.port, () => {
            console.log(`exec-guard server running on port ${this.port}`);
            console.log(`API endpoints:`);
            console.log(`  POST   /exec              Execute command`);
            console.log(`  GET    /process/:pid      Get process status`);
            console.log(`  GET    /process/:pid/logs Get process logs`);
            console.log(`  DELETE /process/:pid      Terminate process`);
            console.log(`  GET    /processes         List all processes`);
            console.log(`  GET    /health            Health check`);
        });
    }
}
exports.Server = Server;
/**
 * 创建并启动服务器
 */
function createServer(port, maxProcesses) {
    return new Server(port, maxProcesses);
}
//# sourceMappingURL=server.js.map