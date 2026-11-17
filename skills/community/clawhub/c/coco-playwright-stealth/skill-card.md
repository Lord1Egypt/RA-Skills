## Description:

Playwright-based web scraping OpenClaw Skill with anti-bot protection. Successfully tested on complex sites like Discuss.com.hk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hongjiahao371-pixel](https://clawhub.ai/user/hongjiahao371-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to choose and run Playwright scraping workflows for dynamic websites, including sites that apply common anti-bot checks. It provides simple and stealth-oriented command patterns, environment-variable configuration, and troubleshooting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The stealth scraper weakens Chromium sandboxing while opening arbitrary websites, which can increase host exposure.

Mitigation: Run the skill only for trusted use cases in a restricted environment; enable Chromium sandboxing or isolate the whole skill in a container or virtual machine when handling untrusted URLs.

Risk: Saved screenshots or HTML files may contain sensitive page content.

Mitigation: Review saved artifacts before sharing or retaining them, and store or delete them according to the user's data-handling requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hongjiahao371-pixel/skills/coco-playwright-stealth)
- [Playwright documentation](https://playwright.dev/)
- [puppeteer-extra-plugin-stealth reference](https://github.com/berstend/puppeteer-extra/tree/master/packages/puppeteer-extra-plugin-stealth)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, JavaScript script references, and JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The referenced Playwright scripts can emit scraped page metadata and content as JSON, and the stealth script can optionally save screenshots and HTML files.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
