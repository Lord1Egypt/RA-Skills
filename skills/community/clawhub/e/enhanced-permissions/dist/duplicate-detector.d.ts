/**
 * Duplicate Detection System
 * Finds and manages duplicate memories
 *
 * Phase 4 Enhancement - Step 2: Auto Organization
 */
import { Memory } from './types';
/**
 * Duplicate pair interface
 */
export interface DuplicatePair {
    id1: string;
    id2: string;
    similarity: number;
    reason: string;
}
/**
 * Duplicate detection options
 */
export interface DuplicateOptions {
    threshold?: number;
    tags?: string[];
    minHotness?: number;
    limit?: number;
    useVectorSimilarity?: boolean;
}
/**
 * Duplicate Detector Class
 *
 * Features:
 * - Text-based similarity (Jaccard, cosine)
 * - Vector-based similarity (if available)
 * - Tag-based filtering
 * - Configurable threshold
 */
export declare class DuplicateDetector {
    private memories;
    /**
     * Set memories to check
     */
    setMemories(memories: Memory[]): void;
    /**
     * Find duplicate memories
     */
    findDuplicates(options?: DuplicateOptions): DuplicatePair[];
    /**
     * Calculate similarity between two memories
     */
    calculateSimilarity(mem1: Memory, mem2: Memory, useVector?: boolean): number;
    /**
     * Calculate cosine similarity for vectors
     */
    private cosineSimilarity;
    /**
     * Calculate text similarity using Jaccard index + word overlap
     */
    private textSimilarity;
    /**
     * Calculate tag similarity
     */
    private tagSimilarity;
    /**
     * Get human-readable reason for similarity
     */
    private getSimilarityReason;
    /**
     * Get statistics about duplicates
     */
    getDuplicateStats(options?: DuplicateOptions): {
        totalMemories: number;
        duplicatePairs: number;
        duplicateMemories: number;
        potentialSavings: number;
        averageSimilarity: number;
    };
    /**
     * Clear memories
     */
    clear(): void;
}
/**
 * Default duplicate detector instance
 */
export declare const defaultDuplicateDetector: DuplicateDetector;
//# sourceMappingURL=duplicate-detector.d.ts.map