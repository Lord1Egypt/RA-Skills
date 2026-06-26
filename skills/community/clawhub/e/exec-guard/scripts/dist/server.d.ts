/**
 * HTTP 服务器
 * 提供 RESTful API 用于远程命令执行
 */
/**
 * HTTP 服务器
 */
export declare class Server {
    private app;
    private executor;
    private port;
    constructor(port?: number, maxProcesses?: number);
    /**
     * 设置中间件
     */
    private setupMiddleware;
    /**
     * 设置路由
     */
    private setupRoutes;
    /**
     * 处理命令执行请求
     */
    private handleExec;
    /**
     * 获取进程状态
     */
    private handleGetProcessStatus;
    /**
     * 获取进程日志
     */
    private handleGetProcessLogs;
    /**
     * 终止进程
     */
    private handleDeleteProcess;
    /**
     * 健康检查
     */
    private handleHealth;
    /**
     * 列出所有进程
     */
    private handleListProcesses;
    /**
     * 启动服务器
     */
    run(): void;
}
/**
 * 创建并启动服务器
 */
export declare function createServer(port?: number, maxProcesses?: number): Server;
//# sourceMappingURL=server.d.ts.map