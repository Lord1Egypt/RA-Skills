/**
 * 后台进程管理器
 * 提供线程安全的进程注册、查询、终止功能
 */
import { ChildProcess } from 'child_process';
import { BackgroundProcess, ProcessStatus, ProcessInfo } from './types';
import { RingBuffer } from './ringbuf';
/**
 * 后台进程扩展结构（包含 RingBuffer）
 */
interface ManagedProcess extends BackgroundProcess {
    stdoutBuffer: RingBuffer;
    stderrBuffer: RingBuffer;
    childProcess: ChildProcess;
    cancelCallback?: () => void;
}
/**
 * 进程管理器
 */
export declare class ProcessManager {
    private processes;
    private readonly maxProcesses;
    constructor(maxProcesses?: number);
    /**
     * 注册新的后台进程
     */
    register(pid: number, command: string, childProcess: ChildProcess, cancelCallback?: () => void): ManagedProcess;
    /**
     * 获取进程信息
     */
    get(pid: number): ManagedProcess | undefined;
    /**
     * 获取进程状态
     */
    getStatus(pid: number): ProcessStatus;
    /**
     * 获取进程完整信息（含输出）
     */
    getProcessInfo(pid: number): ProcessInfo;
    /**
     * 终止进程
     */
    terminate(pid: number): Promise<void>;
    /**
     * 移除进程记录
     */
    remove(pid: number): void;
    /**
     * 清理已完成的进程记录
     */
    cleanupCompleted(): number;
    /**
     * 列出所有进程
     */
    list(): ProcessStatus[];
    /**
     * 获取进程数量
     */
    size(): number;
    /**
     * 更新进程状态
     */
    updateStatus(pid: number, updates: Partial<ManagedProcess>): void;
    /**
     * 获取进程的 stdout Buffer
     */
    getStdoutBuffer(pid: number): RingBuffer | undefined;
    /**
     * 获取进程的 stderr Buffer
     */
    getStderrBuffer(pid: number): RingBuffer | undefined;
}
export {};
//# sourceMappingURL=process-manager.d.ts.map