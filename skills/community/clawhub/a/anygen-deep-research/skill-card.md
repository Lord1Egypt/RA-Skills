## Description:

Deep Research uses the AnyGen CLI and AnyGen workflow to generate in-depth research and comprehensive analysis reports on user-specified topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[logictortoise](https://clawhub.ai/user/logictortoise)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill when they need an agent to produce deep research reports for market, technology, investment, regulatory, patent, academic, due diligence, or competitive analysis topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research topics, prompts, and submitted material may be processed by AnyGen through the CLI and remote deep research workflow.

Mitigation: Use the skill only when the user accepts AnyGen processing, and avoid submitting secrets or confidential research topics unless that handling is approved.

Risk: The skill installs and delegates to unpinned external components that can change after review.

Mitigation: Review the skill before installing, trust the @anygen/cli npm package source, and prefer pinned or audited workflow versions where available.

## Reference(s):

- [Deep Research Skill on ClawHub](https://clawhub.ai/logictortoise/skills/anygen-deep-research)
- [AnyGen](https://www.anygen.io)
- [@anygen/cli npm package](https://www.npmjs.com/package/@anygen/cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown research reports and agent guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the AnyGen CLI, ANYGEN_API_KEY authentication, and the anygen-workflow-generate workflow with operation type deep_research.]

## Skill Version(s):

3.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
