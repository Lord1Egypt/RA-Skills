/**
 * 跨平台命令构建
 * 根据不同操作系统包装命令，确保跨平台兼容性
 */
import { ChildProcess } from 'child_process';
/**
 * 构建跨平台命令
 * Windows: 使用 cmd.exe /c <command>
 * Linux/macOS: 使用 bash -c "<command>"
 */
export declare function buildCommand(command: string, workingDir?: string, env?: Record<string, string>): ChildProcess;
/**
 * 验证工作目录
 */
export declare function validateWorkingDir(dir: string): void;
/**
 * 杀死进程及其所有子进程
 * 使用 tree-kill 实现跨平台进程终止
 */
export declare function killProcess(childProcess: ChildProcess | null): Promise<void>;
/**
 * 获取当前平台的 shell 命令格式
 */
export declare function getShellCommand(): string;
/**
 * 获取平台名称
 */
export declare function getPlatform(): 'windows' | 'linux' | 'macos' | 'other';
//# sourceMappingURL=platform.d.ts.map