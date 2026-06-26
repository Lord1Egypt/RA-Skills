import type Database from 'better-sqlite3';
import type { ChunkId, ChunkRow, Embedding, EmbedModel, EntityId, EntityKind, EntityRow, EdgeRelation, EdgeDerive, EdgeRow, FileId, FileRow, SourceId, SourceKind, SourceRow } from './primitives.types.js';
import type { ListFilter } from './cairn.types.js';
export interface InsertSourceInput {
    kind: SourceKind;
    uri: string;
    label: string | null;
    embed_model: EmbedModel;
    ts: number;
}
export interface UpsertFileInput {
    source_id: SourceId;
    path: string;
    hash: string;
    mtime: number;
    lang: string | null;
}
export interface UpsertFileResult {
    file_id: FileId;
    changed: boolean;
}
export interface SearchHitRaw {
    chunk_id: ChunkId;
    rank: number;
}
export interface SearchFilter {
    source_id?: SourceId;
    kind?: SourceKind;
}
export interface HydratedHit {
    chunk: ChunkRow;
    file: FileRow;
    source: SourceRow;
}
export interface UpsertEntityInput {
    id: EntityId;
    source_id: SourceId;
    kind: EntityKind;
    name: string;
    source: string | null;
    line_start: number | null;
    line_end: number | null;
    embedding: Embedding;
}
export interface UpsertEdgeInput {
    from_id: EntityId;
    to_id: EntityId;
    relation: EdgeRelation;
    confidence: number;
    derive: EdgeDerive;
}
export interface Db {
    insertSource(input: InsertSourceInput): SourceRow;
    getSource(ref: SourceId | string): SourceRow | null;
    listSources(filter?: ListFilter): SourceRow[];
    deleteSource(id: SourceId): void;
    touchSource(id: SourceId, ts: number): void;
    upsertFile(input: UpsertFileInput): UpsertFileResult;
    getFile(source_id: SourceId, path: string): FileRow | null;
    listFiles(source_id: SourceId): FileRow[];
    deleteFilesNotIn(source_id: SourceId, paths: string[]): FileId[];
    clearFileHashes(source_id: SourceId): void;
    replaceChunks(file_id: FileId, chunks: {
        content: string;
        start_line: number;
        end_line: number;
    }[], embeddings: Embedding[]): ChunkId[];
    deleteChunksForFile(file_id: FileId): number;
    upsertEntity(input: UpsertEntityInput): {
        rowid: number;
        inserted: boolean;
    };
    getEntity(id: EntityId): EntityRow | null;
    getEntitiesBySource(source: string): EntityRow[];
    getActiveEntitiesForSource(source_id: SourceId): EntityRow[];
    searchEntitiesByEmbedding(queryVec: Embedding, k: number): EntityRow[];
    softDeleteEntity(id: EntityId): void;
    deleteEntity(id: EntityId): void;
    softDeleteMissingEntities(source: string, keepIds: Set<EntityId>): number;
    upsertEdges(edges: UpsertEdgeInput[]): void;
    getEdges(entityId: EntityId): EdgeRow[];
    getEdgesInbound(entityId: EntityId): EdgeRow[];
    getEdgesForMany(ids: EntityId[]): Map<EntityId, EdgeRow[]>;
    getEdgesInboundForMany(ids: EntityId[]): Map<EntityId, EdgeRow[]>;
    deleteParseEdgesForSources(paths: string[]): number;
    deleteDocEdgesForSource(path: string): number;
    getDocExtractedHash(file_id: FileId): string | null;
    setDocExtractedHash(file_id: FileId, hash: string): void;
    replaceEntityTags(entity_id: EntityId, tags: string[]): void;
    getTagsForEntity(entity_id: EntityId): string[];
    getEntitiesByTag(tag: string, k?: number): EntityRow[];
    getTagsForMany(ids: EntityId[]): Map<EntityId, string[]>;
    listTags(): Array<{
        tag: string;
        count: number;
    }>;
    addSourceLink(from: SourceId, to: SourceId): void;
    removeSourceLink(from: SourceId, to: SourceId): void;
    listSourceLinks(): Array<{
        from: SourceId;
        to: SourceId;
    }>;
    getSourcesLinkedFrom(from: SourceId): SourceId[];
    getSourcesLinkingTo(to: SourceId): SourceId[];
    get rawDb(): Database.Database;
    searchFts(query: string, k: number, filter?: SearchFilter): SearchHitRaw[];
    searchVec(queryVec: Embedding, k: number, filter?: SearchFilter): SearchHitRaw[];
    hydrate(chunkIds: ChunkId[]): Map<ChunkId, HydratedHit>;
    close(): void;
}
