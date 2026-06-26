/**
 * Conversation Context Analyzer
 * Analyzes conversation to extract context for memory suggestions
 *
 * Phase 4 Enhancement - Step 3: Smart Suggestions
 */
/**
 * Conversation context interface
 */
export interface ConversationContext {
    keywords: string[];
    topics: string[];
    entities: string[];
    sentiment?: 'positive' | 'negative' | 'neutral';
    urgency?: 'high' | 'medium' | 'low';
    timeRange?: {
        from?: string;
        to?: string;
    };
}
/**
 * Message interface
 */
export interface Message {
    role: 'user' | 'assistant' | 'system';
    content: string;
    timestamp?: number;
}
/**
 * Analysis options
 */
export interface AnalysisOptions {
    extractKeywords?: boolean;
    extractTopics?: boolean;
    extractEntities?: boolean;
    detectSentiment?: boolean;
    detectUrgency?: boolean;
    maxKeywords?: number;
    minKeywordLength?: number;
}
/**
 * Conversation Analyzer Class
 *
 * Features:
 * - Keyword extraction
 * - Topic classification
 * - Entity recognition
 * - Sentiment analysis (basic)
 * - Urgency detection
 */
export declare class ConversationAnalyzer {
    private stopWords;
    /**
     * Analyze conversation messages
     */
    analyze(messages: Message[], options?: AnalysisOptions): ConversationContext;
    /**
     * Extract keywords from text
     */
    private extractKeywords;
    /**
     * Extract topics from keywords
     */
    private extractTopics;
    /**
     * Extract entities from text
     */
    private extractEntities;
    /**
     * Detect sentiment (basic)
     */
    private detectSentiment;
    /**
     * Detect urgency (basic)
     */
    private detectUrgency;
    /**
     * Get context summary
     */
    getContextSummary(context: ConversationContext): string;
}
/**
 * Default conversation analyzer instance
 */
export declare const defaultConversationAnalyzer: ConversationAnalyzer;
//# sourceMappingURL=conversation-analyzer.d.ts.map