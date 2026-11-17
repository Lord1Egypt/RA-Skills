## Description:

Academic data search and analysis using AMiner Open Platform APIs for scholars, papers, institutions, journals, patents, and composite research workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ye4wzp](https://clawhub.ai/user/ye4wzp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and research analysts use this skill to query AMiner academic data, assemble scholar and paper profiles, analyze institutions and venues, answer natural-language paper questions, and search patents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command-line examples can expose an AMiner API token in shell history or process listings.

Mitigation: Set the token through AMINER_TOKEN or a secret store instead of typing it into commands.

Risk: Academic queries may include confidential or regulated research topics.

Mitigation: Avoid submitting sensitive topics unless AMiner's data handling is acceptable for the use case.

Risk: The security review notes a missing client implementation could affect workflow reliability.

Mitigation: Confirm the client implementation and API behavior before relying on the workflows.

## Reference(s):

- [AMiner Open Platform API Documentation](https://open.aminer.cn/open/doc)
- [AMiner Console](https://open.aminer.cn/open/board?tab=control)
- [ClawHub Skill Page](https://clawhub.ai/ye4wzp/skills/aminer-academic-search)
- [Publisher Profile](https://clawhub.ai/user/ye4wzp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and API workflow descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose AMiner API calls and workflows that require an AMINER_TOKEN and may incur AMiner API costs.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
