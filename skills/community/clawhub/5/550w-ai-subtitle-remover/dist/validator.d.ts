import type { SkillResponse, EstimateCreditsResult } from "./types";
export declare function validateCredential(userNo: string | undefined | null, apiKey: string | undefined | null): SkillResponse | null;
export declare function normalizePageParams(params: {
    page?: number;
    size?: number;
}): {
    page: number;
    size: number;
};
export declare function estimateCredits(width: number, height: number, duration: number): EstimateCreditsResult;
export declare function validate(action: string, params: Record<string, any>): SkillResponse | null;
