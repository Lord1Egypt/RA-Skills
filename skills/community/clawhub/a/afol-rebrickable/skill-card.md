## Description:

Use the Rebrickable API through the included CLI for LEGO catalog lookup, user set/part lists, build analysis, lost parts, and guarded collection writes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[musketyr](https://clawhub.ai/user/musketyr)

### License/Terms of Use:

MIT-0

## Use Case:

External LEGO builders and collection managers use this skill to query Rebrickable catalog data, analyze buildability, and manage user set, part, and lost-part lists through guarded CLI commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access a Rebrickable API key and, for private actions, a user token.

Mitigation: Install only when comfortable granting that access, keep credentials in environment variables, avoid command-line user tokens, and use only the official Rebrickable API base URL.

Risk: Mutating commands can create, update, or delete Rebrickable collection data.

Mitigation: Run a dry run first, restate the exact platform, IDs, set or part values, quantities, and operation, then require explicit confirmation before using --yes.

Risk: Credential handling is under-scoped and write guidance is inconsistent according to the security summary.

Mitigation: Review credential handling and write-operation guidance before deployment, with evidence.security as the authoritative risk source.

Risk: Broad private inventory reads, especially all-parts, can expose more collection data than needed.

Mitigation: Use filters and small page sizes where possible, and summarize only the private fields needed for the user's task.

## Reference(s):

- [AFOL Rebrickable ClawHub Skill](https://clawhub.ai/musketyr/skills/afol-rebrickable)
- [Rebrickable OpenAPI Reference](references/openapi/rebrickable.yaml)
- [Rebrickable Tool Guidance](references/prompts/rebrickable-tools.txt)
- [Rebrickable API](https://rebrickable.com/api/v3)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Private Rebrickable collection data should be summarized only as needed.]

## Skill Version(s):

1.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
