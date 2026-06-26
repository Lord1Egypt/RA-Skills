## Description: <br>
Generates a Markdown report from CSV survey responses with keyword-based sentiment counts, sample responses, and basic recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1477009639zw-blip](https://clawhub.ai/user/1477009639zw-blip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts can use this skill to turn open-ended beta survey responses in a CSV file into a concise Markdown report with sentiment totals, sample comments, and follow-up recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The advertised AI clustering and external-LLM capabilities are not clearly aligned with the bundled implementation. <br>
Mitigation: Treat results as basic keyword-based summarization and verify conclusions before using them for product or customer decisions. <br>
Risk: Survey responses may contain sensitive user or customer feedback. <br>
Mitigation: Review inputs for sensitive data and confirm whether any future implementation sends data to OpenAI, Anthropic, or another provider before using confidential responses. <br>
Risk: The command writes a report to a caller-supplied output path and could overwrite an existing file. <br>
Mitigation: Choose a non-critical output path and review the generated report before sharing it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/1477009639zw-blip/betasurvey) <br>
- [Publisher profile](https://clawhub.ai/user/1477009639zw-blip) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report written to a file, with a short shell status message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a CSV input path and writes to a user-selected Markdown output path; default output file is report.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
