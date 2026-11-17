## Description:

Translates Chinese search needs into English, Japanese, and Korean to find US, EP, JP, KR, and PCT patents, then summarizes results in Chinese and exports a spreadsheet-friendly patent list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

External users describe an invention or technology in Chinese and use the skill to search foreign patent publications across the US, Europe, Japan, Korea, and PCT collections. It prepares a CSV patent list with original titles and Chinese summaries to support preliminary research, not formal patentability conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid API key handling and request security need review.

Mitigation: Use HTTPS and same-origin request handling, provision credentials securely, and avoid the shared plaintext key file.

Risk: Technical details submitted for patent searches may not be approved for sharing with PatentMax.

Mitigation: Submit only technical details approved for PatentMax.

Risk: Paid searches may incur unexpected spend or omit requested countries.

Mitigation: Set a spending limit and verify that searches retain the requested countries.

## Reference(s):

- [PatentMax API reference](references/api-reference.md)
- [Patent search workflow](references/search-workflow.md)
- [Patent query syntax](references/query-syntax.md)
- [PatentMax API](https://api.ip930.com)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)

## Skill Output:

**Output Type(s):** [Analysis, Files, Guidance]

**Output Format:** [CSV patent list and Chinese-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Spreadsheet-friendly CSV includes original patent titles and Chinese descriptions; translations are for reference.]

## Skill Version(s):

1.0.2 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
