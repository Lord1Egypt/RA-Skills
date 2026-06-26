import { VaultCredentials } from '../vault/index.js';
export declare function cacheCredentials(site: string, credentials: VaultCredentials): Promise<void>;
export declare function getCachedCredentials(site: string): Promise<VaultCredentials | null>;
export declare function clearCredentialCache(): void;
export declare function isCacheValid(site: string): boolean;
