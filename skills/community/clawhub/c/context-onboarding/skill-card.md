## Description: <br>
Provides new contributors and agents with a concise tour of workspace identity files and onboarding tips. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CrimsonDevil333333](https://clawhub.ai/user/CrimsonDevil333333) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, contributors, and agents use this skill to quickly orient themselves to a workspace's identity documents, operating rules, tooling notes, and onboarding guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected snippets may expose sensitive or private workspace content when users point --files or --workspace at secrets, config files, home directories, or system paths. <br>
Mitigation: Use the default identity files or explicitly approved markdown/docs, and avoid passing sensitive paths because snippets may appear in agent output or logs. <br>


## Reference(s): <br>
- [Context Onboarding Guidelines](references/context-guidelines.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/CrimsonDevil333333/context-onboarding) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown guidance with CLI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prints excerpts from selected workspace documents; output depends on --files, --lines, --brief, and --workspace options.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
