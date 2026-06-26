## Description: <br>
Transforms articles, blog posts, reports, URLs, files, or pasted text into self-contained HTML infographics, with optional PNG export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Fengsh0923](https://clawhub.ai/user/Fengsh0923) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, content teams, and developers use this skill to turn long-form text into visual summaries, choosing an outline, layout, style, illustration posture, and output format before generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: PNG export may download and install Playwright and Chromium and may modify the local Python environment. <br>
Mitigation: Use the PNG export helper only in a sandbox or pre-provision the browser dependencies manually before running it. <br>
Risk: The skill may process article text, URLs, or local files through browser-based rendering for infographic output. <br>
Mitigation: Avoid providing sensitive local files or private text unless the execution and rendering environment is trusted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Fengsh0923/article-to-infographic) <br>
- [Style presets reference](references/style-presets.md) <br>
- [Illustration integration guide](references/illustrations-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with generated self-contained HTML and optional PNG export commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated HTML is intended to be self-contained; PNG export may invoke a local browser rendering helper.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
