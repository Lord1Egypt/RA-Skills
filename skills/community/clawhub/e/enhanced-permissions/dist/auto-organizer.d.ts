/**
 * Auto Organizer System
 * Automatically organizes memories
 *
 * Phase 4 Enhancement - Step 2: Auto Organization
 */
import { Memory } from './types';
import { MergeStrategy } from './memory-merger';
/**
 * Auto organize options
 */
export interface AutoOrganizeOptions {
    mergeDuplicates?: boolean;
    mergeThreshold?: number;
    mergeStrategy?: MergeStrategy;
    autoTag?: boolean;
    markOutdated?: boolean;
    outdatedAge?: number;
    summarizeRelated?: boolean;
    dryRun?: boolean;
}
/**
 * Auto organize result
 */
export interface AutoOrganizeResult {
    success: boolean;
    duplicatesFound: number;
    duplicatesMerged: number;
    memoriesTagged: number;
    memoriesMarkedOutdated: number;
    summariesCreated: number;
    changes: string[];
    error?: string;
}
/**
 * Auto Organizer Class
 *
 * Features:
 * - Automatic duplicate detection and merging
 * - Auto-tagging of untagged memories
 * - Outdated memory detection
 * - Related memory summarization
 * - Dry run mode
 */
export declare class AutoOrganizer {
    private duplicateDetector;
    private memoryMerger;
    private memories;
    constructor();
    /**
     * Set memories to organize
     */
    setMemories(memories: Memory[]): void;
    /**
     * Run auto organization
     */
    autoOrganize(options?: AutoOrganizeOptions): Promise<AutoOrganizeResult>;
    /**
     * Handle duplicate detection and merging
     */
    private handleDuplicates;
    /**
     * Auto-tag untagged memories
     */
    private autoTagUntagged;
    /**
     * Suggest tags based on content
     */
    private suggestTags;
    /**
     * Mark outdated memories
     */
    private markOutdatedMemories;
    /**
     * Summarize related memories
     */
    private summarizeRelatedMemories;
    /**
     * Get memories
     */
    getMemories(): Memory[];
    /**
     * Clear memories
     */
    clear(): void;
}
/**
 * Default auto organizer instance
 */
export declare const defaultAutoOrganizer: AutoOrganizer;
//# sourceMappingURL=auto-organizer.d.ts.map