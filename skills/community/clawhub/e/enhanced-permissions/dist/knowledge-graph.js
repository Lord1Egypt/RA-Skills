"use strict";
/**
 * Knowledge Graph Core
 * Main graph management and operations
 *
 * Phase 5 Enhancement - Step 1: Graph Memory
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.defaultKnowledgeGraph = exports.KnowledgeGraph = void 0;
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
class KnowledgeGraph {
    constructor() {
        this.entities = new Map();
        this.relations = new Map();
        this.entityIndex = new Map(); // name -> entity IDs
    }
    /**
     * Create entity
     */
    createEntity(name, type, description, properties = {}) {
        const now = Date.now();
        const entity = {
            id: this.generateId('ent'),
            type,
            name,
            description,
            properties,
            memoryIds: [],
            createdAt: now,
            updatedAt: now
        };
        this.entities.set(entity.id, entity);
        // Index by name
        const lowerName = name.toLowerCase();
        if (!this.entityIndex.has(lowerName)) {
            this.entityIndex.set(lowerName, []);
        }
        this.entityIndex.get(lowerName).push(entity.id);
        return entity;
    }
    /**
     * Get entity by ID
     */
    getEntity(entityId) {
        return this.entities.get(entityId) || null;
    }
    /**
     * Find entities by name
     */
    findEntitiesByName(name) {
        const lowerName = name.toLowerCase();
        const ids = this.entityIndex.get(lowerName) || [];
        return ids.map(id => this.entities.get(id)).filter(Boolean);
    }
    /**
     * Update entity
     */
    updateEntity(entityId, updates) {
        const entity = this.entities.get(entityId);
        if (!entity)
            return null;
        Object.assign(entity, updates, { updatedAt: Date.now() });
        this.entities.set(entityId, entity);
        return entity;
    }
    /**
     * Delete entity
     */
    deleteEntity(entityId) {
        const entity = this.entities.get(entityId);
        if (!entity)
            return false;
        // Remove relations
        const relationsToRemove = Array.from(this.relations.values())
            .filter(r => r.fromEntityId === entityId || r.toEntityId === entityId);
        relationsToRemove.forEach(r => this.relations.delete(r.id));
        // Remove from index
        const lowerName = entity.name.toLowerCase();
        const ids = this.entityIndex.get(lowerName) || [];
        const filteredIds = ids.filter(id => id !== entityId);
        if (filteredIds.length === 0) {
            this.entityIndex.delete(lowerName);
        }
        else {
            this.entityIndex.set(lowerName, filteredIds);
        }
        // Remove entity
        this.entities.delete(entityId);
        return true;
    }
    /**
     * Create relationship
     */
    createRelation(fromEntityId, toEntityId, type, strength = 1.0, properties = {}) {
        const fromEntity = this.entities.get(fromEntityId);
        const toEntity = this.entities.get(toEntityId);
        if (!fromEntity || !toEntity)
            return null;
        const now = Date.now();
        const relation = {
            id: this.generateId('rel'),
            fromEntityId,
            toEntityId,
            type,
            strength: Math.min(1, Math.max(0, strength)),
            properties,
            createdAt: now,
            updatedAt: now
        };
        this.relations.set(relation.id, relation);
        return relation;
    }
    /**
     * Get relations for entity
     */
    getRelations(entityId, direction = 'both') {
        return Array.from(this.relations.values()).filter(r => {
            if (direction === 'out')
                return r.fromEntityId === entityId;
            if (direction === 'in')
                return r.toEntityId === entityId;
            return r.fromEntityId === entityId || r.toEntityId === entityId;
        });
    }
    /**
     * Update relation
     */
    updateRelation(relationId, updates) {
        const relation = this.relations.get(relationId);
        if (!relation)
            return null;
        Object.assign(relation, updates, { updatedAt: Date.now() });
        this.relations.set(relationId, relation);
        return relation;
    }
    /**
     * Delete relation
     */
    deleteRelation(relationId) {
        return this.relations.delete(relationId);
    }
    /**
     * Query graph
     */
    queryGraph(query) {
        const results = [];
        // Find matching entities
        let matchingEntities = [];
        if (query.entity) {
            // Search by ID or name
            const byId = this.entities.get(query.entity);
            const byName = this.findEntitiesByName(query.entity);
            matchingEntities = [...(byId ? [byId] : []), ...byName];
        }
        else {
            matchingEntities = Array.from(this.entities.values());
        }
        // Filter by type
        if (query.entityType) {
            matchingEntities = matchingEntities.filter(e => e.type === query.entityType);
        }
        // Get connections for each entity
        for (const entity of matchingEntities.slice(0, query.limit || 100)) {
            const connected = this.getConnectedEntity(entity.id, query);
            if (connected) {
                results.push(connected);
            }
        }
        return results;
    }
    /**
     * Get connected entity
     */
    getConnectedEntity(entityId, query) {
        const entity = this.entities.get(entityId);
        if (!entity)
            return null;
        const relations = this.getRelations(entityId, query.direction || 'both');
        // Filter by relation type
        let filteredRelations = relations;
        if (query.relationType) {
            filteredRelations = relations.filter(r => r.type === query.relationType);
        }
        // Get connected entities
        const connectedEntityIds = new Set();
        filteredRelations.forEach(r => {
            connectedEntityIds.add(r.fromEntityId === entityId ? r.toEntityId : r.fromEntityId);
        });
        const connectedEntities = Array.from(connectedEntityIds)
            .map(id => this.entities.get(id))
            .filter(Boolean);
        return {
            entity,
            incomingRelations: filteredRelations.filter(r => r.toEntityId === entityId),
            outgoingRelations: filteredRelations.filter(r => r.fromEntityId === entityId),
            connectedEntities
        };
    }
    /**
     * Find path between entities
     */
    findPath(fromEntityId, toEntityId, maxDepth = 5) {
        const fromEntity = this.entities.get(fromEntityId);
        const toEntity = this.entities.get(toEntityId);
        if (!fromEntity || !toEntity)
            return null;
        // BFS to find shortest path
        const queue = [{
                entityId: fromEntityId,
                path: [],
                visited: new Set([fromEntityId])
            }];
        while (queue.length > 0 && queue[0].path.length < maxDepth) {
            const current = queue.shift();
            // Get outgoing relations
            const relations = this.getRelations(current.entityId, 'out');
            for (const relation of relations) {
                const nextEntityId = relation.toEntityId;
                if (nextEntityId === toEntityId) {
                    // Found path
                    const entities = [fromEntity];
                    const path = [...current.path, relation];
                    // Collect entities in path
                    let currentId = fromEntityId;
                    for (const rel of path) {
                        if (rel.fromEntityId === currentId) {
                            const next = this.entities.get(rel.toEntityId);
                            if (next)
                                entities.push(next);
                            currentId = rel.toEntityId;
                        }
                    }
                    return {
                        startEntity: fromEntity,
                        endEntity: toEntity,
                        relations: path,
                        entities,
                        length: path.length
                    };
                }
                if (!current.visited.has(nextEntityId)) {
                    queue.push({
                        entityId: nextEntityId,
                        path: [...current.path, relation],
                        visited: new Set([...current.visited, nextEntityId])
                    });
                }
            }
        }
        return null; // No path found
    }
    /**
     * Get graph statistics
     */
    getStats() {
        const entities = Array.from(this.entities.values());
        const relations = Array.from(this.relations.values());
        const entitiesByType = entities.reduce((acc, e) => {
            acc[e.type] = (acc[e.type] || 0) + 1;
            return acc;
        }, {});
        const relationsByType = relations.reduce((acc, r) => {
            acc[r.type] = (acc[r.type] || 0) + 1;
            return acc;
        }, {});
        const totalEntities = entities.length;
        const totalRelations = relations.length;
        const averageRelationsPerEntity = totalEntities > 0 ? totalRelations / totalEntities : 0;
        // Density = actual relations / possible relations
        const maxRelations = totalEntities * (totalEntities - 1);
        const density = maxRelations > 0 ? totalRelations / maxRelations : 0;
        return {
            totalEntities,
            totalRelations,
            entitiesByType,
            relationsByType,
            averageRelationsPerEntity,
            density
        };
    }
    /**
     * Export graph to JSON
     */
    exportToJSON() {
        return JSON.stringify({
            entities: Array.from(this.entities.values()),
            relations: Array.from(this.relations.values()),
            exportedAt: new Date().toISOString()
        }, null, 2);
    }
    /**
     * Import graph from JSON
     */
    importFromJSON(jsonString) {
        try {
            const data = JSON.parse(jsonString);
            let importedCount = 0;
            // Import entities
            if (Array.isArray(data.entities)) {
                for (const entityData of data.entities) {
                    this.entities.set(entityData.id, entityData);
                    // Index by name
                    const lowerName = entityData.name.toLowerCase();
                    if (!this.entityIndex.has(lowerName)) {
                        this.entityIndex.set(lowerName, []);
                    }
                    this.entityIndex.get(lowerName).push(entityData.id);
                    importedCount++;
                }
            }
            // Import relations
            if (Array.isArray(data.relations)) {
                for (const relationData of data.relations) {
                    this.relations.set(relationData.id, relationData);
                }
            }
            return importedCount;
        }
        catch {
            return 0;
        }
    }
    /**
     * Clear graph
     */
    clear() {
        this.entities.clear();
        this.relations.clear();
        this.entityIndex.clear();
    }
    /**
     * Generate unique ID
     */
    generateId(prefix) {
        return `${prefix}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }
}
exports.KnowledgeGraph = KnowledgeGraph;
/**
 * Default knowledge graph instance
 */
exports.defaultKnowledgeGraph = new KnowledgeGraph();
//# sourceMappingURL=knowledge-graph.js.map