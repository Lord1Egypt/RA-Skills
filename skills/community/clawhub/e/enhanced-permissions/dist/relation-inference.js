"use strict";
/**
 * Relation Inference Engine
 * Infers relationships between entities
 *
 * Phase 5 Enhancement - Step 1: Graph Memory
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.RelationInferenceEngine = void 0;
exports.createInferenceEngine = createInferenceEngine;
const index_1 = require("./index");
const graph_types_1 = require("./graph-types");
/**
 * Relation Inference Engine
 *
 * Features:
 * - Rule-based inference
 * - Transitive inference
 * - Symmetric inference
 * - Pattern-based inference
 */
class RelationInferenceEngine {
    constructor(graph) {
        this.graph = graph;
    }
    /**
     * Infer relations for entity
     */
    inferRelations(entityId) {
        const entity = this.graph.getEntity(entityId);
        if (!entity)
            return [];
        const inferred = [];
        // Get all entities
        const allEntities = this.graph.queryGraph({});
        // Try to infer relations with other entities
        for (const connected of allEntities) {
            if (connected.entity.id !== entityId) {
                const relations = this.inferRelationPair(entity, connected.entity);
                inferred.push(...relations);
            }
        }
        return inferred;
    }
    /**
     * Infer relation between two entities
     */
    inferRelationPair(entity1, entity2) {
        const relations = [];
        // Check for transitive relations
        const transitive = this.inferTransitive(entity1, entity2);
        if (transitive) {
            relations.push(transitive);
        }
        // Check for symmetric relations
        const symmetric = this.inferSymmetric(entity1, entity2);
        if (symmetric) {
            relations.push(symmetric);
        }
        // Check for pattern-based relations
        const patternBased = this.inferPatternBased(entity1, entity2);
        relations.push(...patternBased);
        return relations;
    }
    /**
     * Infer transitive relations
     * If A uses B and B is-part-of C, then A uses C
     */
    inferTransitive(entity1, entity2) {
        const relations1 = this.graph.getRelations(entity1.id, 'out');
        const relations2 = this.graph.getRelations(entity2.id, 'in');
        // Look for common intermediate entity
        for (const rel1 of relations1) {
            const intermediateId = rel1.toEntityId;
            for (const rel2 of relations2) {
                if (rel2.fromEntityId === intermediateId) {
                    // Found transitive path
                    return {
                        fromEntityId: entity1.id,
                        toEntityId: entity2.id,
                        type: rel1.type,
                        confidence: rel1.strength * rel2.strength * 0.8,
                        reason: `Transitive: ${entity1.name} ${rel1.type} ${this.graph.getEntity(intermediateId)?.name} ${rel2.type} ${entity2.name}`
                    };
                }
            }
        }
        return null;
    }
    /**
     * Infer symmetric relations
     * If A similar-to B, then B similar-to A
     */
    inferSymmetric(entity1, entity2) {
        const relations = this.graph.getRelations(entity1.id, 'out');
        const symmetricTypes = [
            index_1.RelationType.SIMILAR_TO,
            index_1.RelationType.RELATED_TO,
            index_1.RelationType.ALTERNATIVE_TO
        ];
        for (const relation of relations) {
            if (symmetricTypes.includes(relation.type) && relation.toEntityId === entity2.id) {
                // Already exists, no need to infer
                return null;
            }
        }
        // Check if entities share many connections
        const connections1 = this.graph.getRelations(entity1.id, 'both');
        const connections2 = this.graph.getRelations(entity2.id, 'both');
        const commonConnections = connections1.filter(r1 => connections2.some(r2 => r1.toEntityId === r2.toEntityId || r1.fromEntityId === r2.fromEntityId));
        if (commonConnections.length >= 3) {
            const confidence = Math.min(1.0, commonConnections.length / 10);
            return {
                fromEntityId: entity1.id,
                toEntityId: entity2.id,
                type: index_1.RelationType.RELATED_TO,
                confidence,
                reason: `Share ${commonConnections.length} common connections`
            };
        }
        return null;
    }
    /**
     * Infer pattern-based relations
     */
    inferPatternBased(entity1, entity2) {
        const relations = [];
        // Technology pattern: If entity1 is technology and entity2 uses it
        if (entity1.type === graph_types_1.EntityType.TECHNOLOGY && entity2.type === graph_types_1.EntityType.PROJECT) {
            // Check if project description mentions technology
            const description = (entity2.description || '').toLowerCase();
            const techName = entity1.name.toLowerCase();
            if (description.includes(techName)) {
                relations.push({
                    fromEntityId: entity2.id,
                    toEntityId: entity1.id,
                    type: index_1.RelationType.USES,
                    confidence: 0.9,
                    reason: `Project description mentions ${entity1.name}`
                });
            }
        }
        // File pattern: If entity1 is file and entity2 is project
        if (entity1.type === graph_types_1.EntityType.FILE && entity2.type === graph_types_1.EntityType.PROJECT) {
            const filePath = entity1.name.toLowerCase();
            const projectName = entity2.name.toLowerCase();
            if (filePath.includes(projectName)) {
                relations.push({
                    fromEntityId: entity1.id,
                    toEntityId: entity2.id,
                    type: index_1.RelationType.PART_OF,
                    confidence: 0.95,
                    reason: `File path contains project name`
                });
            }
        }
        // Temporal pattern: If entities created close in time
        const timeDiff = Math.abs(entity1.createdAt - entity2.createdAt);
        const daysDiff = timeDiff / (1000 * 60 * 60 * 24);
        if (daysDiff < 1 && entity1.type === entity2.type) {
            relations.push({
                fromEntityId: entity1.id,
                toEntityId: entity2.id,
                type: index_1.RelationType.RELATED_TO,
                confidence: 0.6,
                reason: `Created within 1 day of each other`
            });
        }
        return relations;
    }
    /**
     * Find missing relations
     */
    findMissingRelations() {
        const queryResult = this.graph.queryGraph({});
        const missing = [];
        for (const connected1 of queryResult) {
            for (const connected2 of queryResult) {
                if (connected1.entity.id < connected2.entity.id) {
                    const existingRelations = this.graph.getRelations(connected1.entity.id, 'out')
                        .filter(r => r.toEntityId === connected2.entity.id);
                    if (existingRelations.length === 0) {
                        const inferredList = this.inferRelationPair(connected1.entity, connected2.entity);
                        for (const inferred of inferredList) {
                            missing.push(inferred);
                        }
                    }
                }
            }
        }
        return missing.sort((a, b) => b.confidence - a.confidence);
    }
    /**
     * Suggest relations to create
     */
    suggestRelations(minConfidence = 0.7) {
        const missing = this.findMissingRelations();
        return missing.filter(r => r.confidence >= minConfidence);
    }
    /**
     * Auto-create high-confidence relations
     */
    autoCreateRelations(minConfidence = 0.9) {
        const suggestions = this.suggestRelations(minConfidence);
        let created = 0;
        for (const suggestion of suggestions) {
            this.graph.createRelation(suggestion.fromEntityId, suggestion.toEntityId, suggestion.type, suggestion.confidence, { inferred: true, reason: suggestion.reason });
            created++;
        }
        return created;
    }
}
exports.RelationInferenceEngine = RelationInferenceEngine;
/**
 * Create inference engine for graph
 */
function createInferenceEngine(graph) {
    return new RelationInferenceEngine(graph);
}
//# sourceMappingURL=relation-inference.js.map