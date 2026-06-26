"use strict";
/**
 * Duplicate Detection System
 * Finds and manages duplicate memories
 *
 * Phase 4 Enhancement - Step 2: Auto Organization
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.defaultDuplicateDetector = exports.DuplicateDetector = void 0;
/**
 * Duplicate Detector Class
 *
 * Features:
 * - Text-based similarity (Jaccard, cosine)
 * - Vector-based similarity (if available)
 * - Tag-based filtering
 * - Configurable threshold
 */
class DuplicateDetector {
    constructor() {
        this.memories = new Map();
    }
    /**
     * Set memories to check
     */
    setMemories(memories) {
        this.memories.clear();
        memories.forEach(m => this.memories.set(m.id, m));
    }
    /**
     * Find duplicate memories
     */
    findDuplicates(options = {}) {
        const { threshold = 0.85, tags, minHotness = 10, limit = 100, useVectorSimilarity = true } = options;
        // Filter memories
        let filtered = Array.from(this.memories.values())
            .filter(m => !m.archived)
            .filter(m => m.hotness >= minHotness);
        // Filter by tags if specified
        if (tags && tags.length > 0) {
            filtered = filtered.filter(m => tags.some(tag => m.tags.includes(tag)));
        }
        const duplicates = [];
        const checked = new Set();
        // Compare all pairs
        for (let i = 0; i < filtered.length; i++) {
            for (let j = i + 1; j < filtered.length; j++) {
                const mem1 = filtered[i];
                const mem2 = filtered[j];
                // Skip if already checked
                const pairKey = [mem1.id, mem2.id].sort().join('-');
                if (checked.has(pairKey)) {
                    continue;
                }
                checked.add(pairKey);
                // Calculate similarity
                const similarity = this.calculateSimilarity(mem1, mem2, useVectorSimilarity);
                // Check if above threshold
                if (similarity >= threshold) {
                    duplicates.push({
                        id1: mem1.id,
                        id2: mem2.id,
                        similarity,
                        reason: this.getSimilarityReason(mem1, mem2, similarity)
                    });
                    // Check limit
                    if (duplicates.length >= limit) {
                        return duplicates;
                    }
                }
            }
        }
        // Sort by similarity (descending)
        return duplicates.sort((a, b) => b.similarity - a.similarity);
    }
    /**
     * Calculate similarity between two memories
     */
    calculateSimilarity(mem1, mem2, useVector = true) {
        // Try vector similarity first (more accurate)
        if (useVector && mem1.vector && mem2.vector) {
            const vectorSim = this.cosineSimilarity(mem1.vector, mem2.vector);
            if (vectorSim > 0.5) {
                return vectorSim;
            }
        }
        // Fallback to text-based similarity
        const textSim = this.textSimilarity(mem1.content, mem2.content);
        const tagSim = this.tagSimilarity(mem1.tags, mem2.tags);
        // Weighted average (70% content, 30% tags)
        return textSim * 0.7 + tagSim * 0.3;
    }
    /**
     * Calculate cosine similarity for vectors
     */
    cosineSimilarity(vec1, vec2) {
        if (vec1.length !== vec2.length) {
            return 0;
        }
        let dotProduct = 0;
        let norm1 = 0;
        let norm2 = 0;
        for (let i = 0; i < vec1.length; i++) {
            dotProduct += vec1[i] * vec2[i];
            norm1 += vec1[i] * vec1[i];
            norm2 += vec2[i] * vec2[i];
        }
        const denominator = Math.sqrt(norm1) * Math.sqrt(norm2);
        if (denominator === 0) {
            return 0;
        }
        return dotProduct / denominator;
    }
    /**
     * Calculate text similarity using Jaccard index + word overlap
     */
    textSimilarity(text1, text2) {
        // Normalize texts
        const normalize = (text) => {
            return text
                .toLowerCase()
                .replace(/[^\w\s]/g, ' ')
                .split(/\s+/)
                .filter(word => word.length > 2); // Ignore short words
        };
        const words1 = new Set(normalize(text1));
        const words2 = new Set(normalize(text2));
        // Jaccard similarity
        const intersection = new Set([...words1].filter(w => words2.has(w)));
        const union = new Set([...words1, ...words2]);
        const jaccard = intersection.size / union.size;
        // Word overlap ratio
        const overlap1 = intersection.size / words1.size;
        const overlap2 = intersection.size / words2.size;
        const overlap = Math.max(overlap1, overlap2);
        // Weighted average
        return jaccard * 0.6 + overlap * 0.4;
    }
    /**
     * Calculate tag similarity
     */
    tagSimilarity(tags1, tags2) {
        if (tags1.length === 0 && tags2.length === 0) {
            return 1; // Both have no tags
        }
        if (tags1.length === 0 || tags2.length === 0) {
            return 0; // One has no tags
        }
        const set1 = new Set(tags1);
        const set2 = new Set(tags2);
        const intersection = [...set1].filter(t => set2.has(t)).length;
        const union = new Set([...set1, ...set2]).size;
        return intersection / union;
    }
    /**
     * Get human-readable reason for similarity
     */
    getSimilarityReason(mem1, mem2, similarity) {
        const reasons = [];
        // Check content overlap
        const words1 = mem1.content.toLowerCase().split(/\s+/);
        const words2 = mem2.content.toLowerCase().split(/\s+/);
        const commonWords = words1.filter(w => words2.includes(w));
        if (commonWords.length > 3) {
            reasons.push(`${commonWords.length} common words`);
        }
        // Check tag overlap
        const commonTags = mem1.tags.filter(t => mem2.tags.includes(t));
        if (commonTags.length > 0) {
            reasons.push(`shared tags: ${commonTags.join(', ')}`);
        }
        // Check vector similarity
        if (mem1.vector && mem2.vector) {
            const vecSim = this.cosineSimilarity(mem1.vector, mem2.vector);
            if (vecSim > 0.7) {
                reasons.push('high vector similarity');
            }
        }
        return reasons.length > 0
            ? reasons.join(', ')
            : `Overall similarity: ${(similarity * 100).toFixed(1)}%`;
    }
    /**
     * Get statistics about duplicates
     */
    getDuplicateStats(options = {}) {
        const duplicates = this.findDuplicates(options);
        const uniqueIds = new Set();
        duplicates.forEach(d => {
            uniqueIds.add(d.id1);
            uniqueIds.add(d.id2);
        });
        const totalMemories = this.memories.size;
        const duplicateMemories = uniqueIds.size;
        const potentialSavings = duplicateMemories - duplicates.length; // If we merge each pair
        const averageSimilarity = duplicates.length > 0
            ? duplicates.reduce((sum, d) => sum + d.similarity, 0) / duplicates.length
            : 0;
        return {
            totalMemories,
            duplicatePairs: duplicates.length,
            duplicateMemories,
            potentialSavings,
            averageSimilarity
        };
    }
    /**
     * Clear memories
     */
    clear() {
        this.memories.clear();
    }
}
exports.DuplicateDetector = DuplicateDetector;
/**
 * Default duplicate detector instance
 */
exports.defaultDuplicateDetector = new DuplicateDetector();
//# sourceMappingURL=duplicate-detector.js.map