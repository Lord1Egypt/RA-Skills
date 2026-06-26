## Description: <br>
Generate QR codes for any URL or text instantly using AceToolz. Returns a hosted image URL ready to share in chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[acetoolz](https://clawhub.ai/user/acetoolz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to generate QR codes for URLs or text and return a hosted QR image link that can be shared in chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: QR payload content is sent to AceToolz and returned as a hosted image URL. <br>
Mitigation: Avoid encoding secrets, private internal links, access tokens, Wi-Fi passwords, or sensitive personal data unless sharing that content with AceToolz is acceptable. <br>
Risk: Very long content can reduce QR code reliability and may exceed the skill's stated 2,000 character limit. <br>
Mitigation: Ask the user to shorten the content or use a URL shortener before generating the QR code. <br>


## Reference(s): <br>
- [AceToolz QR Generator](https://www.acetoolz.com/generate/tools/qr-generator) <br>
- [AceToolz QR Generator API](https://www.acetoolz.com/api/openclaw/qr-generator) <br>
- [ClawHub Skill Page](https://clawhub.ai/acetoolz/acetoolz-qr) <br>
- [AceToolz Publisher Profile](https://clawhub.ai/user/acetoolz) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown response with a hosted QR image URL and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns qr_image_url as the primary shareable output; qr_data_url may be used only on platforms that support base64 data URLs.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
