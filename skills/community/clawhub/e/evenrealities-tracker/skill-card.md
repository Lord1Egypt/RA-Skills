## Description:

Tracks Evenrealities orders by checking the public tracking page, recording status history, and notifying only when an order status changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thibautrey](https://clawhub.ai/user/thibautrey)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to monitor Evenrealities smart ring orders, schedule daily checks, and keep local status history for change-only notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores email addresses, order IDs, and status history in local memory files.

Mitigation: Use restrictive file permissions, keep memory files out of version control, and store only orders the user intends to track.

Risk: The skill submits an email address and order ID to track.evenrealities.com during each status check.

Mitigation: Use the skill only when the user is comfortable sending those order lookup details to Evenrealities' tracking site.

Risk: Console output can include personal order details.

Mitigation: Avoid shared logs or mask output when running the tracker in automated or shared environments.

Risk: Browser automation depends on Playwright and downloaded browser binaries.

Mitigation: Install Playwright in a controlled environment and pin the dependency before relying on the skill in automation.

## Reference(s):

- [Evenrealities Tracking](https://track.evenrealities.com)
- [Playwright Python Documentation](https://playwright.dev/python/docs/intro)
- [Example Orders Configuration](references/evenrealities-orders-example.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When run, the tracker produces status text and local JSON files for order configuration and status history.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
