import { PromptTemplate } from './types';

export class PromptRegistry {
    private templates: Map<string, PromptTemplate> = new Map();

    register(template: PromptTemplate): void {
        if (this.templates.has(template.name)) {
            console.warn(`Overwriting existing prompt template: ${template.name}`);
        }
        this.templates.set(template.name, template);
    }

    get(name: string): PromptTemplate | undefined {
        return this.templates.get(name);
    }

    list(): string[] {
        return Array.from(this.templates.keys());
    }
}

export const promptRegistry = new PromptRegistry();
