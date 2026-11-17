## Description:

Automates research by conducting literature searches, running experiments, and generating LaTeX papers from detailed research topics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[donwrightdesigns](https://clawhub.ai/user/donwrightdesigns)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and external users use this agent to turn a research topic into literature review, experiment execution, analysis, and paper-generation outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous runs can delegate high-impact code and agent actions with weak containment or approval controls.

Mitigation: Install and run in a disposable or tightly sandboxed environment, avoid automatic approval for first runs, and prefer Docker execution without fallback to local execution.

Risk: Generated code and research artifacts may handle credentials or produce content that needs review before reuse.

Mitigation: Keep API keys out of inherited environments, review generated artifacts and reusable skill content before deployment, and scan outputs before publication.

Risk: Setup may install or invoke third-party tooling that affects the local environment.

Mitigation: Review setup prompts and package sources before accepting global installs such as opencode-ai@latest.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/donwrightdesigns/skills/auto-research-claw)
- [README](README.md)
- [Integration guide](docs/integration-guide.md)
- [Tester guide](docs/TESTER_GUIDE.md)
- [Paper showcase](docs/showcase/SHOWCASE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, LaTeX, BibTeX, JSON reports, generated experiment files, charts, and shell-command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include generated research artifacts, experiment results, citation verification reports, and reusable lessons from runs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
