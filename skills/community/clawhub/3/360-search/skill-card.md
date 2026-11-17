## Description:

Searches the 360 Search engine for web, news, and image results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[feiyang2007](https://clawhub.ai/user/feiyang2007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to issue web, news, and image searches against 360 Search and return result metadata for Chinese-language search workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to 360 Search/so.com.

Mitigation: Use only when sending the query terms to that external search service is acceptable.

Risk: The scanner notes Chinese-only output and packaging rough edges, including missing or inconsistent examples.

Mitigation: Review and test the packaged scripts in the target environment before relying on the results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/feiyang2007/skills/360-search)
- [360 Search](https://www.so.com)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration]

**Output Format:** [JSON search-result records and Markdown usage notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search scripts accept a JSON argument with query and optional max_results fields.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
