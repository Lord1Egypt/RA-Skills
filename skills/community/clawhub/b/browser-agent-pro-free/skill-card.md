## Description: <br>
Browser Agent Pro Free lets an agent use natural-language instructions to navigate web pages, take screenshots, fill forms, and perform basic data extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to automate Chromium-based browsing workflows, including page navigation, screenshots, form entry, and basic current-page data capture. It is suited for repeatable web research, form assistance, and page archiving where saved artifacts and logs are expected. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved screenshots, scraped data, and operation logs may contain sensitive webpage or form data. <br>
Mitigation: Avoid sensitive logged-in sessions or personal-data forms unless retaining those records is intentional, and periodically delete or configure retention for stored browser artifacts. <br>
Risk: Browser automation can perform sensitive actions such as login, payment, deletion, or form submission if directed by a user. <br>
Mitigation: Require explicit confirmation before sensitive operations and review the page state before any submission or irreversible action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/browser-agent-pro-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown and plain text with file paths, shell commands, screenshots, CSV/JSON/Markdown data files, and JSONL logs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Browser artifacts are stored under ~/workspace/browser by date; the free version limits scraping to current-page data and up to 100 records per run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
