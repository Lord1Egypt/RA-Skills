interface SkillContent {
    summary: string;
    body: string;
    raw: string;
}
export declare class SkillLoader {
    private skillsDir;
    private cache;
    constructor(pluginRootDir: string);
    load(skillFile: string): SkillContent;
    getSummary(skillFile: string): string;
    getBody(skillFile: string): string;
    private parse;
}
export {};
//# sourceMappingURL=skill-loader.d.ts.map