/**
 * Core Skill Interface
 * 
 * @module asf-v4/core/skill
 */

export interface SkillContext {
  logger?: any;
  mempalace?: any;
  [key: string]: any;
}

export abstract class Skill {
  constructor(protected name: string, protected context: SkillContext) {}
}