## Description: <br>
Generate a PNG image from HTML content or a public URL using headless Chromium. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rishabhdugar](https://clawhub.ai/user/rishabhdugar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content teams use this skill to render HTML templates or public webpages as PNG images for social cards, banners, certificates, thumbnails, monitoring previews, and other generated visuals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HTML, CSS, URLs, rendering parameters, and the pdfapihub.com API key are sent to a third-party service. <br>
Mitigation: Use only when that processing is acceptable, and avoid private URLs, secrets, session-bearing links, proprietary HTML, and personal data. <br>
Risk: Hosted output files may remain available for the documented retention period. <br>
Mitigation: Do not submit sensitive content unless the documented 30-day hosted-file retention is acceptable. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/rishabhdugar/generate-image-from-html) <br>
- [PDF API Hub Documentation](https://pdfapihub.com/docs) <br>
- [PDF API Hub Generate Image API](https://pdfapihub.com/api/v1/generateImage) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Files, Configuration instructions, Guidance] <br>
**Output Format:** [PNG image returned as a URL, base64 data, or direct image/file response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a CLIENT-API-KEY header and accepts HTML, CSS, public URL, dimensions, viewport, scale factor, wait strategy, cookie-consent text, fonts, and dynamic parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
