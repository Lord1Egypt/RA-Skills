interface RegistryHttpClient {
    get<T>(path: string, options?: {
        params?: Record<string, string>;
    }): Promise<{
        data: T;
    }>;
}
export interface ComponentSuggestion {
    dependency: string;
    version: string;
    component: string;
    namespace: string;
    name: string;
    description: string;
    documentation?: string;
    readme?: string;
    registryUrl?: string;
    targets: string[];
    idfDependency?: string;
    score: number;
    addDependencyCommand: string;
    manifestSnippet: string;
}
export interface ResolveComponentResult {
    status: 'OK' | 'NOT_FOUND';
    query: string;
    target?: string;
    suggestion?: ComponentSuggestion;
    candidates?: ComponentSuggestion[];
    reason?: string;
}
export declare class ComponentRegistry {
    private readonly client;
    private readonly registryBaseUrl;
    constructor(client?: RegistryHttpClient, registryBaseUrl?: string);
    resolveComponent(query: string, target?: string): Promise<ResolveComponentResult>;
    private rankComponents;
    private scoreComponent;
    private toSuggestion;
    private normalizeToken;
    private createDefaultClient;
}
export {};
