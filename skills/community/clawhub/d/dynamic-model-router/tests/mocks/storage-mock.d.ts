/**
 * 存储模块Mock - 用于测试中替代真实的文件系统存储
 */
export declare class MockStorage {
    private initialized;
    initialize(): Promise<void>;
    saveHistoricalPerformance(data: any): Promise<void>;
    loadHistoricalPerformance(limit?: number): Promise<any[]>;
    saveLearningModel(modelId: string, data: any): Promise<void>;
    loadLearningModel(modelId: string): Promise<any | null>;
    getStorageStats(): Promise<any>;
    cleanupOldData(_maxAgeHours?: number): Promise<void>;
    shutdown(): Promise<void>;
    clear(): void;
    getSize(): number;
}
export declare function getMockStorage(): MockStorage;
export default getMockStorage;
//# sourceMappingURL=storage-mock.d.ts.map