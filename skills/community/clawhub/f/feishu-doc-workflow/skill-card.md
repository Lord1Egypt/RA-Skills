## Description:

Guides agents through Feishu docx writing, editing, image placement, public sharing, and troubleshooting for 400/403 document errors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dadaniya99](https://clawhub.ai/user/dadaniya99)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to edit and format Feishu docx documents, insert images at block-level positions, configure public read-only sharing, and troubleshoot common Feishu document permission failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can make Feishu documents publicly readable through link sharing.

Mitigation: Confirm the document contains no sensitive, internal, personal, or confidential information before using the public-link workflow.

Risk: A Feishu app with document editing and sharing permissions may affect documents beyond the intended workflow if installed in an inappropriate environment.

Mitigation: Install only where the configured Feishu app permissions are intended for document editing and sharing.

Risk: Incorrect block targeting can place images or edits in the wrong part of a document.

Mitigation: Use the documented read/list-blocks workflow before edits and re-read the document after changes.

## Reference(s):

- [Feishu Doc Workflow on ClawHub](https://clawhub.ai/dadaniya99/skills/feishu-doc-workflow)
- [dadaniya99 ClawHub Profile](https://clawhub.ai/user/dadaniya99)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline commands, API request examples, and configuration checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Feishu docx permissions, public sharing settings, and troubleshooting steps.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
