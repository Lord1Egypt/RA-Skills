import { SiteConfig } from '../config/loader.js';
export interface VaultCredentials {
    username?: string;
    password?: string;
    token?: string;
}
export { extractDomain, extractSiteKey, search1PasswordItems, interactiveCredentialDiscovery } from './discovery.js';
export declare abstract class VaultProvider {
    abstract name: string;
    abstract isAvailable(): boolean;
    abstract getCredentials(site: string, config: SiteConfig): Promise<VaultCredentials>;
}
export declare function getVaultProvider(name: string): VaultProvider;
export declare function getSiteCredentials(site: string): Promise<VaultCredentials>;
export declare function listAvailableVaults(): string[];
