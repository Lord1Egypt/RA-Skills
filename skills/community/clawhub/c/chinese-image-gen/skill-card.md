## Description: <br>
Generate Chinese vertical images (750x1334px) for microblog and social-media use with Playwright, Chromium, and Google Fonts Noto Sans SC. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wdmcygah](https://clawhub.ai/user/wdmcygah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and social-media operators use this skill to produce Chinese-language vertical image cards, infographics, comparison cards, and data summaries where readable CJK text and pixel-level layout control matter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rendering may make network requests to Google Fonts for Noto Sans SC. <br>
Mitigation: For confidential content, air-gapped systems, or restricted environments, replace the CDN font with an approved local font before rendering. <br>
Risk: The skill requires installing Playwright and Chromium and launches Chromium for local rendering. <br>
Mitigation: Install dependencies only in approved environments and run the renderer in an isolated workspace when processing untrusted HTML. <br>
Risk: The helper launches Chromium with no-sandbox arguments. <br>
Mitigation: Avoid rendering untrusted HTML directly; isolate the process or adapt the launch configuration to the host security policy. <br>


## Reference(s): <br>
- [Chinese Image Gen on ClawHub](https://clawhub.ai/wdmcygah/chinese-image-gen) <br>
- [Noto Sans SC Google Fonts CSS](https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;700&display=swap) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with inline HTML, CSS, Python, and shell code blocks; rendered PNG image files when the helper script is run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default image viewport is 750x1334px; width and height can be overridden when running the helper script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
