import { V as VaultConfig, S as StoreOptions, D as Document, a as SearchOptions, b as SearchResult, c as SyncOptions, d as SyncResult, C as Category, M as MemoryType, H as HandoffDocument, e as SessionRecap } from './types-DO8rJ490.js';
export { f as DEFAULT_CATEGORIES, g as DEFAULT_CONFIG, h as MEMORY_TYPES, T as TYPE_TO_CATEGORY, i as VaultMeta } from './types-DO8rJ490.js';
export { setupCommand } from './commands/setup.js';
export { TemplateVariables, buildTemplateVariables, renderTemplate } from './lib/template-engine.js';

/**
 * ClawVault - The elephant's memory
 */

declare class ClawVault {
    private config;
    private search;
    private initialized;
    constructor(vaultPath: string);
    /**
     * Initialize a new vault
     */
    init(options?: Partial<VaultConfig>): Promise<void>;
    /**
     * Load an existing vault
     */
    load(): Promise<void>;
    /**
     * Reindex all documents
     */
    reindex(): Promise<number>;
    /**
     * Load a document from disk
     */
    private loadDocument;
    /**
     * Store a new document
     */
    store(options: StoreOptions): Promise<Document>;
    /**
     * Quick store to inbox
     */
    capture(note: string, title?: string): Promise<Document>;
    /**
     * Search the vault (BM25 via qmd)
     */
    find(query: string, options?: SearchOptions): Promise<SearchResult[]>;
    /**
     * Semantic/vector search (via qmd vsearch)
     */
    vsearch(query: string, options?: SearchOptions): Promise<SearchResult[]>;
    /**
     * Combined search with query expansion (via qmd query)
     */
    query(query: string, options?: SearchOptions): Promise<SearchResult[]>;
    /**
     * Get a document by ID or path
     */
    get(idOrPath: string): Promise<Document | null>;
    /**
     * List documents in a category
     */
    list(category?: string): Promise<Document[]>;
    /**
     * Sync vault to another location (for Obsidian on Windows, etc.)
     */
    sync(options: SyncOptions): Promise<SyncResult>;
    /**
     * Get vault statistics
     */
    stats(): Promise<{
        documents: number;
        categories: {
            [key: string]: number;
        };
        links: number;
        tags: string[];
    }>;
    /**
     * Get all categories
     */
    getCategories(): Category[];
    /**
     * Check if vault is initialized
     */
    isInitialized(): boolean;
    /**
     * Get vault path
     */
    getPath(): string;
    /**
     * Get vault name
     */
    getName(): string;
    /**
     * Get qmd collection name
     */
    getQmdCollection(): string;
    /**
     * Get qmd collection root
     */
    getQmdRoot(): string;
    /**
     * Store a memory with type classification
     * Automatically routes to correct category based on type
     */
    remember(type: MemoryType, title: string, content: string, frontmatter?: Record<string, unknown>): Promise<Document>;
    /**
     * Create a session handoff document
     * Call this before context death or long pauses
     */
    createHandoff(handoff: Omit<HandoffDocument, 'created'>): Promise<Document>;
    /**
     * Format handoff as readable markdown
     */
    private formatHandoff;
    /**
     * Generate a session recap - who I was
     * Call this on bootstrap to restore context
     */
    generateRecap(options?: {
        handoffLimit?: number;
        brief?: boolean;
    }): Promise<SessionRecap>;
    /**
     * Format recap as readable markdown for injection
     */
    formatRecap(recap: SessionRecap, options?: {
        brief?: boolean;
    }): string;
    /**
     * Parse a handoff document back into structured form
     */
    private parseHandoff;
    private applyQmdConfig;
    private slugify;
    private saveIndex;
    private createTemplates;
    private generateReadme;
    private getCategoryDescription;
}
/**
 * Find and open the nearest vault (walks up directory tree)
 */
declare function findVault(startPath?: string): Promise<ClawVault | null>;
/**
 * Create a new vault
 */
