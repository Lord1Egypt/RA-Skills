## Description: <br>
Convert HTML DOM nodes to images (PNG/JPEG/SVG/Blob). Supports rendering options such as filter, backgroundColor, quality, and pixelRatio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to add browser-side export workflows that convert selected DOM elements into PNG, JPEG, SVG, or Blob outputs, including React components and downloadable images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exported images can include private or sensitive content visible inside the selected DOM node. <br>
Mitigation: Review the target element before export and use filters or redaction to exclude sensitive sub-elements. <br>
Risk: Installing the wrong npm package could add an unintended dependency. <br>
Mitigation: Verify that html-to-image is the intended npm package before installing it. <br>
Risk: Browser rendering can fail for CORS-tainted canvas content, very large DOM nodes, or unsupported browsers. <br>
Mitigation: Test exports with representative page content and document fallback behavior for unsupported cases. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openlark/dom-to-image) <br>
- [Publisher profile](https://clawhub.ai/user/openlark) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands] <br>
**Output Format:** [Markdown with inline bash, JavaScript, and TypeScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides installation and browser export options; does not generate image files directly.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
