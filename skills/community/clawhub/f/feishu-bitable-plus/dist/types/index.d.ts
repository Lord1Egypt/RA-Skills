/**
 * 核心类型定义
 * Core Type Definitions
 */
export interface FeishuResponse<T = any> {
    code: number;
    msg: string;
    data?: T;
}
export interface BitableMeta {
    app_token: string;
    name: string;
    description?: string;
    tables: TableMeta[];
}
export interface TableMeta {
    table_id: string;
    name: string;
    description?: string;
    fields: FieldMeta[];
}
export interface FieldMeta {
    field_id: string;
    field_name: string;
    type: FieldType;
    property?: FieldProperty;
}
export type FieldType = 1 | 2 | 3 | 4 | 5 | 7 | 11 | 13 | 15 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 1001 | 1002 | 1003 | 1004 | 1005;
export interface FieldProperty {
    options?: FieldOption[];
    formatter?: string;
    date_formatter?: string;
    auto_fill?: boolean;
}
export interface FieldOption {
    id?: string;
    name: string;
    color?: number;
}
export interface BitableRecord {
    record_id: string;
    fields: RecordFields;
    created_time?: number;
    updated_time?: number;
}
export interface RecordFields {
    [key: string]: any;
}
export interface QueryCondition {
    field: string;
    operator: 'equals' | 'notEquals' | 'contains' | 'notContains' | 'greaterThan' | 'lessThan' | 'greaterThanOrEqual' | 'lessThanOrEqual' | 'isEmpty' | 'isNotEmpty';
    value?: any;
}
export interface QueryOptions {
    conditions?: QueryCondition[];
    filter?: string;
    sort?: SortOption[];
    pageSize?: number;
    pageToken?: string;
}
export interface SortOption {
    field: string;
    order: 'asc' | 'desc';
}
export interface OperationResult<T = any> {
    success: boolean;
    data?: T;
    error?: ErrorInfo;
    meta?: OperationMeta;
}
export interface ErrorInfo {
    code: string;
    message: string;
    details?: any;
}
export interface OperationMeta {
    duration: number;
    affectedRows?: number;
    pageToken?: string;
    hasMore?: boolean;
}
export interface IntentResult {
    intent: IntentType;
    confidence: number;
    entities: IntentEntities;
    originalText: string;
}
export type IntentType = 'LIST_RECORDS' | 'GET_RECORD' | 'CREATE_RECORD' | 'UPDATE_RECORD' | 'DELETE_RECORD' | 'BATCH_CREATE' | 'BATCH_UPDATE' | 'BATCH_DELETE' | 'SYNC_TABLES' | 'GENERATE_REPORT' | 'ANALYZE_DATA' | 'UNKNOWN';
export interface IntentEntities {
    tableName?: string;
    tableId?: string;
    recordId?: string;
    conditions?: QueryCondition[];
    data?: RecordFields;
    fields?: string[];
    targetTable?: string;
    reportType?: string;
    [key: string]: any;
}
export interface Workflow {
    id: string;
    name: string;
    trigger: WorkflowTrigger;
    actions: WorkflowAction[];
    enabled: boolean;
    createdAt: Date;
    updatedAt: Date;
}
export interface WorkflowTrigger {
    type: 'schedule' | 'webhook' | 'manual';
    config: ScheduleConfig | WebhookConfig | ManualConfig;
}
export interface ScheduleConfig {
    cron: string;
    timezone?: string;
}
export interface WebhookConfig {
    tableId: string;
    event: 'record_created' | 'record_updated' | 'record_deleted';
}
export interface ManualConfig {
    description?: string;
}
export interface WorkflowAction {
    type: 'create_record' | 'update_record' | 'delete_record' | 'send_message' | 'export_data' | 'webhook';
    config: any;
}
export interface AppConfig {
    feishu: {
        appId: string;
        appSecret: string;
        baseUrl?: string;
    };
    cache: {
        ttl: number;
        checkperiod: number;
    };
    retry: {
        maxRetries: number;
        delay: number;
    };
}
//# sourceMappingURL=index.d.ts.map