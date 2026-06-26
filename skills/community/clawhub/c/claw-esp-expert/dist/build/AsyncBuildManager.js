"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.AsyncBuildManager = void 0;
const fs_1 = require("../common/fs");
const path_1 = __importDefault(require("path"));
const PartitionAdvisor_1 = require("./PartitionAdvisor");
const process_1 = require("../common/process");
class AsyncBuildManager {
    constructor() {
        this.partitionAdvisor = new PartitionAdvisor_1.PartitionAdvisor();
    }
    /**
     * 执行异步编译，并实时反馈进度
     */
    async build(projectPath, onProgress) {
        onProgress?.("🔍 正在初始化构建环境...");
        try {
            // 1. 检查 CMakeLists.txt 是否存在
            if (!await (0, fs_1.pathExists)(path_1.default.join(projectPath, 'CMakeLists.txt'))) {
                return { success: false, errorType: 'ENV_ERROR', cleanError: "未找到 CMakeLists.txt，请确认当前目录是标准的 ESP-IDF 工程。" };
            }
            // 2. 启动构建进程并捕获合并输出
            onProgress?.("🚀 启动 idf.py build (此过程可能需要 1-3 分钟)...");
            await (0, process_1.spawnCombined)('idf.py', ['build'], {
                cwd: projectPath,
                env: { ...process.env, FORCE_COLOR: '1' },
                onData: (data) => {
                    const progressMatch = data.match(/\[(\d+)\/(\d+)\]/);
                    if (progressMatch) {
                        const current = parseInt(progressMatch[1]);
                        const total = parseInt(progressMatch[2]);
                        const percent = Math.round((current / total) * 100);
                        if (percent % 10 === 0)
                            onProgress?.(`⚡ 编译进度: ${percent}% (${current}/${total})`);
                    }
                }
            });
            return { success: true };
        }
        catch (error) {
            // 3. 进入“编译现场分析”模式
            return await this.diagnoseError(projectPath, error.output || error.message);
        }
    }
    /**
     * 核心诊断算法：语义化提取错误
     */
    async diagnoseError(projectPath, rawLog) {
        const trimmedRawLog = rawLog.slice(-1200);
        // 模式 A: 分区表溢出 (最常见的初学者错误)
        if (rawLog.includes("is too large")
            || rawLog.includes("app partition is too small for binary")
            || rawLog.includes("overflow")
            || rawLog.includes("section `.flash.app' will not fit in region `iram0_0_seg'")) {
            if (rawLog.includes("iram0_0_seg")
                || rawLog.includes("dram0_0_seg")
                || rawLog.includes("region `iram")
                || rawLog.includes("region `dram")) {
                return {
                    success: false,
                    errorType: 'MEMORY_OVERFLOW',
                    rawError: trimmedRawLog,
                    cleanError: 'IRAM/DRAM 段溢出，说明运行时内存布局超过芯片限制。',
                    suggestion: '请优先检查日志中的 overflow 段，尝试减少静态缓冲区、关闭不必要组件，或将可放入 Flash 的代码/常量移出 IRAM/DRAM。'
                };
            }
            const partitionAdvice = await this.partitionAdvisor.analyzeProject(projectPath, rawLog);
            return {
                success: false,
                errorType: 'PARTITION_OVERFLOW',
                cleanError: partitionAdvice.status === 'OK'
                    ? `程序体积超过了分区表设定的 ${partitionAdvice.targetPartition?.name || 'app'} 限制。`
                    : "程序体积超过了分区表设定的 app 限制。",
                suggestion: partitionAdvice.suggestion,
                partitionAdvice
            };
        }
        // 模式 B: 缺少头文件 / include 依赖
        const missingHeaderMatch = rawLog.match(/fatal error: ([^:]+): No such file or directory/);
        if (missingHeaderMatch) {
            const header = missingHeaderMatch[1].trim();
            return {
                success: false,
                errorType: 'MISSING_HEADER',
                rawError: trimmedRawLog,
                cleanError: `缺少头文件：${header}`,
                suggestion: `请检查该头文件是否来自某个组件但未加入工程依赖。若是第三方/官方组件，请优先使用 resolve_component 查询组件名，并把依赖写入 idf_component.yml 或 CMakeLists.txt。`
            };
        }
        // 模式 C: 组件依赖/解析失败
        const componentErrorMatch = rawLog.match(/Failed to resolve component '([^']+)'(?: required by component '([^']+)')?/);
        if (componentErrorMatch) {
            const missingComponent = componentErrorMatch[1];
            const requiredBy = componentErrorMatch[2];
            return {
                success: false,
                errorType: 'COMPONENT_ERROR',
                rawError: trimmedRawLog,
                cleanError: requiredBy
                    ? `组件依赖解析失败：${requiredBy} 依赖的 ${missingComponent} 未找到。`
                    : `组件依赖解析失败：未找到 ${missingComponent}。`,
                suggestion: `请先确认组件名是否正确，再用 resolve_component 查询官方 Component Registry，并将结果合并到 idf_component.yml。`
            };
        }
        // 模式 D: SDK 配置缺失 / CONFIG_* 宏未定义
        const configErrorMatch = rawLog.match(/error: ['"]?(CONFIG_[A-Z0-9_]+)['"]? undeclared/);
        if (configErrorMatch) {
            return {
                success: false,
                errorType: 'CONFIG_ERROR',
                rawError: trimmedRawLog,
                cleanError: `配置宏未定义：${configErrorMatch[1]}`,
                suggestion: '请检查 menuconfig / sdkconfig.defaults 是否启用了对应配置项；如果该配置来自某个组件，也请确认组件依赖已经正确接入。'
            };
        }
        // 模式 E: 标准 C 语法错误 (提取文件名和行号)
        const cErrorMatch = rawLog.match(/(.+\.[ch]):(\d+):(\d+): (error: .+)($|\n)/);
        if (cErrorMatch) {
            return {
                success: false,
                errorType: 'COMPILATION_ERROR',
                rawError: trimmedRawLog,
                cleanError: `代码错误: 在 ${path_1.default.basename(cErrorMatch[1])} 的第 ${cErrorMatch[2]} 行发生 [${cErrorMatch[4]}]`,
                suggestion: "请 AI 检查该行代码逻辑，通常是缺少分号、头文件未包含或变量名拼写错误。"
            };
        }
        // 模式 F: 链接错误 (组件依赖丢失)
        if (rawLog.includes("undefined reference to")) {
            return {
                success: false,
                errorType: 'LINK_ERROR',
                rawError: trimmedRawLog,
                cleanError: "符号引用未定义（链接失败）。",
                suggestion: "这通常是因为在 CMakeLists.txt 的 PRIV_REQUIRES 中漏掉了必要的组件库。请检查是否引入了对应的驱动组件。"
            };
        }
        return {
            success: false,
            errorType: 'COMPILATION_ERROR',
            rawError: trimmedRawLog,
            cleanError: "未识别的编译错误，请参考原始日志末尾。"
        };
    }
}
exports.AsyncBuildManager = AsyncBuildManager;
//# sourceMappingURL=AsyncBuildManager.js.map