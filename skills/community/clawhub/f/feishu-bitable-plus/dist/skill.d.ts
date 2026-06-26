/**
 * FeishuBitable-Plus 技能核心
 * Main Skill Coordinator
 */
import { OperationResult, TableMeta, BitableRecord, QueryOptions } from './types';
interface ExecuteOptions {
    appToken?: string;
    tableId?: string;
}
export declare class FeishuBitableSkill {
    private client;
    private intentEngine;
    private configManager;
    private isInitialized;
    constructor();
    /**
     * 初始化技能
     */
    initialize(): Promise<void>;
    /**
     * 执行自然语言命令
     */
    executeNaturalLanguage(text: string, options?: ExecuteOptions): Promise<OperationResult<any>>;
    /**
     * 根据意图执行操作
     */
    private executeByIntent;
    /**
     * 根据表名查找表格
     */
    private findTableByName;
    /**
     * 列出所有表格
     */
    listTables(appToken: string): Promise<OperationResult<TableMeta[]>>;
    /**
     * 列出记录
     */
    listRecords(appToken: string, tableId: string, options?: QueryOptions): Promise<OperationResult<{
        records: BitableRecord[];
        hasMore: boolean;
        pageToken?: string;
    }>>;
    /**
     * 创建记录
     */
    createRecord(appToken: string, tableId: string, fields: Record<string, any>): Promise<OperationResult<BitableRecord>>;
    /**
     * 更新记录
     */
    updateRecord(appToken: string, tableId: string, recordId: string, fields: Record<string, any>): Promise<OperationResult<BitableRecord>>;
    /**
     * 删除记录
     */
    deleteRecord(appToken: string, tableId: string, recordId: string): Promise<OperationResult<void>>;
    /**
     * 批量创建记录
     */
    batchCreateRecords(appToken: string, tableId: string, records: Array<{
        fields: Record<string, any>;
    }>): Promise<OperationResult<{
        records: BitableRecord[];
    }>>;
    /**
     * 同步两个表格
     */
    private syncTables;
    /**
     * 生成报表
     */
    private generateReport;
    /**
     * 生成汇总统计
     */
    private generateSummaryStats;
    /**
     * 生成分布统计
     */
    private generateDistributionStats;
    /**
     * 数据分析
     */
    private analyzeData;
    /**
     * 推断字段类型
     */
    private inferFieldType;
}
export {};
//# sourceMappingURL=skill.d.ts.map