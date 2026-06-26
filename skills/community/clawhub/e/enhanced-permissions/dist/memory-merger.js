"use strict";
/**
 * Memory Merger System
 * Merges duplicate and related memories
 *
 * Phase 4 Enhancement - Step 2: Auto Organization
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.defaultMemoryMerger = exports.MemoryMerger = exports.MergeStrategy = void 0;
/**
 * Merge strategy enum
 */
var MergeStrategy;
(function (MergeStrategy) {
    MergeStrategy["KEEP_BEST"] = "keep-best";
    MergeStrategy["KEEP_NEWEST"] = "keep-newest";
    MergeStrategy["KEEP_OLDEST"] = "keep-oldest";
    MergeStrategy["COMBINE"] = "combine";
    MergeStrategy["KEEP_SHORTEST"] = "keep-shortest";
    MergeStrategy["KEEP_LONGEST"] = "keep-longest"; // Keep detailed version
})(MergeStrategy || (exports.MergeStrategy = MergeStrategy = {}));
/**
 * Memory Merger Class
 *
 * Features:
 * - Multiple merge strategies
 * - Content combination
 * - Tag merging
 * - Version history preservation
 */
class MemoryMerger {
    constructor() {
        this.memories = new Map();
    }
    /**
     * Set memories to work with
     */
    setMemories(memories) {
        this.memories.clear();
        memories.forEach(m => this.memories.set(m.id, m));
    }
    /**
     * Merge duplicate memories
     */
    merge(memoryIds, strategy = MergeStrategy.KEEP_BEST, userId) {
        if (memoryIds.length < 2) {
            return {
                success: false,
                error: 'Need at least 2 memories to merge'
            };
        }
        // Get all memories
        const memories = memoryIds
            .map(id => this.memories.get(id))
            .filter((m) => m !== undefined);
        if (memories.length !== memoryIds.length) {
            return {
                success: false,
                error: 'Some memories not found'
            };
        }
        // Execute merge based on strategy
        switch (strategy) {
            case MergeStrategy.KEEP_BEST:
                return this.mergeKeepBest(memories, userId);
            case MergeStrategy.KEEP_NEWEST:
                return this.mergeKeepNewest(memories, userId);
            case MergeStrategy.KEEP_OLDEST:
                return this.mergeKeepOldest(memories, userId);
            case MergeStrategy.COMBINE:
                return this.mergeCombine(memories, userId);
            case MergeStrategy.KEEP_SHORTEST:
                return this.mergeKeepShortest(memories, userId);
            case MergeStrategy.KEEP_LONGEST:
                return this.mergeKeepLongest(memories, userId);
            default:
                return {
                    success: false,
                    error: `Unknown strategy: ${strategy}`
                };
        }
    }
    /**
     * Strategy: Keep the one with highest hotness
     */
    mergeKeepBest(memories, userId) {
        // Sort by hotness (descending)
        const sorted = [...memories].sort((a, b) => b.hotness - a.hotness);
        const keeper = sorted[0];
        const toRemove = sorted.slice(1);
        // Merge tags from all
        const allTags = new Set(keeper.tags);
        toRemove.forEach(m => m.tags.forEach(t => allTags.add(t)));
        keeper.tags = Array.from(allTags);
        return {
            success: true,
            keptId: keeper.id,
            mergedIds: toRemove.map(m => m.id),
            newContent: keeper.content
        };
    }
    /**
     * Strategy: Keep the most recent
     */
    mergeKeepNewest(memories, userId) {
        // Sort by timestamp (descending)
        const sorted = [...memories].sort((a, b) => b.timestamp - a.timestamp);
        const keeper = sorted[0];
        const toRemove = sorted.slice(1);
        // Merge tags
        const allTags = new Set(keeper.tags);
        toRemove.forEach(m => m.tags.forEach(t => allTags.add(t)));
        keeper.tags = Array.from(allTags);
        return {
            success: true,
            keptId: keeper.id,
            mergedIds: toRemove.map(m => m.id),
            newContent: keeper.content
        };
    }
    /**
     * Strategy: Keep the original (oldest)
     */
    mergeKeepOldest(memories, userId) {
        // Sort by timestamp (ascending)
        const sorted = [...memories].sort((a, b) => a.timestamp - b.timestamp);
        const keeper = sorted[0];
        const toRemove = sorted.slice(1);
        // Merge tags
        const allTags = new Set(keeper.tags);
        toRemove.forEach(m => m.tags.forEach(t => allTags.add(t)));
        keeper.tags = Array.from(allTags);
        return {
            success: true,
            keptId: keeper.id,
            mergedIds: toRemove.map(m => m.id),
            newContent: keeper.content
        };
    }
    /**
     * Strategy: Combine content together
     */
    mergeCombine(memories, userId) {
        // Sort by timestamp
        const sorted = [...memories].sort((a, b) => a.timestamp - b.timestamp);
        const keeper = sorted[0];
        const toRemove = sorted.slice(1);
        // Combine content
        const contents = sorted.map(m => m.content.trim());
        const combinedContent = this.combineContents(contents);
        // Merge all tags
        const allTags = new Set();
        sorted.forEach(m => m.tags.forEach(t => allTags.add(t)));
        // Update keeper
        keeper.content = combinedContent;
        keeper.tags = Array.from(allTags);
        return {
            success: true,
            keptId: keeper.id,
            mergedIds: toRemove.map(m => m.id),
            newContent: combinedContent
        };
    }
    /**
     * Strategy: Keep the shortest (most concise)
     */
    mergeKeepShortest(memories, userId) {
        // Sort by content length (ascending)
        const sorted = [...memories].sort((a, b) => a.content.length - b.content.length);
        const keeper = sorted[0];
        const toRemove = sorted.slice(1);
        // Merge tags
        const allTags = new Set(keeper.tags);
        toRemove.forEach(m => m.tags.forEach(t => allTags.add(t)));
        keeper.tags = Array.from(allTags);
        return {
            success: true,
            keptId: keeper.id,
            mergedIds: toRemove.map(m => m.id),
            newContent: keeper.content
        };
    }
    /**
     * Strategy: Keep the longest (most detailed)
     */
    mergeKeepLongest(memories, userId) {
        // Sort by content length (descending)
        const sorted = [...memories].sort((a, b) => b.content.length - a.content.length);
        const keeper = sorted[0];
        const toRemove = sorted.slice(1);
        // Merge tags
        const allTags = new Set(keeper.tags);
        toRemove.forEach(m => m.tags.forEach(t => allTags.add(t)));
        keeper.tags = Array.from(allTags);
        return {
            success: true,
            keptId: keeper.id,
            mergedIds: toRemove.map(m => m.id),
            newContent: keeper.content
        };
    }
    /**
     * Combine multiple contents intelligently
     */
    combineContents(contents) {
        if (contents.length === 1) {
            return contents[0];
        }
        if (contents.length === 2) {
            // For 2 contents, try to merge intelligently
            return this.mergeTwoContents(contents[0], contents[1]);
        }
        // For multiple contents, join with separators
        return contents.join('\n\n---\n\n');
    }
    /**
     * Merge two contents intelligently
     */
    mergeTwoContents(content1, content2) {
        // If one contains the other, return the longer one
        if (content1.includes(content2)) {
            return content1;
        }
        if (content2.includes(content1)) {
            return content2;
        }
        // Try to find common sentences and merge
        const sentences1 = content1.split(/[.!?]+/).map(s => s.trim()).filter(s => s.length > 0);
        const sentences2 = content2.split(/[.!?]+/).map(s => s.trim()).filter(s => s.length > 0);
        // Find unique sentences
        const unique1 = sentences1.filter(s => !sentences2.some(s2 => this.similarity(s, s2) > 0.8));
        const unique2 = sentences2.filter(s => !sentences1.some(s1 => this.similarity(s, s1) > 0.8));
        // Combine unique sentences
        const allSentences = [...unique1, ...unique2];
        if (allSentences.length === 0) {
            // If all sentences are similar, return the longer content
            return content1.length > content2.length ? content1 : content2;
        }
        return allSentences.join('. ') + '.';
    }
    /**
     * Simple string similarity
     */
    similarity(s1, s2) {
        const words1 = new Set(s1.toLowerCase().split(/\s+/));
        const words2 = new Set(s2.toLowerCase().split(/\s+/));
        const intersection = [...words1].filter(w => words2.has(w)).length;
        const union = new Set([...words1, ...words2]).size;
        return union > 0 ? intersection / union : 0;
    }
    /**
     * Get memories
     */
    getMemories() {
        return Array.from(this.memories.values());
    }
    /**
     * Clear memories
     */
    clear() {
        this.memories.clear();
    }
}
exports.MemoryMerger = MemoryMerger;
/**
 * Default memory merger instance
 */
exports.defaultMemoryMerger = new MemoryMerger();
//# sourceMappingURL=memory-merger.js.map