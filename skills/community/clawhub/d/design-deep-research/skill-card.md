## Description:

Graphic design deep research: automatically collects design references across domestic and international platforms (Behance, Dribbble, Pinterest, Zcool, Huaban), performs cluster analysis on aesthetic trends, and outputs visual HTML research reports with reusable exploratory prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fize](https://clawhub.ai/user/fize)

### License/Terms of Use:

MIT-0

## Use Case:

Designers, creative strategists, and agents use this skill to research visual directions, gather verified design references, cluster aesthetic trends, and create reusable exploratory prompt seeds before producing finished design work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may include untrusted user or web content.

Mitigation: Review and sanitize report content before opening or sharing generated HTML files.

Risk: Research briefs may contain confidential project details.

Mitigation: Use non-sensitive briefs unless the workflow is updated to protect confidential inputs and generated reports.

Risk: Collected links and image URLs may be stale, broken, or unsafe.

Mitigation: Validate source links and image URLs before relying on them in a report or downstream design workflow.

Risk: The workflow writes to a generated design-research directory.

Mitigation: Check the target output path before running the skill to avoid overwriting existing research artifacts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fize/skills/design-deep-research)
- [Publisher Profile](https://clawhub.ai/user/fize)
- [Aesthetic Analysis Framework](references/analysis-framework.md)
- [Design Research Platform Guide](references/platform-guide.md)
- [HTML Research Report Template](references/report-template.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown research notes, shell commands, configuration guidance, exploratory prompt text, and standalone HTML report code.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a design-research workspace containing reference notes and a browser-viewed report.html.]

## Skill Version(s):

0.1.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
