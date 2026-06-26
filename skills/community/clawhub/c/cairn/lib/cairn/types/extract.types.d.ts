import type { EdgeDerive, EdgeRelation, EntityId, EntityKind } from './primitives.types.js';
export interface ExtractedEntity {
    id: EntityId;
    kind: EntityKind;
    name: string;
    line_start: number;
    line_end: number;
}
export interface ExtractedEdge {
    from_id: EntityId;
    to_id: EntityId;
    relation: EdgeRelation;
    confidence: number;
    derive: EdgeDerive;
}
export interface ExtractedFile {
    entities: ExtractedEntity[];
    fnCalls: Map<string, Set<string>>;
    fnRefs: Map<string, Set<string>>;
}
export type EntityParser = (content: string, filePath: string) => ExtractedFile;
export interface PerFileForEdges {
    filePath: string;
    content: string;
    entities: ExtractedEntity[];
    fnCalls: Map<string, Set<string>>;
    fnRefs: Map<string, Set<string>>;
}
