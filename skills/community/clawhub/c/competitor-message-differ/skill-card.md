## Description: <br>
Compares competitor messaging and information architecture to identify useful lessons, points to avoid copying, differentiation opportunities, and validation suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, product, and strategy teams use this skill to turn competitor copy, page excerpts, and audience context into a structured, reviewable messaging comparison. It is intended for strategy analysis and validation planning, not for copying competitor content or inventing competitor facts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input may include sensitive competitor, customer, or positioning material. <br>
Mitigation: Use only necessary local inputs, redact sensitive material before processing or sharing reports, and avoid sensitive directories. <br>
Risk: The local script can write a report to a user-selected output path. <br>
Mitigation: Use dry-run or an explicit review output path when testing, and inspect generated Markdown before using it in downstream work. <br>
Risk: The artifact includes unused broader audit modes that can inspect local files if intentionally enabled. <br>
Mitigation: Do not modify resources/spec.json to enable audit modes unless local file auditing is the intended task. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/52YuanChangXing/competitor-message-differ) <br>
- [README.md](artifact/README.md) <br>
- [resources/spec.json](artifact/resources/spec.json) <br>
- [resources/template.md](artifact/resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Structured Markdown by default, with optional JSON from the local script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write a local report when an output path is provided; otherwise prints to stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
