## Description:

Autonomous B2B outbound engine that turns job board hiring signals into qualified pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[getlemnos32](https://clawhub.ai/user/getlemnos32)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and marketing operators use this skill to turn U.S. job-board hiring signals into verified business contacts and load net-new leads into a Hunter.io outbound campaign.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The skill can add scraped contacts to a live outbound email campaign.

Mitigation: Test with a non-sending campaign first and add a manual approval or dry-run step before allowing campaign writes.

Risk: Lead data may be stored locally or printed in places that are broadly accessible.

Mitigation: Run in a restricted workspace, use low-privilege credentials, and apply retention controls to local lead and tracking files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/getlemnos32/skills/b2b-outbound-sniper)
- [ClawHub publisher profile](https://clawhub.ai/user/getlemnos32)
- [Apify console](https://console.apify.com)
- [Hunter.io API key](https://app.hunter.io/api-key)
- [Hunter.io campaigns](https://app.hunter.io/campaigns)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, Python scripts, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local lead and tracking files when the bundled scripts are run.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
