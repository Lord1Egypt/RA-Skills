## Description: <br>
Nutcracker is an embedded UX research skill for OpenClaw that observes interactions, runs post-task and end-of-day surveys, tracks cost, redacts PII before local storage, and compiles daily insight reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[giulianomorse](https://clawhub.ai/user/giulianomorse) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users and product research teams use this skill to study real assistant workflows, collect structured feedback, identify friction and delight, track task cost, and generate local UX reports for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad UX monitoring may capture sensitive conversations, client data, credentials, financial data, medical details, or proprietary work in local logs and reports. <br>
Mitigation: Install only with clear user intent, pause or stop observation for sensitive work, and treat ~/.uxr-observer/ reports and bundles as confidential. <br>
Risk: The skill promises PII redaction, but the security evidence warns that redaction safeguards may not be fully enforced. <br>
Mitigation: Avoid using the skill with sensitive data unless independent redaction and retention controls are added, and manually review generated files before relying on or sharing them. <br>
Risk: Generated daily reports and supersummary.zip bundles may disclose sensitive observations if shared without review. <br>
Mitigation: Share reports only through user-initiated workflows after reviewing the contents and confirming the recipient. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/giulianomorse/ethnoai) <br>
- [Analysis Framework](references/analysis-framework.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Natural-language guidance, JSONL observation and survey records, Markdown reports, and Python command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local files under ~/.uxr-observer/ and may produce daily reports and zipped case-study bundles.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
