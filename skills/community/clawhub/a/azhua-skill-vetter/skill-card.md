## Description:

Security-first skill vetting for AI agents. Use before installing any skill from ClawdHub, GitHub, or other sources. Checks for red flags, permission scope, and suspicious patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fatfingererr](https://clawhub.ai/user/fatfingererr)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to review skills before installation by checking source credibility, file behavior, permission scope, and security risk indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub lookup commands could be aimed at repositories outside the intended review scope.

Mitigation: Run lookup commands only for candidate repositories being reviewed and confirm the target before using the results.

Risk: A file review could expand into unrelated local files or credentials.

Mitigation: Limit review to the candidate skill artifact and avoid credential stores, personal configuration, and unrelated workspace files.

Risk: The checklist output could be treated as an automatic security decision.

Mitigation: Use the report as review guidance and require human approval for high-risk findings or install decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fatfingererr/skills/azhua-skill-vetter)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown vetting report with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report includes source, author, version, metrics, red flags, permissions, risk level, verdict, and notes.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata, artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
