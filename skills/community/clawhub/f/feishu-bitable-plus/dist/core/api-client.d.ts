/**
 * 飞书API客户端
 * Feishu API Client with intelligent caching and retry
 */
import { BitableMeta, FieldMeta, BitableRecord, QueryOptions, OperationResult, AppConfig } from '../types';
export declare class FeishuApiClient {
    private client;
    private cache;
    private config;
    private tenantAccessToken;
    private tokenExpireTime;
    constructor(config: AppConfig);
    /**
     * 获取租户访问令牌
     */
    private getTenantAccessToken;
    /**
     * API错误处理
     */
    private handleApiError;
    private sleep;
    /**
     * 带重试的API请求
     */
    private requestWithRetry;
    private isRetryableError;
    /**
     * 获取多维表格元数据
     */
    getBitableMeta(appToken: string): Promise<OperationResult<BitableMeta>>;
    /**
     * 获取表格字段列表
     */
    getTableFields(appToken: string, tableId: string): Promise<OperationResult<FieldMeta[]>>;
    /**
     * 查询记录列表
     */
    listRecords(appToken: string, tableId: string, options?: QueryOptions): Promise<OperationResult<{
        records: BitableRecord[];
        hasMore: boolean;
        pageToken?: string;
    }>>;
    /**
     * 获取单条记录
     */
    getRecord(appToken: string, tableId: string, recordId: string): Promise<OperationResult<BitableRecord>>;
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
     * 清除缓存
     */
    clearCache(): void;
}
//# sourceMappingURL=api-client.d.ts.map