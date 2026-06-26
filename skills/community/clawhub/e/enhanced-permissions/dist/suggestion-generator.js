"use strict";
/**
 * Memory Suggestion Generator
 * Generates smart memory suggestions based on conversation context
 *
 * Phase 4 Enhancement - Step 3: Smart Suggestions
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.defaultSuggestionGenerator = exports.SuggestionGenerator = void 0;
/**
 * Suggestion Generator Class
 *
 * Features:
 * - Context-based memory retrieval
 * - Relevance scoring
 * - Natural language prompts
 * - Configurable filters
 */
class SuggestionGenerator {
    constructor() {
        this.memories = [];
    }
    /**
     * Set memories to search
     */
    setMemories(memories) {
        this.memories = memories;
    }
    /**
     * Generate memory suggestions based on context
     */
    generateSuggestions(context, options = {}) {
        const { limit = 3, minRelevance = 0.7, minHotness = 20, includeArchived = false, maxDisplayLength = 100 } = options;
        // Filter memories
        let eligible = this.memories.filter(m => {
            if (m.archived && !includeArchived)
                return false;
            // Check hotness threshold
            if (m.hotness < minHotness)
                return false;
            return true;
        });
        // Score memories by relevance
        const scored = eligible
            .map(memory => ({
            memory,
            score: this.calculateRelevance(memory, context),
            matchedKeywords: this.getMatchedKeywords(memory, context),
            matchedTopics: this.getMatchedTopics(memory, context)
        }))
            .filter(item => item.score >= minRelevance)
            .sort((a, b) => b.score - a.score)
            .slice(0, limit);
        // Generate suggestions
        return scored.map(item => ({
            memory: item.memory,
            relevance: item.score,
            reason: this.generateReason(item),
            matchedKeywords: item.matchedKeywords,
            matchedTopics: item.matchedTopics,
            displayText: this.truncateText(item.memory.content, maxDisplayLength)
        }));
    }
    /**
     * Calculate relevance score
     */
    calculateRelevance(memory, context) {
        let score = 0;
        // Keyword matching (40% weight)
        const keywordScore = this.calculateKeywordScore(memory, context);
        score += keywordScore * 0.4;
        // Topic matching (30% weight)
        const topicScore = this.calculateTopicScore(memory, context);
        score += topicScore * 0.3;
        // Entity matching (20% weight)
        const entityScore = this.calculateEntityScore(memory, context);
        score += entityScore * 0.2;
        // Hotness bonus (10% weight)
        const hotnessScore = memory.hotness / 100;
        score += hotnessScore * 0.1;
        return Math.min(1.0, score);
    }
    /**
     * Calculate keyword matching score
     */
    calculateKeywordScore(memory, context) {
        const memoryText = (memory.content + ' ' + memory.tags.join(' ')).toLowerCase();
        const matchedKeywords = context.keywords.filter(k => memoryText.includes(k.toLowerCase()));
        if (context.keywords.length === 0)
            return 0;
        return matchedKeywords.length / context.keywords.length;
    }
    /**
     * Calculate topic matching score
     */
    calculateTopicScore(memory, context) {
        const memoryTags = memory.tags.map(t => t.toLowerCase());
        const matchedTopics = context.topics.filter(t => memoryTags.includes(t.toLowerCase()));
        if (context.topics.length === 0)
            return 0;
        return matchedTopics.length / context.topics.length;
    }
    /**
     * Calculate entity matching score
     */
    calculateEntityScore(memory, context) {
        const memoryText = memory.content.toLowerCase();
        const matchedEntities = context.entities.filter(e => memoryText.includes(e.toLowerCase()));
        if (context.entities.length === 0)
            return 0;
        return matchedEntities.length / context.entities.length;
    }
    /**
     * Get matched keywords
     */
    getMatchedKeywords(memory, context) {
        const memoryText = (memory.content + ' ' + memory.tags.join(' ')).toLowerCase();
        return context.keywords.filter(k => memoryText.includes(k.toLowerCase()));
    }
    /**
     * Get matched topics
     */
    getMatchedTopics(memory, context) {
        const memoryTags = memory.tags.map(t => t.toLowerCase());
        return context.topics.filter(t => memoryTags.includes(t.toLowerCase()));
    }
    /**
     * Generate human-readable reason
     */
    generateReason(item) {
        const reasons = [];
        if (item.matchedKeywords.length > 0) {
            reasons.push(`mentions ${item.matchedKeywords.slice(0, 3).join(', ')}`);
        }
        if (item.matchedTopics.length > 0) {
            reasons.push(`related to ${item.matchedTopics.join(', ')}`);
        }
        if (item.memory.hotness > 70) {
            reasons.push('highly relevant');
        }
        if (reasons.length === 0) {
            reasons.push('contextually relevant');
        }
        return reasons.join(' and ');
    }
    /**
     * Truncate text to max length
     */
    truncateText(text, maxLength) {
        if (text.length <= maxLength)
            return text;
        return text.substring(0, maxLength - 3) + '...';
    }
    /**
     * Generate display prompt for suggestions
     */
    generatePrompt(suggestions) {
        if (suggestions.length === 0) {
            return '';
        }
        if (suggestions.length === 1) {
            const s = suggestions[0];
            return `💡 Related memory: ${s.displayText}`;
        }
        const prompts = suggestions.map((s, i) => {
            return `${i + 1}. ${s.displayText} (${(s.relevance * 100).toFixed(0)}% match)`;
        });
        return `💡 Found ${suggestions.length} related memories:\n${prompts.join('\n')}`;
    }
    /**
     * Get suggestions as natural language
     */
    generateNaturalLanguage(suggestions) {
        return suggestions.map(s => {
            const templates = [
                `You previously mentioned: "${s.displayText}"`,
                `Related to your earlier note: "${s.displayText}"`,
                `This connects to: "${s.displayText}"`,
                `Remember this? "${s.displayText}"`
            ];
            // Choose template based on relevance
            const index = Math.floor(s.relevance * (templates.length - 1));
            return templates[index];
        });
    }
}
exports.SuggestionGenerator = SuggestionGenerator;
/**
 * Default suggestion generator instance
 */
exports.defaultSuggestionGenerator = new SuggestionGenerator();
//# sourceMappingURL=suggestion-generator.js.map