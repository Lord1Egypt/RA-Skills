## Description:

AMiner Data Search helps agents answer complex academic data requests by selecting AMiner APIs and workflows for scholars, papers, institutions, venues, and patents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[canxiangcc](https://clawhub.ai/user/canxiangcc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research-focused agents use this skill to compose AMiner Open Platform calls for complex scholarly search, paper deep dives, scholar profiles, institution analysis, venue monitoring, and patent lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use paid AMiner API credits.

Mitigation: Review planned call chains before execution, require explicit confirmation for high-cost workflows, and prefer free AMiner APIs or the free AMiner skill for simple lookups.

Risk: Academic queries, scholar names, organization names, venue names, and patent searches may be sent to AMiner.

Mitigation: Avoid submitting sensitive or confidential research queries unless AMiner use is approved for that data.

Risk: The bundled client does not enforce the skill's promised high-cost confirmation by itself.

Mitigation: Have the agent or reviewer manually enforce cost confirmation and inspect cost summaries before running expensive workflows.

Risk: AMINER_API_KEY is required for live API use.

Mitigation: Provide the token through an environment variable or secret manager and avoid pasting credentials into chat or command-line arguments.

## Reference(s):

- [AMiner Open Platform API Catalog](artifact/references/api-catalog.md)
- [AMiner Open Platform Documentation](https://open.aminer.cn/open/docs)
- [AMiner API Console](https://open.aminer.cn/open/board?tab=control)
- [ClawHub Skill Page](https://clawhub.ai/canxiangcc/skills/aminer-open-academic)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with API call plans, shell commands, JSON snippets, academic result summaries, entity links, and cost reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AMINER_API_KEY for live AMiner calls; cost-aware workflows should report API usage and total estimated or incurred cost.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
