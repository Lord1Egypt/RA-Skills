## Description:

Bidding Compliance Guard locally checks Chinese bidding, procurement, and related business text for common high-risk compliance phrases, including bid rigging, false qualifications, competitor disparagement, price manipulation, bribery, and exclusionary clauses, then returns risk levels and suggested revisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

External compliance, procurement, bidding, and agent developers can run this local guard before publishing or submitting Chinese bidding documents, procurement announcements, qualification notices, award notices, business responses, or company publicity. It flags high-frequency risky wording and suggests revisions, but it does not replace legal review.

### Deployment Geography for Use:

Global, with intended use limited to Chinese PRC bidding and procurement text.

## Known Risks and Mitigations:

Risk: The guard is limited to Chinese PRC bidding and procurement compliance phrasing and uses simple keyword matching, so it can miss issues or flag harmless negations.

Mitigation: Use results as screening guidance and have qualified legal or compliance reviewers confirm final documents against official laws and project facts.

Risk: The documented --file option is not implemented in the CLI evidence.

Mitigation: Use --text or --stdin until file-input behavior is implemented and verified.

Risk: The CLI help title has a wrong domain label.

Mitigation: Review and correct user-facing help text before operational rollout.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwumit/skills/bidding-compliance-guard)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Plain text or JSON findings with decision, risk level, matched terms, categories, spans, and revision suggestions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local keyword matching over user-supplied text; no network use, telemetry, dynamic execution, or third-party dependencies are indicated by the evidence.]

## Skill Version(s):

1.0.0 (source: release evidence, SKILL.md frontmatter, CHANGELOG, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
