## Description:

Reviews code for security, performance, and style issues, then returns scored findings and improvement suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[467718584](https://clawhub.ai/user/467718584)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review code paths for security, performance, and style issues and receive prioritized findings, scores, summaries, and suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reviews code paths explicitly provided by the user, which may include sensitive source code.

Mitigation: Provide only intended code paths and use it only in environments where that review scope is acceptable.

Risk: The skill and expected review output are Chinese-language, which may be unsuitable for reviewers who cannot validate the guidance.

Mitigation: Have a Chinese-capable reviewer validate findings and recommendations before applying changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/467718584/skills/eo-ability-code-review)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with scores, prioritized issues, suggestions, and summary text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include security, performance, style, and overall scores.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
