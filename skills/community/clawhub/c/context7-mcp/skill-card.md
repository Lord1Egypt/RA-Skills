## Description:

This skill helps an agent answer library, framework, and API questions by fetching current Context7 documentation for setup, configuration, code examples, and version-aware reference queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to retrieve current library, framework, and API documentation when answering setup questions, generating code, or checking version-specific behavior. It is most useful for programming prompts that mention packages such as React, Next.js, Prisma, Supabase, Vue, Svelte, Express, or Tailwind.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger external Context7 documentation lookups for many programming prompts that mention frameworks or libraries.

Mitigation: Use it when current or version-specific documentation is needed, and avoid unnecessary lookups for general coding help that does not require external reference material.

Risk: Fetched documentation or examples may still be incomplete, stale for a requested version, or mismatched to the user's exact library selection.

Mitigation: Resolve the closest official or primary library ID, prefer version-specific IDs when available, scope each query to one concept, and cite the relevant library version in the response.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, API Calls, Code, Markdown]

**Output Format:** [Markdown guidance with tool-call parameters and code examples when documentation supports them]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform external documentation lookups through Context7 and should cite library versions when relevant.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
