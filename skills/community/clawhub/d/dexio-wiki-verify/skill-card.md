## Description:

Checks high-priority LLM wiki claims against cited sources, corrects unsupported or outdated claims and their copies, and reports the verification results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dexio](https://clawhub.ai/user/dexio)

### License/Terms of Use:

MIT-0

## Use Case:

Wiki maintainers and agents use this skill to check decision-critical or questionable wiki pages against their cited sources, correct errors across copied pages, and document what remains unverified.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect corrections may change decision-critical wiki pages or propagate across pages that repeat a claim.

Mitigation: Review wiki diffs and change notes, especially for decision-critical pages, before relying on the changes.

Risk: The agent reads wiki pages and their cited sources during verification.

Mitigation: Confirm access to the wiki and cited sources is appropriate before installing or running the skill.

## Reference(s):

- [Wiki Verify (Dexio) on ClawHub](https://clawhub.ai/dexio/skills/dexio-wiki-verify)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Updated wiki pages and a written verification report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Claim classifications, dated corrections, and unresolved issues are recorded.]

## Skill Version(s):

1.1.0 (source: skill frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
