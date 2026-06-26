interface VaultStatus {
    vaultName: string;
    vaultPath: string;
    health: 'ok' | 'warning';
    issues: string[];
    checkpoint: {
        exists: boolean;
        timestamp?: string;
        age?: string;
        sessionKey?: string;
        model?: string;
        tokenEstimate?: number;
    };
    qmd: {
        collection: string;
        root: string;
        indexStatus: 'present' | 'missing' | 'root-mismatch';
        error?: string;
    };
    git?: {
        repoRoot: string;
        clean: boolean;
        dirtyCount: number;
    };
    links: {
        total: number;
        orphans: number;
    };
    documents: number;
    categories: Record<string, number>;
}
declare function getStatus(vaultPath: string): Promise<VaultStatus>;
declare function formatStatus(status: VaultStatus): string;
declare function statusCommand(vaultPath: string, options?: {
    json?: boolean;
}): Promise<void>;

export { type VaultStatus, formatStatus, getStatus, statusCommand };
