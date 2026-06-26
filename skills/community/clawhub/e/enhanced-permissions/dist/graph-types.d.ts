/**
 * Knowledge Graph Data Structures
 * Core types for memory knowledge graph
 *
 * Phase 5 Enhancement - Step 1: Graph Memory
 */
/**
 * Entity types in knowledge graph
 */
export declare enum EntityType {
    CONCEPT = "concept",// Abstract concept (TypeScript, React)
    PROJECT = "project",// Project (Project-X)
    PERSON = "person",// Person (developer, user)
    ORGANIZATION = "org",// Organization (company, team)
    TECHNOLOGY = "technology",// Technology stack
    FILE = "file",// File path
    URL = "url",// URL/Link
    CODE = "code",// Code snippet
    MEMORY = "memory"
}
/**
 * Relationship types
 */
export declare enum RelationType {
    CONTAINS = "contains",
    PART_OF = "part_of",
    INSTANCE_OF = "instance_of",
    DEPENDS_ON = "depends_on",
    REQUIRES = "requires",
    USES = "uses",
    SIMILAR_TO = "similar_to",
    RELATED_TO = "related_to",
    ALTERNATIVE_TO = "alternative_to",
    CREATED_BEFORE = "created_before",
    CREATED_AFTER = "created_after",
    UPDATED_BY = "updated_by",
    CAUSES = "causes",
    ENABLES = "enables",
    PREVENTS = "prevents",
    CREATED_BY = "created_by",
    OWNED_BY = "owned_by",
    USED_BY = "used_by",
    CUSTOM = "custom"
}
/**
 * Graph entity interface
 */
export interface GraphEntity {
    id: string;
    type: EntityType;
    name: string;
    description?: string;
    properties: Record<string, any>;
    memoryIds: string[];
    createdAt: number;
    updatedAt: number;
}
/**
 * Graph relationship interface
 */
export interface GraphRelation {
    id: string;
    fromEntityId: string;
    toEntityId: string;
    type: RelationType;
    customType?: string;
    strength: number;
    properties: Record<string, any>;
    createdAt: number;
    updatedAt: number;
}
/**
 * Graph query interface
 */
export interface GraphQuery {
    entity?: string;
    entityType?: EntityType;
    relationType?: RelationType;
    direction?: 'in' | 'out' | 'both';
    maxDepth?: number;
    limit?: number;
}
/**
 * Path in graph
 */
export interface GraphPath {
    startEntity: GraphEntity;
    endEntity: GraphEntity;
    relations: GraphRelation[];
    entities: GraphEntity[];
    length: number;
}
/**
 * Graph statistics
 */
export interface GraphStats {
    totalEntities: number;
    totalRelations: number;
    entitiesByType: Record<EntityType, number>;
    relationsByType: Record<RelationType, number>;
    averageRelationsPerEntity: number;
    density: number;
}
/**
 * Entity with connections
 */
export interface ConnectedEntity {
    entity: GraphEntity;
    incomingRelations: GraphRelation[];
    outgoingRelations: GraphRelation[];
    connectedEntities: GraphEntity[];
}
//# sourceMappingURL=graph-types.d.ts.map