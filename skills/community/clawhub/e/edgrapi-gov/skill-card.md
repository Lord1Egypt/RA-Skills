## Description:

Retrieves US federal contract opportunities, awards, grants, and House stock-trading disclosures through Edgrapi in a normalized JSON format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paperandbeyond23-gif](https://clawhub.ai/user/paperandbeyond23-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, procurement teams, and developers use this skill to find US federal opportunities, awards, grants, and House trading disclosures when users request sourced records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calls send an Edgrapi API key to Edgrapi.com.

Mitigation: Use a dedicated key and grant network access only if sending it to Edgrapi.com is acceptable.

Risk: Each tool call consumes Edgrapi credits.

Mitigation: Run searches only for explicit federal-data requests and monitor credit use.

Risk: House disclosures can lag and report dollar ranges; results do not cover Senate trades or state and local procurement.

Mitigation: State the source, coverage, disclosure lag, and amount ranges when reporting results.

## Reference(s):

- [Edgrapi](https://edgrapi.com)
- [ClawHub skill listing](https://clawhub.ai/paperandbeyond23-gif/skills/edgrapi-gov)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON records or text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records cover US federal sources and House trades only; trade values are ranges and disclosures may lag.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
