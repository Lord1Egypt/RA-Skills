## Description:

Income Tracker records multi-source income, summarizes earnings, analyzes trends, and produces simple charts for freelancers, creators, and side-business users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as freelancers, creators, and small teams use this skill to record income from multiple platforms or projects, review period summaries, inspect source mix, and export records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Income records are stored locally in plaintext JSON and may contain sensitive financial details.

Mitigation: Use a private DATA_PATH on a machine or account you control, avoid shared or synced folders unless reviewed, and protect backups appropriately.

Risk: The bundled lockfile references non-HTTPS npm mirror URLs.

Mitigation: Regenerate the lockfile with an HTTPS npm registry before production deployment.

Risk: Cloud sync and backup behavior is described as optional future functionality and is not covered by the clean security verdict.

Mitigation: Review any cloud-sync or automated backup integration separately before enabling it for income data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/onlyloveher/skills/cn-income-tracker)
- [Artifact homepage](https://clawhub.com/skills/income-tracker)
- [Publisher profile](https://clawhub.ai/user/onlyloveher)

## Skill Output:

**Output Type(s):** [Text, JSON, CSV, Configuration]

**Output Format:** [JSON responses with text summaries, ASCII charts, and optional CSV or JSON export data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores and reads income records from a local JSON data path configured by DATA_PATH.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact files declare 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
