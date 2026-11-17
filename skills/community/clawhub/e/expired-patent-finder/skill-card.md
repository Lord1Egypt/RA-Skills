## Description:

检索某技术方向中已失效的中国发明专利，按失效原因整理清单并标出需要进一步核实的事项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

External users and small businesses can use this skill to find and organize lapsed Chinese invention patents related to a technology area, then review candidate technical solutions. It is a research aid, not a legal-status or freedom-to-operate opinion.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Credential handling may expose API keys or send them to unexpected destinations.

Mitigation: Use trial access and public technical terms for evaluation, avoid pasting production keys into chat, and use a corrected release with restricted credential destinations and safe redirect handling.

Risk: Malformed patent numbers may escape the file cache.

Mitigation: Use a corrected release that validates cache filenames before relying on cached files.

Risk: API calls can incur charges.

Mitigation: Check trial and pricing status before searching and monitor usage.

## Reference(s):

- [Search workflow](references/search-workflow.md)
- [Patent query syntax](references/query-syntax.md)
- [Known search pitfalls](references/pitfalls.md)
- [PatentMax API platform](https://api.ip930.com/features/api-platform)
- [ClawHub skill release](https://clawhub.ai/ip930/skills/expired-patent-finder)

## Skill Output:

**Output Type(s):** [CSV, Text, Analysis, Guidance]

**Output Format:** [UTF-8 CSV file with a concise text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lists candidate patents with lapse reasons and items to verify; legal status should be checked against official registers, and the results are not an FTO determination.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
