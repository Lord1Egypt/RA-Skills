import { EntityIndex } from './entity-index.js';

/**
 * Auto-link entities in markdown content.
 * Only links first occurrence of each entity.
 * Skips protected ranges (frontmatter, code, existing links, URLs).
 */
declare function autoLink(content: string, index: EntityIndex): string;
/**
 * Show what would be linked (dry run)
 */
declare function dryRunLink(content: string, index: EntityIndex): Array<{
    alias: string;
    path: string;
    line: number;
}>;
/**
 * Find unlinked mentions of entities (suggested links).
 */
declare function findUnlinkedMentions(content: string, index: EntityIndex): Array<{
    alias: string;
    path: string;
    line: number;
}>;

export { autoLink, dryRunLink, findUnlinkedMentions };
