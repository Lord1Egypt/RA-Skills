## Description:

Helps marketers and growth teams estimate dark social contribution by specifying share-link UTM hygiene, self-reported attribution capture, GA4 direct-traffic decomposition, and branded-search-lift proxy analysis while labeling derived numbers as Estimated or proxy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, growth, and analytics practitioners use this skill to explain otherwise unattributed direct traffic, design share-link and self-reported attribution instrumentation, and present dark-social estimates without treating proxies as measured conversions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GA4/GSC exports, form inventories, and marketing-memory records may contain sensitive customer, traffic, or business data.

Mitigation: Use only approved, minimized exports in the agent environment and avoid supplying unnecessary personal or confidential fields.

Risk: Optional saved results or proposed channel facts could preserve inaccurate attribution claims.

Mitigation: Approve save or propose steps only after reviewing that generated facts are accurate, source-labeled, and appropriate to retain.

Risk: Dark-social decomposition and branded-search lift can be misread as measured attribution.

Mitigation: Keep heuristic outputs labeled Estimated or proxy and report self-reported counts alongside, not merged into, click-based attribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/dark-social-attributor)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown attribution pack with instrumentation specs, labeled estimate tables, and a handoff summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Derived attribution numbers are labeled Estimated or proxy; optional save and propose steps require user approval.]

## Skill Version(s):

19.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
