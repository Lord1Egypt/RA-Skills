import { type PatchSuggestion } from '../common/PatchSuggestion';
export interface PartitionEntry {
    name: string;
    type: string;
    subtype: string;
    offset?: number;
    size?: number;
    flags?: string;
    lineIndex: number;
    rawLine: string;
}
export interface PartitionAdvice {
    status: 'OK' | 'NO_PARTITION_TABLE' | 'NO_APP_PARTITION' | 'INSUFFICIENT_DATA';
    partitionFile?: string;
    targetPartition?: PartitionEntry;
    appBinarySizeBytes?: number;
    currentPartitionSizeBytes?: number;
    overflowBytes?: number;
    recommendedSizeBytes?: number;
    recommendedSizeHex?: string;
    availableSizeBytes?: number;
    availableSizeHex?: string;
    warning?: string;
    suggestion: string;
    updatedManifest?: string;
    patch?: PatchSuggestion;
}
export declare class PartitionAdvisor {
    private readonly appPartitionAlignment;
    private readonly minimumExtraHeadroom;
    analyzeProject(projectPath: string, rawLog?: string): Promise<PartitionAdvice>;
    private loadPartitionTable;
    private resolvePartitionFile;
    private pickTargetPartition;
    private extractPartitionName;
    private extractNumber;
    private findAvailableSize;
    private buildUpdatedManifest;
    private parseSize;
    private alignToAppBoundary;
    private formatHex;
}
