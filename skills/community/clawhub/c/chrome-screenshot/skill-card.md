## Description:

Take full-page screenshots of HTML files as PNG images using Chrome + puppeteer-core, without downloading any browser; it can also generate PDF via Chrome's print-to-PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cclam5](https://clawhub.ai/user/cclam5)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert locally authored HTML reports, data visualizations, and shareable pages into PNG screenshots or PDF documents when browser or canvas tooling is unavailable or impractical.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill weakens browser isolation and handles inputs unsafely during local screenshot execution.

Mitigation: Use only HTML you authored and prefer a revised version that keeps Chrome sandboxing enabled and passes arguments to Node as data.

Risk: The local HTTP server can serve files from the HTML file's directory during capture.

Mitigation: Run it from a minimal directory containing only approved assets and no sensitive neighboring files.

Risk: Global dependency resolution can make the execution environment harder to review and reproduce.

Mitigation: Pin puppeteer-core locally and verify Chrome, Node.js, and Python dependencies before installation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/cclam5/skills/chrome-screenshot)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Files]

**Output Format:** [Markdown with bash commands and generated PNG or PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local Chrome, Node.js, Python 3, and puppeteer-core; output path and viewport width are configurable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
