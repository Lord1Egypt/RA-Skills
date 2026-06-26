"use strict";
/**
 * Conversation Context Analyzer
 * Analyzes conversation to extract context for memory suggestions
 *
 * Phase 4 Enhancement - Step 3: Smart Suggestions
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.defaultConversationAnalyzer = exports.ConversationAnalyzer = void 0;
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
class ConversationAnalyzer {
    constructor() {
        this.stopWords = new Set([
            'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'must', 'shall',
            'can', 'need', 'dare', 'ought', 'used', 'to', 'of', 'in',
            'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into',
            'through', 'during', 'before', 'after', 'above', 'below',
            'between', 'under', 'again', 'further', 'then', 'once',
            'here', 'there', 'when', 'where', 'why', 'how', 'all',
            'each', 'few', 'more', 'most', 'other', 'some', 'such',
            'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
            'too', 'very', 'just', 'and', 'but', 'if', 'or', 'because',
            'until', 'while', 'although', 'though', 'after', 'before',
            'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves',
            'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him',
            'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its',
            'itself', 'they', 'them', 'their', 'theirs', 'themselves',
            'what', 'which', 'who', 'whom', 'this', 'that', 'these',
            'those', 'am'
        ]);
    }
    /**
     * Analyze conversation messages
     */
    analyze(messages, options = {}) {
        const { extractKeywords = true, extractTopics = true, extractEntities = true, detectSentiment = false, detectUrgency = false, maxKeywords = 10, minKeywordLength = 3 } = options;
        // Combine all message content
        const combinedText = messages
            .map(m => m.content)
            .join(' ');
        const context = {
            keywords: [],
            topics: [],
            entities: []
        };
        // Extract keywords
        if (extractKeywords) {
            context.keywords = this.extractKeywords(combinedText, maxKeywords, minKeywordLength);
        }
        // Extract topics
        if (extractTopics) {
            context.topics = this.extractTopics(context.keywords);
        }
        // Extract entities
        if (extractEntities) {
            context.entities = this.extractEntities(combinedText);
        }
        // Detect sentiment
        if (detectSentiment) {
            context.sentiment = this.detectSentiment(combinedText);
        }
        // Detect urgency
        if (detectUrgency) {
            context.urgency = this.detectUrgency(combinedText);
        }
        return context;
    }
    /**
     * Extract keywords from text
     */
    extractKeywords(text, maxCount, minLength) {
        // Normalize text
        const normalized = text
            .toLowerCase()
            .replace(/[^\w\s]/g, ' ')
            .split(/\s+/)
            .filter(word => word.length >= minLength);
        // Remove stop words
        const filtered = normalized.filter(word => !this.stopWords.has(word));
        // Count word frequency
        const frequency = new Map();
        filtered.forEach(word => {
            frequency.set(word, (frequency.get(word) || 0) + 1);
        });
        // Sort by frequency and return top N
        const sorted = Array.from(frequency.entries())
            .sort((a, b) => b[1] - a[1])
            .slice(0, maxCount)
            .map(entry => entry[0]);
        return sorted;
    }
    /**
     * Extract topics from keywords
     */
    extractTopics(keywords) {
        const topics = [];
        const topicMap = {
            'programming': ['typescript', 'javascript', 'python', 'java', 'code', 'programming', 'developer'],
            'frontend': ['react', 'vue', 'angular', 'html', 'css', 'frontend', 'ui', 'ux'],
            'backend': ['node', 'nodejs', 'express', 'api', 'backend', 'server', 'database'],
            'devops': ['docker', 'kubernetes', 'aws', 'azure', 'gcp', 'deploy', 'ci', 'cd', 'devops'],
            'testing': ['test', 'testing', 'jest', 'mocha', 'pytest', 'unit', 'integration'],
            'database': ['sql', 'mongodb', 'postgres', 'mysql', 'redis', 'database', 'db'],
            'security': ['security', 'auth', 'authentication', 'authorization', 'encryption', 'oauth'],
            'performance': ['performance', 'optimization', 'cache', 'speed', 'latency'],
            'documentation': ['docs', 'documentation', 'readme', 'wiki', 'guide'],
            'project': ['project', 'task', 'issue', 'bug', 'feature', 'release']
        };
        // Match keywords to topics
        const topicScores = new Map();
        for (const [topic, topicKeywords] of Object.entries(topicMap)) {
            const score = keywords.filter(k => topicKeywords.includes(k)).length;
            if (score > 0) {
                topicScores.set(topic, score);
            }
        }
        // Sort topics by score and return
        const sortedTopics = Array.from(topicScores.entries())
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5)
            .map(entry => entry[0]);
        return sortedTopics;
    }
    /**
     * Extract entities from text
     */
    extractEntities(text) {
        const entities = [];
        // Pattern for project names (Project-X, MyProject, etc.)
        const projectPattern = /\b[A-Z][a-zA-Z]*(?:-[A-Z][a-zA-Z]*)?\b/g;
        const projects = text.match(projectPattern) || [];
        entities.push(...projects.filter(p => p.length > 2));
        // Pattern for version numbers (v1.0.0, 2.3.1, etc.)
        const versionPattern = /\bv?\d+\.\d+(\.\d+)?\b/g;
        const versions = text.match(versionPattern) || [];
        entities.push(...versions);
        // Pattern for URLs
        const urlPattern = /https?:\/\/[^\s]+/g;
        const urls = text.match(urlPattern) || [];
        entities.push(...urls);
        // Pattern for file paths
        const pathPattern = /\b(?:[a-zA-Z]:\\)?(?:[\w-]+\\)+[\w-]+\b/g;
        const paths = text.match(pathPattern) || [];
        entities.push(...paths);
        // Remove duplicates
        return [...new Set(entities)];
    }
    /**
     * Detect sentiment (basic)
     */
    detectSentiment(text) {
        const positiveWords = new Set([
            'good', 'great', 'excellent', 'amazing', 'awesome', 'wonderful',
            'fantastic', 'perfect', 'love', 'like', 'happy', 'pleased',
            'satisfied', 'success', 'successful', 'works', 'working'
        ]);
        const negativeWords = new Set([
            'bad', 'terrible', 'awful', 'horrible', 'hate', 'dislike',
            'unhappy', 'angry', 'frustrated', 'failed', 'failure',
            'error', 'broken', 'wrong', 'problem', 'issue'
        ]);
        const words = text.toLowerCase().split(/\s+/);
        let positiveCount = 0;
        let negativeCount = 0;
        words.forEach(word => {
            if (positiveWords.has(word))
                positiveCount++;
            if (negativeWords.has(word))
                negativeCount++;
        });
        if (positiveCount > negativeCount)
            return 'positive';
        if (negativeCount > positiveCount)
            return 'negative';
        return 'neutral';
    }
    /**
     * Detect urgency (basic)
     */
    detectUrgency(text) {
        const urgentWords = new Set([
            'urgent', 'asap', 'immediately', 'now', 'emergency',
            'critical', 'important', 'deadline', 'today', 'right now'
        ]);
        const mediumWords = new Set([
            'soon', 'shortly', 'quickly', 'fast', 'priority',
            'need', 'should', 'could', 'maybe'
        ]);
        const words = text.toLowerCase().split(/\s+/);
        let urgentCount = 0;
        let mediumCount = 0;
        words.forEach(word => {
            if (urgentWords.has(word))
                urgentCount++;
            if (mediumWords.has(word))
                mediumCount++;
        });
        if (urgentCount > 0)
            return 'high';
        if (mediumCount > 1)
            return 'medium';
        return 'low';
    }
    /**
     * Get context summary
     */
    getContextSummary(context) {
        const parts = [];
        if (context.keywords.length > 0) {
            parts.push(`Keywords: ${context.keywords.slice(0, 5).join(', ')}`);
        }
        if (context.topics.length > 0) {
            parts.push(`Topics: ${context.topics.join(', ')}`);
        }
        if (context.entities.length > 0) {
            parts.push(`Entities: ${context.entities.slice(0, 5).join(', ')}`);
        }
        if (context.sentiment) {
            parts.push(`Sentiment: ${context.sentiment}`);
        }
        if (context.urgency) {
            parts.push(`Urgency: ${context.urgency}`);
        }
        return parts.join(' | ');
    }
}
exports.ConversationAnalyzer = ConversationAnalyzer;
/**
 * Default conversation analyzer instance
 */
exports.defaultConversationAnalyzer = new ConversationAnalyzer();
//# sourceMappingURL=conversation-analyzer.js.map