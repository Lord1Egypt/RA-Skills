## Description: <br>
Faq Distiller extracts FAQ entries from customer support conversations, reviews, tickets, or chat logs and organizes them by user stage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Support, documentation, and knowledge-base teams use this skill to turn customer conversations, reviews, tickets, or chat logs into reviewable FAQ drafts for help centers, onboarding docs, and pre-sales FAQ material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input records may contain customer names, contact details, account identifiers, tokens, or ticket IDs. <br>
Mitigation: Redact sensitive customer and account data before using the skill. <br>
Risk: Generated FAQ answers may be incomplete, misleading, or unsuitable for publication without review. <br>
Mitigation: Review the generated FAQ draft before sharing, publishing, or using it as support guidance. <br>
Risk: The local helper reads the user-provided input path and can write a report to a user-provided output path. <br>
Mitigation: Run the helper only on intended local files and choose an output path appropriate for the workspace. <br>
Risk: Changing the bundled spec to an audit mode can enable local file inspection beyond the default FAQ-drafting behavior. <br>
Mitigation: Keep the shipped structured-brief configuration unless local inspection is intentional and approved. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/52YuanChangXing/faq-distiller) <br>
- [README](artifact/README.md) <br>
- [Structured FAQ specification](artifact/resources/spec.json) <br>
- [Output template](artifact/resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, configuration] <br>
**Output Format:** [Markdown by default, with an optional JSON wrapper from the local helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces reviewable FAQ sections, escalation items, missing-document notes, and maintenance suggestions; the helper can write the report to a user-provided local output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
