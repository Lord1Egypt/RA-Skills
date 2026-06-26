// src/lib/template-engine.ts
function buildTemplateVariables(input = {}, now = /* @__PURE__ */ new Date()) {
  const datetime = input.datetime ?? now.toISOString();
  const date = input.date ?? datetime.split("T")[0];
  return {
    title: input.title ?? "",
    type: input.type ?? "",
    date,
    datetime
  };
}
function renderTemplate(template, variables) {
  return template.replace(/\{\{\s*([a-zA-Z0-9_-]+)\s*\}\}/g, (match, key) => {
    const value = variables[key];
    return value !== void 0 ? String(value) : match;
  });
}

export {
  buildTemplateVariables,
  renderTemplate
};
