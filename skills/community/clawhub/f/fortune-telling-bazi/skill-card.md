## Description:

Fortune Telling Bazi calculates local BaZi birth charts, manages multiple saved profiles, and produces single-person or joint analysis summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youhan2021](https://clawhub.ai/user/youhan2021)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to collect birth details with consent, calculate Chinese BaZi charts locally, manage saved profiles, and generate individual or multi-person interpretive summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores names, exact birth dates and times, gender, and derived BaZi profiles in plaintext local JSON files.

Mitigation: Use the skill only with consent, avoid committing the data directory to a repository, and remove or deactivate profiles when no longer needed.

Risk: The local lunar and BaZi calculation tables are documented for dates from 1899 through 2060.

Mitigation: Confirm entered birth dates are within the documented calculation range before relying on generated summaries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/youhan2021/skills/fortune-telling-bazi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or Markdown-like BaZi reports with optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local JSON profile storage; no remote API or third-party runtime dependency.]

## Skill Version(s):

1.0.2 (source: ClawHub server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
