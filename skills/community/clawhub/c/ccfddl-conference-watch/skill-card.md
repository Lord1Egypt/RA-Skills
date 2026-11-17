## Description:

Fetch and filter academic conference deadlines from CCFDDL for CCF conference, CFP, venue selection, and deadline queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengwm64](https://clawhub.ai/user/fengwm64)

### License/Terms of Use:

MIT-0

## Use Case:

Students, researchers, and academic authors use this skill to find upcoming CCFDDL conference deadlines by venue name, research category, and CCF rank, then review the results as a concise sorted table.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conference deadline data may be incomplete, stale, or unavailable from the public CCFDDL source.

Mitigation: Verify important submission deadlines against the official conference page before relying on them.

Risk: Broad academic deadline wording can activate the skill for queries where CCFDDL is not the intended source.

Mitigation: Confirm that the user wants CCFDDL-based conference deadline information before presenting results as authoritative.

## Reference(s):

- [CCFDDL](https://ccfddl.com)
- [CCFDDL conference deadlines RSS feed](https://ccfddl.com/conference/deadlines_zh.xml)
- [ClawHub skill page](https://clawhub.ai/fengwm64/skills/ccfddl-conference-watch)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown table with a concise summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are filtered to upcoming deadlines, sorted by earliest deadline, and preserve source timezone labels.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
