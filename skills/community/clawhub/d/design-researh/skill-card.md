## Description:

Design Research Scout helps design teams clarify fuzzy briefs, run early-stage research, set direction, and collect qualified inspiration references from approved design sites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhusunlangzi668](https://clawhub.ai/user/zhusunlangzi668)

### License/Terms of Use:

MIT-0

## Use Case:

Design teams use this skill before visual execution to validate requirements, clarify briefs, frame research questions, choose distinct design directions, and gather inspiration references or search leads. It is especially suited for early-stage design research, moodboard preparation, competitive or cross-industry reference collection, and Chinese-language design handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may perform external design-site searches using information from user briefs.

Mitigation: Avoid sharing confidential brief details in external searches; review generated search terms before use when briefs contain sensitive business, client, or campaign information.

Risk: The bundled MCP configuration downloads current npm packages at runtime and includes unpinned MCP package versions.

Mitigation: Pin MCP package versions before deployment, review the MCP servers, and use a limited Brave API key.

Risk: Research conclusions and inspiration recommendations may be misleading if the brief is incomplete or source coverage is weak.

Mitigation: Keep the skill's brief calibration step, require explicit source coverage notes, and review outputs before using them for client or production design decisions.

## Reference(s):

- [Brief Intake Checklist](references/brief-intake-checklist.md)
- [Online Image Search Workflow](references/image-search-workflow.md)
- [Quality Gate](references/quality-gate.md)
- [Chinese Output Template](references/output-template-zh.md)
- [Common Use Cases](references/use-cases.md)
- [Art Inspiration Search Guide](references/art-inspiration-search.md)
- [Expert Routing](references/expert-routing.md)
- [Example Scenario: Activity Page Research](references/example-scenario-activity-page.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown in Chinese by default, with research sections, design directions, reference links or keyword packs, and quality judgments.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include links from Behance, Zcool, Huaban, and Xiaohongshu when browsing is available; otherwise returns site-specific search keywords and screening guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
