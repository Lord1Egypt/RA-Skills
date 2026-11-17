## Description:

一体化健身追踪系统。自动同步饮食记录和身体状态到 intervals.icu。支持配置引导和错误处理。

This skill is ready for commercial/non-commercial use.

## Publisher:

[leozvc](https://clawhub.ai/user/leozvc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to record meals, estimate nutrition, generate fitness status reports, and synchronize wellness data with Intervals.icu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Intervals.icu API credentials are stored in a local plaintext configuration file.

Mitigation: Use the skill only on trusted machines, keep the config file private, restrict file permissions, and rotate the API key if it may have been exposed.

Risk: Credential files may be committed or shared if the local installation does not actually ignore the config directory.

Mitigation: Add a real .gitignore or move credentials outside the project before committing, archiving, or sharing the skill directory.

Risk: Meal parsing can write wellness data to Intervals.icu.

Mitigation: Use dry-run mode until parsed nutrition and target dates are confirmed.

## Reference(s):

- [Fitness Principles](references/fitness_principles.md)
- [Intervals API Docs](references/intervals_api_docs.md)
- [Intervals.icu API Integration Cookbook](https://forum.intervals.icu/t/intervals-icu-api-integration-cookbook/80090)
- [API access to Intervals.icu](https://forum.intervals.icu/t/api-access-to-intervals-icu/609)
- [Intervals.icu official API documentation](https://intervals.icu/api-docs.html)
- [OpenFoodFacts API](https://wiki.openfoodfacts.org/Main_Page)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, command-line text, JSON configuration, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write wellness data to Intervals.icu unless dry-run mode is used.]

## Skill Version(s):

3.6.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
