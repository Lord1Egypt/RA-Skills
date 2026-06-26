/**
 * Relation Inference Engine
 * Infers relationships between entities
 *
 * Phase 5 Enhancement - Step 1: Graph Memory
 */
import { KnowledgeGraph, RelationType } from './index';
/**
 * Inferred relation interface
 */
export interface InferredRelation {
    fromEntityId: string;
    toEntityId: string;
    type: RelationType;
    confidence: number;
    reason: string;
}
/**
 * Relation Inference Engine
 *
 * Features:
 * - Rule-based inference
 * - Transitive inference
 * - Symmetric inference
 * - Pattern-based inference
 */
export declare class RelationInferenceEngine {
    private graph;
    constructor(graph: KnowledgeGraph);
    /**
     * Infer relations for entity
     */
    inferRelations(entityId: string): InferredRelation[];
    /**
     * Infer relation between two entities
     */
    private inferRelationPair;
    /**
     * Infer transitive relations
     * If A uses B and B is-part-of C, then A uses C
     */
    private inferTransitive;
    /**
     * Infer symmetric relations
     * If A similar-to B, then B similar-to A
     */
    private inferSymmetric;
    /**
     * Infer pattern-based relations
     */
    private inferPatternBased;
    /**
     * Find missing relations
     */
    findMissingRelations(): InferredRelation[];
    /**
     * Suggest relations to create
     */
    suggestRelations(minConfidence?: number): InferredRelation[];
    /**
     * Auto-create high-confidence relations
     */
    autoCreateRelations(minConfidence?: number): number;
}
/**
 * Create inference engine for graph
 */
export declare function createInferenceEngine(graph: KnowledgeGraph): RelationInferenceEngine;
//# sourceMappingURL=relation-inference.d.ts.map