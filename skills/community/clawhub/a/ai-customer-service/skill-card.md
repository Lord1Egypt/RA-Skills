## Description:

Build AI-powered customer service knowledge bases by extracting FAQs from documents or websites, enabling automated replies and multi-format exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dagangtj](https://clawhub.ai/user/dagangtj)

### License/Terms of Use:

MIT

## Use Case:

Customer service teams and developers use this skill to turn FAQ documents or website FAQ pages into searchable knowledge bases, test answer matching, and export support content for automation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Website scraping accepts user-supplied URLs, which can expose users to unsafe or unintended network requests.

Mitigation: Only scrape trusted URLs, prevent untrusted users or prompts from choosing URLs, and use extra controls in cloud or corporate networks.

Risk: CSV exports created from scraped or third-party FAQ content may be unsafe when opened in spreadsheet software.

Mitigation: Treat CSV exports as untrusted, review or sanitize spreadsheet-sensitive cells, and avoid opening unreviewed exports in privileged environments.

Risk: The CLI reads local FAQ files and writes output paths selected by the user.

Mitigation: Run the tool in a controlled working directory and review input and output paths before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dagangtj/skills/ai-customer-service)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands plus JSON, CSV, or Markdown knowledge base exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local CLI workflow that reads FAQ inputs, writes selected output files, and can optionally use enhanced matching when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
