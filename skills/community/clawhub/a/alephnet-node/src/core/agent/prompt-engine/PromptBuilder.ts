import { PromptContext, ToolDefinition } from './types';

export interface PromptSection {
    id: string;
    priority: number;
    content: string | ((context: PromptContext) => string | Promise<string>);
}

export class PromptBuilder {
    private sections: PromptSection[] = [];
    private tools: ToolDefinition[] = [];
    private safetyLevel: 'strict' | 'flexible' = 'strict';
    private context: PromptContext;

    constructor(context: PromptContext) {
        this.context = context;
    }

    addSection(section: PromptSection): this {
        // Replace existing section if same ID
        const index = this.sections.findIndex(s => s.id === section.id);
        if (index !== -1) {
            this.sections[index] = section;
        } else {
            this.sections.push(section);
        }
        return this;
    }

    addToolDefinitions(tools: ToolDefinition[]): this {
        this.tools.push(...tools);
        return this;
    }

    setSafetyLevel(level: 'strict' | 'flexible'): this {
        this.safetyLevel = level;
        return this;
    }

    async build(): Promise<string> {
        // 1. Add Default Sections if missing
        
        // Safety Section
        if (!this.sections.find(s => s.id === 'safety')) {
            this.addSection({
                id: 'safety',
                priority: 90, // High priority
                content: this.getSafetyContent()
            });
        }

        // Runtime Context
        if (!this.sections.find(s => s.id === 'runtime')) {
            this.addSection({
                id: 'runtime',
                priority: 20,
                content: this.getRuntimeContent()
            });
        }

        // Tooling Section
        if (this.tools.length > 0 && !this.sections.find(s => s.id === 'tooling')) {
            this.addSection({
                id: 'tooling',
                priority: 80,
                content: this.getToolingContent()
            });
        }

        // Sort sections by priority (Descending)
        this.sections.sort((a, b) => b.priority - a.priority);

        // Build content
        const parts: string[] = [];
        
        for (const section of this.sections) {
            let content = '';
            try {
                if (typeof section.content === 'function') {
                    content = await section.content(this.context);
                } else {
                    content = section.content;
                }
            } catch (err) {
                if (this.context.logger) {
                    this.context.logger.warn(`Failed to build section ${section.id}:`, err);
                } else {
                    console.warn(`Failed to build section ${section.id}:`, err);
                }
                continue;
            }

            if (content && content.trim().length > 0) {
                parts.push(content);
            }
        }

        return parts.join('\n\n');
    }

    private getSafetyContent(): string {
        if (this.safetyLevel === 'strict') {
            return `## Safety
1. Prioritize human oversight and safety.
2. Do not attempt to bypass safety constraints.
3. Do not generate harmful or malicious content.
4. If a request is ambiguous, ask for clarification.`;
        } else {
            return `## Safety
Operate with standard safety protocols. Prioritize user intent while maintaining system integrity.`;
        }
    }

    private getRuntimeContent(): string {
        const { runtime, workspaceDir } = this.context;
        const lines = [`## Runtime`];
        if (runtime) {
            lines.push(`OS: ${runtime.os}`);
            lines.push(`Time: ${runtime.time}`);
            lines.push(`Model: ${runtime.model}`);
        }
        lines.push(`Workspace: ${workspaceDir}`);
        return lines.join('\n');
    }

    private getToolingContent(): string {
        return `## Tooling
You have access to the following tools. Call them exactly as listed.

${this.tools.map(t => {
    const params = Object.keys(t.function.parameters.properties).join(', ');
    return `- **${t.function.name}**(${params}): ${t.function.description || 'No description'}`;
}).join('\n')}`;
    }
}
