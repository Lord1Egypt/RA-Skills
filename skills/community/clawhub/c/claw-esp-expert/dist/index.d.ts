export declare const skillTools: {
    /**
     * 工具：环境巡检与一键安装
     */
    manage_env(args: {
        action: "check" | "install";
        version?: string;
    }): Promise<import("./env").EnvCheckResult | {
        status: "MANUAL_INSTALL_REQUIRED";
        path: string;
        version: string;
        options: {
            github: {
                repository: string;
                commands: string[];
            };
            gitee: {
                repository: string;
                mirrorAssets: string;
                commands: string[];
            };
        };
        suggestion: string;
    }>;
    /**
     * 工具：智能 Demo 导航
     */
    explore_demo(args: {
        query: string;
    }): Promise<{
        status: string;
        reason: string;
        env: import("./env").EnvCheckResult;
        query?: undefined;
        matches?: undefined;
        module?: undefined;
    } | {
        status: string;
        query: string;
        reason: string;
        env?: undefined;
        matches?: undefined;
        module?: undefined;
    } | {
        status: string;
        query: string;
        matches: string[];
        module: import("./search/ProjectNavigator").ModuleBrief;
        reason?: undefined;
        env?: undefined;
    }>;
    /**
     * 工具：官方 Component Registry 组件建议
     */
    resolve_component(args: {
        query: string;
        target?: string;
        manifest?: string;
        manifestPath?: string;
    }): Promise<import("./registry/ComponentRegistry").ResolveComponentResult | {
        manifestUpdate: import("./registry/ComponentManifest").ManifestMergeResult;
        status: "OK" | "NOT_FOUND";
        query: string;
        target?: string;
        suggestion?: import("./registry/ComponentRegistry").ComponentSuggestion;
        candidates?: import("./registry/ComponentRegistry").ComponentSuggestion[];
        reason?: string;
    } | {
        status: string;
        query: string;
        target: string;
        reason: any;
    }>;
    /**
     * 工具：分析分区表与 app 体积溢出建议
     */
    analyze_partitions(args: {
        projectPath: string;
        rawLog?: string;
    }): Promise<import("./build/PartitionAdvisor").PartitionAdvice>;
    /**
     * 工具：Panic 日志解码
     */
    decode_panic(args: {
        chip: string;
        elfPath: string;
        log: string;
        addr2lineBin?: string;
    }): Promise<import("./monitor/PanicDecoder").PanicDecodeResult>;
    /**
     * 工具：分析 monitor 日志并在检测到 panic 时串联解码
     */
    analyze_monitor(args: {
        chip: string;
        log: string;
        elfPath?: string;
        addr2lineBin?: string;
    }): Promise<import("./monitor/MonitorAnalyzer").MonitorAnalysisResult>;
    /**
     * 工具：执行 flash + monitor，并在 panic 时自动分析
     */
    flash_and_monitor(args: {
        projectPath: string;
        chip: string;
        port?: string;
        baud?: number;
        elfPath?: string;
        addr2lineBin?: string;
        timeoutMs?: number;
    }): Promise<import("./monitor/FlashMonitorManager").FlashMonitorResult>;
    /**
     * 工具：最小执行闭环，串联 build -> flash_and_monitor
     */
    execute_project(args: {
        projectPath: string;
        chip: string;
        port?: string;
        baud?: number;
        elfPath?: string;
        addr2lineBin?: string;
    }): Promise<import("./workflow/ExecutionOrchestrator").ExecuteProjectResult>;
    /**
     * 工具：安全构建 (核心闭环)
     */
    safe_build(args: {
        projectPath: string;
        chip?: string;
    }): Promise<{
        status: string;
        reason: string;
        env: import("./env").EnvCheckResult;
        chip?: undefined;
        resolvedChip?: undefined;
        issues?: undefined;
        build?: undefined;
    } | {
        status: string;
        chip: string;
        resolvedChip: string;
        reason: any;
        env?: undefined;
        issues?: undefined;
        build?: undefined;
    } | {
        status: string;
        reason: string;
        chip: string;
        resolvedChip: string;
        issues: import("./build/PinmuxAuditor").AuditResult[];
        env?: undefined;
        build?: undefined;
    } | {
        status: string;
        chip: string;
        resolvedChip: string;
        issues: import("./build/PinmuxAuditor").AuditResult[];
        build: import("./build/AsyncBuildManager").BuildResult;
        reason?: undefined;
        env?: undefined;
    }>;
};
