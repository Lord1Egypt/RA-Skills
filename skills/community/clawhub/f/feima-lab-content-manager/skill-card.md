## Description: <br>
Feima Lab Content Manager helps agents turn text or Markdown into Feima Lab-style MDX articles, generate local previews, localize images, manage article metadata, and save, publish, unpublish, or query Feima Lab content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fangshan101-coder](https://clawhub.ai/user/fangshan101-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content authors and developers use this skill to draft Feima Lab blog or news articles, preview MDX locally, prepare metadata, and optionally publish or update remote articles through the Feima Lab backend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can save, publish, unpublish, and upload files to live Feima Lab content systems. <br>
Mitigation: Confirm the target article, backend, publish action, and file paths before running remote write operations; use dry-run or query commands first when available. <br>
Risk: Remote API actions require an internal API key, and mishandling that key could expose privileged access. <br>
Mitigation: Keep the API key in the user's shell environment only, do not store it in persistent skill memory or article metadata, and stop when the key is missing or rejected. <br>
Risk: Image localization and upload behavior can read local file paths referenced by article content. <br>
Mitigation: Avoid running the skill on untrusted Markdown with local file references, and restrict image or file inputs to the intended article directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fangshan101-coder/feima-lab-content-manager) <br>
- [Artifact README](README.md) <br>
- [API publish workflow](references/api-publish-workflow.md) <br>
- [API error handling](references/api-error-handling.md) <br>
- [Metadata schema](references/meta-schema.md) <br>
- [Component selection guide](references/component-selection.md) <br>
- [Feima style snapshot](references/feima-style-snapshot.json) <br>
- [Feima Lab repository](https://github.com/fangshan101-coder/feima-lab) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated MDX, JSON, HTML, and image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May also call Feima Lab API scripts that return JSON or table-formatted status output.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
