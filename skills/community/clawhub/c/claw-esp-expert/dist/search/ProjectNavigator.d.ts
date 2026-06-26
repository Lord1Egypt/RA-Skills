export interface ModuleBrief {
    name: string;
    path: string;
    description: string;
    hardwareRequirements: string[];
    treeStructure: string;
}
export declare class ProjectNavigator {
    private idfPath;
    constructor(idfPath: string);
    /**
     * 语义化搜索：根据关键词在 examples 目录中寻找匹配项
     */
    findExamples(query: string): Promise<string[]>;
    /**
     * 核心逻辑：获取模块深度信息 (README 优先)
     */
    getModuleDetails(modulePath: string): Promise<ModuleBrief>;
    /**
     * 寻找 README，支持中英文优先级
     */
    private findReadme;
    /**
     * 提取 README 中的功能摘要 (通常是第一段)
     */
    private extractSummary;
    /**
     * 提取硬件依赖 (寻找 "Hardware Required" 或 "硬件需求" 关键字)
     */
    private extractHardwareInfo;
    /**
     * 生成精简目录树 (深度为2)
     */
    private generateConciseTree;
}
