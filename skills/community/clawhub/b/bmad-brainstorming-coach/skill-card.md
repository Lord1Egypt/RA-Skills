## Description:

Activates the BMad Brainstorming Coach agent, Carson, to facilitate innovation workshops, brainstorming sessions, creative prompting, and structured idea exploration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[airclear](https://clawhub.ai/user/airclear)

### License/Terms of Use:


## Use Case:

Employees and external users can use this skill to run guided brainstorming sessions, choose creative techniques, organize ideas, and document next steps. It is suited to ideation workshops, innovation planning, and creative problem exploration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads unbundled local project files such as BMad configuration and agent manifest files.

Mitigation: Use it only in trusted workspaces and review referenced local files before installation or activation.

Risk: The skill writes brainstorming session documents under the configured output folder.

Mitigation: Confirm the configured output folder before use and review generated session documents before sharing them.

Risk: Party Mode and YOLO-style flows may rely on local hooks or broader workspace behavior.

Mitigation: Avoid these modes in sensitive projects unless the referenced local files and hooks have been verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/airclear/skills/bmad-brainstorming-coach)
- [Agent definition](references/agent_definition.md)
- [Workflow engine](references/workflow_engine.xml)
- [Brainstorming workflow](assets/workflows/brainstorming/workflow.md)
- [Party Mode workflow](assets/workflows/party-mode/workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Conversational text and Markdown session documents, with occasional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save brainstorming session notes under the configured output folder.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
