import { Credential, SkillResponse } from "./types";
export declare class CredentialManager {
    private readonly storagePath;
    private readonly legacyStoragePath;
    constructor(storagePath?: string);
    get(): Credential | null;
    private readFile;
    set(credential: Credential): void;
    isConfigured(): boolean;
    getGuideMessage(locale?: string, region?: string): SkillResponse;
}
