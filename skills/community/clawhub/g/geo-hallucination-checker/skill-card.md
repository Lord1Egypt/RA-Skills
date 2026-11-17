## Description:

Detects and annotates hallucinations, unsupported claims, fabricated studies, and incorrect conclusions in text so that AI only cites verifiable, trustworthy content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geoly-geo](https://clawhub.ai/user/geoly-geo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content reviewers, and teams preparing published or GEO-optimized content use this skill to fact-check drafts, classify unsupported or risky claims, and produce safer evidence-friendly rewrites when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording may cause the skill to be invoked for a wide range of fact-checking and content review tasks.

Mitigation: Use explicit task constraints when narrow activation is desired, such as source limits, domain scope, or whether external lookup is allowed.

Risk: The optional heuristic script is not a full fact-checking engine and may miss or over-flag claims.

Mitigation: Treat script output as a pre-screening aid and require source review and human judgment before publication or citation.

## Reference(s):

- [Hallucination Guide](references/hallucination_guide.md)
- [ClawHub Skill Page](https://clawhub.ai/geoly-geo/skills/geo-hallucination-checker)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summary, claim-level table, and optional hallucination-safe rewrite]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include claim status, risk level, rationale, suggested fixes, and safer replacement copy.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
