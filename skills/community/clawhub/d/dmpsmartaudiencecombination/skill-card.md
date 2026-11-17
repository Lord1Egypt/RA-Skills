## Description:

Turns natural-language campaign requirements into DMP tag-combination plans and parameters for creating combined audiences.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mingri26](https://clawhub.ai/user/mingri26)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams and DMP operators use this skill to translate campaign requirements into eligible audience tags, compare combinations, and create combined audience segments in 明日DMP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated scripts can create or change DMP audience resources without reliably enforcing the documented final-plan approval.

Mitigation: Require explicit user approval of the exact final plan before allowing any audience-creation action, and review account changes afterward.

Risk: The skill can access DMP credentials and execute a loosely discovered authentication helper.

Mitigation: Review before installation, verify the exact mingdata-dmp-auth package before execution, and grant credential access only in a trusted environment.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/mingri26/skills/dmpsmartaudiencecombination)
- [明日DMP API reference](references/api_reference.md)
- [明日DMP authentication skill](https://clawhub.ai/mingri26/mingdata-dmp-auth)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, JSON]

**Output Format:** [Markdown guidance and JSON audience rules and creation parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create DMP audience resources and report audience IDs and task status.]

## Skill Version(s):

1.0.1 (source: server release metadata; embedded skill metadata says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
