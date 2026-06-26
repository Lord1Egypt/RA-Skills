export declare function isHostAllowed(url: string): {
    allowed: boolean;
    reason?: string;
};
export declare function validateUrl(url: string): {
    valid: boolean;
    error?: string;
};
