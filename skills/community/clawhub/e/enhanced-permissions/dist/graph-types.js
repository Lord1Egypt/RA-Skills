"use strict";
/**
 * Knowledge Graph Data Structures
 * Core types for memory knowledge graph
 *
 * Phase 5 Enhancement - Step 1: Graph Memory
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.RelationType = exports.EntityType = void 0;
/**
 * Entity types in knowledge graph
 */
var EntityType;
(function (EntityType) {
    EntityType["CONCEPT"] = "concept";
    EntityType["PROJECT"] = "project";
    EntityType["PERSON"] = "person";
    EntityType["ORGANIZATION"] = "org";
    EntityType["TECHNOLOGY"] = "technology";
    EntityType["FILE"] = "file";
    EntityType["URL"] = "url";
    EntityType["CODE"] = "code";
    EntityType["MEMORY"] = "memory"; // Regular memory
})(EntityType || (exports.EntityType = EntityType = {}));
/**
 * Relationship types
 */
var RelationType;
(function (RelationType) {
    // Hierarchical
    RelationType["CONTAINS"] = "contains";
    RelationType["PART_OF"] = "part_of";
    RelationType["INSTANCE_OF"] = "instance_of";
    // Dependency
    RelationType["DEPENDS_ON"] = "depends_on";
    RelationType["REQUIRES"] = "requires";
    RelationType["USES"] = "uses";
    // Similarity
    RelationType["SIMILAR_TO"] = "similar_to";
    RelationType["RELATED_TO"] = "related_to";
    RelationType["ALTERNATIVE_TO"] = "alternative_to";
    // Temporal
    RelationType["CREATED_BEFORE"] = "created_before";
    RelationType["CREATED_AFTER"] = "created_after";
    RelationType["UPDATED_BY"] = "updated_by";
    // Causal
    RelationType["CAUSES"] = "causes";
    RelationType["ENABLES"] = "enables";
    RelationType["PREVENTS"] = "prevents";
    // Attribution
    RelationType["CREATED_BY"] = "created_by";
    RelationType["OWNED_BY"] = "owned_by";
    RelationType["USED_BY"] = "used_by";
    // Custom
    RelationType["CUSTOM"] = "custom";
})(RelationType || (exports.RelationType = RelationType = {}));
//# sourceMappingURL=graph-types.js.map