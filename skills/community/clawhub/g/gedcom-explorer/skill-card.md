## Description:

GEDCOM Explorer generates a self-contained interactive HTML dashboard from a GEDCOM (.ged) file, with family-tree views, people search, timeline events, daily alerts, and person detail modals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justinhartbiz](https://clawhub.ai/user/justinhartbiz)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to turn GEDCOM genealogy exports into a local, searchable family history dashboard for exploration and sharing with intended recipients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GEDCOM-supplied HTML or JavaScript may execute in the generated dashboard.

Mitigation: Process only GEDCOM files from trusted sources and avoid opening generated dashboards from unknown GEDCOM inputs until data escaping is confirmed safe.

Risk: The generated HTML is a shareable export that can include private or hidden family-tree records.

Mitigation: Keep generated HTML files private unless publishing the complete family-tree data is intentional.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justinhartbiz/skills/gedcom-explorer)
- [Publisher profile](https://clawhub.ai/user/justinhartbiz)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands that produce a single-file HTML dashboard]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated HTML embeds parsed family-tree data and can be opened locally without a server.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
