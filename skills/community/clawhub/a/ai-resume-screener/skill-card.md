## Description:

Automatically parse, score, and rank large batches of resumes by matching candidate information against job requirements, with support for multiple resume formats and screening analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

HR teams and recruiters use this skill to configure resume parsing, batch screening, candidate scoring, ranking, and analytics against defined job requirements. It is intended for hiring workflows that include authorization to process candidate data and human review of screening results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports bulk processing and ranking of sensitive candidate data without built-in privacy, consent, retention, or access-control guidance.

Mitigation: Use only with authorization to process the resumes, define where candidate data may be stored or sent, and apply privacy, deletion, and audit controls before use.

Risk: Automated resume scoring can affect hiring outcomes and may produce incorrect or biased rankings.

Mitigation: Require human review of recommendations, validate scoring criteria against job requirements, and monitor outcomes for bias before making hiring decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/skills/ai-resume-screener)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with YAML and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides resume-screening workflow guidance, job-requirement configuration examples, and ranking-oriented command examples.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
