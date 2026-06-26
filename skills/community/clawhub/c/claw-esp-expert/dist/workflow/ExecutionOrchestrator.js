"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ExecutionOrchestrator = void 0;
class ExecutionOrchestrator {
    constructor(auditor, builder, flashMonitorManager) {
        this.auditor = auditor;
        this.builder = builder;
        this.flashMonitorManager = flashMonitorManager;
    }
    async execute(args) {
        const resolvedChip = this.auditor.resolveChipTarget(args.chip);
        await this.auditor.loadSocRules(args.chip);
        const issues = await this.auditor.auditSourceCode(args.projectPath);
        const fatalIssues = issues.filter((item) => item.level === 'FATAL' || item.level === 'CRITICAL');
        if (fatalIssues.length > 0) {
            return {
                status: 'REJECTED',
                chip: args.chip,
                resolvedChip,
                issues: fatalIssues,
                summary: '硬件物理规则冲突，已在构建前拦截。'
            };
        }
        args.onProgress?.('build:start');
        const build = await this.builder.build(args.projectPath, args.onProgress);
        if (!build.success) {
            return {
                status: 'BUILD_FAILED',
                chip: args.chip,
                resolvedChip,
                issues,
                build,
                summary: build.cleanError || '构建失败。'
            };
        }
        args.onProgress?.('flash_monitor:start');
        const flashMonitor = await this.flashMonitorManager.run({
            projectPath: args.projectPath,
            chip: args.chip,
            port: args.port,
            baud: args.baud,
            elfPath: args.elfPath,
            addr2lineBin: args.addr2lineBin
        });
        if (flashMonitor.status !== 'SUCCESS') {
            return {
                status: 'FLASH_FAILED',
                chip: args.chip,
                resolvedChip,
                issues,
                build,
                flashMonitor,
                summary: flashMonitor.reason || flashMonitor.analysis?.suggestion || 'flash/monitor 执行失败。'
            };
        }
        return {
            status: 'SUCCESS',
            chip: args.chip,
            resolvedChip,
            issues,
            build,
            flashMonitor,
            summary: flashMonitor.analysis?.suggestion || '构建、烧录与 monitor 执行完成。'
        };
    }
}
exports.ExecutionOrchestrator = ExecutionOrchestrator;
//# sourceMappingURL=ExecutionOrchestrator.js.map