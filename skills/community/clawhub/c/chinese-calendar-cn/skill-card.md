## Description:

Chinese Calendar Cn is advertised as a local Chinese lunar calendar reference skill for solar terms, zodiac years, traditional festivals, auspicious-date guidance, Heavenly Stems and Earthly Branches, and lunar-calendar conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to provide Chinese-calendar reference guidance for cultural-date lookup and planning, but release evidence shows the bundled executable currently returns generic placeholder guidance rather than the advertised calendar commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The advertised Chinese calendar commands do not match the bundled executable behavior.

Mitigation: Run and review the artifact command output before deployment; do not rely on missing calendar commands until the implementation is corrected.

Risk: Calendar conversion, auspicious-date selection, or culturally date-sensitive guidance may be generic or incorrect.

Mitigation: Cross-check outputs with authoritative Chinese calendar references before using them for planning or automation.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/bytesagain-lab/skills/chinese-calendar-cn)
- [Publisher profile](https://clawhub.ai/user/bytesagain-lab)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text with Markdown-style headings from Bash command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external APIs or credential requirements are described; verify output against authoritative calendar references before relying on it.]

## Skill Version(s):

5.0.1 (source: release evidence; artifact frontmatter reports 5.0.0 and script reports 4.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
