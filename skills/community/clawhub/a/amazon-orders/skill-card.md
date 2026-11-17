## Description:

Download and query your Amazon order history via an unofficial Python API and CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pfernandez98](https://clawhub.ai/user/pfernandez98)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to install and operate the unofficial amazon-orders Python package and CLI for Amazon.com order-history retrieval, filtering, and export.

### Deployment Geography for Use:

Global; functional support is stated for the English Amazon.com site.

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned unofficial package that handles Amazon credentials.

Mitigation: Use a virtual environment, avoid sudo, consider pinning and verifying the amazon-orders package, and expose Amazon credentials only to the command that needs them.

Risk: Exported order-history files can contain sensitive purchase and account data in plaintext.

Mitigation: Store exported files in a private protected location with restrictive permissions and remove them when no longer needed.

Risk: The underlying tool is an unofficial scraper for Amazon's consumer website and may break when Amazon changes page behavior.

Mitigation: Review generated commands and validate retrieved order data before relying on it for decisions or downstream automation.

## Reference(s):

- [Amazon Orders ClawHub release](https://clawhub.ai/pfernandez98/skills/amazon-orders)
- [amazon-orders project homepage](https://github.com/alexdlaird/amazon-orders)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of plaintext JSON or TSV order-history exports through CLI commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
