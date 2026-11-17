## Description:

Playwright-based web scraping OpenClaw Skill with anti-bot protection. Successfully tested on complex sites like Discuss.com.hk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gu-yunyu](https://clawhub.ai/user/gu-yunyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to fetch content from dynamic or anti-bot-protected websites with Playwright, optionally saving screenshots or HTML for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can browse arbitrary untrusted pages with stealth-oriented browser settings and broad URL access.

Mitigation: Run it in an isolated environment with restricted network access and use only URLs you are authorized to access.

Risk: Saved screenshots or HTML can retain sensitive page content.

Mitigation: Avoid private or sensitive URLs, choose controlled output paths, and review or delete generated files after use.

Risk: The documentation points users to optional third-party skill installation instructions outside this package.

Mitigation: Review any separately installed skill and its dependencies before running those optional instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gu-yunyu/skills/coco-playwright-stealth-1-0-0)
- [Playwright official documentation](https://playwright.dev/)
- [puppeteer-extra-plugin-stealth reference](https://github.com/berstend/puppeteer-extra/tree/master/packages/puppeteer-extra-plugin-stealth)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands; scripts emit JSON and may write screenshot or HTML files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses URL input and optional environment variables such as HEADLESS, WAIT_TIME, SCREENSHOT_PATH, SAVE_HTML, and USER_AGENT.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json; artifact frontmatter, package.json, and changelog state 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
