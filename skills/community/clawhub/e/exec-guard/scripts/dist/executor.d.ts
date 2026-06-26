/**
 * 命令执行器
 * 提供同步和异步两种执行模式，支持超时控制和输出截断
 */
import { ExecRequest, ExecResponse, ProcessStatus, ProcessInfo } from './types';
import { ProcessManager } from './process-manager';
/**
 * 命令执行器
 */
export declare class CommandExecutor {
    private processManager;
    constructor(processManager: ProcessManager);
    /**
     * 执行命令（主入口）
     * 根据请求的 runInBackground 字段决定同步或异步执行
     */
    execute(req: ExecRequest): Promise<ExecResponse>;
    /**
     * 验证请求的合法性
     */
    private validateRequest;
    /**
     * 获取超时时间（带默认值）
     */
    private getTimeout;
    /**
     * 获取监控窗口时长
     */
    private getWatchDuration;
    /**
     * 是否启用了监控窗口
     */
    private hasWatchWindow;
    /**
     * 同步执行命令
     */
    private executeSync;
    /**
     * 后台执行命令
     * 支持监控窗口模式
     */
    private executeBackground;
    /**
     * 带监控窗口的后台执行
     * 等待 watchDuration 秒观察进程状态
     */
    private executeWithWatchWindow;
    /**
     * 获取后台进程状态
     */
    getProcessStatus(pid: number): ProcessStatus;
    /**
     * 获取后台进程完整信息
     */
    getProcessInfo(pid: number): ProcessInfo;
    /**
     * 终止后台进程
     */
    terminateProcess(pid: number): Promise<void>;
    /**
     * 列出所有后台进程
     */
    listProcesses(): ProcessStatus[];
    /**
     * 清理已完成的进程记录
     */
    cleanupCompletedProcesses(): number;
}
//# sourceMappingURL=executor.d.ts.map