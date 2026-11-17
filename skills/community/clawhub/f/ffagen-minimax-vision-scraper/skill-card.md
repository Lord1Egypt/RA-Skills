## Description:

Captures webpages with Playwright and sends screenshots to the MiniMax vision API so an agent can extract visible page content without parsing HTML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ffagen](https://clawhub.ai/user/ffagen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to capture rendered webpages and ask MiniMax vision to summarize or extract visible page details such as news, financial data, or product information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webpage screenshots and prompts are sent to MiniMax for visual analysis.

Mitigation: Do not use the skill on logged-in pages, internal dashboards, localhost or private-network services, or pages containing secrets.

Risk: The artifact includes an embedded MiniMax API key fallback.

Mitigation: Remove or rotate the embedded key and require MINIMAX_API_KEY to be supplied through the environment before routine use.

Risk: The browser launch weakens sandboxing and automation protections for scraping.

Mitigation: Run the browser with normal sandboxing where possible and review the execution environment before installation.

Risk: User-controlled URLs and screenshot output paths can expand what the skill accesses or writes.

Mitigation: Apply stricter URL allowlists, private-network blocking, and output-path controls before routine use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ffagen/skills/ffagen-minimax-vision-scraper)
- [Referenced Playwright scraper skill](https://clawhub.ai/skills/scraper)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Console text and Markdown-style guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the captured webpage, the prompt, and the MiniMax vision API response.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
