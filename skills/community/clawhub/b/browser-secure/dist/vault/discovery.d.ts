import { VaultCredentials } from './index.js';
import { SiteConfig } from '../config/loader.js';
interface BitwardenItem {
    id: string;
    name: string;
    login?: {
        username?: string;
        password?: string;
    };
    fields?: Array<{
        name: string;
        value: string;
        type: number;
    }>;
    notes?: string;
}
interface OnePasswordItem {
    id: string;
    title: string;
    vault: {
        id: string;
        name: string;
    };
    urls?: Array<{
        primary: boolean;
        href: string;
    }>;
    fields?: Array<{
        id: string;
        label: string;
        value?: string;
    }>;
}
/**
 * Extract domain from URL for matching
 */
export declare function extractDomain(url: string): string;
/**
 * Extract base name for site key (e.g., "neilpatel" from "app.neilpatel.com")
 */
export declare function extractSiteKey(domain: string): string;
/**
 * Check if Bitwarden CLI is available and logged in
 */
export declare function isBitwardenAvailable(): boolean;
/**
 * Check if 1Password CLI is available
 */
export declare function is1PasswordAvailable(): boolean;
/**
 * Search Bitwarden for items matching a domain
 */
export declare function searchBitwardenItems(domain: string): BitwardenItem[];
/**
 * Search 1Password for items matching a domain
 */
export declare function search1PasswordItems(domain: string): OnePasswordItem[];
/**
 * Get detailed fields for a 1Password item
 */
export declare function get1PasswordItemFields(itemId: string): Array<{
    label: string;
    value?: string;
}>;
/**
 * Interactive credential selection - supports Bitwarden (default) and 1Password
 */
export declare function interactiveCredentialDiscovery(url: string, domain: string): Promise<{
    credentials: VaultCredentials;
    siteConfig: SiteConfig;
    siteKey: string;
} | null>;
export {};
