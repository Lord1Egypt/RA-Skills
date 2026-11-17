## Description:

cn-holidays helps agents query Chinese statutory public holidays by year, month, or date using the Nager.Date public API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tonyhuya](https://clawhub.ai/user/tonyhuya)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents can look up China public holiday dates for a full year, a specific month, or a specific day. It is suited for planning and scheduling workflows that need public-holiday awareness, but users should verify official notices when adjusted leave or make-up workday schedules matter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Holiday lookups are sent to the Nager.Date public API.

Mitigation: Confirm that sending the requested year, month, or date to a public API is acceptable for the workflow before use.

Risk: Nager.Date holiday data does not include Chinese adjusted leave or make-up workday schedules.

Mitigation: Verify official Chinese government holiday notices before using the output for operational, payroll, travel, or compliance decisions.

Risk: The skill relies on local curl and python3 availability.

Mitigation: Install or approve these dependencies before running the skill in an agent environment.

## Reference(s):

- [cn-holidays on ClawHub](https://clawhub.ai/tonyhuya/skills/cn-holidays)
- [Nager.Date](https://date.nager.at/)
- [Nager.Date Public Holidays API](https://date.nager.at/api/v3/PublicHolidays)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text with optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access to the Nager.Date public API and local curl and python3 availability.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
