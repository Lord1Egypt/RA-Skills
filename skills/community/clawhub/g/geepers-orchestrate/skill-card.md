## Description:

Run multi-agent Dream Cascade (hierarchical 3-tier synthesis) or Dream Swarm (parallel multi-domain search) workflows via the dr.eamer.dev orchestration API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lukeslp](https://clawhub.ai/user/lukeslp)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to route complex research and synthesis tasks through multi-agent Dream Swarm or Dream Cascade workflows when a single query or source is insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, research questions, selected sources, and task details are sent to the dr.eamer.dev API.

Mitigation: Avoid submitting secrets, personal data, regulated data, or confidential business material unless the service's privacy, retention, and security practices have been reviewed.

Risk: The skill depends on an external orchestration API and may take 10-60 seconds for orchestration requests.

Mitigation: Use it for multi-agent research and synthesis tasks where external API latency is acceptable.

## Reference(s):

- [Geepers Orchestrate on ClawHub](https://clawhub.ai/lukeslp/skills/geepers-orchestrate)
- [dr.eamer.dev orchestration API](https://api.dr.eamer.dev)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON request examples, and API response descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses from the external orchestration API include a synthesized result, sources, agent count, and duration.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
