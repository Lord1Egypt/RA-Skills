## Description:

Babata Browser is a lightweight browser automation skill for JS-rendered pages, form filling, screenshot evidence, and interactive web tasks, with CloakBrowser anti-detection and Playwright fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meta-evo-creator](https://clawhub.ai/user/meta-evo-creator)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to navigate dynamic websites, extract rendered content, fill forms, capture screenshots, scroll pages, and run scoped JavaScript when simpler fetch or search tools are insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Anti-detection browser automation can be misused or conflict with site policies.

Mitigation: Use only for authorized browsing workflows and do not use it to bypass site policies or access controls.

Risk: The skill can execute arbitrary JavaScript in visited pages.

Mitigation: Review JavaScript before execution and restrict runs to trusted tasks and controlled environments.

Risk: Browser sessions may expose credentials or sensitive screenshots.

Mitigation: Avoid real credentials on untrusted sites and check page content before capturing screenshots.

Risk: The Playwright fallback launches Chromium with reduced sandboxing and dependencies are not pinned exactly.

Mitigation: Run in a restricted container or VM and pin audited dependency versions before deployment.

## Reference(s):

- [Babata Browser ClawHub Skill Page](https://clawhub.ai/meta-evo-creator/skills/babata-browser)
- [Meta-Evo Publisher Profile](https://clawhub.ai/user/meta-evo-creator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON-compatible task results with optional inline Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce extracted page text, link lists, table rows, screenshot file paths, executed step summaries, or browser automation guidance.]

## Skill Version(s):

3.1.0 (source: frontmatter, pyproject.toml, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
