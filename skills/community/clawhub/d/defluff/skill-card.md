## Description: <br>
Defluff analyzes pasted corporate email to classify likely authorship, infer AI prompts when applicable, triage urgency and intent, and identify common scam patterns while mirroring the email's language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yozaz](https://clawhub.ai/user/yozaz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Email users and reviewers use Defluff to triage single messages, threads, or batches into terse authorship verdicts, action bullets, scam red flags, and response priority. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private or sensitive email content may be exposed to the configured agent or model during analysis. <br>
Mitigation: Analyze only email content the user is permitted to process, and redact secrets, credentials, or unnecessary personal data before use. <br>
Risk: The skill can over-apply email analysis to ordinary summaries or ambiguous pasted text. <br>
Mitigation: Ask explicitly for the desired analysis type and output language; when the input is not clearly email, the skill asks whether it is a single email, thread, or batch. <br>
Risk: Authorship, prompt-reversal, urgency, or scam classifications are probabilistic and may be wrong. <br>
Mitigation: Treat verdicts as triage guidance and verify high-impact security, payment, hiring, or business decisions through independent channels. <br>


## Reference(s): <br>
- [Defluff on ClawHub](https://clawhub.ai/yozaz/defluff) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Structured Markdown with Authored, optional Prompt, Verdict, bullets, and thread or batch triage sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Mirrors the input email language; preserves names, numbers, dates, and amounts.] <br>

## Skill Version(s): <br>
0.0.9 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
