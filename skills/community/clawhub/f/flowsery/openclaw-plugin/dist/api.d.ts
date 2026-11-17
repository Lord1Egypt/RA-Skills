export declare const API_BASE_URL = "https://analytics.flowsery.com/analytics/api/v1";
export type PluginConfig = {
    apiKey?: string;
};
export declare function readConfig(api: {
    config?: unknown;
}): PluginConfig;
export declare function callApi(cfg: PluginConfig, method: "GET" | "POST" | "PATCH" | "DELETE", path: string, options?: {
    body?: unknown;
    query?: Record<string, unknown>;
    signal?: AbortSignal;
}): Promise<unknown>;
