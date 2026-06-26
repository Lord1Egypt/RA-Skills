export interface SitePlaybook {
    discovery: {
        method: 'search' | 'browse' | 'direct';
        search_url?: string;
        search_input_selector?: string;
        search_submit_action?: string;
        browse_url?: string;
    };
    access: {
        login_required: boolean;
        login_url?: string;
        login_form_selector?: string;
    };
    extraction: {
        title_selector?: string;
        body_selector?: string;
        author_selector?: string;
        date_selector?: string;
    };
}
export interface SiteProfile {
    id: string;
    name: string;
    url: string;
    login_required: boolean;
    vault_config?: {
        provider: string;
        vault?: string;
        item?: string;
        username_field?: string;
        password_field?: string;
    };
    search?: {
        available: boolean;
        input_selector?: string;
        submit_action?: string;
    };
    navigation: Array<{
        name: string;
        url: string;
    }>;
    content_selectors: {
        title?: string;
        body?: string;
        author?: string;
        date?: string;
    };
    playbook?: SitePlaybook;
    sample_excerpt?: string;
    init_confirmed_at?: string;
    screenshots?: string[];
}
export declare function getSiteProfile(id: string): SiteProfile | undefined;
export declare function listSiteProfiles(): SiteProfile[];
export declare function saveSiteProfile(profile: SiteProfile): void;
export declare function deleteSiteProfile(id: string): void;
export interface Capture {
    id: string;
    site_id: string;
    url: string;
    referrer?: string;
    discovery_method?: string;
    title?: string;
    excerpt?: string;
    full_text?: string;
    html_path?: string;
    word_count?: number;
    captured_at: string;
    credentials_used: boolean;
    screenshot?: string;
    selectors_used?: Record<string, string>;
    approval_chain: {
        site_access?: {
            approved: boolean;
            auto: boolean;
        };
        credential_use?: {
            approved: boolean;
            auto: boolean;
        };
        extract_content?: {
            approved: boolean;
            auto: boolean;
        };
        record_content?: {
            approved: boolean;
            auto: boolean;
        };
    };
}
export declare function getCapture(id: string): Capture | undefined;
export declare function listCaptures(): Capture[];
export declare function listCapturesBySite(siteId: string): Capture[];
export declare function saveCapture(capture: Capture): void;
export declare function urlAlreadyCaptured(url: string): boolean;
export declare function exportToMarkdown(): string;
export declare function exportToJson(): string;
