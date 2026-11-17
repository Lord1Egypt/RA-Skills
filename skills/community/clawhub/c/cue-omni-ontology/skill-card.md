## Description:

Turns user-selected public documents into reusable, source-linked business knowledge packages and change briefs, with optional checks that extracted numbers match their cited sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT

## Use Case:

Analysts and developers use the skill to organize public reports and announcements into reusable, source-linked knowledge packages, compare changes across releases, and prepare evidence briefs for disclosure tracking, supplier diligence, or product monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial evidence checks may accept unsupported numbers or misleading page citations.

Mitigation: Manually compare numeric values, units, excerpts, and page citations with the original documents; treat generated strengths and causal links as heuristics.

Risk: External installer and parser behavior has not been verified.

Mitigation: Prefer a reviewed installer version and immutable skill revision, and authorize cloud parsing only for the intended documents.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huhoo/skills/cue-omni-ontology)
- [Knowledge contract](references/knowledge-contract.md)
- [Update policy](references/update-policy.md)
- [Verification record](references/verification.md)
- [Task recipes](references/task-recipes.md)
- [Official cue-omni-reader setup](https://github.com/sensedeal/cue-skills/blob/main/cue-omni-reader/references/setup.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, HTML]

**Output Format:** [Evidence briefs and reusable knowledge packages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source excerpts and citations; optional numeric checks compare extracted values with source text. Human review is needed to confirm evidence and conclusions.]

## Skill Version(s):

0.3.18 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
