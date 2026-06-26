"use strict";
/**
 * Entity Extractor
 * Automatically extracts entities from text
 *
 * Phase 5 Enhancement - Step 1: Graph Memory
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.defaultEntityExtractor = exports.EntityExtractor = void 0;
const graph_types_1 = require("./graph-types");
/**
 * Entity Extractor Class
 *
 * Features:
 * - Technology detection
 * - Project name detection
 * - File path detection
 * - URL detection
 * - Confidence scoring
 */
class EntityExtractor {
    constructor() {
        // Technology keywords
        this.technologies = new Set([
            'typescript', 'javascript', 'python', 'java', 'c++', 'c#', 'go', 'rust',
            'react', 'vue', 'angular', 'svelte', 'next.js', 'nuxt',
            'node', 'nodejs', 'express', 'nestjs', 'fastapi', 'django', 'flask',
            'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'vercel', 'netlify',
            'mongodb', 'postgresql', 'mysql', 'redis', 'elasticsearch',
            'git', 'github', 'gitlab', 'bitbucket',
            'jest', 'mocha', 'pytest', 'vitest', 'cypress', 'playwright',
            'webpack', 'vite', 'rollup', 'esbuild',
            'graphql', 'rest', 'api', 'microservice',
            'machine learning', 'ml', 'ai', 'deep learning', 'nlp'
        ]);
        // Project name patterns
        this.projectPatterns = [
            /\bProject[-_][A-Z][a-zA-Z]*\b/gi,
            /\b[A-Z][a-zA-Z]*[-_]?[A-Z][a-zA-Z]*\b/g,
            /\b[A-Z]{2,}[0-9]*\b/g
        ];
    }
    /**
     * Extract entities from text
     */
    extractEntities(text, options = {}) {
        const { minConfidence = 0.7, extractTechnologies = true, extractProjects = true, extractPeople = false, extractOrganizations = false, extractFiles = true, extractURLs = true } = options;
        const entities = [];
        // Extract technologies
        if (extractTechnologies) {
            entities.push(...this.extractTechnologies(text));
        }
        // Extract projects
        if (extractProjects) {
            entities.push(...this.extractProjects(text));
        }
        // Extract files
        if (extractFiles) {
            entities.push(...this.extractFiles(text));
        }
        // Extract URLs
        if (extractURLs) {
            entities.push(...this.extractURLs(text));
        }
        // Filter by confidence
        return entities.filter(e => e.confidence >= minConfidence);
    }
    /**
     * Extract technology entities
     */
    extractTechnologies(text) {
        const entities = [];
        const lowerText = text.toLowerCase();
        for (const tech of this.technologies) {
            const index = lowerText.indexOf(tech.toLowerCase());
            if (index !== -1) {
                const confidence = this.calculateTechnologyConfidence(tech, text, index);
                if (confidence >= 0.5) {
                    entities.push({
                        name: tech,
                        type: graph_types_1.EntityType.TECHNOLOGY,
                        confidence,
                        position: {
                            start: index,
                            end: index + tech.length
                        },
                        context: text.substring(Math.max(0, index - 20), Math.min(text.length, index + tech.length + 20))
                    });
                }
            }
        }
        return entities;
    }
    /**
     * Extract project names
     */
    extractProjects(text) {
        const entities = [];
        for (const pattern of this.projectPatterns) {
            const matches = text.matchAll(pattern);
            for (const match of matches) {
                const name = match[0];
                // Filter out common false positives
                if (!this.isFalsePositive(name)) {
                    entities.push({
                        name,
                        type: graph_types_1.EntityType.PROJECT,
                        confidence: 0.8,
                        position: {
                            start: match.index,
                            end: match.index + name.length
                        },
                        context: text.substring(Math.max(0, match.index - 20), Math.min(text.length, match.index + name.length + 20))
                    });
                }
            }
        }
        return entities;
    }
    /**
     * Extract file paths
     */
    extractFiles(text) {
        const entities = [];
        // Windows paths
        const winPathPattern = /[A-Za-z]:\\(?:[\w-]+\\)*[\w-]+(?:\.\w+)?/g;
        // Unix paths
        const unixPathPattern = /(?:\/[\w-]+)+\/?[\w-]*(?:\.\w+)?/g;
        // Relative paths
        const relativePathPattern = /\.\.?\/[\w-]+(?:\/[\w-]+)*(?:\.\w+)?/g;
        const patterns = [winPathPattern, unixPathPattern, relativePathPattern];
        for (const pattern of patterns) {
            const matches = text.matchAll(pattern);
            for (const match of matches) {
                const path = match[0];
                if (path.length > 3 && !path.includes('http')) {
                    entities.push({
                        name: path,
                        type: graph_types_1.EntityType.FILE,
                        confidence: 0.9,
                        position: {
                            start: match.index,
                            end: match.index + path.length
                        }
                    });
                }
            }
        }
        return entities;
    }
    /**
     * Extract URLs
     */
    extractURLs(text) {
        const entities = [];
        const urlPattern = /https?:\/\/[^\s<>"{}|\\^`\[\]]+/g;
        const matches = text.matchAll(urlPattern);
        for (const match of matches) {
            const url = match[0];
            entities.push({
                name: url,
                type: graph_types_1.EntityType.URL,
                confidence: 1.0,
                position: {
                    start: match.index,
                    end: match.index + url.length
                }
            });
        }
        return entities;
    }
    /**
     * Calculate technology confidence
     */
    calculateTechnologyConfidence(tech, text, position) {
        let confidence = 0.7;
        // Check surrounding context
        const context = text.substring(Math.max(0, position - 30), Math.min(text.length, position + tech.length + 30));
        const lowerContext = context.toLowerCase();
        // Boost if near programming keywords
        const programmingKeywords = ['using', 'with', 'in', 'for', 'language', 'framework', 'library', 'tool'];
        if (programmingKeywords.some(k => lowerContext.includes(k))) {
            confidence += 0.2;
        }
        // Boost if capitalized
        if (tech[0] === tech[0].toUpperCase()) {
            confidence += 0.1;
        }
        return Math.min(1.0, confidence);
    }
    /**
     * Check if project name is false positive
     */
    isFalsePositive(name) {
        const falsePositives = new Set([
            'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL',
            'CAN', 'HAD', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY',
            'GET', 'HAS', 'HIM', 'HIS', 'HOW', 'ITS', 'MAY', 'NEW',
            'NOW', 'OLD', 'SEE', 'TWO', 'WAY', 'WHO', 'BOY', 'DID'
        ]);
        return falsePositives.has(name.toUpperCase());
    }
    /**
     * Get entity type from name
     */
    getEntityType(name) {
        const lower = name.toLowerCase();
        if (this.technologies.has(lower)) {
            return graph_types_1.EntityType.TECHNOLOGY;
        }
        if (name.startsWith('http://') || name.startsWith('https://')) {
            return graph_types_1.EntityType.URL;
        }
        if (name.includes('/') || name.includes('\\')) {
            return graph_types_1.EntityType.FILE;
        }
        if (this.projectPatterns.some(p => {
            p.lastIndex = 0;
            return p.test(name);
        })) {
            return graph_types_1.EntityType.PROJECT;
        }
        return graph_types_1.EntityType.CONCEPT;
    }
}
exports.EntityExtractor = EntityExtractor;
/**
 * Default entity extractor instance
 */
exports.defaultEntityExtractor = new EntityExtractor();
//# sourceMappingURL=entity-extractor.js.map