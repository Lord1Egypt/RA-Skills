## Description:

Converts PPTX or PDF pitch decks into responsive, self-contained HTML presentations for browser-based sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wulaosiji](https://clawhub.ai/user/wulaosiji)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, founders, and operators use this skill to convert existing pitch decks or PDFs into a single offline-ready HTML presentation with navigation, fullscreen, mobile, and print support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The custom color option can inject active script into generated HTML.

Mitigation: Use trusted color values, prefer the default color until validation is added, and review generated HTML before sharing or hosting it.

Risk: Generated presentations contain the source deck's text and images.

Mitigation: Treat generated HTML as confidential when the input deck is confidential, and avoid hosting it on authenticated or sensitive origins.

Risk: Runtime dependencies are installed from Python package indexes.

Mitigation: Install dependencies in a virtual environment and prefer pinned, reviewed versions.

## Reference(s):

- [Deck Web Converter ClawHub Listing](https://clawhub.ai/wulaosiji/skills/deck-web-converter)
- [UniqueClub](https://uniqueclub.ai)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell commands that produce a self-contained HTML file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated HTML may contain the original deck's confidential text and images.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
