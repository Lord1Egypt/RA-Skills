import type { Chat } from '../types/chat.types.js';
import { type DocExtractRaw, type PromptCtx, type ResolveResult } from '../types/doc-extract.types.js';
import type { EntityRow } from '../types/primitives.types.js';
import { slugify } from './normalize.js';
export { slugify };
export declare const conceptId: (docPath: string, slug: string, source_id?: number | string) => string;
export declare const buildUserPrompt: (ctx: PromptCtx) => string;
export declare const resolveExtraction: (raw: DocExtractRaw, docPath: string, codeEntities: Pick<EntityRow, "id" | "name">[], source_id?: number | string) => ResolveResult;
export declare const extractDoc: (chat: Chat, ctx: PromptCtx & {
    source_id?: number | string;
}) => Promise<{
    raw: DocExtractRaw;
    resolved: ResolveResult;
}>;
