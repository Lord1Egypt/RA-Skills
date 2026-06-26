/**
 * Knowledge Graph Core
 * Main graph management and operations
 *
 * Phase 5 Enhancement - Step 1: Graph Memory
 */
import { GraphEntity, GraphRelation, GraphQuery, GraphPath, GraphStats, ConnectedEntity, EntityType, RelationType } from './graph-types';
/**
 * Knowledge Graph Class
 *
 * Features:
 * - Entity management
 * - Relationship management
 * - Graph traversal
 * - Path finding
 * - Pattern matching
 */
export declare class KnowledgeGraph {
    private entities;
    private relations;
    private entityIndex;
    /**
     * Create entity
     */
    createEntity(name: string, type: EntityType, description?: string, properties?: Record<string, any>): GraphEntity;
    /**
     * Get entity by ID
     */
    getEntity(entityId: string): GraphEntity | null;
    /**
     * Find entities by name
     */
    findEntitiesByName(name: string): GraphEntity[];
    /**
     * Update entity
     */
    updateEntity(entityId: string, updates: Partial<GraphEntity>): GraphEntity | null;
    /**
     * Delete entity
     */
    deleteEntity(entityId: string): boolean;
    /**
     * Create relationship
     */
    createRelation(fromEntityId: string, toEntityId: string, type: RelationType, strength?: number, properties?: Record<string, any>): GraphRelation | null;
    /**
     * Get relations for entity
     */
    getRelations(entityId: string, direction?: 'in' | 'out' | 'both'): GraphRelation[];
    /**
     * Update relation
     */
    updateRelation(relationId: string, updates: Partial<GraphRelation>): GraphRelation | null;
    /**
     * Delete relation
     */
    deleteRelation(relationId: string): boolean;
    /**
     * Query graph
     */
    queryGraph(query: GraphQuery): ConnectedEntity[];
    /**
     * Get connected entity
     */
    private getConnectedEntity;
    /**
     * Find path between entities
     */
    findPath(fromEntityId: string, toEntityId: string, maxDepth?: number): GraphPath | null;
    /**
     * Get graph statistics
     */
    getStats(): GraphStats;
    /**
     * Export graph to JSON
     */
    exportToJSON(): string;
    /**
     * Import graph from JSON
     */
    importFromJSON(jsonString: string): number;
    /**
     * Clear graph
     */
    clear(): void;
    /**
     * Generate unique ID
     */
    private generateId;
}
/**
 * Default knowledge graph instance
 */
export declare const defaultKnowledgeGraph: KnowledgeGraph;
//# sourceMappingURL=knowledge-graph.d.ts.map