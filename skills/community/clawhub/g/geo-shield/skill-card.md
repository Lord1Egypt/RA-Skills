## Description:

Geo Shield checks URLs for heuristic signs of GEO poisoning, AI-targeted misinformation, SEO manipulation, and AI-optimized risky content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rfdiosuao](https://clawhub.ai/user/rfdiosuao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate a quick credibility and risk report for a submitted URL, including GEO-pattern counts, domain/source scoring, content-quality indicators, and verification suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may present URL credibility reports without fetching or analyzing the submitted webpage content.

Mitigation: Treat generated reports as heuristic signals only and verify the target content manually until actual page fetching and analysis are implemented.

Risk: Heuristic domain and pattern scoring can misclassify information quality or source credibility.

Mitigation: Cross-check important claims against authoritative sources and clearly label scores as non-definitive.

Risk: Broad command and natural-language triggers may activate during unrelated conversations.

Mitigation: Prefer explicit commands for production use and narrow activation triggers before broad deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rfdiosuao/skills/geo-shield)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with a credibility score, risk level, feature counts, content-quality indicators, and verification suggestions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single URL-oriented report; the artifact declares no runtime external API dependency.]

## Skill Version(s):

1.0.0 (source: server release, artifact skill.json, artifact package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
