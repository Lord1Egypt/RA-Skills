## Description:

Generates Chinese-language vertical social-media images at 750x1334 pixels by rendering HTML and CSS with Playwright, Chromium, and Noto Sans SC from Google Fonts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wdmcygah](https://clawhub.ai/user/wdmcygah)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content creators, and agents use this skill to create precise Chinese-language data cards, comparison graphics, and vertical social-media images where readable text matters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rendering untrusted HTML in Chromium with the browser sandbox disabled can expose the local environment to unsafe browser behavior.

Mitigation: Render only trusted or agent-generated HTML, pin Playwright where possible, and run the renderer in a disposable or restricted environment when inputs may be untrusted.

Risk: The default font setup makes outbound requests to Google Fonts.

Mitigation: Replace the CDN font with a reviewed local font asset when outbound network access or third-party font loading is not acceptable.

## Reference(s):

- [Google Fonts: Noto Sans SC](https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;700&display=swap)
- [ClawHub skill page](https://clawhub.ai/wdmcygah/skills/chinese-image-gen)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML, CSS, and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rendered images are typically PNG files sized 750x1334 pixels.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
