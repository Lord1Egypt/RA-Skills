import type { EmbedModel, EntityId, SourceId, SourceKind, SourceRow, EntityRow, EdgeRow, ChunkId } from './primitives.types.js';
export type CairnRuntime = 'embedded' | 'ollama';
export interface CairnOptions {
    dbPath?: string;
    runtime?: CairnRuntime;
    ollamaUrl?: string;
    embedModel?: EmbedModel;
    chatModel?: string;
    modelCacheDir?: string;
}
export type AddInput = {
    kind: 'web';
    url: string;
    label?: string;
} | {
    kind: 'code';
    path: string;
    label?: string;
    include?: string[];
    exclude?: string[];
    force?: boolean;
} | {
    kind: 'file';
    path: string;
    label?: string;
} | {
    kind: 'text';
    content: string;
    label?: string;
} | {
    kind: 'pdf';
    path: string;
    label?: string;
};
export interface AddResult {
    source_id: SourceId;
    files_indexed: number;
    chunks_created: number;
}
export interface RefreshResult {
    source_id: SourceId;
    files_changed: number;
    files_unchanged: number;
    chunks_created: number;
    chunks_deleted: number;
}
export interface SearchOptions {
    k?: number;
    source?: SourceId | string;
    kind?: SourceKind;
    tag?: string;
}
export interface Hit {
    chunk_id: ChunkId;
    source: SourceRow;
    file_path: string;
    start_line: number;
    end_line: number;
    content: string;
    score: number;
    fts_rank: number | null;
    vec_rank: number | null;
}
export interface EntityWithEdges {
    entity: EntityRow;
    edges_out: EdgeRow[];
    edges_in: EdgeRow[];
    tags: string[];
}
export interface AskHit extends Hit {
    entities: EntityWithEdges[];
}
export interface AskOptions extends SearchOptions {
    maxEntitiesPerHit?: number;
    maxEdgesPerEntity?: number;
}
export interface PathOptions {
    maxDepth?: number;
    directed?: boolean;
}
export interface PathStep {
    edge: EdgeRow;
    reversed: boolean;
}
export interface PathResult {
    entities: EntityRow[];
    steps: PathStep[];
}
export interface ListFilter {
    kind?: SourceKind;
}
export interface GraphQuery {
    query?: string;
    entity_id?: EntityId;
    k?: number;
    tag?: string;
}
export interface GraphHit {
    entity: EntityRow;
    edges_out: EdgeRow[];
    edges_in: EdgeRow[];
    tags: string[];
    score: number | null;
}
export interface TagCount {
    tag: string;
    count: number;
}
