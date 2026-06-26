import type { AskHit, AskOptions, GraphHit, GraphQuery, Hit, ListFilter, PathOptions, PathResult, SearchOptions, TagCount } from './cairn.types.js';
import type { EntityId, SourceRow } from './primitives.types.js';
export interface Retrieve {
    search(query: string, opts?: SearchOptions): Promise<Hit[]>;
    list(filter?: ListFilter): Promise<SourceRow[]>;
    graph(input: GraphQuery): Promise<GraphHit[]>;
    ask(query: string, opts?: AskOptions): Promise<AskHit[]>;
    path(from: EntityId, to: EntityId, opts?: PathOptions): Promise<PathResult | null>;
    listTags(): Promise<TagCount[]>;
}
