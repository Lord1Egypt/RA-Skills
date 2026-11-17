## Description:

Checks AI answers, articles, and claims by decomposing facts, retrieving reference information, running multi-perspective verification, checking internal consistency, and reporting a confidence score.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuehengzhang10-hub](https://clawhub.ai/user/xuehengzhang10-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Users and developers use this skill to fact-check AI-generated answers or longer claims in Chinese or English. It produces a transparent verification report with atomic facts, source-based judgments, multi-perspective reasoning, consistency checks, and an overall score.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional reference scripts can send user text to configured external LLM providers.

Mitigation: Use the core zero-configuration skill for sensitive content, or run the optional scripts only after accepting the providers' data handling policies.

Risk: Optional reference scripts use API keys and configurable API endpoints.

Mitigation: Run them in a dedicated virtual environment with least-privileged keys, avoid exposing unrelated environment variables, and set custom API base URLs only for trusted endpoints.

Risk: Fact-checking outputs can still be uncertain or wrong when references are incomplete or conflicting.

Mitigation: Review the cited sources, fact-level verdicts, and unable-to-verify items before relying on the final score.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuehengzhang10-hub/skills/checktruth)
- [Optional multi-model reference implementation](reference/README.md)
- [Skill design document](docs/skill_design.md)
- [Open-source research notes](docs/opensource_research.md)
- [FActScore reference project](https://github.com/shmsw25/FActScore)
- [xVerify reference project](https://github.com/IAAR-Shanghai/xVerify)
- [AIQualityKit reference project](https://github.com/LambertClark/AIQualityKit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown verification report, with optional JSON output from reference scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports fact-level verdicts, confidence scores, cited references, consistency findings, and an overall score; optional scripts may write verification_result.json.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
