/**
 * ClawVault Types - The elephant's memory structure
 */
interface VaultConfig {
    /** Root path of the vault */
    path: string;
    /** Name of the vault */
    name: string;
    /** Categories to create on init */
    categories: string[];
    /** qmd collection name (defaults to vault name if not set) */
    qmdCollection?: string;
    /** Root path for qmd collection (defaults to vault path) */
    qmdRoot?: string;
    /** Custom templates path (optional) */
    templatesPath?: string;
}
interface VaultMeta {
    name: string;
    version: string;
    created: string;
    lastUpdated: string;
    categories: string[];
    documentCount: number;
    /** qmd collection name (defaults to vault name if not set) */
    qmdCollection?: string;
    /** Root path for qmd collection (defaults to vault path) */
    qmdRoot?: string;
}
interface Document {
    /** Unique ID (relative path without extension) */
    id: string;
    /** Full file path */
    path: string;
    /** Category (folder name) */
    category: string;
    /** Document title */
    title: string;
    /** Raw content */
    content: string;
    /** Frontmatter metadata */
    frontmatter: Record<string, unknown>;
    /** Extracted wiki-links [[like-this]] */
    links: string[];
    /** Tags extracted from content */
    tags: string[];
    /** Last modified timestamp */
    modified: Date;
}
interface SearchResult {
    /** Document that matched */
    document: Document;
    /** Relevance score (0-1) */
    score: number;
    /** Matching snippet */
    snippet: string;
    /** Which terms matched */
    matchedTerms: string[];
}
interface SearchOptions {
    /** Max results to return */
    limit?: number;
    /** Minimum score threshold (0-1) */
    minScore?: number;
    /** Filter by category */
    category?: string;
    /** Filter by tags */
    tags?: string[];
    /** Include full content in results */
    fullContent?: boolean;
}
interface StoreOptions {
    /** Category to store in */
    category: string;
    /** Document title (used for filename) */
    title: string;
    /** Content body */
    content: string;
    /** Frontmatter metadata */
    frontmatter?: Record<string, unknown>;
    /** Override existing file */
    overwrite?: boolean;
    /** Trigger qmd update after storing */
    qmdUpdate?: boolean;
    /** Trigger qmd embed after storing (implies qmdUpdate) */
    qmdEmbed?: boolean;
}
interface SyncOptions {
    /** Target directory to sync to */
    target: string;
    /** Delete files in target not in source */
    deleteOrphans?: boolean;
    /** Dry run - don't actually sync */
    dryRun?: boolean;
}
interface SyncResult {
    copied: string[];
    deleted: string[];
    unchanged: string[];
    errors: string[];
}
type Category = 'preferences' | 'decisions' | 'patterns' | 'people' | 'projects' | 'goals' | 'transcripts' | 'inbox' | 'templates' | 'facts' | 'feelings' | 'lessons' | 'commitments' | 'handoffs' | string;
declare const DEFAULT_CATEGORIES: Category[];
/**
 * Memory Type Taxonomy (Benthic's 8 categories)
 * Knowing WHAT KIND of thing helps you know WHERE to put it
 */
type MemoryType = 'fact' | 'feeling' | 'decision' | 'lesson' | 'commitment' | 'preference' | 'relationship' | 'project';
declare const MEMORY_TYPES: MemoryType[];
/**
 * Memory type to category mapping
 */
declare const TYPE_TO_CATEGORY: Record<MemoryType, Category>;
/**
 * Handoff document - bridges sessions
 */
interface HandoffDocument {
    /** When this handoff was created */
    created: string;
    /** Session key or identifier */
    sessionKey?: string;
    /** What I was working on */
    workingOn: string[];
    /** What is currently blocked */
    blocked: string[];
    /** What comes next */
    nextSteps: string[];
    /** Emotional state/energy */
    feeling?: string;
    /** Key decisions made */
    decisions?: string[];
    /** Open questions */
    openQuestions?: string[];
}
/**
 * Session recap - who I was when I woke up
 */
interface SessionRecap {
    /** When recap was generated */
    generated: string;
    /** Recent handoffs (last N) */
    recentHandoffs: HandoffDocument[];
    /** Active projects */
    activeProjects: string[];
    /** Pending commitments */
    pendingCommitments: string[];
    /** Recent decisions made */
    recentDecisions?: string[];
    /** Recent lessons learned */
    recentLessons: string[];
    /** Key relationships to remember */
    keyRelationships: string[];
    /** Current emotional arc */
    emotionalArc?: string;
}
declare const DEFAULT_CONFIG: Partial<VaultConfig>;

export { type Category as C, type Document as D, type HandoffDocument as H, type MemoryType as M, type StoreOptions as S, TYPE_TO_CATEGORY as T, type VaultConfig as V, type SearchOptions as a, type SearchResult as b, type SyncOptions as c, type SyncResult as d, type SessionRecap as e, DEFAULT_CATEGORIES as f, DEFAULT_CONFIG as g, MEMORY_TYPES as h, type VaultMeta as i };
