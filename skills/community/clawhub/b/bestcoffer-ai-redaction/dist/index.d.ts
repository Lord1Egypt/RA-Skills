interface FileInfo {
    name?: string;
    fileName?: string;
    filename?: string;
    originalName?: string;
    originalFilename?: string;
    path?: string;
    filePath?: string;
    filepath?: string;
    tempPath?: string;
    size?: number;
    type?: string;
    mimeType?: string;
}
interface SkillParameters {
    file: FileInfo | string;
    fileName?: string;
    instruction: string;
    apiKey?: string;
}
interface SkillContext {
    parameters: SkillParameters;
}
declare class AIRedactionSkill {
    private readonly API_BASE_URL;
    private readonly WEBSITE_URL;
    constructor();
    private normalizeFile;
    private validateFile;
    private validateInstruction;
    private uploadAndCreateTask;
    execute(context: SkillContext): Promise<{
        taskUrl: string;
        errorMessage: string;
    }>;
}
declare const skill: AIRedactionSkill;
export default skill;
