## Description:

AI-powered ingestion of CSV, JSON, and XLSX files with automatic schema generation and Supabase database integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sschepis](https://clawhub.ai/user/sschepis)

### License/Terms of Use:

MIT

## Use Case:

Developers and data engineers use this skill to import CSV, JSON, and XLSX datasets into Supabase while generating schema and mapping guidance with LLM assistance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install and npx examples may resolve a package identity that differs from the scoped package metadata.

Mitigation: Verify the intended package identity, prefer a pinned scoped package version, and avoid bare npx execution until the package name is corrected and confirmed.

Risk: The skill requests Supabase and OpenAI credentials, including guidance that mentions a Supabase service role key.

Mitigation: Use least-privilege credentials where possible, store secrets outside prompts and source files, and rotate any credentials exposed during testing.

Risk: The artifact contains documentation and package metadata but no implementation files to inspect.

Mitigation: Require the missing source or built implementation files before installation or execution, then review and scan them.

Risk: Data imports may include sensitive datasets that are uploaded to Supabase.

Mitigation: Redact or minimize sensitive fields before import and confirm the target Supabase project, tables, and access controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sschepis/skills/flexible-data-importer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, TypeScript examples, environment configuration, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe file ingestion, schema generation, type mapping, batching, and Supabase upload steps.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, package-lock.json, SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
