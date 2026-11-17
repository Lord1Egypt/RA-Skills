## Description:

Automates Douyin keyword searches with Playwright and returns scraped search result data in JSON, CSV, or text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urhd528](https://clawhub.ai/user/urhd528)

### License/Terms of Use:

MIT License

## Use Case:

Developers and analysts use this skill to run keyword searches on Douyin and collect result metadata for review or downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency setup can modify the local Python environment and download Playwright or browser binaries.

Mitigation: Install and run the skill in an isolated Python environment, and review dependencies before setup.

Risk: Browser scraping may use a logged-in Douyin session, and failed runs can save debug_screenshot.png with page contents.

Mitigation: Use a dedicated Douyin test account or browser session, and delete debug_screenshot.png after failed scrapes.

Risk: Automated scraping may conflict with Douyin terms or create unwanted traffic.

Mitigation: Follow Douyin terms and robots guidance, keep limits and frequency low, and stop if access controls or rate limits appear.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/urhd528/skills/douyin-keyword-search)
- [Skill Documentation](artifact/skill.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; runtime script output can be JSON, CSV, or plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write results to a user-specified output file and may create debug_screenshot.png after failed scraping.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
