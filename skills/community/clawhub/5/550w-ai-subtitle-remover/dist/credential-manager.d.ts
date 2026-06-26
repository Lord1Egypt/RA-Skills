import { Credential, SkillResponse } from "./types";
export declare class CredentialManager {
    private readonly storagePath;
    constructor(storagePath?: string);
    get(): Credential | null;
    set(credential: Credential): void;
    isConfigured(): boolean;
    getGuideMessage(): SkillResponse;
}
