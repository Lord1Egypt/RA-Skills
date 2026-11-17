## Description:

Carbonstop CCDB helps agents search, compare, and match carbon emission factors for materials, energy, transport, packaging, food, product carbon footprint, corporate carbon accounting, and lifecycle assessment workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carbonstop-official](https://clawhub.ai/user/carbonstop-official)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and sustainability analysts use this skill to query CCDB through ccdb-cli, inspect factor metadata, and select appropriate emission factors for product carbon footprint, enterprise accounting, and LCA tasks. It guides authentication, search, detail lookup, result-link handling, and common permission or restricted-value cases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing ccdb-cli can introduce supply-chain risk if the package or binary source is not verified.

Mitigation: Verify the package or release source before installation, avoid elevated privileges, and prefer a pinned or checksum-verified release when available.

Risk: CCDB credentials, API keys, OAuth tokens, and diagnostic logs may expose account access if pasted into chat or printed in commands.

Mitigation: Use secure local configuration or controlled stdin, do not request or display secrets, and share only non-sensitive error codes, request IDs, HTTP status, or Retry-After values.

Risk: Emission factors can be misapplied when material, geography, year, unit, accounting type, technology route, or lifecycle boundary does not match the user's task.

Mitigation: Confirm the selection criteria before querying, read factor details before recommending a specific factor, preserve returned units and source metadata, and clearly state assumptions and mismatches.

Risk: Restricted or masked values can be mistaken for usable numeric data.

Mitigation: Treat masked, null, or missing values as unavailable rather than zero, explain access restrictions, and use only returned guidance or detail links for follow-up.

## Reference(s):

- [ClawHub ccdb skill page](https://clawhub.ai/carbonstop-official/skills/ccdb)
- [ccdb-cli releases](https://github.com/carbonstop/ccdb-cli/releases/latest)
- [ccdb-cli configuration](https://github.com/carbonstop/ccdb-cli/blob/main/docs/CONFIGURATION.md)
- [ccdb-cli repository](https://github.com/carbonstop/ccdb-cli)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown, configuration]

**Output Format:** [Markdown with inline shell commands, linked factor references, and concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-reading guidance for ccdb-cli responses and explicit notes about restricted values, access limitations, credentials, and source boundaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
