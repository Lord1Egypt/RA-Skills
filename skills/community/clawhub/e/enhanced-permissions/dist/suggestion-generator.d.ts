/**
 * Memory Suggestion Generator
 * Generates smart memory suggestions based on conversation context
 *
 * Phase 4 Enhancement - Step 3: Smart Suggestions
 */
import { Memory } from './types';
import { ConversationContext } from './conversation-analyzer';
/**
 * Suggestion interface
 */
export interface MemorySuggestion {
    memory: Memory;
    relevance: number;
    reason: string;
    matchedKeywords: string[];
    matchedTopics: string[];
    displayText: string;
}
/**
 * Suggestion options
 */
export interface SuggestionOptions {
    limit?: number;
    minRelevance?: number;
    minHotness?: number;
    includeArchived?: boolean;
    maxDisplayLength?: number;
}
/**
 * Suggestion Generator Class
 *
 * Features:
 * - Context-based memory retrieval
 * - Relevance scoring
 * - Natural language prompts
 * - Configurable filters
 */
export declare class SuggestionGenerator {
    private memories;
    /**
     * Set memories to search
     */
    setMemories(memories: Memory[]): void;
    /**
     * Generate memory suggestions based on context
     */
    generateSuggestions(context: ConversationContext, options?: SuggestionOptions): MemorySuggestion[];
    /**
     * Calculate relevance score
     */
    private calculateRelevance;
    /**
     * Calculate keyword matching score
     */
    private calculateKeywordScore;
    /**
     * Calculate topic matching score
     */
    private calculateTopicScore;
    /**
     * Calculate entity matching score
     */
    private calculateEntityScore;
    /**
     * Get matched keywords
     */
    private getMatchedKeywords;
    /**
     * Get matched topics
     */
    private getMatchedTopics;
    /**
     * Generate human-readable reason
     */
    private generateReason;
    /**
     * Truncate text to max length
     */
    private truncateText;
    /**
     * Generate display prompt for suggestions
     */
    generatePrompt(suggestions: MemorySuggestion[]): string;
    /**
     * Get suggestions as natural language
     */
    generateNaturalLanguage(suggestions: MemorySuggestion[]): string[];
}
/**
 * Default suggestion generator instance
 */
export declare const defaultSuggestionGenerator: SuggestionGenerator;
//# sourceMappingURL=suggestion-generator.d.ts.map