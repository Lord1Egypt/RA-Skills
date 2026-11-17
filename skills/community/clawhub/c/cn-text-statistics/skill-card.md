## Description:

Provides local Chinese text statistics, including line counts, character counts, English word counts, and optional frequency output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators working with Chinese-language text use this skill to get quick local statistics from inline text or a specified UTF-8 text file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read a local text file explicitly passed with --file and print summary statistics plus optional frequency output.

Mitigation: Run it only on files the user intends to analyze, and avoid frequency output for sensitive text when repeated terms could reveal private content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-text-statistics)
- [Artifact SKILL.md](artifact/SKILL.md)
- [Text statistics script](artifact/scripts/text_stats.py)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text statistics with optional word-frequency lines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the Python standard library and reads only inline text or the local file path explicitly passed by the user.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
