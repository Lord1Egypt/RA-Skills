/**
 * Baozi Claw - OpenClaw Skill
 *
 * Main entry point for the baozi-claw skill.
 */
export interface ToolResult {
    success: boolean;
    data?: unknown;
    error?: string;
}
export interface SkillTool {
    name: string;
    description: string;
    execute: (args: Record<string, unknown>) => Promise<ToolResult>;
}
export declare const tools: SkillTool[];
declare const _default: {
    metadata: {
        name: string;
        description: string;
        version: string;
    };
    tools: SkillTool[];
};
export default _default;
