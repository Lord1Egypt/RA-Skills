"use strict";
/**
 * Memory Manager with Hotness Scoring
 * Based on Claw Code memory system
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.defaultMemoryManager = exports.MemoryManager = void 0;
exports.getHotnessDelta = getHotnessDelta;
exports.calculateDecayedHotness = calculateDecayedHotness;
exports.shouldArchive = shouldArchive;
exports.isEligibleForRecall = isEligibleForRecall;
const version_control_1 = require("./version-control");
const auto_organizer_1 = require("./auto-organizer");
const duplicate_detector_1 = require("./duplicate-detector");
const memory_merger_1 = require("./memory-merger");
const conversation_analyzer_1 = require("./conversation-analyzer");
const suggestion_generator_1 = require("./suggestion-generator");
const suggestion_trigger_1 = require("./suggestion-trigger");
/**
 * Hotness change values for different events
 */
const HOTNESS_DELTA = {
    created: 50, // New memory starts at 50
    accessed: 5, // +5 when accessed
    referenced: 10, // +10 when referenced in conversation
    daily_decay: -1, // -1 per day natural decay
    archived: -50 // Reset to 0 when archived
};
/**
 * Constants
 */
const CONSTANTS = {
    MAX_HOTNESS: 100,
    MIN_HOTNESS: 0,
    ARCHIVE_THRESHOLD: 10, // Memories with hotness < 10 are archived
    RECALL_THRESHOLD: 20, // Only recall memories with hotness > 20
    DECAY_RATE: 0.99 // Daily decay multiplier
};
/**
 * Calculate hotness change for an event
 */
function getHotnessDelta(event) {
    return HOTNESS_DELTA[event] || 0;
}
/**
 * Calculate decayed hotness based on age
 * Formula: baseHotness * (0.99 ^ ageInDays)
 */
function calculateDecayedHotness(baseHotness, ageInDays) {
    const decayed = baseHotness * Math.pow(CONSTANTS.DECAY_RATE, ageInDays);
    return Math.max(CONSTANTS.MIN_HOTNESS, Math.min(CONSTANTS.MAX_HOTNESS, decayed));
}
/**
 * Check if a memory should be archived
 */
function shouldArchive(memory) {
    const age = Date.now() - memory.timestamp;
    const ageInDays = age / (1000 * 60 * 60 * 24);
    const decayedHotness = calculateDecayedHotness(memory.hotness, ageInDays);
    return decayedHotness < CONSTANTS.ARCHIVE_THRESHOLD && !memory.archived;
}
/**
 * Check if a memory is eligible for recall
 */
