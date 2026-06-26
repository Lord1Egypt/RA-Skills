/**
 * OpenViking Integration for OpenClaw
 * Vector-based memory search and embeddings
 *
 * Phase 3: OpenViking Integration
 */
/**
 * OpenViking Service Class
 *
 * Provides vector embedding generation and similarity search
 * using OpenViking backend
 */
export declare class OpenVikingService {
    private available;
    private apiKey;
    private baseUrl;
    private embeddingModel;
    private vlmModel;
    constructor();
    /**
     * Check if OpenViking is available
     */
    private checkAvailability;
    /**
     * Check if service is available
     */
    isAvailable(): boolean;
    /**
     * Generate embedding for text
     *
     * @param text - Text to embed
     * @returns Vector embedding (1024 dimensions)
     */
    generateEmbedding(text: string): Promise<number[]>;
    /**
     * Generate embeddings for multiple texts (batch)
     *
     * @param texts - Array of texts to embed
     * @returns Array of vector embeddings
     */
    generateBatchEmbeddings(texts: string[]): Promise<number[][]>;
    /**
     * Calculate cosine similarity between two vectors
     *
     * @param vector1 - First vector
     * @param vector2 - Second vector
     * @returns Similarity score (0-1)
     */
    cosineSimilarity(vector1: number[], vector2: number[]): number;
    /**
     * Find most similar memories
     *
     * @param query - Query text
     * @param memories - Array of memories with embeddings
     * @param limit - Maximum results to return
     * @returns Sorted memories by similarity
     */
    findSimilarMemories(query: string, memories: Array<{
        id: string;
        content: string;
        vector?: number[];
    }>, limit?: number): Promise<Array<{
        id: string;
        score: number;
    }>>;
    /**
     * Fallback text-based search
     */
    private textBasedSearch;
    /**
     * Configure API key
     */
    setApiKey(apiKey: string): void;
    /**
     * Get configuration status
     */
    getStatus(): {
        available: boolean;
        apiKeyConfigured: boolean;
        baseUrl: string;
        embeddingModel: string;
    };
}
/**
 * Default OpenViking service instance
 */
export declare const defaultOpenVikingService: OpenVikingService;
//# sourceMappingURL=openviking-integration.d.ts.map