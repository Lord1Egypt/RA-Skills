export type SourceId = number;
export type FileId = number;
export type ChunkId = number;
export type EntityId = string;
export type SourceKind = 'web' | 'code' | 'file' | 'text' | 'pdf';
export type EmbedModel = 'nomic-embed-text';
export type EntityKind = 'function' | 'struct' | 'enum' | 'constant' | 'concept';
export type EdgeRelation = 'calls' | 'defines' | 'verifies' | 'references' | 'depends_on' | 'evolved_from' | 'mitigates';
export type EdgeDerive = 'parse' | 'doc';
export type Embedding = Float32Array;
export interface Chunk {
    content: string;
    start_line: number;
    end_line: number;
}
export interface SourceRow {
    id: SourceId;
    kind: SourceKind;
    uri: string;
    label: string | null;
    embed_model: EmbedModel;
    added_at: number;
    last_indexed_at: number;
}
export interface FileRow {
    id: FileId;
    source_id: SourceId;
    path: string;
    hash: string;
    mtime: number;
    lang: string | null;
}
export interface ChunkRow {
    id: ChunkId;
    file_id: FileId;
    content: string;
    start_line: number;
    end_line: number;
}
export interface EntityRow {
    id: EntityId;
    kind: EntityKind;
    name: string;
    source: string | null;
    line_start: number | null;
    line_end: number | null;
    created_at: number;
    removed_at: number | null;
}
export interface EdgeRow {
    from_id: EntityId;
    to_id: EntityId;
    relation: EdgeRelation;
    confidence: number;
    derive: EdgeDerive;
}
