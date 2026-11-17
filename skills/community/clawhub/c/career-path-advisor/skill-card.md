## Description:

Map your career trajectory: skill gap analysis, role transitions, and personalized learning roadmaps based on market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and career advisors use this skill to compare a professional profile with target-role market demands, explore career transitions, and produce skill-gap analyses, learning roadmaps, and offer decision matrices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI script unsafely embeds a user-provided target role into Python code, so crafted profile or target-role text could run unintended code on the user's machine.

Mitigation: Review before installing, do not run the script on profile or target-role text supplied by untrusted parties, and change the script to pass target_role as JSON data or an argument before broader use.

Risk: Career plans, salary ranges, and market trends may be wrong, stale, or overconfident for a user's location, industry, or experience level.

Mitigation: Treat outputs as planning guidance, verify market data and job requirements from current public sources, and avoid presenting the roadmap as a guaranteed career outcome.

## Reference(s):

- [Role categories and transferable skill mappings](artifact/references/roles.json)
- [Input schema](artifact/schemas/input.schema.json)
- [Output schema](artifact/schemas/output.schema.json)
- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/career-path-advisor)
- [jq documentation](https://stedolan.github.io/jq/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown report or JSON object with career profile, exploration, gap analysis, paths, resources, and warnings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include text radar charts, gap matrices, salary ranges, milestone plans, and weighted offer comparisons.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, skill.json, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
