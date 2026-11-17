## Description:

Cn Ascii Art converts supplied text into ASCII art with selectable font styles and Chinese-language usage guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to generate ASCII-art text banners, signatures, and quick CLI-rendered text decorations from English or Chinese input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional pyfiglet dependency could be installed from an untrusted or unpinned environment.

Mitigation: Install pyfiglet from a trusted package source in a pinned virtual environment before using the CLI.

Risk: The included website links are promotional and are not required for the ASCII-art tool to run.

Mitigation: Treat those links as publisher information, and review them separately before following them in a managed environment.

Risk: Chinese characters may render incompletely because ASCII-art fonts are primarily designed for Latin text.

Mitigation: Preview generated output before publishing it, especially when using Chinese text or non-default fonts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-ascii-art)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text and Markdown with bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can run as a local Python CLI; uses pyfiglet when installed and falls back to simple uppercase output.]

## Skill Version(s):

1.2.6 (source: server release evidence, released 2026-06-07)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
