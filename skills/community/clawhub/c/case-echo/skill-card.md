## Description: <br>
Extract simple structured JSON fields from a short Chinese medical case description. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heyheya11](https://clawhub.ai/user/heyheya11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to convert short Chinese medical case summaries into standardized JSON fields such as sex, age, diagnosis, stage, EGFR, PD-L1, and brain metastasis status. It structures text only and does not provide diagnosis or treatment recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical case text may contain sensitive personal or clinical information. <br>
Mitigation: Treat input case text as sensitive and avoid unnecessary disclosure or retention. <br>
Risk: Unsafe shell string construction could expose case text or alter command execution. <br>
Mitigation: Invoke the bundled script with safe argument passing instead of interpolating untrusted text into a shell command string. <br>
Risk: Structured extraction can omit or misread fields when the input wording differs from the parser's simple patterns. <br>
Mitigation: Review extracted JSON before using it in downstream analysis, and do not treat it as medical diagnosis or treatment guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/heyheya11/case-echo) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/heyheya11) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands] <br>
**Output Format:** [JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Missing fields are returned as null, and raw_text preserves the input text.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
