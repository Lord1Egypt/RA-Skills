## Description: <br>
Automated novel-writing assistant that helps create outlines, world-building, chapter drafts, quality checks, and final manuscripts through an OpenClaw or CLI workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tanson515](https://clawhub.ai/user/tanson515) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
External users and writers use this skill to plan, draft, review, revise, and merge long-form fanfiction or web-novel manuscripts with staged checkpoints and local project state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Promised human approval gates may not be enforced before some file writes and state commits. <br>
Mitigation: Review generated files and state changes before relying on them, and do not treat manual mode as a guaranteed approval gate for every internal step. <br>
Risk: The skill writes prompts, outlines, drafts, manuscript text, logs, and state into local run directories. <br>
Mitigation: Run it only in an isolated workspace you are comfortable letting the skill modify, and keep backups for important manuscripts. <br>
Risk: Prompts and manuscript text may be sent to the configured OpenClaw model provider. <br>
Mitigation: Keep run directories private and avoid including sensitive content unless the configured model provider and data-handling terms are acceptable. <br>


## Reference(s): <br>
- [Fanfic Writer ClawHub listing](https://clawhub.ai/tanson515/fanfic-writer) <br>
- [Prompt Templates for Fanfic Writer](artifact/references/prompts.md) <br>
- [Installation Guide](artifact/INSTALL_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown, plain text manuscript files, JSON configuration/state files, and CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local run directories containing prompts, outlines, drafts, chapters, logs, state panels, and final manuscript outputs.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
