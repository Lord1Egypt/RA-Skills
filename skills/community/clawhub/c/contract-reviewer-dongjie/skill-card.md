## Description:

Analyzes contract text to extract key clauses, risk indicators, obligations, compliance notes, and negotiation recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dj-520-ai](https://clawhub.ai/user/dj-520-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Consultants, freelancers, small business owners, and analysts use this skill to get a fast structured review of contract text, including clause categories, risks, obligations, and negotiation points. It is a lightweight aid and should not be treated as legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides simple keyword-based contract checks that may miss issues or overstate legal risk.

Mitigation: Use the output as triage guidance only and have qualified legal or compliance reviewers validate important contract decisions.

Risk: The release evidence notes a stale lockfile with unnecessary dependency data.

Mitigation: Regenerate or remove the lockfile before installation in strict workflows so unused dependencies are not processed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dj-520-ai/skills/contract-reviewer-dongjie)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Structured text or JSON-like findings with a summary, detected clauses, risk labels, notes, and input length.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Input is contract text; findings are based on keyword and pattern matching.]

## Skill Version(s):

0.1.0 (source: server release metadata, artifact/package.json, artifact/skill.yaml, artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
