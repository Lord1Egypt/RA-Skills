/**
 * Memory Version Control System
 * Adds version history to memories
 *
 * Phase 4 Enhancement - Step 1
 */
import { Memory } from './types';
/**
 * Version entry interface
 */
export interface VersionEntry {
    version: number;
    content: string;
    timestamp: number;
    changedBy?: string;
    changeReason?: string;
    hotness: number;
    tags: string[];
}
/**
 * Memory with version history
 */
export interface VersionedMemory extends Memory {
    version: number;
    history: VersionEntry[];
    originalCreatedAt: number;
    lastModifiedAt: number;
}
/**
 * Version control options
 */
export interface VersionOptions {
    maxVersions?: number;
    autoVersion?: boolean;
    trackHotness?: boolean;
    trackTags?: boolean;
}
/**
 * Version history query options
 */
export interface HistoryQuery {
    fromVersion?: number;
    toVersion?: number;
    fromDate?: number;
    toDate?: number;
    limit?: number;
}
/**
 * Version Control Manager
 *
 * Features:
 * - Automatic versioning on updates
 * - Version history tracking
 * - Rollback to any version
 * - Diff between versions
 * - Automatic cleanup of old versions
 */
export declare class VersionControlManager {
    private memories;
    private options;
    constructor(options?: VersionOptions);
    /**
     * Create a new versioned memory
     */
    createVersionedMemory(memoryId: string, content: string, tags?: string[], userId?: string): VersionedMemory;
    /**
     * Update memory content (creates new version)
     */
    updateMemory(memoryId: string, newContent: string, userId?: string, reason?: string): VersionedMemory | null;
    /**
     * Get version history
     */
    getHistory(memoryId: string, query?: HistoryQuery): VersionEntry[];
    /**
     * Get specific version
     */
    getVersion(memoryId: string, version: number): VersionEntry | null;
    /**
     * Rollback to specific version
     */
    rollback(memoryId: string, targetVersion: number, userId?: string): VersionedMemory | null;
    /**
     * Get diff between two versions
     */
    getDiff(memoryId: string, version1: number, version2: number): {
        version1: VersionEntry | null;
        version2: VersionEntry | null;
        hasChanges: boolean;
        changes: {
            contentChanged: boolean;
            hotnessChanged: boolean;
            tagsChanged: boolean;
        } | null;
    };
    /**
     * Get memory with full version info
     */
    getVersionedMemory(memoryId: string): VersionedMemory | null;
    /**
     * Get version statistics
     */
    getVersionStats(memoryId: string): {
        totalVersions: number;
        currentVersion: number;
        firstVersion: number;
        lastModified: number;
        averageVersionLifespan: number;
    } | null;
    /**
     * Cleanup old versions (manual trigger)
     */
    cleanupOldVersions(memoryId: string, keepLast?: number): number;
    /**
     * Export version history to JSON
     */
    exportToJSON(memoryId: string): string | null;
    /**
     * Import version history from JSON
     */
    importFromJSON(jsonString: string): VersionedMemory | null;
    /**
     * Get all memories
     */
    getAllMemories(): VersionedMemory[];
    /**
     * Clear all memories
     */
    clear(): void;
    /**
     * Generate unique ID
     */
    private generateId;
}
/**
 * Default version control manager instance
 */
export declare const defaultVersionControl: VersionControlManager;
//# sourceMappingURL=version-control.d.ts.map