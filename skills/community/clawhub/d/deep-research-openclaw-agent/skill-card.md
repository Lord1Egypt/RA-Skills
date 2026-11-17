## Description:

Install and wire a structured OpenClaw deep-research sub-agent with hybrid search, artifact-based runs, claim verification, report linting, and validated finalization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[milleniumgenai](https://clawhub.ai/user/milleniumgenai)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to install and configure a reproducible deep-research sub-agent workflow with planning, discovery, verification, synthesis, validation, and final report delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install flow asks users to run code from an unpinned third-party repository without integrity checks.

Mitigation: Review the referenced repository, pin it to a trusted commit or release, and run the validation checks in a constrained environment before using the skill for real work.

Risk: Tavily-backed scouting may send queries or research context outside the local machine.

Mitigation: Configure TAVILY_API_KEY only when network-backed research is intended and approved for the data being researched.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/milleniumgenai/skills/deep-research-openclaw-agent)
- [Project homepage](https://github.com/MilleniumGenAI/deep-research-openclaw-agent)
- [Root README](https://github.com/MilleniumGenAI/deep-research-openclaw-agent/blob/main/README.md)
- [Sub-agent contract](https://github.com/MilleniumGenAI/deep-research-openclaw-agent/blob/main/openclaw/workspace-researcher/SOUL.md)
- [Main handoff contract](https://github.com/MilleniumGenAI/deep-research-openclaw-agent/blob/main/openclaw/main-deep-research-skill.md)
- [Runtime scripts](https://github.com/MilleniumGenAI/deep-research-openclaw-agent/tree/main/openclaw/workspace-researcher/scripts)
- [Agent config template](https://github.com/MilleniumGenAI/deep-research-openclaw-agent/blob/main/openclaw/agent-config.template.json)
- [Known limits](https://github.com/MilleniumGenAI/deep-research-openclaw-agent/blob/main/docs/known-limits.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include OpenClaw command examples, validation steps, report expectations, and explicit gaps or conflicts.]

## Skill Version(s):

0.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
