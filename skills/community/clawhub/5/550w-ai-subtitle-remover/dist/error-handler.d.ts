import { ApiResponse, SkillResponse } from "./types";
export declare function createErrorResponse(code: number, message: string): SkillResponse;
export declare function mapApiError(apiResponse: ApiResponse, locale?: unknown, region?: unknown): SkillResponse;
export declare function createTimeoutErrorResponse(timeoutMs: number, locale?: unknown): SkillResponse;
