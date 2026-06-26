import { TemplateVariables } from '../lib/template-engine.js';

interface TemplateCommandContext {
    vaultPath?: string;
    cwd?: string;
    builtinDir?: string;
}
interface TemplateCreateOptions extends TemplateCommandContext {
    title?: string;
    type?: string;
}
interface TemplateAddOptions extends TemplateCommandContext {
    name: string;
    overwrite?: boolean;
}
declare function listTemplates(options?: TemplateCommandContext): string[];
declare function createFromTemplate(name: string, options?: TemplateCreateOptions): {
    outputPath: string;
    templatePath: string;
    variables: TemplateVariables;
};
declare function addTemplate(file: string, options: TemplateAddOptions): {
    templatePath: string;
    name: string;
};

export { type TemplateAddOptions, type TemplateCommandContext, type TemplateCreateOptions, addTemplate, createFromTemplate, listTemplates };
