"use strict";
/**
 * Memory Version Control System
 * Adds version history to memories
 *
 * Phase 4 Enhancement - Step 1
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.defaultVersionControl = exports.VersionControlManager = void 0;
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
class VersionControlManager {
    constructor(options = {}) {
        this.memories = new Map();
        this.options = {
            maxVersions: 50,
            autoVersion: true,
            trackHotness: true,
            trackTags: true,
            ...options
        };
    }
    /**
     * Create a new versioned memory
     */
    createVersionedMemory(memoryId, content, tags = [], userId) {
        const now = Date.now();
        const initialVersion = {
            version: 1,
            content,
            timestamp: now,
            changedBy: userId,
            changeReason: 'Initial creation',
            hotness: 50,
            tags: [...tags]
        };
        const memory = {
            id: memoryId,
            content,
            timestamp: now,
            hotness: 50,
            tags: [...tags],
            archived: false,
            accessCount: 0,
            lastAccessed: now,
            // Version control fields
            version: 1,
            history: [initialVersion],
            originalCreatedAt: now,
            lastModifiedAt: now
        };
        this.memories.set(memory.id, memory);
        return memory;
    }
    /**
     * Update memory content (creates new version)
     */
    updateMemory(memoryId, newContent, userId, reason) {
        const memory = this.memories.get(memoryId);
        if (!memory) {
            return null;
        }
        const now = Date.now();
        const newVersion = memory.version + 1;
        // Create new version entry
        const versionEntry = {
            version: newVersion,
            content: newContent,
            timestamp: now,
            changedBy: userId,
            changeReason: reason || 'Content update',
            hotness: memory.hotness,
            tags: this.options.trackTags ? [...memory.tags] : []
        };
        // Update memory
        memory.version = newVersion;
        memory.content = newContent;
        memory.lastModifiedAt = now;
        memory.history.push(versionEntry);
        // Cleanup old versions if exceeds max
        if (memory.history.length > this.options.maxVersions) {
            const toRemove = memory.history.length - this.options.maxVersions;
            memory.history.splice(0, toRemove);
        }
        this.memories.set(memoryId, memory);
        return memory;
    }
    /**
     * Get version history
     */
    getHistory(memoryId, query = {}) {
        const memory = this.memories.get(memoryId);
        if (!memory) {
            return [];
        }
        let history = [...memory.history];
        // Filter by version range
        if (query.fromVersion !== undefined) {
            history = history.filter(v => v.version >= query.fromVersion);
        }
        if (query.toVersion !== undefined) {
            history = history.filter(v => v.version <= query.toVersion);
        }
        // Filter by date range
        if (query.fromDate !== undefined) {
            history = history.filter(v => v.timestamp >= query.fromDate);
        }
        if (query.toDate !== undefined) {
            history = history.filter(v => v.timestamp <= query.toDate);
        }
        // Limit results
        if (query.limit !== undefined) {
            history = history.slice(-query.limit);
        }
        return history;
    }
    /**
     * Get specific version
     */
    getVersion(memoryId, version) {
        const memory = this.memories.get(memoryId);
        if (!memory) {
            return null;
        }
        return memory.history.find(v => v.version === version) || null;
    }
    /**
     * Rollback to specific version
     */
    rollback(memoryId, targetVersion, userId) {
        const memory = this.memories.get(memoryId);
        if (!memory) {
            return null;
        }
        const targetEntry = memory.history.find(v => v.version === targetVersion);
        if (!targetEntry) {
            return null;
        }
        // Create rollback version
        const now = Date.now();
        const newVersion = memory.version + 1;
        const rollbackEntry = {
            version: newVersion,
            content: targetEntry.content,
            timestamp: now,
            changedBy: userId,
            changeReason: `Rollback to version ${targetVersion}`,
            hotness: targetEntry.hotness,
            tags: this.options.trackTags ? [...targetEntry.tags] : []
        };
        // Update memory
        memory.version = newVersion;
        memory.content = targetEntry.content;
        memory.hotness = targetEntry.hotness;
        if (this.options.trackTags) {
            memory.tags = [...targetEntry.tags];
        }
        memory.lastModifiedAt = now;
        memory.history.push(rollbackEntry);
        // Cleanup old versions
        if (memory.history.length > this.options.maxVersions) {
            const toRemove = memory.history.length - this.options.maxVersions;
            memory.history.splice(0, toRemove);
        }
        this.memories.set(memoryId, memory);
        return memory;
    }
    /**
     * Get diff between two versions
     */
    getDiff(memoryId, version1, version2) {
        const memory = this.memories.get(memoryId);
        if (!memory) {
            return {
                version1: null,
                version2: null,
                hasChanges: false,
                changes: null
            };
        }
        const v1 = memory.history.find(v => v.version === version1) || null;
        const v2 = memory.history.find(v => v.version === version2) || null;
        if (!v1 || !v2) {
            return {
                version1: v1,
                version2: v2,
                hasChanges: false,
                changes: null
            };
        }
        const contentChanged = v1.content !== v2.content;
        const hotnessChanged = v1.hotness !== v2.hotness;
        const tagsChanged = JSON.stringify(v1.tags) !== JSON.stringify(v2.tags);
        return {
            version1: v1,
            version2: v2,
            hasChanges: contentChanged || hotnessChanged || tagsChanged,
            changes: {
                contentChanged,
                hotnessChanged,
                tagsChanged
            }
        };
    }
    /**
     * Get memory with full version info
     */
    getVersionedMemory(memoryId) {
        return this.memories.get(memoryId) || null;
    }
    /**
     * Get version statistics
     */
    getVersionStats(memoryId) {
        const memory = this.memories.get(memoryId);
        if (!memory || memory.history.length === 0) {
            return null;
        }
        const totalVersions = memory.history.length;
        const currentVersion = memory.version;
        const firstVersion = memory.history[0].version;
        const lastModified = memory.lastModifiedAt;
        // Calculate average version lifespan
        let totalLifespan = 0;
        for (let i = 1; i < memory.history.length; i++) {
            const lifespan = memory.history[i].timestamp - memory.history[i - 1].timestamp;
            totalLifespan += lifespan;
        }
        const averageVersionLifespan = totalVersions > 1 ? totalLifespan / (totalVersions - 1) : 0;
        return {
            totalVersions,
            currentVersion,
            firstVersion,
            lastModified,
            averageVersionLifespan
        };
    }
    /**
     * Cleanup old versions (manual trigger)
     */
    cleanupOldVersions(memoryId, keepLast = 10) {
        const memory = this.memories.get(memoryId);
        if (!memory) {
            return 0;
        }
        const beforeCount = memory.history.length;
        if (beforeCount <= keepLast) {
            return 0;
        }
        const toRemove = beforeCount - keepLast;
        memory.history.splice(0, toRemove);
        this.memories.set(memoryId, memory);
        return toRemove;
    }
    /**
     * Export version history to JSON
     */
    exportToJSON(memoryId) {
        const memory = this.memories.get(memoryId);
        if (!memory) {
            return null;
        }
        return JSON.stringify({
            id: memory.id,
            currentVersion: memory.version,
            history: memory.history,
            exportedAt: new Date().toISOString()
        }, null, 2);
    }
    /**
     * Import version history from JSON
     */
    importFromJSON(jsonString) {
        try {
            const data = JSON.parse(jsonString);
            if (!data.id || !data.history || !Array.isArray(data.history)) {
                return null;
            }
            const memory = {
                ...data,
                archived: false,
                accessCount: 0,
                lastAccessed: Date.now()
            };
            this.memories.set(memory.id, memory);
            return memory;
        }
        catch {
            return null;
        }
    }
    /**
     * Get all memories
     */
    getAllMemories() {
        return Array.from(this.memories.values());
    }
    /**
     * Clear all memories
     */
    clear() {
        this.memories.clear();
    }
    /**
     * Generate unique ID
     */
    generateId() {
        return `mem_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }
}
exports.VersionControlManager = VersionControlManager;
/**
 * Default version control manager instance
 */
exports.defaultVersionControl = new VersionControlManager({
    maxVersions: 50,
    autoVersion: true,
    trackHotness: true,
    trackTags: true
});
//# sourceMappingURL=version-control.js.map