## Description: <br>
Processes court notice SMS messages and court-document PDFs by downloading the PDF, extracting case details, classifying the document, creating calendar events for hearing-related notices, setting reminders, and returning a concise summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[breezewang19](https://clawhub.ai/user/breezewang19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to turn court SMS links or court-document PDFs into extracted case summaries and, when the document appears to require attendance or response, local calendar reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive legal documents and stores downloaded PDFs on the user's Desktop. <br>
Mitigation: Use only trusted court links, confirm the destination file is appropriate, and avoid running it on shared or untrusted machines. <br>
Risk: The skill can modify Calendar data and install persistent LaunchAgent reminder files. <br>
Mitigation: Review planned Calendar and reminder changes before execution and remove generated LaunchAgent files when reminders are no longer needed. <br>
Risk: The security evidence flags weak scoping and unsafe script generation around AppleScript and plist values. <br>
Mitigation: Prefer a reviewed version that escapes AppleScript and plist values, asks for confirmation, and clearly documents any event-deletion behavior. <br>


## Reference(s): <br>
- [Document type rules](references/document_types.md) <br>
- [Court SMS template](references/sms_template.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown summary with shell command workflows and local calendar/reminder file changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May download PDFs, create Calendar entries, and write LaunchAgent reminder files on macOS.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
