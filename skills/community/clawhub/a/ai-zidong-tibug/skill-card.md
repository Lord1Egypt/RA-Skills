## Description: <br>
Normalizes informal bug descriptions or review notes into single-issue, reproducible ZenTao bug records and can submit each issue to ZenTao with fixed fields and result backfill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elsemk](https://clawhub.ai/user/elsemk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA engineers, product teams, and agents use this skill to convert scattered Chinese bug notes into complete ZenTao-ready defect records, including assignee, title, reproduction steps, expected result, severity, priority, attachments, and submission status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create real external ZenTao defect tickets using supplied credentials. <br>
Mitigation: Use only when ZenTao ticket creation is intended; review product, module, assignee, title, steps, expected result, severity, priority, and attachments before submission. <br>
Risk: The skill stores a reusable ZenTao token locally. <br>
Mitigation: Use a least-privileged account, protect the saved token file, and delete or rotate the token after use when appropriate. <br>
Risk: A default ZenTao endpoint or misconfigured endpoint could submit data to the wrong system. <br>
Mitigation: Set ZENTAO_URL explicitly and confirm the target system before running submission scripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/elsemk/ai-zidong-tibug) <br>
- [templates-zh.md](references/templates-zh.md) <br>
- [submit-bugs-input.example.json](references/submit-bugs-input.example.json) <br>
- [module-map.example.json](references/module-map.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown defect records with optional JSON inputs, shell commands, and ZenTao submission result details.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create real ZenTao tickets and local authentication state when configured with credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