function isEligibleForRecall(memory) {
    if (memory.archived)
        return false;
    const age = Date.now() - memory.timestamp;
    const ageInDays = age / (1000 * 60 * 60 * 24);
    const decayedHotness = calculateDecayedHotness(memory.hotness, ageInDays);
    return decayedHotness > CONSTANTS.RECALL_THRESHOLD;
}
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
class MemoryManager {
    constructor(enableVersionControl = true, enableAutoOrganize = true, enableSuggestions = true) {
        this.memories = new Map();
        this.openVikingAvailable = false;
        // Check if OpenViking is available
        this.checkOpenViking();
        // Initialize version control
        if (enableVersionControl) {
            this.versionControl = new version_control_1.VersionControlManager({
                maxVersions: 50,
                autoVersion: true,
                trackHotness: true,
                trackTags: true
            });
        }
        // Initialize auto organizer
        if (enableAutoOrganize) {
            this.autoOrganizer = new auto_organizer_1.AutoOrganizer();
            this.duplicateDetector = new duplicate_detector_1.DuplicateDetector();
            this.memoryMerger = new memory_merger_1.MemoryMerger();
            this.updateOrganizerMemories();
        }
        // Initialize smart suggestions
        if (enableSuggestions) {
            this.conversationAnalyzer = new conversation_analyzer_1.ConversationAnalyzer();
            this.suggestionGenerator = new suggestion_generator_1.SuggestionGenerator();
            this.suggestionTrigger = new suggestion_trigger_1.SuggestionTrigger();
            this.updateSuggestionMemories();
        }
    }
    /**
     * Store a new memory
     */
    async store(content, tags = [], userId) {
        const memory = {
            id: this.generateId(),
            content,
            timestamp: Date.now(),
            hotness: HOTNESS_DELTA.created, // Start at 50
            tags,
            accessCount: 0,
            lastAccessed: Date.now(),
            archived: false
        };
        // Generate vector embedding if OpenViking available
        if (this.openVikingAvailable) {
            try {
                memory.vector = await this.generateEmbedding(content);
            }
            catch (error) {
                console.warn('Failed to generate vector embedding:', error);
            }
        }
        this.memories.set(memory.id, memory);
        // Also store in version control if enabled
        if (this.versionControl) {
            this.versionControl.createVersionedMemory(memory.id, content, tags, userId);
        }
        return memory.id;
    }
    /**
     * Recall memories based on query
     */
    async recall(query, options = {}) {
        const { limit = 5, minHotness = CONSTANTS.RECALL_THRESHOLD, tags, includeArchived = false } = options;
        // Filter eligible memories
        let eligible = Array.from(this.memories.values()).filter(memory => {
            // Skip archived unless requested
            if (memory.archived && !includeArchived)
                return false;
            // Check hotness threshold
            const age = Date.now() - memory.timestamp;
            const ageInDays = age / (1000 * 60 * 60 * 24);
            const decayedHotness = calculateDecayedHotness(memory.hotness, ageInDays);
            if (decayedHotness < minHotness)
                return false;
            // Filter by tags if specified
            if (tags && tags.length > 0) {
                return tags.some(tag => memory.tags.includes(tag));
            }
            return true;
        });
        // Score by relevance (can be enhanced with vector similarity)
        const scored = await Promise.all(eligible.map(async (memory) => ({
            memory,
            score: await this.calculateRelevance(query, memory)
        })));
        // Sort by score and return top N
        return scored
            .sort((a, b) => b.score - a.score)
            .slice(0, limit)
            .map(s => s.memory);
    }
    /**
     * Touch a memory (update hotness on access)
     */
    touchMemory(id) {
        const memory = this.memories.get(id);
        if (memory) {
            memory.hotness += getHotnessDelta('accessed');
            memory.hotness = Math.min(CONSTANTS.MAX_HOTNESS, memory.hotness);
            memory.accessCount++;
            memory.lastAccessed = Date.now();
        }
    }
    /**
     * Reference a memory (e.g., mentioned in conversation)
     */
    referenceMemory(id) {
        const memory = this.memories.get(id);
        if (memory) {
            memory.hotness += getHotnessDelta('referenced');
            memory.hotness = Math.min(CONSTANTS.MAX_HOTNESS, memory.hotness);
        }
    }
    /**
     * Archive cold memories
     */
    archiveColdMemories() {
        const toArchive = [];
        for (const memory of this.memories.values()) {
            if (shouldArchive(memory)) {
                memory.archived = true;
                memory.hotness = 0;
                toArchive.push(memory);
            }
        }
        if (toArchive.length > 0) {
            console.log(`📦 Archived ${toArchive.length} cold memories`);
        }
        return toArchive;
    }
    /**
     * Get memory by ID
     */
    getMemory(id) {
        return this.memories.get(id);
    }
    /**
     * Get all memories (for debugging)
     */
    getAllMemories() {
        return Array.from(this.memories.values());
    }
    /**
     * Get statistics
     */
    getStats() {
        const memories = Array.from(this.memories.values());
        const active = memories.filter(m => !m.archived);
        const archived = memories.filter(m => m.archived);
        const avgHotness = active.reduce((sum, m) => sum + m.hotness, 0) / (active.length || 1);
        return {
            total: memories.length,
            active: active.length,
            archived: archived.length,
            averageHotness: avgHotness
        };
    }
    /**
     * Apply daily decay to all memories
     */
    applyDailyDecay() {
        for (const memory of this.memories.values()) {
            if (!memory.archived) {
                memory.hotness += getHotnessDelta('daily_decay');
                memory.hotness = Math.max(CONSTANTS.MIN_HOTNESS, memory.hotness);
            }
        }
    }
    // === Private Methods ===
    async checkOpenViking() {
        try {
            // Check if OpenViking is installed
            const { exec } = await Promise.resolve().then(() => __importStar(require('child_process')));
            await new Promise((resolve, reject) => {
                exec('python -c "import openviking"', (error) => {
                    if (error)
                        reject(error);
                    else
                        resolve(true);
                });
            });
            this.openVikingAvailable = true;
            console.log('✅ OpenViking available - vector search enabled');
        }
        catch {
            this.openVikingAvailable = false;
            console.log('⚠️ OpenViking not available - using basic search');
        }
    }
    async generateEmbedding(content) {
        // Placeholder - would call OpenViking API
        // Return dummy vector for now
        return new Array(1024).fill(0).map(() => Math.random());
    }
    async calculateRelevance(query, memory) {
        // Simple relevance scoring (can be enhanced with vector similarity)
        let score = memory.hotness;
        // Boost if query matches content
        if (memory.content.toLowerCase().includes(query.toLowerCase())) {
            score += 20;
        }
        // Boost if query matches tags
        const queryTags = query.toLowerCase().split(' ');
        for (const tag of memory.tags) {
            if (queryTags.some(qt => tag.toLowerCase().includes(qt))) {
                score += 10;
            }
        }
        // Boost recent memories
        const ageInDays = (Date.now() - memory.timestamp) / (1000 * 60 * 60 * 24);
        if (ageInDays < 7) {
            score += 5;
        }
        return score;
    }
    generateId() {
        return `mem_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }
    /**
     * Update organizer memories (call after significant changes)
     */
    updateOrganizerMemories() {
        if (this.autoOrganizer) {
            const memories = Array.from(this.memories.values());
            this.autoOrganizer.setMemories(memories);
            this.duplicateDetector.setMemories(memories);
            this.memoryMerger.setMemories(memories);
        }
    }
    /**
     * Update suggestion memories
     */
    updateSuggestionMemories() {
        if (this.suggestionGenerator) {
            const memories = Array.from(this.memories.values());
            this.suggestionGenerator.setMemories(memories);
        }
    }
    // === Version Control Methods ===
    /**
     * Update memory with version tracking
     */
    updateMemory(memoryId, newContent, userId, reason) {
        const memory = this.memories.get(memoryId);
        if (!memory) {
            return null;
        }
        // Update the memory
        memory.content = newContent;
        memory.lastAccessed = Date.now();
        this.memories.set(memoryId, memory);
        // Create new version
        if (this.versionControl) {
            this.versionControl.updateMemory(memoryId, newContent, userId, reason);
        }
        return memory;
    }
    /**
     * Get version history
     */
    getVersionHistory(memoryId, limit = 10) {
        if (!this.versionControl) {
            return [];
        }
        // Get from version control
        const history = this.versionControl.getHistory(memoryId, { limit });
        console.log(`🕐 Version history: ${history.length} versions for ${memoryId}`);
        return history;
    }
    /**
     * Rollback to previous version
     */
    rollbackMemory(memoryId, version, userId) {
        if (!this.versionControl) {
            return null;
        }
        const result = this.versionControl.rollback(memoryId, version, userId);
        if (!result) {
            return null;
        }
        // Update main memory
        const memory = this.memories.get(memoryId);
        if (memory) {
            memory.content = result.content;
            memory.hotness = result.hotness;
            memory.tags = result.tags;
            this.memories.set(memoryId, memory);
        }
        return memory;
    }
    /**
     * Get version statistics
     */
    getVersionStats(memoryId) {
        if (!this.versionControl) {
            return null;
        }
        return this.versionControl.getVersionStats(memoryId);
    }
    // === Auto Organization Methods ===
    /**
     * Run auto organization
     */
    async autoOrganize(options = {}) {
        if (!this.autoOrganizer) {
            return {
                success: false,
                duplicatesFound: 0,
                duplicatesMerged: 0,
                memoriesTagged: 0,
                memoriesMarkedOutdated: 0,
                summariesCreated: 0,
                changes: [],
                error: 'Auto organization not enabled'
            };
        }
        // Update memories before organizing
        this.updateOrganizerMemories();
        const result = await this.autoOrganizer.autoOrganize(options);
        // Update main memories if not dry run
        if (!options.dryRun && result.success) {
            const organizedMemories = this.autoOrganizer.getMemories();
            organizedMemories.forEach(m => this.memories.set(m.id, m));
        }
        return result;
    }
    /**
     * Find duplicates
     */
    findDuplicates(options = {}) {
        if (!this.duplicateDetector) {
            return [];
        }
        this.duplicateDetector.setMemories(Array.from(this.memories.values()));
        return this.duplicateDetector.findDuplicates(options);
    }
    /**
     * Merge memories
     */
    mergeMemories(memoryIds, strategy = memory_merger_1.MergeStrategy.KEEP_BEST) {
        if (!this.memoryMerger) {
            return {
                success: false,
                error: 'Memory merger not enabled'
            };
        }
        this.memoryMerger.setMemories(Array.from(this.memories.values()));
        const result = this.memoryMerger.merge(memoryIds, strategy);
        if (result.success) {
            // Update main memories
            this.updateOrganizerMemories();
        }
        return result;
    }
    /**
     * Get duplicate statistics
     */
    getDuplicateStats(options = {}) {
        if (!this.duplicateDetector) {
            return null;
        }
        this.duplicateDetector.setMemories(Array.from(this.memories.values()));
        return this.duplicateDetector.getDuplicateStats(options);
    }
    // === Smart Suggestion Methods ===
    /**
     * Get memory suggestions based on conversation
     */
    async suggestMemories(messages, options = {}) {
        if (!this.conversationAnalyzer || !this.suggestionGenerator || !this.suggestionTrigger) {
            return [];
        }
        // Check if should show suggestion
        if (!this.suggestionTrigger.shouldShowSuggestion()) {
            return [];
        }
        // Analyze conversation
        const context = this.conversationAnalyzer.analyze(messages, options);
        // Update memories
        this.updateSuggestionMemories();
        // Generate suggestions
        const suggestions = this.suggestionGenerator.generateSuggestions(context, options);
        // Filter out already shown/dismissed
        const filtered = suggestions.filter(s => !this.suggestionTrigger.wasShown(s.memory.id) &&
            !this.suggestionTrigger.wasDismissed(s.memory.id));
        // Track shown suggestions
        filtered.forEach(s => this.suggestionTrigger.trackShown(s.memory.id));
        return filtered;
    }
    /**
     * Analyze conversation context
     */
    analyzeConversation(messages, options = {}) {
        if (!this.conversationAnalyzer) {
            return { keywords: [], topics: [], entities: [] };
        }
        return this.conversationAnalyzer.analyze(messages, options);
    }
    /**
     * Track message (for trigger)
     */
    trackMessage() {
        if (this.suggestionTrigger) {
            this.suggestionTrigger.onMessage();
        }
    }
    /**
     * Dismiss a suggestion
     */
    dismissSuggestion(memoryId) {
        if (this.suggestionTrigger) {
            this.suggestionTrigger.trackDismissed(memoryId);
        }
    }
    /**
     * Get suggestion trigger state
     */
    getSuggestionState() {
        if (!this.suggestionTrigger) {
            return null;
        }
        return this.suggestionTrigger.getState();
    }
    /**
     * Configure suggestion trigger
     */
    configureSuggestions(config) {
        if (!this.suggestionTrigger) {
            this.suggestionTrigger = new suggestion_trigger_1.SuggestionTrigger(config);
        }
        else {
            this.suggestionTrigger.updateConfig(config);
        }
    }
}
exports.MemoryManager = MemoryManager;
/**
 * Default memory manager instance
 */
exports.defaultMemoryManager = new MemoryManager();
//# sourceMappingURL=memory-manager.js.map