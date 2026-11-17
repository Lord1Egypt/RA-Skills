## Description:

AI Fact Checker verifies factual claims in AI-generated text by extracting checkable statements, searching the web, assigning confidence scores, and suggesting corrections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rudagebil11-jpg](https://clawhub.ai/user/rudagebil11-jpg)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check factual claims in AI-generated answers, documents, or short statements. It produces a structured fact-checking report with per-claim confidence scores, source links, and correction guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for checking is passed to online search, which can expose secrets or confidential material.

Mitigation: Warn users not to submit secrets or confidential text, and route sensitive claims through an approved internal search or review process.

Risk: The scanner reports that checked text can become shell command execution through the script's current command construction.

Mitigation: Review before installing, replace shell string interpolation with an argument-array API such as execFileSync, and add input length and timeout controls.

## Reference(s):

- [Ai Fact Checker ClawHub page](https://clawhub.ai/rudagebil11-jpg/skills/ai-fact-checker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown fact-checking report with confidence scores, verdicts, source links, and corrections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires web search access; no additional API key is described in the artifact.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
