## Description:

Helps agents search public Douyin videos and accounts, check trends, retrieve post details and comments, and return structured data for content analysis and batch downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

External content, marketing, and research teams use it to find public Douyin videos and accounts, track trends, inspect posts and comments, and organize results for content planning or internal analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Supplied keywords, links, or IDs are sent to a third-party API.

Mitigation: Avoid submitting sensitive queries or identifiers, and review the service's data handling before use.

Risk: Keyword-based account discovery may return results outside the user's expectations.

Mitigation: Confirm the search intent and review candidate accounts before using their data.

Risk: The security scan was partial, so some behavior remains unverified.

Mitigation: Review the skill and its outbound API use before installing.

## Reference(s):

- [Service and token setup](https://www.guaikei.com)
- [Command options](references/options.md)
- [Output contract](references/contract.md)
- [Error handling](references/errors.md)
- [Environment and usage FAQ](references/faq.md)
- [Demand mining guide](references/demand-mining.md)
- [Customer acquisition guide](references/customer-acquisition.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Analysis, Guidance]

**Output Format:** [Structured JSON with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are saved under logs/ for most queries; hot-list results are returned directly. Download links may expire.]

## Skill Version(s):

1.5.0 (source: SKILL.md frontmatter, package.json, changelog; released 2026-11-10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
