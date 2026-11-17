import { ApiResponse, Credential, TIMEOUT_CONFIG } from "./types";
export declare class ApiClient {
    private credential;
    private baseUrl;
    private locale?;
    constructor(credential: Credential, locale?: unknown);
    post(endpoint: string, params: Record<string, string>, timeout: number): Promise<ApiResponse>;
    upload(endpoint: string, params: Record<string, string>, file: {
        name: string;
        data: any;
    }, timeout: number, fieldName?: string): Promise<ApiResponse>;
    private safeHeader;
    private request;
    private parseResponse;
    private handleError;
}
export { TIMEOUT_CONFIG };
