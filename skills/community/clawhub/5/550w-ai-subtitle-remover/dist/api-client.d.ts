import { ApiResponse, Credential, TIMEOUT_CONFIG } from "./types";
export declare class ApiClient {
    private credential;
    private baseUrl;
    constructor(credential: Credential);
    post(endpoint: string, params: Record<string, string>, timeout: number): Promise<ApiResponse>;
    upload(endpoint: string, params: Record<string, string>, file: {
        name: string;
        data: any;
    }, timeout: number): Promise<ApiResponse>;
    private parseResponse;
    private handleError;
}
export { TIMEOUT_CONFIG };
