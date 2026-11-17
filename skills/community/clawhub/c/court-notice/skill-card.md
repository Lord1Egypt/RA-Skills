## Description:

Processes court SMS messages and court-document PDFs by downloading the PDF, extracting case details, classifying the document, creating calendar reminders for hearing-related notices, and returning a concise summary report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[breezewang19](https://clawhub.ai/user/breezewang19)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to process received court notices, extract key hearing details, and prepare calendar reminders and user-facing summaries. It is most relevant when court-document links arrive by SMS and the user needs structured follow-up information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can silently download court-document PDFs and save them to a fixed Desktop path.

Mitigation: Require explicit user confirmation before download, validate that links come from trusted court-document sources, and avoid overwriting fixed Desktop filenames.

Risk: The helper can write Calendar events and persistent local reminders without enough user control.

Mitigation: Require confirmation before Calendar writes or reminder creation, and prefer Calendar-native alerts over LaunchAgents where possible.

Risk: Extracted court-document text can contain sensitive legal information.

Mitigation: Avoid printing full document text by default and limit summaries to the minimum details needed for the user's requested workflow.

Risk: Unescaped values passed into AppleScript or plist content can create execution or data-integrity risk.

Mitigation: Escape or pass all AppleScript and plist values as data rather than executable source.

## Reference(s):

- [Document type rules](references/document_types.md)
- [Court SMS template](references/sms_template.txt)
- [ClawHub skill page](https://clawhub.ai/breezewang19/skills/court-notice)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown summary with shell command examples and generated calendar/reminder configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save PDFs to the Desktop, create Calendar events, and configure local reminders when helper scripts are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
