import type { AskHit, AskOptions, GraphHit, GraphQuery, Hit, ListFilter, PathOptions, PathResult, SearchOptions, TagCount } from '../types/cairn.types.js';
import type { Db } from '../types/db.types.js';
import type { Embed } from '../types/embed.types.js';
import type { EntityId, SourceRow } from '../types/primitives.types.js';
import type { Retrieve } from '../types/retrieve.types.js';
export declare class RetrieveProvider implements Retrieve {
    private db;
    private embed;
    constructor(db: Db, embed: Embed);
    search(query: string, opts?: SearchOptions): Promise<Hit[]>;
    private taggedFileSet;
    list(filter?: ListFilter): Promise<SourceRow[]>;
    graph(input: GraphQuery): Promise<GraphHit[]>;
    ask(query: string, opts?: AskOptions): Promise<AskHit[]>;
    listTags(): Promise<TagCount[]>;
    path(from: EntityId, to: EntityId, opts?: PathOptions): Promise<PathResult | null>;
    private reconstructPath;
    private buildGraphHit;
    private buildFilter;
    private resolveSourceId;
}
