## Description:

Ctrip Compare helps agents collect, summarize, and compare Ctrip package tour products from Ctrip search or detail URLs and produce a Markdown recommendation report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangxiaoshuai98](https://clawhub.ai/user/zhangxiaoshuai98)

### License/Terms of Use:

MIT-0

## Use Case:

External travelers and travel planners use this skill to compare Ctrip group tour products by price, itinerary, attractions, photo services, lodging, meals, and reviews before choosing a package.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control an existing Chromium browser session over CDP, which may expose logged-in pages or account context.

Mitigation: Use a dedicated temporary browser profile or isolated browser instance instead of an everyday logged-in browser.

Risk: The workflow may terminate and restart local browser processes when CDP is unavailable, which can interrupt unsaved browser work.

Mitigation: Save or close browser work before any restart or process-kill step and confirm the selected browser before proceeding.

Risk: Unvalidated URLs could direct browser automation away from expected Ctrip vacation pages.

Mitigation: Verify every URL is a real vacations.ctrip.com page before extraction.

Risk: The skill writes raw and summarized travel data to a local output folder.

Mitigation: Choose a limited output folder and review generated files before sharing them.

## Reference(s):

- [Ctrip Compare ClawHub skill page](https://clawhub.ai/zhangxiaoshuai98/skills/ctrip-compare)
- [Ctrip group travel](https://vacations.ctrip.com/grouptravel)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, plain-text extracted data and summaries, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes project folders containing raw extraction files, compressed summaries, and a final comparison report.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
