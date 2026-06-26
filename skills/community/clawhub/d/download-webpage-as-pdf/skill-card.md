## Description: <br>
Saves a live webpage as a high-fidelity PDF that preserves browser layout and lazy-loaded images using the agent-browser CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tenequm](https://clawhub.ai/user/tenequm) <br>

### License/Terms of Use: <br>
Apache License 2.0 <br>


## Use Case: <br>
Developers, agents, and operators use this skill to save a user-selected webpage as a local PDF when browser-layout fidelity and image completeness matter. It is intended for full-page visual capture rather than reader-mode article extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may capture private or logged-in page content in the generated PDF. <br>
Mitigation: Use an isolated browser session for private or authenticated sites and review the PDF before sharing or storing it. <br>
Risk: The PDF may reflect a cleaned-up or transformed page state rather than an untouched legal or compliance record. <br>
Mitigation: Do not rely on the output as the sole compliance archive; preserve the source URL, capture time, and any required original records separately. <br>
Risk: Lazy-loaded images or manually trimmed footer pages can lead to an incomplete capture. <br>
Mitigation: Check the returned broken-image count, inspect page count and file size with pdfinfo, and visually review the result before treating it as complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tenequm/download-webpage-as-pdf) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a browser-automation recipe and verification checks for a local PDF output.] <br>

## Skill Version(s): <br>
0.1.3 (source: SKILL.md frontmatter and CHANGELOG, released 2026-05-08) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
