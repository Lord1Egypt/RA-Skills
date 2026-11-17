## Description:

Finds cross-discipline clash and property-conflict candidates in CAD drawings, using axis-grid locations when available; every candidate requires human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lisong2003-lgtm](https://clawhub.ai/user/lisong2003-lgtm)

### License/Terms of Use:

CC-BY-NC-SA-4.0

## Use Case:

Developers and engineering teams use it to review DWG/DXF drawings or parsed drawing data before cross-discipline coordination. It reports possible overlaps and attribute conflicts for human review; it does not perform BIM clash detection or calculate quantities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A report may appear complete even when wall or opening extraction did not finish, and helper commands require review before use.

Mitigation: Review helper command requirements before execution; confirm wall and opening extraction completed and inspect the results instead of relying on a completed status alone.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/lisong2003-lgtm/skills/cad-clash-check)
- [Publisher profile](https://clawhub.ai/user/lisong2003-lgtm)

## Skill Output:

**Output Type(s):** [Files, JSON, Markdown]

**Output Format:** [JSON and Markdown clash reports and construction-plan templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Candidate locations and attribute conflicts for human review; no quantity estimates.]

## Skill Version(s):

0.3.4 (source: ClawHub release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
