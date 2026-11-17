## Description:

Exa AI search + Research API. Supports web/code search, content extraction, and async multi-step research tasks with outputSchema.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xieshaocong33ethan](https://clawhub.ai/user/xieshaocong33ethan)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to search the web and code, extract URL content, crawl related pages, and run asynchronous Exa research workflows with optional structured output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Structured research output can upload local JSON schema file contents to Exa when SCHEMA_FILE is set.

Mitigation: Use only a dedicated non-sensitive JSON schema file; do not point SCHEMA_FILE at secrets, credentials, key material, or confidential documents.

Risk: The SCHEMA_FILE guard blocks obvious sensitive filenames but may not identify every confidential local file.

Mitigation: Review or constrain agent-selected SCHEMA_FILE paths before execution, and keep schema files separate from private project data.

Risk: Queries, URLs, research instructions, and optional schema content are sent to Exa API endpoints.

Mitigation: Avoid confidential queries or URLs, and review intended data disclosure before running search, content extraction, or research commands.

Risk: The search script defaults LOCATION to NL when no location is supplied.

Mitigation: Set LOCATION explicitly for location-sensitive tasks, or unset or override it when NL is not appropriate.

Risk: Storing EXA_API_KEY beside the skill can expose credentials if local files are shared or inspected.

Mitigation: Prefer setting EXA_API_KEY through the execution environment rather than storing it in a local .env file.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xieshaocong33ethan/skills/exa-full)
- [Exa](https://exa.ai)
- [Exa Docs](https://docs.exa.ai/)
- [Exa Subpage Crawling Reference](https://docs.exa.ai/reference/crawling-subpages)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and EXA_API_KEY; optional environment variables control search type, filters, crawling, research model, polling, and structured output schema.]

## Skill Version(s):

1.2.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
