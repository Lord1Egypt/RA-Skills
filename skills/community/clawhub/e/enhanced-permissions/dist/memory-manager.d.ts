/**
 * Memory Manager with Hotness Scoring
 * Based on Claw Code memory system
 */
import { Memory, MemoryEvent, RecallOptions } from './types';
import { AutoOrganizeOptions, AutoOrganizeResult } from './auto-organizer';
import { DuplicateOptions, DuplicatePair } from './duplicate-detector';
import { MergeStrategy, MergeResult } from './memory-merger';
import { ConversationContext, Message, AnalysisOptions } from './conversation-analyzer';
import { MemorySuggestion, SuggestionOptions } from './suggestion-generator';
import { TriggerConfig } from './suggestion-trigger';
/**
 * Calculate hotness change for an event
 */
export declare function getHotnessDelta(event: MemoryEvent): number;
/**
 * Calculate decayed hotness based on age
 * Formula: baseHotness * (0.99 ^ ageInDays)
 */
export declare function calculateDecayedHotness(baseHotness: number, ageInDays: number): number;
/**
 * Check if a memory should be archived
 */
export declare function shouldArchive(memory: Memory): boolean;
/**
 * Check if a memory is eligible for recall
 */
export declare function isEligibleForRecall(memory: Memory): boolean;
/**
 * Memory Manager Class
 *
 * Features:
 * - Hotness scoring and decay
 * - Automatic archival
 * - Smart recall based on relevance
 * - Vector search integration (optional)
 *
 * Usage:
 * ```typescript
 * const memoryManager = new MemoryManager();
 *
 * // Store a memory
 * const id = await memoryManager.store('User prefers TypeScript', ['preference', 'coding']);
 *
 * // Recall memories
 * const memories = await memoryManager.recall('coding preferences', { limit: 5 });
 *
 * // Touch a memory (update hotness)
 * memoryManager.touchMemory(id);
 *
 * // Archive cold memories
 * const archived = memoryManager.archiveColdMemories();
 * ```
 */
export declare class MemoryManager {
    private memories;
    private openVikingAvailable;
    private versionControl;
    private autoOrganizer;
    private duplicateDetector;
    private memoryMerger;
    private conversationAnalyzer;
    private suggestionGenerator;
    private suggestionTrigger;
    constructor(enableVersionControl?: boolean, enableAutoOrganize?: boolean, enableSuggestions?: boolean);
    /**
     * Store a new memory
     */
    store(content: string, tags?: string[], userId?: string): Promise<string>;
    /**
     * Recall memories based on query
     */
    recall(query: string, options?: RecallOptions): Promise<Memory[]>;
    /**
     * Touch a memory (update hotness on access)
     */
    touchMemory(id: string): void;
    /**
     * Reference a memory (e.g., mentioned in conversation)
     */
    referenceMemory(id: string): void;
    /**
     * Archive cold memories
     */
    archiveColdMemories(): Memory[];
    /**
     * Get memory by ID
     */
    getMemory(id: string): Memory | undefined;
    /**
     * Get all memories (for debugging)
     */
    getAllMemories(): Memory[];
    /**
     * Get statistics
     */
    getStats(): {
        total: number;
        active: number;
        archived: number;
        averageHotness: number;
    };
    /**
     * Apply daily decay to all memories
     */
    applyDailyDecay(): void;
    private checkOpenViking;
    private generateEmbedding;
    private calculateRelevance;
    private generateId;
    /**
     * Update organizer memories (call after significant changes)
     */
    private updateOrganizerMemories;
    /**
     * Update suggestion memories
     */
    private updateSuggestionMemories;
    /**
     * Update memory with version tracking
     */
    updateMemory(memoryId: string, newContent: string, userId?: string, reason?: string): Memory | null;
    /**
     * Get version history
     */
    getVersionHistory(memoryId: string, limit?: number): import("./version-control").VersionEntry[];
    /**
     * Rollback to previous version
     */
    rollbackMemory(memoryId: string, version: number, userId?: string): Memory | null;
    /**
     * Get version statistics
     */
    getVersionStats(memoryId: string): {
        totalVersions: number;
        currentVersion: number;
        firstVersion: number;
        lastModified: number;
        averageVersionLifespan: number;
    };
    /**
     * Run auto organization
     */
    autoOrganize(options?: AutoOrganizeOptions): Promise<AutoOrganizeResult>;
    /**
     * Find duplicates
     */
    findDuplicates(options?: DuplicateOptions): DuplicatePair[];
    /**
     * Merge memories
     */
    mergeMemories(memoryIds: string[], strategy?: MergeStrategy): MergeResult;
    /**
     * Get duplicate statistics
     */
    getDuplicateStats(options?: DuplicateOptions): {
        totalMemories: number;
        duplicatePairs: number;
        duplicateMemories: number;
        potentialSavings: number;
        averageSimilarity: number;
    };
    /**
     * Get memory suggestions based on conversation
     */
    suggestMemories(messages: Message[], options?: SuggestionOptions & AnalysisOptions): Promise<MemorySuggestion[]>;
    /**
     * Analyze conversation context
     */
    analyzeConversation(messages: Message[], options?: AnalysisOptions): ConversationContext;
    /**
     * Track message (for trigger)
     */
    trackMessage(): void;
    /**
     * Dismiss a suggestion
     */
    dismissSuggestion(memoryId: string): void;
    /**
     * Get suggestion trigger state
     */
    getSuggestionState(): import("./suggestion-trigger").TriggerState;
    /**
     * Configure suggestion trigger
     */
    configureSuggestions(config: Partial<TriggerConfig>): void;
}
/**
 * Default memory manager instance
 */
export declare const defaultMemoryManager: MemoryManager;
//# sourceMappingURL=memory-manager.d.ts.map