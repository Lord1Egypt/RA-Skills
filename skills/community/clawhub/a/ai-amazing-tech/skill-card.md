## Description:

Routes technology-domain keywords or patent search queries to technology landscape, patent mining, or technology intelligence briefing workflows and produces unified HTML reports using PatSnap patent data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

IPR teams, R&D engineers, and strategy decision-makers use this skill to analyze technology landscapes, mine patent opportunities, and produce technology intelligence briefs from technology keywords or patent search queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may connect the agent to a PatSnap MCP account and web-search tools for patent and industry research.

Mitigation: Install only in environments where those account connections and tool permissions are intended and reviewed.

Risk: Generated HTML reports may contain sensitive patent strategy, competitive intelligence, or business-planning content.

Mitigation: Treat generated reports as confidential business documents and review them before sharing outside the intended audience.

Risk: HTML reports can load chart and style assets from external CDNs unless those assets are bundled or integrity-pinned.

Mitigation: Prefer bundled or integrity-pinned assets before opening or distributing reports in high-trust browser contexts.

## Reference(s):

- [Reference UI Template](references/reference_ui_template.html)
- [PatSnap Open Platform](https://open.zhihuiya.com/)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [HTML reports with structured narrative, charts, source labels, and user confirmation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are expected to show matched_total patent counts and use a consistent visual template across the three modules.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
