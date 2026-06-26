## Description: <br>
Checks meeting summaries for evidence, owner and date confirmation, privacy, and attribution before notes or follow-ups are shared. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindbomber](https://clawhub.ai/user/mindbomber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to review meeting summaries, minutes, action items, decisions, and follow-ups against available transcripts, notes, chat, agendas, or calendar evidence. It helps label uncertainty, request confirmation for owners or dates, redact sensitive content, and block unsupported sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting summaries can contain unsupported decisions, commitments, owners, dates, or attributions. <br>
Mitigation: Ground each material item in transcript or meeting evidence, label uncertain items, and ask for confirmation when evidence is missing. <br>
Risk: Meeting context may include secrets, customer data, employee information, or unrelated private content. <br>
Mitigation: Use only necessary meeting context, redact sensitive or unrelated details, and prefer minimal redacted payloads for any approved checker. <br>
Risk: The server evidence includes unrelated capability tags that could confuse users about the skill behavior. <br>
Mitigation: Rely on the security summary and artifact behavior: this release is instruction-only and does not make purchases, handle crypto, execute code, or access data by itself. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mindbomber/aana-meeting-summary-checker) <br>
- [Meeting summary checker schema](schemas/meeting-summary-checker.schema.json) <br>
- [Redacted meeting summary checker example](examples/redacted-meeting-summary-checker.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with a structured text checklist and optional JSON review payload] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; expects meeting evidence supplied by the user or an approved host tool; no code execution, persistence, or autonomous transcript access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
