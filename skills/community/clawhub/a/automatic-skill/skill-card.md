## Description:

Automatic Skill helps agents research, design, generate, review, test, and publish OpenClaw skills through a staged prompt-generation pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cosmofang](https://clawhub.ai/user/cosmofang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to run a repeatable pipeline for generating, reviewing, self-checking, and publishing OpenClaw skills. It is also used to inspect pipeline status, run selected stages, or iterate an existing skill before release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can guide an agent to generate and execute new skill code on the user's machine.

Mitigation: Run in a disposable workspace, prefer dry-run first, and review generated package.json and scripts before npm install or execution.

Risk: Publishing stages can push commits and publish public artifacts using user-provided GitHub and ClawHub credentials.

Mitigation: Keep publishing tokens out of the environment until the upload step, use narrowly scoped tokens, prefer the PR workflow, and inspect files before any public push or ClawHub publish.

Risk: The security verdict is suspicious because the pipeline lacks strong containment around generated code and publishing actions.

Mitigation: Treat generated output as untrusted until reviewed, scanned, and approved for the target account and repository.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cosmofang/skills/automatic-skill)
- [Publisher Profile](https://clawhub.ai/user/cosmofang)
- [Project Homepage](https://github.com/Cosmofang/automatic-skill)
- [Referenced GitHub Skill Pattern](https://clawhub.ai/steipete/github)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown prompt text with JSON snippets and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stages produce agent-facing prompts; later stages may ask the agent to write files, run checks, or publish with user-provided credentials.]

## Skill Version(s):

1.4.1 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
