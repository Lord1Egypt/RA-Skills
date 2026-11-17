## Description:

Uses AMiner Open Platform APIs to query and analyze academic data about scholars, papers, institutions, venues, and patents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrhenghu](https://clawhub.ai/user/mrhenghu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and research operations teams use this skill to retrieve academic profiles, publication details, institutional research outputs, venue papers, academic search results, and patent information from AMiner.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real AMiner tokens could be exposed if placed directly in commands, logs, or shared prompts.

Mitigation: Use an environment variable or protected prompt for the token and avoid storing it in command history or shared artifacts.

Risk: Some AMiner workflows call paid APIs and may incur charges.

Mitigation: Confirm user intent before paid API calls and prefer free lookup APIs when they satisfy the request.

Risk: Academic searches may send confidential research topics, unpublished ideas, or sensitive organization names to an external API.

Mitigation: Avoid submitting confidential topics or sensitive identifiers unless the user has approved external API use.

Risk: The raw API mode exposes a broader callable surface than the documented guided workflows.

Mitigation: Prefer the named workflows and only use raw mode after checking the requested API and parameters.

## Reference(s):

- [AMiner Open Platform Documentation](https://open.aminer.cn/open/doc)
- [AMiner Open Platform Console](https://open.aminer.cn/open/board?tab=control)
- [AMiner API Catalog](references/api-catalog.md)
- [ClawHub Skill Page](https://clawhub.ai/mrhenghu/skills/aminer-open-academic-1-0-5)
- [Publisher Profile](https://clawhub.ai/user/mrhenghu)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include AMiner API call chains, selected entities, search candidates, academic metadata, citation previews, patent details, and structured error responses.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
