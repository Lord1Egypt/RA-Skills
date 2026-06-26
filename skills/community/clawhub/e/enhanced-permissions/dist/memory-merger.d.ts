/**
 * Memory Merger System
 * Merges duplicate and related memories
 *
 * Phase 4 Enhancement - Step 2: Auto Organization
 */
import { Memory } from './types';
/**
 * Merge strategy enum
 */
export declare enum MergeStrategy {
    KEEP_BEST = "keep-best",// Keep the one with highest hotness
    KEEP_NEWEST = "keep-newest",// Keep the most recent
    KEEP_OLDEST = "keep-oldest",// Keep the original
    COMBINE = "combine",// Merge content together
    KEEP_SHORTEST = "keep-shortest",// Keep concise version
    KEEP_LONGEST = "keep-longest"
}
/**
 * Merge result interface
 */
export interface MergeResult {
    success: boolean;
    keptId?: string;
    mergedIds?: string[];
    newContent?: string;
    error?: string;
}
/**
 * Memory Merger Class
 *
 * Features:
 * - Multiple merge strategies
 * - Content combination
 * - Tag merging
 * - Version history preservation
 */
export declare class MemoryMerger {
    private memories;
    /**
     * Set memories to work with
     */
    setMemories(memories: Memory[]): void;
    /**
     * Merge duplicate memories
     */
    merge(memoryIds: string[], strategy?: MergeStrategy, userId?: string): MergeResult;
    /**
     * Strategy: Keep the one with highest hotness
     */
    private mergeKeepBest;
    /**
     * Strategy: Keep the most recent
     */
    private mergeKeepNewest;
    /**
     * Strategy: Keep the original (oldest)
     */
    private mergeKeepOldest;
    /**
     * Strategy: Combine content together
     */
    private mergeCombine;
    /**
     * Strategy: Keep the shortest (most concise)
     */
    private mergeKeepShortest;
    /**
     * Strategy: Keep the longest (most detailed)
     */
    private mergeKeepLongest;
    /**
     * Combine multiple contents intelligently
     */
    private combineContents;
    /**
     * Merge two contents intelligently
     */
    private mergeTwoContents;
    /**
     * Simple string similarity
     */
    private similarity;
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
 * Default memory merger instance
 */
export declare const defaultMemoryMerger: MemoryMerger;
//# sourceMappingURL=memory-merger.d.ts.map