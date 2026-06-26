export interface SitePolicy {
    approvalTier: 'none' | 'prompt' | 'always' | '2fa';
    sessionTtlMinutes?: number;
    require2fa: boolean;
}
export interface SiteConfig {
    vault: string;
    item: string;
    usernameField?: string;
    passwordField?: string;
    tokenField?: string;
    policy?: SitePolicy;
}
export interface SessionConfig {
    ttlMinutes: number;
    warningAtMinutes: number;
    credentialCacheMinutes: number;
}
export interface AuditConfig {
    enabled: boolean;
    logPath: string;
    retentionDays: number;
    mode: 'file' | 'webhook' | 'both';
    webhook?: {
        url: string;
        headers?: Record<string, string>;
    };
}
export interface SecurityConfig {
    defaultTtl: number;
    requireApprovalForLogin: boolean;
    screenshotEveryAction: boolean;
    network: {
        blockLocalhost: boolean;
        blockPrivateIps: boolean;
        allowedHosts: string[];
    };
    audit: AuditConfig;
    session: SessionConfig;
}
export interface IsolationConfig {
    incognitoMode: boolean;
    secureWorkdir: boolean;
    autoCleanup: boolean;
}
export interface BrowserSecureConfig {
    vault: {
        provider: '1password' | 'bitwarden' | 'hashicorp' | 'keychain' | 'env';
        sites: Record<string, SiteConfig>;
    };
    security: SecurityConfig;
    isolation: IsolationConfig;
}
export declare function getConfigPath(): string;
export declare function expandPath(p: string): string;
export declare function loadConfig(): BrowserSecureConfig;
export declare function getSitePolicy(site: string): SitePolicy | undefined;
export declare function getSessionConfig(): SessionConfig;
export declare function saveConfig(config: BrowserSecureConfig): void;
export declare function getAuditLogPath(): string;
export declare function getAuditWebhookUrl(): string | undefined;
export declare function checkCredentialSource(source: string): {
    valid: boolean;
    error?: string;
};
