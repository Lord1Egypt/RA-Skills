## Description:

China Express helps agents query Chinese package status through browser automation on Kuaidi100 and report only live page results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to check Chinese package tracking numbers, interpret delivery-message text, identify likely carriers, and summarize one or more shipments from the official Kuaidi100 web page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tracking numbers or pasted delivery-message text may be sent to Kuaidi100 during browser-based lookup.

Mitigation: Avoid pasting unnecessary personal details and use the skill only when sharing shipment information with Kuaidi100 is acceptable.

Risk: The tracking page may require captcha, login, phone verification, or other manual checks.

Mitigation: Treat those cases as blocked and report the verification requirement instead of bypassing it or using another source.

Risk: Package status can be wrong if stale page content, mismatched tracking numbers, or unsupported browser automation are treated as successful results.

Mitigation: Return a status only after the live Kuaidi100 page clearly shows the current query's tracking number and logistics events.

## Reference(s):

- [Kuaidi100 package tracking](https://www.kuaidi100.com/)
- [ClawHub skill homepage](https://clawhub.ai/ToBeWin/china-express)
- [ClawHub release page](https://clawhub.ai/tobewin/skills/china-express)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown status summaries or concise blocker messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs current status, carrier, tracking number, latest time, and one to three recent tracking events when the live page supports them.]

## Skill Version(s):

3.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
