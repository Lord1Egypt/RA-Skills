## Description:

企业别名智能生成器为企业名单批量生成精准别名，支持上市公司股票简称、政府机构全称、通用词和地名过滤以及别名去重。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hyqdq888](https://clawhub.ai/user/hyqdq888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data operations teams use this skill to process Excel company lists and generate standardized company aliases for entity matching, fuzzy search, and data cleaning workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company names may be sent to Baidu during alias lookup, including when users expected network lookup to be disabled.

Mitigation: Disable or remove network lookup before processing confidential company lists, and run the skill in an environment without outbound network access when privacy is required.

Risk: The script includes a hard-coded private fallback input path.

Mitigation: Remove the fallback path and require explicit input and output file paths for every run.

Risk: Alias generation depends on an external generate_alias module that is not bundled or pinned in the artifact.

Mitigation: Bundle or pin the dependency to reviewed code before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hyqdq888/skills/company-alias-generator)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with bash examples and generated Excel .xlsx files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 with openpyxl and requests; network lookup behavior should be reviewed before use with confidential company lists.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
