## Description:

This skill helps agents retrieve and manage App Store Connect apps, TestFlight builds and testers, customer reviews, sales reports, and team users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to inspect App Store Connect apps, builds, reviews, sales and finance reports, beta testers, and team users, and to perform supported management actions after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP server implementation is absent from this package, so its actual write-approval behavior was not assessed.

Mitigation: Use a trusted MCP server and verify it requests approval before writes; limit the Apple API key to the roles and apps needed.

## Reference(s):

- [App Store Connect API](https://developer.apple.com/documentation/appstoreconnectapi)

## Skill Output:

**Output Type(s):** [Structured data, Reports, Guidance]

**Output Format:** [Structured MCP tool results; sales and finance reports are represented as row data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sales report results default to 500 rows and include the total row count.]

## Skill Version(s):

1.4.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