declare function createVault(vaultPath: string, options?: Partial<VaultConfig>): Promise<ClawVault>;

/**
 * ClawVault Search Engine - qmd Backend
 * Uses qmd CLI for BM25 and vector search
 */

declare const QMD_INSTALL_URL = "https://github.com/tobi/qmd";
declare const QMD_INSTALL_COMMAND = "bun install -g github:tobi/qmd";
declare class QmdUnavailableError extends Error {
    constructor(message?: string);
}
/**
 * Check if qmd is available
 */
declare function hasQmd(): boolean;
/**
 * Trigger qmd update (reindex)
 */
declare function qmdUpdate(collection?: string): void;
/**
 * Trigger qmd embed (create/update vector embeddings)
 */
declare function qmdEmbed(collection?: string): void;
/**
 * QMD Search Engine - wraps qmd CLI
 */
declare class SearchEngine {
    private documents;
    private collection;
    private vaultPath;
    private collectionRoot;
    /**
     * Set the collection name (usually vault name)
     */
    setCollection(name: string): void;
    /**
     * Set the vault path for file resolution
     */
    setVaultPath(vaultPath: string): void;
    /**
     * Set the collection root for qmd:// URI resolution
     */
    setCollectionRoot(root: string): void;
    /**
     * Add or update a document in the local cache
     * Note: qmd indexing happens via qmd update command
     */
    addDocument(doc: Document): void;
    /**
     * Remove a document from the local cache
     */
    removeDocument(id: string): void;
    /**
     * No-op for qmd - indexing is managed externally
     */
    rebuildIDF(): void;
    /**
     * BM25 search via qmd
     */
    search(query: string, options?: SearchOptions): SearchResult[];
    /**
     * Vector/semantic search via qmd vsearch
     */
    vsearch(query: string, options?: SearchOptions): SearchResult[];
    /**
     * Combined search with query expansion (qmd query command)
     */
    query(query: string, options?: SearchOptions): SearchResult[];
    private runQmdQuery;
    /**
     * Convert qmd results to ClawVault SearchResult format
     */
    private convertResults;
    /**
     * Convert qmd:// URI to file path
     */
    private qmdUriToPath;
    /**
     * Clean up qmd snippet format
     */
    private cleanSnippet;
    /**
     * Get all cached documents
     */
    getAllDocuments(): Document[];
    /**
     * Get document count
     */
    get size(): number;
    /**
     * Clear the local document cache
     */
    clear(): void;
    /**
     * Export documents for persistence
     */
    export(): {
        documents: Document[];
    };
    /**
     * Import from persisted data
     */
    import(data: {
        documents: Document[];
    }): void;
}
/**
 * Find wiki-links in content
 */
declare function extractWikiLinks(content: string): string[];
/**
 * Find tags in content (#tag format)
 */
declare function extractTags(content: string): string[];

/**
 * ClawVault 🐘 — An Elephant Never Forgets
 *
 * Structured memory system for AI agents with Obsidian-compatible markdown
 * and embedded semantic search.
 *
 * @example
 * ```typescript
 * import { ClawVault, createVault, findVault } from 'clawvault';
 *
 * // Create a new vault
 * const vault = await createVault('./my-memory');
 *
 * // Store a memory
 * await vault.store({
 *   category: 'decisions',
 *   title: 'Use ClawVault',
 *   content: 'Decided to use ClawVault for memory management.'
 * });
 *
 * // Search memories
 * const results = await vault.find('memory management');
 * console.log(results);
 * ```
 */

declare const VERSION: string;

export { Category, ClawVault, Document, HandoffDocument, MemoryType, QMD_INSTALL_COMMAND, QMD_INSTALL_URL, QmdUnavailableError, SearchEngine, SearchOptions, SearchResult, SessionRecap, StoreOptions, SyncOptions, SyncResult, VERSION, VaultConfig, createVault, extractTags, extractWikiLinks, findVault, hasQmd, qmdEmbed, qmdUpdate };
