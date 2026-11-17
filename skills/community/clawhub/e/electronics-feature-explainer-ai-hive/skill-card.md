## Description:

Turns 3C electronics product-structure and feature demonstration requests into a Chinese production workflow with scripts, storyboard prompts, runnable AI-HIVE commands, generated media task handling, and acceptance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, 3C brands, digital commerce teams, tech media, product trainers, and developers use this skill to turn authorized product facts and media into Chinese 3C explainer scripts, shot plans, prompts, runnable AI-HIVE commands, and delivery checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AI-HIVE API keys may be exposed through logs, repositories, screenshots, or shared configuration files.

Mitigation: Use environment variables or the local config flow, keep keys out of prompts and commits, and verify local config permissions before sharing outputs.

Risk: Generation tasks may upload media and incur AI-HIVE charges.

Mitigation: Confirm the model, route, pricing snapshot, prompt, uploaded files, and output destination before submission; use small samples for batch workflows.

Risk: Generated product visuals or claims may overstate engineering details, performance, availability, or platform results.

Mitigation: Anchor scripts to official product facts and authorized materials, mark uncertain facts for review, and avoid presenting generated scenes as real tests or certified diagrams.

Risk: Local video helpers depend on external tools and Python packages.

Mitigation: Run in a virtual environment with pinned dependencies and confirm ffmpeg availability before processing deliverables.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/electronics-feature-explainer-ai-hive)
- [AI-HIVE chat and API access](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON task records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include production briefs, storyboards, prompts, AI-HIVE routing choices, pricing snapshots, task IDs, local file paths, and acceptance checklists.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
