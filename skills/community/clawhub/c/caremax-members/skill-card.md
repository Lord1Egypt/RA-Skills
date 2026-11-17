## Description:

Manage family member profiles in CareMax Health for listing members, switching profiles, and scoping health queries to a selected member.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kittenyang](https://clawhub.ai/user/kittenyang)

### License/Terms of Use:

MIT-0

## Use Case:

CareMax users and their agents use this skill to list family member profiles and run member-scoped CareMax health queries for spouses, children, parents, or other linked profiles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an external caremax-auth sibling skill and can initiate authentication for sensitive health data.

Mitigation: Install only a trusted and reviewed caremax-auth dependency, and confirm the CareMax account and server URL before authentication begins.

Risk: Member-scoped queries can expose health data for spouses, children, parents, or other linked profiles.

Mitigation: Confirm the intended family member before running memberId-scoped indicator, record, or search queries.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/kittenyang/skills/caremax-members)
- [ClawHub publisher profile](https://clawhub.ai/user/kittenyang)

## Skill Output:

**Output Type(s):** [guidance, shell commands, API calls, configuration]

**Output Format:** [Markdown guidance with inline bash commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a sibling caremax-auth skill and authenticated CareMax access before member data can be queried.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata, created 2026-03-29)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
