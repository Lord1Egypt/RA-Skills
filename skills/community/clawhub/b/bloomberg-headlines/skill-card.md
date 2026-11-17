## Description:

Fetches the latest Bloomberg top headlines and helps an agent present the news in Chinese with links and localized publish times.

This skill is ready for commercial/non-commercial use.

## Publisher:

[8treenet](https://clawhub.ai/user/8treenet)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve recent Bloomberg market and financial headlines, then present each item with a title, source link, and localized publish time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs the mutable third-party Go executable bbgwire@latest.

Mitigation: Review the upstream bbgwire module before installation, prefer a pinned reviewed version, and run it with limited local file and credential exposure.

## Reference(s):

- [Bloomberg Headlines on ClawHub](https://clawhub.ai/8treenet/skills/bloomberg-headlines)
- [bbgwire Go module](https://github.com/8treenet/bbgwire)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summary of headline records with title, URL, and localized publish time; the underlying command returns JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Displays up to 50 recent Bloomberg headlines in Chinese.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
