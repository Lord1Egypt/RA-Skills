## Description:

Execute professional tasks through ClawWork, including document generation, analysis, automation, model comparison, and task economics tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felipetruman](https://clawhub.ai/user/felipetruman)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to launch ClawWork tasks, inspect agent status, compare model options, and run professional work with cost, earnings, and quality metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill launches code from a local ClawWork checkout that may not be verified by the skill package.

Mitigation: Install only after reviewing and pinning the local ClawWork checkout, and keep filesystem permissions restricted on the ClawWork directory.

Risk: Task prompts and API keys may be exposed to the local ClawWork code and configured model or sandbox providers.

Mitigation: Use scoped credentials in the ClawWork .env file, avoid confidential business data unless the trust boundary is acceptable, and rotate keys if exposure is suspected.

Risk: The skill writes temporary task configuration during execution.

Mitigation: Review temp-file handling and run with least-privilege access until that behavior is tightened.

## Reference(s):

- [ClawWork repository](https://github.com/HKUDS/ClawWork)
- [GDPVal dataset](https://openai.com/index/gdpval/)
- [ClawWork leaderboard](https://hkuds.github.io/ClawWork/)
- [ClawHub skill page](https://clawhub.ai/felipetruman/skills/clawwork)
- [Publisher profile](https://clawhub.ai/user/felipetruman)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and terminal text with optional generated task outputs and JSON-backed runtime configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke local ClawWork code, configured model providers, sandbox execution, and temporary task configuration files.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact __version__)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
