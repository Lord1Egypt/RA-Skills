export type ActionTier = 'read_only' | 'form_fill' | 'authentication' | 'destructive';
export type ApprovalTier = 'none' | 'prompt' | 'always' | '2fa';
export interface ApprovalRequest {
    action: string;
    site?: string;
    details?: Record<string, unknown>;
    tier: ActionTier;
}
export interface ApprovalResult {
    approved: boolean;
    token?: string;
    duration?: number;
    remember?: boolean;
    requires2fa?: boolean;
}
export interface UnattendedOptions {
    enabled: boolean;
    credentialSource: 'env' | 'vault' | 'cache';
    skipApproval?: boolean;
}
export declare function getActionTier(action: string): ActionTier;
export declare function checkCredentialSource(source: string): {
    valid: boolean;
    error?: string;
};
export declare function requestApproval(request: ApprovalRequest, options?: {
    skipPrompt?: boolean;
    autoApprove?: boolean;
    unattended?: UnattendedOptions;
}): Promise<ApprovalResult>;
export declare function verify2FA(code: string): Promise<boolean>;
export declare function closeApprover(): void;
export { getCachedCredentials, cacheCredentials, isCacheValid, clearCredentialCache } from './credential-cache.js';
