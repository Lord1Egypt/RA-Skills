## Description: <br>
Firecrawl Interact helps an agent control a live browser session on a scraped page to click, fill forms, navigate multi-step flows, and extract data with natural language prompts or code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eohmig](https://clawhub.ai/user/eohmig) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when simple scraping is not enough, such as for JavaScript-driven pages, pagination, login flows, form submission, or authenticated browser sessions. It is intended as an escalation step after search, scrape, map, or crawl workflows fail to reach the needed content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate with authenticated browser sessions and may click, type, submit forms, or otherwise affect real website state. <br>
Mitigation: Use it only on sites and accounts where browser automation is acceptable, and require confirmation before login, purchase, submission, deletion, account change, or other state-changing action. <br>
Risk: Persisted browser profiles can reuse cookies and local storage across sessions. <br>
Mitigation: Prefer read-only reconnects such as no-save-changes when inspecting authenticated pages, and stop sessions when interaction is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eohmig/firecrawl-interact) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce extracted page content or write output to a user-specified path through the Firecrawl CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
