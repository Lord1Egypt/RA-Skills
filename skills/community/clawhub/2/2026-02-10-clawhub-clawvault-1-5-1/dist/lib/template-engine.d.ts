interface TemplateVariables {
    title: string;
    date: string;
    datetime: string;
    type: string;
}
declare function buildTemplateVariables(input?: Partial<TemplateVariables>, now?: Date): TemplateVariables;
declare function renderTemplate(template: string, variables: TemplateVariables): string;

export { type TemplateVariables, buildTemplateVariables, renderTemplate };
