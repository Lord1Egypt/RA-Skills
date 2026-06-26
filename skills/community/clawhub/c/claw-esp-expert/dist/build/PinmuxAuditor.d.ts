export interface AuditResult {
    level: 'INFO' | 'WARNING' | 'CRITICAL' | 'FATAL';
    pin?: number;
    file?: string;
    line?: number;
    evidence?: string;
    message: string;
    suggestion: string;
}
export declare class PinmuxAuditor {
    private rules;
    private readonly maxAuditPin;
    private readonly chipAliasRules;
    resolveChipTarget(target?: string): string;
    /**
     * 加载对应芯片的物理规则库
     */
    loadSocRules(target?: string): Promise<void>;
    /**
     * 核心审计函数：对源码进行静态扫描
     */
    auditSourceCode(projectPath: string): Promise<AuditResult[]>;
    /**
     * 规则 1：拦截对内部 Flash/PSRAM 引脚的操作 (FATAL)
     */
    private checkFlashPins;
    /**
     * 规则 2：检查 Input-Only 引脚是否被误设为输出 (ERROR)
     */
    private checkInputOnlyPins;
    /**
     * 规则 3：Strapping 引脚风险评估 (WARNING)
     */
    private checkStrappingPins;
    /**
     * 规则 4：ADC2 与 Wi-Fi 冲突审计 (CRITICAL)
     */
    private checkAdc2WifiConflict;
    /**
     * 工具函数：从源码中提取更丰富的 GPIO 引用方式
     */
    private collectPinOccurrences;
    private buildSymbolTable;
    private extractPinsFromLine;
    private extractSymbolDefinitions;
    private isSymbolDefinitionLine;
    private resolvePinExpression;
    private looksLikePinRelatedIdentifier;
    private isOutputContext;
    private isAdcContext;
    private getSnippet;
    private findFirstOccurrence;
    private dedupeResults;
    private getFiles;
}
