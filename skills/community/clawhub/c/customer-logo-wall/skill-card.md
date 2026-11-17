## Description:

Processes customer spreadsheets, researches company Chinese names, downloads and verifies logos, normalizes image formats, and generates a customer logo wall PowerPoint deck.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heavenchenggong](https://clawhub.ai/user/heavenchenggong)

### License/Terms of Use:

MIT-0

## Use Case:

Business, sales, marketing, and operations users can use this skill to turn customer company lists into presentation-ready logo wall decks with Chinese company names, tier grouping, logo retrieval, logo checking, and PPT generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic web downloads and under-scoped file writes can affect local files outside the intended result set.

Mitigation: Run the skill in a dedicated working directory, use copied input spreadsheets, choose isolated output folders, and avoid elevated privileges.

Risk: Customer names and optional official URLs may be sent to public search engines and websites during logo lookup.

Mitigation: Review customer lists for sensitivity before execution and remove confidential entries when public search disclosure is not acceptable.

Risk: Untrusted companies JSON can influence downloaded content and output paths.

Mitigation: Use trusted or reviewed companies JSON and keep logo output in a dedicated directory before generating the deck.

## Reference(s):

- [Customer Logo Wall Skill on ClawHub](https://clawhub.ai/heavenchenggong/skills/customer-logo-wall)
- [Logo Format Issues](references/logo-format-issues.md)
- [Logo Verification](references/logo-verification.md)
- [PPT Design](references/ppt-design.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated files such as JSON reports, normalized logo images, updated spreadsheets, and PowerPoint decks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write or overwrite local spreadsheet, logo, JSON report, and PPTX files in user-selected paths.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
