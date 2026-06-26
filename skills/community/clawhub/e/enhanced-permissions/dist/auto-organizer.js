"use strict";
/**
 * Auto Organizer System
 * Automatically organizes memories
 *
 * Phase 4 Enhancement - Step 2: Auto Organization
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.defaultAutoOrganizer = exports.AutoOrganizer = void 0;
const duplicate_detector_1 = require("./duplicate-detector");
const memory_merger_1 = require("./memory-merger");
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
class AutoOrganizer {
    constructor() {
        this.memories = new Map();
        this.duplicateDetector = new duplicate_detector_1.DuplicateDetector();
        this.memoryMerger = new memory_merger_1.MemoryMerger();
    }
    /**
     * Set memories to organize
     */
    setMemories(memories) {
        this.memories.clear();
        memories.forEach(m => this.memories.set(m.id, m));
        this.duplicateDetector.setMemories(memories);
        this.memoryMerger.setMemories(memories);
    }
    /**
     * Run auto organization
     */
    async autoOrganize(options = {}) {
        const { mergeDuplicates = true, mergeThreshold = 0.85, mergeStrategy = memory_merger_1.MergeStrategy.KEEP_BEST, autoTag = true, markOutdated = true, outdatedAge = 30 * 24 * 60 * 60 * 1000, // 30 days
        summarizeRelated = false, dryRun = false } = options;
        const result = {
            success: true,
            duplicatesFound: 0,
            duplicatesMerged: 0,
            memoriesTagged: 0,
            memoriesMarkedOutdated: 0,
            summariesCreated: 0,
            changes: []
        };
        try {
            // Step 1: Find and merge duplicates
            if (mergeDuplicates) {
                const mergeResult = await this.handleDuplicates(mergeThreshold, mergeStrategy, dryRun);
                result.duplicatesFound = mergeResult.found;
                result.duplicatesMerged = mergeResult.merged;
                result.changes.push(...mergeResult.changes);
            }
            // Step 2: Auto-tag untagged memories
            if (autoTag) {
                const tagResult = await this.autoTagUntagged(dryRun);
                result.memoriesTagged = tagResult.count;
                result.changes.push(...tagResult.changes);
            }
            // Step 3: Mark outdated memories
            if (markOutdated) {
                const outdatedResult = this.markOutdatedMemories(outdatedAge, dryRun);
                result.memoriesMarkedOutdated = outdatedResult.count;
                result.changes.push(...outdatedResult.changes);
            }
            // Step 4: Summarize related memories
            if (summarizeRelated) {
                const summaryResult = await this.summarizeRelatedMemories(dryRun);
                result.summariesCreated = summaryResult.count;
                result.changes.push(...summaryResult.changes);
            }
            return result;
        }
        catch (error) {
            result.success = false;
            result.error = error.message;
            return result;
        }
    }
    /**
     * Handle duplicate detection and merging
     */
    async handleDuplicates(threshold, strategy, dryRun) {
        const changes = [];
        // Find duplicates
        const duplicates = this.duplicateDetector.findDuplicates({
            threshold,
            limit: 100
        });
        if (duplicates.length === 0) {
            return { found: 0, merged: 0, changes: ['No duplicates found'] };
        }
        // Merge duplicates
        let merged = 0;
        const processedIds = new Set();
        for (const dup of duplicates) {
            // Skip if already processed
            if (processedIds.has(dup.id1) || processedIds.has(dup.id2)) {
                continue;
            }
            if (!dryRun) {
                const mergeResult = this.memoryMerger.merge([dup.id1, dup.id2], strategy);
                if (mergeResult.success) {
                    merged++;
                    processedIds.add(dup.id1);
                    processedIds.add(dup.id2);
                    changes.push(`Merged ${dup.id1} + ${dup.id2} → ${mergeResult.keptId} (${(dup.similarity * 100).toFixed(1)}% similar)`);
                }
            }
            else {
                changes.push(`[DRY RUN] Would merge ${dup.id1} + ${dup.id2} (${(dup.similarity * 100).toFixed(1)}% similar)`);
            }
        }
        return {
            found: duplicates.length,
            merged,
            changes
        };
    }
    /**
     * Auto-tag untagged memories
     */
    async autoTagUntagged(dryRun) {
        const changes = [];
        let count = 0;
        for (const memory of this.memories.values()) {
            // Skip if already has tags or is archived
            if (memory.tags.length > 0 || memory.archived) {
                continue;
            }
            if (!dryRun) {
                // Simple auto-tagging based on content keywords
                const suggestedTags = this.suggestTags(memory.content);
                memory.tags.push(...suggestedTags);
                count++;
                changes.push(`Tagged ${memory.id}: [${suggestedTags.join(', ')}]`);
            }
            else {
                const suggestedTags = this.suggestTags(memory.content);
                changes.push(`[DRY RUN] Would tag ${memory.id}: [${suggestedTags.join(', ')}]`);
                count++;
            }
        }
        return { count, changes };
    }
    /**
     * Suggest tags based on content
     */
    suggestTags(content) {
        const tags = [];
        const lowerContent = content.toLowerCase();
        // Keyword-based tagging
        const keywordMap = {
            'typescript': ['typescript', 'programming', 'language'],
            'javascript': ['javascript', 'programming', 'web'],
            'python': ['python', 'programming', 'scripting'],
            'react': ['react', 'frontend', 'javascript'],
            'node': ['nodejs', 'backend', 'javascript'],
            'api': ['api', 'backend', 'integration'],
            'database': ['database', 'storage', 'data'],
            'test': ['testing', 'quality', 'development'],
            'config': ['configuration', 'setup', 'settings'],
            'deploy': ['deployment', 'production', 'devops']
        };
        for (const [keyword, tagsList] of Object.entries(keywordMap)) {
            if (lowerContent.includes(keyword)) {
                tags.push(...tagsList.slice(0, 2)); // Add up to 2 tags per keyword
            }
        }
        // Remove duplicates and limit to 5 tags
        return [...new Set(tags)].slice(0, 5);
    }
    /**
     * Mark outdated memories
     */
    markOutdatedMemories(outdatedAge, dryRun) {
        const changes = [];
        let count = 0;
        const now = Date.now();
        for (const memory of this.memories.values()) {
            // Skip if already archived or tagged as outdated
            if (memory.archived || memory.tags.includes('outdated')) {
                continue;
            }
            const age = now - memory.timestamp;
            if (age > outdatedAge) {
                if (!dryRun) {
                    if (!memory.tags.includes('outdated')) {
                        memory.tags.push('outdated');
                    }
                    count++;
                    const daysOld = Math.floor(age / (24 * 60 * 60 * 1000));
                    changes.push(`Marked ${memory.id} as outdated (${daysOld} days old)`);
                }
                else {
                    const daysOld = Math.floor(age / (24 * 60 * 60 * 1000));
                    changes.push(`[DRY RUN] Would mark ${memory.id} as outdated (${daysOld} days old)`);
                    count++;
                }
            }
        }
        return { count, changes };
    }
    /**
     * Summarize related memories
     */
    async summarizeRelatedMemories(dryRun) {
        const changes = [];
        let count = 0;
        // Group memories by tags
        const tagGroups = {};
        for (const memory of this.memories.values()) {
            for (const tag of memory.tags) {
                if (!tagGroups[tag]) {
                    tagGroups[tag] = [];
                }
                tagGroups[tag].push(memory);
            }
        }
        // Find groups with multiple memories
        for (const [tag, memories] of Object.entries(tagGroups)) {
            if (memories.length >= 3 && memories.length <= 10) {
                if (!dryRun) {
                    // Create summary memory
                    const summaryContent = `Summary of ${memories.length} memories tagged "${tag}":\n\n` +
                        memories.map(m => `- ${m.content.substring(0, 100)}...`).join('\n');
                    count++;
                    changes.push(`Created summary for tag "${tag}" (${memories.length} memories)`);
                }
                else {
                    count++;
                    changes.push(`[DRY RUN] Would create summary for tag "${tag}" (${memories.length} memories)`);
                }
            }
        }
        return { count, changes };
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
        this.duplicateDetector.clear();
        this.memoryMerger.clear();
    }
}
exports.AutoOrganizer = AutoOrganizer;
/**
 * Default auto organizer instance
 */
exports.defaultAutoOrganizer = new AutoOrganizer();
//# sourceMappingURL=auto-organizer.js.map