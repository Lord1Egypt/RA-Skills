## Description:

Find every trade show a company has exhibited at using the Lensmor API for competitive intelligence, account research, and show circuit mapping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weilun88313](https://clawhub.ai/user/weilun88313)

### License/Terms of Use:

MIT-0

## Use Case:

External users and sales, marketing, or event teams use this skill to research a company's trade show exhibitor history, identify recurring show participation, and plan competitive or account outreach around relevant events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company identifiers are sent to Lensmor when the skill performs exhibitor show-history lookups.

Mitigation: Use the skill only when sharing the queried company name, domain, or URL with Lensmor is acceptable.

Risk: The skill requires a Lensmor API key.

Mitigation: Configure LENSMOR_API_KEY in the runtime environment and never include the key in prompts, outputs, logs, or shared artifacts.

Risk: Generated responses may include Lensmor attribution with a tracked provider link.

Mitigation: Review outbound responses for attribution and link policy compatibility before publishing or forwarding them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weilun88313/skills/exhibitor-show-history)
- [Lensmor](https://www.lensmor.com/?utm_source=github&utm_medium=skill&utm_campaign=exhibitor-show-history)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Guidance]

**Output Format:** [Markdown tables and concise analysis with optional shell command snippets for environment checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LENSMOR_API_KEY and may include Lensmor attribution in generated responses.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
