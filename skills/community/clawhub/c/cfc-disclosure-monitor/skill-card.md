## Description:

Collects public disclosure announcements from 30 licensed consumer finance company websites, downloads supporting PDFs or attachments, extracts cooperation entities, and writes structured disclosure knowledge-graph data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linwumeng](https://clawhub.ai/user/linwumeng)

### License/Terms of Use:

MIT-0

## Use Case:

Compliance, risk, and data operations teams use this skill to monitor Chinese consumer finance company disclosure pages, collect announcement text and attachments, and query extracted cooperation relationships.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports hardcoded API credentials.

Mitigation: Remove embedded credentials from the release, rotate any exposed keys, and require users to provide secrets through their own environment or secret manager.

Risk: The security review reports that document contents or images may be sent to third-party AI services.

Mitigation: Require explicit opt-in for external AI processing and document what data is transmitted before use.

Risk: The security review reports weakened browser security and unsafe download handling.

Mitigation: Run the crawler in an isolated environment, restore normal browser security settings where possible, and harden URL and filename validation before broad use.

Risk: The skill mutates persistent ontology data.

Mitigation: Back up ontology files before running collection or parsing jobs and review generated updates before relying on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linwumeng/skills/cfc-disclosure-monitor)
- [Publisher profile](https://clawhub.ai/user/linwumeng)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell command examples; runtime artifacts are JSON disclosure records, PDF or image attachments, and ontology data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run crawlers against external company websites, download public disclosure files, and update persistent ontology data.]

## Skill Version(s):

4.5.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
