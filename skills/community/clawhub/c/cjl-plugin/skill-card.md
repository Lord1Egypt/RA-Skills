## Description:

CJL Skills Collection is a personal Claude Code plugin with 17 production skills for paper analysis, content cards, presentation design, relationship analysis, writing, travel research, vocabulary learning, and related workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcjl](https://clawhub.ai/user/0xcjl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill collection in Claude Code to run focused workflows for research, writing, visual content, presentations, travel preparation, investment analysis, vocabulary learning, and media download tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill collection includes broad file-writing workflows that can create notes and outputs under ~/Documents/notes and ~/Downloads.

Mitigation: Review the requested workflow and confirm output paths before allowing file writes.

Risk: The X/Twitter downloader includes a browser-cookie fallback for yt-dlp.

Mitigation: Use the Chrome-cookie fallback only when the user explicitly intends to allow yt-dlp to read browser session cookies.

Risk: Some workflows rely on mutable dependency installation or remote scripts, including Playwright setup and CDN-hosted Chart.js.

Mitigation: Pin dependencies where possible and check remote scripts before sharing or deploying generated cards and slides.

Risk: Generated cards and slides may contain hardcoded attribution or output that needs human review.

Mitigation: Inspect generated visual outputs for attribution, accuracy, and suitability before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xcjl/skills/cjl-plugin)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown and org-mode text with inline shell commands, generated HTML/PPTX guidance, PNG visual files, and downloaded media files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Several workflows write files under ~/Documents/notes or ~/Downloads.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact SKILL.md frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
