/**
 * Entity Extractor
 * Automatically extracts entities from text
 *
 * Phase 5 Enhancement - Step 1: Graph Memory
 */
import { EntityType } from './graph-types';
/**
 * Extracted entity interface
 */
export interface ExtractedEntity {
    name: string;
    type: EntityType;
    confidence: number;
    position: {
        start: number;
        end: number;
    };
    context?: string;
}
/**
 * Entity extraction options
 */
export interface ExtractionOptions {
    minConfidence?: number;
    extractTechnologies?: boolean;
    extractProjects?: boolean;
    extractPeople?: boolean;
    extractOrganizations?: boolean;
    extractFiles?: boolean;
    extractURLs?: boolean;
}
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
export declare class EntityExtractor {
    private technologies;
    private projectPatterns;
    /**
     * Extract entities from text
     */
    extractEntities(text: string, options?: ExtractionOptions): ExtractedEntity[];
    /**
     * Extract technology entities
     */
    private extractTechnologies;
    /**
     * Extract project names
     */
    private extractProjects;
    /**
     * Extract file paths
     */
    private extractFiles;
    /**
     * Extract URLs
     */
    private extractURLs;
    /**
     * Calculate technology confidence
     */
    private calculateTechnologyConfidence;
    /**
     * Check if project name is false positive
     */
    private isFalsePositive;
    /**
     * Get entity type from name
     */
    getEntityType(name: string): EntityType;
}
/**
 * Default entity extractor instance
 */
export declare const defaultEntityExtractor: EntityExtractor;
//# sourceMappingURL=entity-extractor.d.ts.map