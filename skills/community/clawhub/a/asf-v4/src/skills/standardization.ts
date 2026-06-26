/**
 * Skills Standardization Module - ANFSF v2.0
 * 
 * @module asf-v4/skills/standardization
 */

export interface StandardizedSkillConfig {
  name: string;
  version: string;
  description: string;
  usage: string[];
  examples: Array<{ query: string; result: string }>;
}

export class StandardizedSkill {
  name: string;
  version: string;
  description: string;
  usage: string[] = [];
  examples: Array<{ query: string; result: string }> = [];

  constructor(config: StandardizedSkillConfig) {
    this.name = config.name;
    this.version = config.version;
    this.description = config.description;
    this.usage = config.usage || [];
    this.examples = config.examples || [];
  }

  addUsage(usage: string): void {
    this.usage.push(usage);
  }

  addExample(query: string, result: string): void {
    this.examples.push({ query, result });
  }

  formatSKILLmd(): string {
    let md = `# ${this.name}\n\n`;
    md += `**Version**: ${this.version}\n\n`;
    md += `**Description**: ${this.description}\n\n`;
    
    if (this.usage.length > 0) {
      md += `## Usage\n\n`;
      this.usage.forEach((usage, index) => {
        md += `${index + 1}. ${usage}\n`;
      });
      md += `\n`;
    }

    if (this.examples.length > 0) {
      md += `## Examples\n\n`;
      this.examples.forEach(({ query, result }) => {
        md += `### Query\n\n\`\`\`text\n${query}\n\`\`\`\n\n`;
        md += `### Result\n\n\`\`\`json\n${result}\n\`\`\`\n\n`;
      });
    }

    return md;
  }
}

// ============================================================================
// Skills Registry
// ============================================================================

export interface SkillsRegistry {
  skills: Record<string, StandardizedSkill>;
  register(skill: StandardizedSkill): void;
  get(name: string): StandardizedSkill | undefined;
  list(): StandardizedSkill[];
  generateSKILLmds(): Record<string, string>;
}

export class DefaultSkillsRegistry implements SkillsRegistry {
  public skills: Record<string, StandardizedSkill> = {};

  register(skill: StandardizedSkill): void {
    this.skills[skill.name] = skill;
  }

  get(name: string): StandardizedSkill | undefined {
    return this.skills[name];
  }

  list(): StandardizedSkill[] {
    return Object.values(this.skills);
  }

  generateSKILLmds(): Record<string, string> {
    const mdMap: Record<string, string> = {};
    for (const [name, skill] of Object.entries(this.skills)) {
      mdMap[name] = skill.formatSKILLmd();
    }
    return mdMap;
  }
}

export function createSkillsRegistry(): SkillsRegistry {
  return new DefaultSkillsRegistry();
}