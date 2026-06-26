import { ApiResponse, SkillResponse } from "./types";
export declare function createErrorResponse(code: number, message: string): SkillResponse;
export declare function mapApiError(apiResponse: ApiResponse): SkillResponse;
export declare function createTimeoutErrorResponse(timeoutMs: number): SkillResponse;
