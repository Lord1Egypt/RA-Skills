"use strict";
/**
 * OpenViking Integration for OpenClaw
 * Vector-based memory search and embeddings
 *
 * Phase 3: OpenViking Integration
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.defaultOpenVikingService = exports.OpenVikingService = void 0;
const child_process_1 = require("child_process");
const util_1 = require("util");
const execAsync = (0, util_1.promisify)(child_process_1.exec);
/**
 * OpenViking Service Class
 *
 * Provides vector embedding generation and similarity search
 * using OpenViking backend
 */
class OpenVikingService {
    constructor() {
        this.available = false;
        this.apiKey = '';
        this.baseUrl = 'https://ark.cn-beijing.volces.com/api/v3';
        this.embeddingModel = 'doubao-embedding-vision-250615';
        this.vlmModel = 'doubao-seed-2-0-pro-260215';
        this.checkAvailability();
    }
    /**
     * Check if OpenViking is available
     */
    async checkAvailability() {
        try {
            await execAsync('python -c "import openviking"');
            this.available = true;
            console.log('✅ OpenViking service available');
        }
        catch {
            this.available = false;
            console.log('⚠️ OpenViking service not available');
        }
    }
    /**
     * Check if service is available
     */
    isAvailable() {
        return this.available;
    }
    /**
     * Generate embedding for text
     *
     * @param text - Text to embed
     * @returns Vector embedding (1024 dimensions)
     */
    async generateEmbedding(text) {
        if (!this.available) {
            throw new Error('OpenViking service not available');
        }
        try {
            const pythonCode = `
import openviking
import json

client = openviking.Client(
    api_key="${this.apiKey}",
    base_url="${this.baseUrl}"
)

response = client.embeddings.create(
    model="${this.embeddingModel}",
    input=${JSON.stringify(text)}
)

embedding = response.data[0].embedding
print(json.dumps(embedding))
`;
            const result = await execAsync(`python -c "${pythonCode}"`);
            const embedding = JSON.parse(result.stdout);
            if (!Array.isArray(embedding) || embedding.length === 0) {
                throw new Error('Invalid embedding response');
            }
            return embedding;
        }
        catch (error) {
            console.error('Failed to generate embedding:', error.message);
            throw error;
        }
    }
    /**
     * Generate embeddings for multiple texts (batch)
     *
     * @param texts - Array of texts to embed
     * @returns Array of vector embeddings
     */
    async generateBatchEmbeddings(texts) {
        if (!this.available) {
            throw new Error('OpenViking service not available');
        }
        try {
            const pythonCode = `
import openviking
import json

client = openviking.Client(
    api_key="${this.apiKey}",
    base_url="${this.baseUrl}"
)

response = client.embeddings.create(
    model="${this.embeddingModel}",
    input=${JSON.stringify(texts)}
)

embeddings = [item.embedding for item in response.data]
print(json.dumps(embeddings))
`;
            const result = await execAsync(`python -c "${pythonCode}"`);
            const embeddings = JSON.parse(result.stdout);
            if (!Array.isArray(embeddings)) {
                throw new Error('Invalid embeddings response');
            }
            return embeddings;
        }
        catch (error) {
            console.error('Failed to generate batch embeddings:', error.message);
            throw error;
        }
    }
    /**
     * Calculate cosine similarity between two vectors
     *
     * @param vector1 - First vector
     * @param vector2 - Second vector
     * @returns Similarity score (0-1)
     */
    cosineSimilarity(vector1, vector2) {
        if (vector1.length !== vector2.length) {
            throw new Error('Vector dimensions must match');
        }
        let dotProduct = 0;
        let norm1 = 0;
        let norm2 = 0;
        for (let i = 0; i < vector1.length; i++) {
            dotProduct += vector1[i] * vector2[i];
            norm1 += vector1[i] * vector1[i];
            norm2 += vector2[i] * vector2[i];
        }
        const denominator = Math.sqrt(norm1) * Math.sqrt(norm2);
        if (denominator === 0) {
            return 0;
        }
        return dotProduct / denominator;
    }
    /**
     * Find most similar memories
     *
     * @param query - Query text
     * @param memories - Array of memories with embeddings
     * @param limit - Maximum results to return
     * @returns Sorted memories by similarity
     */
    async findSimilarMemories(query, memories, limit = 5) {
        if (!this.available) {
            // Fallback to text-based search
            return this.textBasedSearch(query, memories, limit);
        }
        try {
            // Generate query embedding
            const queryEmbedding = await this.generateEmbedding(query);
            // Calculate similarity for each memory
            const scored = memories
                .filter(m => m.vector && m.vector.length > 0)
                .map(memory => ({
                id: memory.id,
                score: this.cosineSimilarity(queryEmbedding, memory.vector)
            }))
                .sort((a, b) => b.score - a.score);
            return scored.slice(0, limit);
        }
        catch (error) {
            console.warn('Vector search failed, falling back to text search:', error);
            return this.textBasedSearch(query, memories, limit);
        }
    }
    /**
     * Fallback text-based search
     */
    textBasedSearch(query, memories, limit) {
        const queryLower = query.toLowerCase();
        const scored = memories.map(memory => {
            const contentLower = memory.content.toLowerCase();
            let score = 0;
            // Simple keyword matching
            if (contentLower.includes(queryLower)) {
                score += 10;
            }
            const queryWords = queryLower.split(' ');
            for (const word of queryWords) {
                if (contentLower.includes(word)) {
                    score += 1;
                }
            }
            return { id: memory.id, score };
        }).sort((a, b) => b.score - a.score);
        return scored.slice(0, limit);
    }
    /**
     * Configure API key
     */
    setApiKey(apiKey) {
        this.apiKey = apiKey;
        console.log('✅ OpenViking API key configured');
    }
    /**
     * Get configuration status
     */
    getStatus() {
        return {
            available: this.available,
            apiKeyConfigured: this.apiKey.length > 0,
            baseUrl: this.baseUrl,
            embeddingModel: this.embeddingModel
        };
    }
}
exports.OpenVikingService = OpenVikingService;
/**
 * Default OpenViking service instance
 */
exports.defaultOpenVikingService = new OpenVikingService();
//# sourceMappingURL=openviking-integration.js.map