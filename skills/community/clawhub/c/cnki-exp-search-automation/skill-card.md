## Description:

Automates CNKI advanced literature search in a browser to collect result lists, article metadata, and abstracts, with headful browser use recommended when anti-bot checks appear.

This skill is ready for commercial/non-commercial use.

## Publisher:

[killgfat](https://clawhub.ai/user/killgfat)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, analysts, and developers use this skill to guide browser-based CNKI searches, collect literature metadata, and extract article abstracts for literature reviews or dataset preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automates CNKI access and may interact with rate limits, anti-bot checks, or site terms.

Mitigation: Use the skill only with authorized CNKI access, keep request rates reasonable, and pause for manual verification when CAPTCHA or slider checks appear.

Risk: Using a logged-in browser profile may expose account session context during browsing.

Mitigation: Use only the intended browser profile, avoid sharing session-derived exports without review, and close or isolate unrelated authenticated sessions when practical.

Risk: Exported literature metadata or abstracts may include sensitive research context or licensed content.

Mitigation: Review JSON or CSV exports before sharing and apply the user's institutional CNKI licensing and data-handling rules.

Risk: CNKI page structure changes can cause selectors or extraction snippets to miss fields or return incomplete results.

Mitigation: Validate a sample of extracted records against the browser page before relying on bulk results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/killgfat/skills/cnki-exp-search-automation)
- [CNKI advanced search](https://kns.cnki.net/kns8s/AdvSearch?type=expert)
- [CNKI professional search fields](references/cnki-fields.md)
- [CNKI professional search query examples](references/query-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with browser-action examples, JavaScript extraction snippets, and JSON or CSV data-shape examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces agent guidance for browser automation and extracted bibliographic data; it does not embed a standalone executable.]

## Skill Version(s):

0.2.0 (source: server release metadata; artifact frontmatter reports 0.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
