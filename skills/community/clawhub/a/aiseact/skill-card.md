## Description:

AISEACT guides agents to plan searches, prioritize primary and authoritative sources, filter low-quality sources, and cross-verify findings for research and fact-checking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stephenlzc](https://clawhub.ai/user/stephenlzc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use AISEACT when they want web research with explicit source planning, authority ranking, and cross-validation. It is most useful for business, technical, policy, academic, and fact-checking tasks where source quality matters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Source guidance may narrow results toward official, mainstream, or pre-rated sources.

Mitigation: Keep the default manual mode, request diverse viewpoints when needed, and use documented overrides to include specific sources.

Risk: Source ratings and reference lists may become stale or reflect methodological bias.

Mitigation: Check current primary sources for important claims and adjust strictness, language, or region preferences for the research context.

Risk: Autonomous invocation can change normal search behavior if enabled.

Mitigation: Use autonomous mode only by explicit configuration choice and apply the documented skip commands when standard search is preferred.

Risk: Modified skill files could change search guidance.

Mitigation: Review SKILL.md and reference documents before deployment; the release evidence reports no executable code, credential access, persistence, or hidden data handling.

## Reference(s):

- [AISEACT ClawHub listing](https://clawhub.ai/stephenlzc/skills/aiseact)
- [Configuration Guide](CONFIGURATION.md)
- [Trust & Transparency Report](TRUST.md)
- [Security Information](SECURITY.md)
- [Quick Source Reference](references/quick-reference.md)
- [Authoritative Sources Recommendation List](references/authority-sources.md)
- [AISEACT Detailed Workflow](references/workflow.md)
- [Search Strategies and Techniques](references/search-strategies.md)
- [Unreliable Sources Reference](references/unreliable-sources.md)
- [Reference Cases](references/case-studies.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown text with citations, source-quality notes, and optional configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include URLs, source reliability labels, uncertainty notes, and user-requested source overrides.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
