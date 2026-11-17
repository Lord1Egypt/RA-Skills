## Description:

Guides agents in generating, editing, streaming, and decomposing images with Seedream through AceDataCloud.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acedatacloud](https://clawhub.ai/user/acedatacloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative teams use this skill to guide image generation, reference-image editing, transparent-background edits, and extraction of editable image layers through AceDataCloud's Seedream API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The AceDataCloud API key could be exposed through prompts or committed configuration.

Mitigation: Keep the key in the gateway environment, use a dedicated key restricted to required Seedream routes, and never include it in prompts or commits.

Risk: Image generation and layer extraction can incur cloud usage charges, including on repeated requests.

Mitigation: Poll returned task IDs instead of resubmitting requests, and check returned usage and current pricing before estimating costs.

Risk: Optional MCP and CLI packages require trust in external package sources.

Mitigation: Install optional packages only after verifying and trusting their sources.

## Reference(s):

- [Seedream skill listing](https://clawhub.ai/acedatacloud/skills/seedream)
- [AceDataCloud API key setup and first run](https://github.com/AceDataCloud/Skills#first-run-with-clawhub-and-openclaw)
- [AceDataCloud authentication guidance](https://github.com/AceDataCloud/Skills/blob/main/skills/_shared/authentication.md)
- [AceDataCloud async task polling guidance](https://github.com/AceDataCloud/Skills/blob/main/skills/_shared/async-tasks.md)
- [Seedream pricing](https://platform.acedata.cloud/services/seedream?tab=pricing)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with API request examples in bash and JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers asynchronous polling, streaming events, image result handling, and usage-based billing.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
