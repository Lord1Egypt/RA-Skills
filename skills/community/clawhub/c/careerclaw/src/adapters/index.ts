/**
 * adapters/index.ts — Public adapter API.
 *
 * Import adapters from here rather than individual files.
 * sources.ts (Phase 3) will use fetchAll() to merge results.
 */

export { fetchRemoteOkJobs, parseRss, stripHtml, stableId } from "./remoteok.js";
export { fetchHnJobs, parseComment } from "./hackernews.js";
export type { HnItem } from "./hackernews.js";
