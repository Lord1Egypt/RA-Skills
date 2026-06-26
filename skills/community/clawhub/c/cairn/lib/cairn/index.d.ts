import type { CairnOptions, CairnRuntime } from './types/cairn.types.js';
import type { Chat } from './types/chat.types.js';
import type { Db } from './types/db.types.js';
import type { Embed } from './types/embed.types.js';
import type { Ingest } from './types/ingest.types.js';
import type { Retrieve } from './types/retrieve.types.js';
export declare class Cairn {
    readonly db: Db;
    readonly embed: Embed;
    readonly chat: Chat;
    readonly ingest: Ingest;
    readonly retrieve: Retrieve;
    readonly runtime: CairnRuntime;
    constructor(opts?: CairnOptions);
    close(): void;
}
export type * from './types/cairn.types.js';
export type * from './types/primitives.types.js';
export type { Db, UpsertEntityInput, UpsertEdgeInput } from './types/db.types.js';
export type { Chat, ChatRuntime } from './types/chat.types.js';
export type { Embed, EmbedRuntime } from './types/embed.types.js';
export type { Ingest } from './types/ingest.types.js';
export type { Retrieve } from './types/retrieve.types.js';
