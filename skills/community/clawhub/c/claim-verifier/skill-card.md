## Description: <br>
Verifies external factual claims in draft content before publishing or sending and produces a structured claim verification report with evidence links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jernejcicorbin-hub](https://clawhub.ai/user/jernejcicorbin-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, marketers, and agents use this skill to check drafts that contain external factual claims before publication or sending. It highlights wrong, weak, conflicting, or unsupported claims and can produce a machine-readable verification report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Draft claims are sent to Prismfy for verification using the user's API key. <br>
Mitigation: Use the skill only with content suitable for Prismfy processing, and prefer a revocable or scoped API key. <br>
Risk: API keys can be exposed if copied into shared shell startup files or logs. <br>
Mitigation: Store PRISMFY_API_KEY in a local secret manager or private environment configuration and avoid committing or sharing dotfiles that contain it. <br>
Risk: The optional hook adds claim-checking reminders to future agent sessions. <br>
Mitigation: Enable the hook only when persistent fact-checking reminders are desired, and disable it for workflows where the reminder is unnecessary. <br>


## Reference(s): <br>
- [Prismfy](https://prismfy.io) <br>
- [ClawHub skill page](https://clawhub.ai/jernejcicorbin-hub/claim-verifier) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Concise Markdown response with optional claim_verification_report.json artifact] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses PRISMFY_API_KEY, curl, and jq; batch output preserves claim order and caps evidence URLs per claim.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release; artifact frontmatter remains 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
