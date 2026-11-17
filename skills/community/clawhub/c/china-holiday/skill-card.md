## Description:

Provides a China mainland calendar helper that identifies statutory holidays, weekends, adjusted workdays, and school vacation periods for supported cities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[violin](https://clawhub.ai/user/violin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations users can use this skill to check Chinese mainland holiday and workday status, list annual holidays, and query configured school vacation windows for supported cities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The chinese-calendar dependency is not pinned, so installs can receive changed package versions over time.

Mitigation: Install in an isolated Python environment and pin chinese-calendar to a reviewed version before production use.

Risk: Holiday and vacation responses are focused on China Mainland rules and the configured supported cities.

Mitigation: Confirm outputs against official calendars or local policy before using them for business-critical scheduling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/violin/skills/china-holiday)
- [ClawHub publisher profile](https://clawhub.ai/user/violin)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Guidance]

**Output Format:** [Plain text responses, Markdown guidance, and Python API call snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and the chinese-calendar Python package; outputs are focused on China Mainland holiday rules.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
