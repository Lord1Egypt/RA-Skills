import type { AddInput, AddResult, RefreshResult } from './cairn.types.js';
import type { SourceId } from './primitives.types.js';
export interface Ingest {
    add(input: AddInput): Promise<AddResult>;
    remove(source: SourceId | string): Promise<void>;
    refresh(source: SourceId | string | 'all'): Promise<RefreshResult[]>;
    reindex(source: SourceId | string | 'all'): Promise<RefreshResult[]>;
    link(from: SourceId | string, to: SourceId | string): Promise<void>;
    unlink(from: SourceId | string, to: SourceId | string): Promise<void>;
    links(): Promise<Array<{
        from: SourceId;
        to: SourceId;
    }>>;
}
