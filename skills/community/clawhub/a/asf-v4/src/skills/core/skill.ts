/**
 *Skill Base Interface
 * 
 * @module asf-v4/skills/core/skill
 */

// ============================================================================
// Skill Base Interface
// ============================================================================

export interface Skill {
  name: string;
  version: string;
  description: string;
  author?: string;
  license?: string;
}

export interface SkillConfig {
  name: string;
  version: string;
  type: string;
  options?: Record<string, any>;
}

export interface SkillContext {
  workspace: string;
  options?: Record<string, any>;
  courseOfAction?: string;
}

export interface SkillResult<T = any> {
  success: boolean;
  data?: T;
  error?: string;
  metadata?: Record<string, any>;
}

// ============================================================================
// Skill Execution
// ============================================================================

export interface SkillExecutor {
  execute(context: SkillContext, config: SkillConfig): Promise<SkillResult>;
}

export class BaseSkill implements SkillExecutor {
  name: string;
  version: string;
  description: string;
  
  constructor(config: { name: string; version: string; description: string }) {
    this.name = config.name;
    this.version = config.version;
    this.description = config.description;
  }
  
  async execute(context: SkillContext, config: SkillConfig): Promise<SkillResult> {
    return {
      success: true,
      data: null,
      metadata: {
        skill: this.name,
        version: this.version
      }
    };
  }
}

// ============================================================================
// Skill Registry
// ============================================================================

export interface SkillRegistry {
  skills: Record<string, Skill>;
  register(skill: Skill): void;
  get(name: string): Skill | undefined;
  list(): Skill[];
}

export class DefaultSkillRegistry implements SkillRegistry {
  public skills: Record<string, Skill> = {};
  
  register(skill: Skill): void {
    this.skills[skill.name] = skill;
  }
  
  get(name: string): Skill | undefined {
    return this.skills[name];
  }
  
  list(): Skill[] {
    return Object.values(this.skills);
  }
}

export function createSkillRegistry(): SkillRegistry {
  return new DefaultSkillRegistry();
}