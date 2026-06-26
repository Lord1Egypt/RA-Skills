## Description: <br>
Identify tasks that waste tokens. Scripts don't hallucinate, don't cost per-run, and don't fail randomly. Spot automation opportunities and build them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to identify deterministic, repetitive, rule-based work and turn it into reusable scripts or script templates for formatting, validation, file operations, API calls, and git workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or adapted automation scripts can edit many files, publish code, or change git history before a user has reviewed the result. <br>
Mitigation: Require explicit approval before running generated scripts, review diffs before any push or pull request, avoid blanket git add -A, and add dry-run or backup steps for bulk edits. <br>
Risk: Generic API and credential templates can be copied into real workflows with overly broad credentials or untrusted hosts. <br>
Mitigation: Replace template credential access with service-specific least-privilege credentials, trusted hosts, and environment-specific review before use. <br>


## Reference(s): <br>
- [Automation Signals](artifact/signals.md) <br>
- [Script Templates](artifact/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands] <br>
**Output Format:** [Markdown with shell command and script template code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes decision criteria for automation candidates and reusable bash templates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
