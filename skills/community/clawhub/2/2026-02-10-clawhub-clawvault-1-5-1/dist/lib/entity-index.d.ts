interface EntityEntry {
    path: string;
    aliases: string[];
}
interface EntityIndex {
    entries: Map<string, string>;
    byPath: Map<string, EntityEntry>;
}
/**
 * Build an entity index from all markdown files in the vault.
 * Extracts linkable names from:
 * - Filename (without .md)
 * - Frontmatter `title` field
 * - Frontmatter `aliases` array
 */
declare function buildEntityIndex(vaultPath: string): EntityIndex;
/**
 * Get all entities sorted by alias length (longest first)
 * This ensures "Justin Dukes" is matched before "Justin"
 */
declare function getSortedAliases(index: EntityIndex): Array<{
    alias: string;
    path: string;
}>;

export { type EntityEntry, type EntityIndex, buildEntityIndex, getSortedAliases };
