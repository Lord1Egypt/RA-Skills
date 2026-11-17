## Description:

Draw tarot cards, cast I Ching hexagrams, and check daily fortunes for fun.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill for entertainment-oriented fortune-telling workflows such as daily fortunes, I Ching-style readings, zodiac checks, and related command-line fortune games.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes local storage, search, export, and history logging that are not clearly disclosed in the advertised fortune-telling use.

Mitigation: Review the scripts before installation and avoid entering sensitive personal information until the publisher clarifies storage behavior and narrows commands to the advertised use.

Risk: Stored local text and command history could expose user-provided content if the local data directory is shared, backed up, or inspected.

Mitigation: Use a dedicated non-sensitive data directory through FORTUNE_TELLER_DIR and remove local history or exported data after testing.

## Reference(s):

- [BytesAgain homepage](https://bytesagain.com)
- [ClawHub skill page](https://clawhub.ai/loutai0307-prog/skills/bytesagain-fortune-teller)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text and Markdown guidance with command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are printed to stdout. The skill may use FORTUNE_TELLER_DIR to choose a local data directory.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
