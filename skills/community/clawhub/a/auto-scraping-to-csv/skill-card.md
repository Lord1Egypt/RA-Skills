## Description:

Scrape any webpage using text-based DOM manipulation and export structured data to CSV.

This skill is ready for commercial/non-commercial use.

## Publisher:

[science-prof-robot](https://clawhub.ai/user/science-prof-robot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect web pages, resolve scraping ambiguity through clarifying questions, and export selected page data as structured CSV files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local browser-control server with broad page interaction capabilities, including JavaScript execution.

Mitigation: Review and harden the bridge before use; bind it to localhost with authentication and remove executeJavascript unless it is explicitly needed.

Risk: The skill may encounter login prompts or sensitive pages during scraping workflows.

Mitigation: Do not provide passwords, tokens, or one-time codes through chat; log in manually in a browser only when authorized.

Risk: The bridge injects a Page-Agent script from a CDN into target pages.

Mitigation: Pin or vendor the Page-Agent script before deployment so the executed browser code is reviewed and version-controlled.

Risk: Scraping can collect data outside the user's authority or a site's permitted use.

Mitigation: Scrape only data the user is authorized to collect and review site terms, robots guidance, and applicable policies before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/science-prof-robot/skills/auto-scraping-to-csv)
- [Project homepage](https://github.com/Science-Prof-Robot/autoclick)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with CSV file outputs and inline command or code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser-control actions through a local Playwright bridge before writing CSV output.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
