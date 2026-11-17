## Description:

24 AI agents for business automation - sales outreach, lead gen, content creation, SEO, ad copy, bookkeeping, proposals, market research, business plans, tech docs, data entry, web scraping, CRM ops, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[resonanceenergy](https://clawhub.ai/user/resonanceenergy)

### License/Terms of Use:

MIT-0

## Use Case:

Business users, operators, and developers use this skill to run specialized remote AI agents for sales, marketing, operations, document processing, research, and professional-service workflows. It also supports batch jobs and predefined multi-agent pipelines with QA status returned in structured outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted prompts, documents, customer records, CRM-like data, transaction text, and generated pipeline outputs are sent to the configured Digital Labour remote service and its listed LLM providers.

Mitigation: Use the trusted HTTPS production endpoint or an approved endpoint, avoid submitting sensitive data unless permitted, and review organizational data-handling requirements before use.

Risk: Changing DIGITAL_LABOUR_API_URL can redirect requests, including optional API keys and business inputs, to another service.

Mitigation: Set DIGITAL_LABOUR_API_URL only in trusted environments and avoid exposing DIGITAL_LABOUR_API_KEY where other users or scripts can alter the API URL.

## Reference(s):

- [Digital Labour API Homepage](https://bitrage-labour-api-production.up.railway.app)
- [ClawHub Skill Page](https://clawhub.ai/resonanceenergy/skills/digital-labour)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON examples; helper scripts return structured JSON from the remote API.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent calls and pipeline steps may return QA status and structured result payloads from the configured remote service.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
