// Cap entity rows fed to the LLM. Sub-1B models choke on long context;
// 60 rows ≈ 600 tokens leaves room for the doc body itself.
export const DOC_ENTITY_CONTEXT_LIMIT = 60;
// Cap doc body sent to the LLM. 8 KB covers most design docs; longer docs
// get truncated.
export const DOC_CONTENT_LIMIT = 8000;
