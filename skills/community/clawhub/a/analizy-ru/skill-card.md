## Description: <br>
Explains medical lab results in Russian, highlights values outside reference ranges, and suggests topics to discuss with a doctor. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aggel008](https://clawhub.ai/user/aggel008) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External Russian-speaking users use this skill to understand medical lab test values, identify out-of-range results, and prepare questions for a doctor. The output is informational and is not a medical diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical lab explanations may be incomplete, incorrect, or mistaken for clinical advice. <br>
Mitigation: Treat the output as informational only and confirm interpretation with a qualified clinician using symptoms, history, age, sex, and lab-specific reference ranges. <br>
Risk: The security review reports local Python command execution and a persistent counter file. <br>
Mitigation: Review before installing, and remove or explicitly disclose the command execution and local state behavior before routine use. <br>
Risk: The security review reports promotional Telegram links appended to some responses. <br>
Mitigation: Remove promotional links or clearly disclose them before deploying the skill in user-facing workflows. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown text with tables, an informational medical disclaimer, and optional shell command behavior described by the artifact.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may append promotional Telegram links and use a local persistent counter according to the artifact.] <br>

## Skill Version(s): <br>
1.0.2 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
