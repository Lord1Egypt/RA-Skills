export interface SkillTool {
  name: string;
  description: string;
  parameters: {
    type: 'object';
    properties: Record<string, unknown>;
    required?: string[];
  };
}

export interface SkillContext {
  config: Record<string, unknown>;
  [key: string]: unknown;
}

export interface SkillResult {
  result?: unknown;
  error?: string;
}

export interface Skill {
  name: string;
  description: string;
  version: string;
  getTools(): SkillTool[];
  executeTool(name: string, params: unknown, context: SkillContext): Promise<SkillResult>;
}
