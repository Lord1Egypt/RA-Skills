## Description:

Classifies financial AI applications into risk grades I–III and provides decision-support guidance in JSON format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and compliance teams use this local CLI to estimate the risk tier and potential obligations of a financial AI application before human review. It does not determine licensing status or replace official regulatory guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Risk grades and obligations may not match current financial regulations.

Mitigation: Use results only as decision support; verify rules and filing requirements against current official sources before acting.

Risk: Incomplete application details can yield an overly conservative grade.

Mitigation: Provide autonomy and impact details, review warnings, and have a qualified person confirm the result.

Risk: The skill requests tool permissions beyond those needed for its local classifier.

Mitigation: Remove or enforce unused Bash, Write, and WebFetch allowances, and run only the bundled Python CLI as intended.

## Reference(s):

- [ClawHub release: fin-ai-classifier](https://clawhub.ai/zhaoxinghua09-cell/skills/fin-ai-classifier)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON on standard output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes risk grade, possible obligations, warnings and a status code; incomplete inputs may produce a conservative grade with warnings.]

## Skill Version(s):

1.0.2 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
