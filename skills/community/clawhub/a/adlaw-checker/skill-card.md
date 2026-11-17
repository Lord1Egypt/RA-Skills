## Description:

Adlaw Checker reviews Chinese advertising copy for Ad Law risk terms, false-advertising phrases, platform-specific rules, and suggested rewrites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eric060](https://clawhub.ai/user/eric060)

### License/Terms of Use:

MIT-0

## Use Case:

Marketers, copywriters, and agents use this skill to screen Chinese advertising copy before publication and receive risk findings, compliance scores, rewrite suggestions, and platform-specific cautions. Its output should support, not replace, human review for important advertising claims.

### Deployment Geography for Use:

Global, for Chinese-language advertising workflows that need Chinese advertising-law screening.

## Known Risks and Mitigations:

Risk: The checker is a rough keyword tool and may miss context, current legal requirements, or jurisdiction-specific interpretation.

Mitigation: Use it for preliminary screening only and require manual legal or compliance review for important advertising copy.

Risk: The documented dependency installation step may introduce unnecessary or unpinned packages into the runtime environment.

Mitigation: Install in an isolated environment and remove or pin dependencies that are not required for the local checker workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eric060/skills/adlaw-checker)
- [Advertising Law reference](http://www.gov.cn/gongbao/content/2015/content_2893774.htm)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON check results, and Python or shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can emit per-text or batch violation lists, risk levels, compliance scores, suggestions, timestamps, and rewritten copy.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
