## Description: <br>
Extracts TTF/OTF fonts from a website using MSCHF Font Interceptor when a user provides a URL or asks what font a site is using. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[honeybee1130](https://clawhub.ai/user/honeybee1130) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, designers, and developers use this skill to identify and extract font files from public websites by submitting a URL to MSCHF Font Interceptor. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted target URLs are shared with the third-party Font Interceptor service. <br>
Mitigation: Use only public URLs that are appropriate to submit to fontinterceptor.mschfmag.com; avoid private dashboards, localhost or intranet pages, staging links, password-reset links, signed URLs, and URLs containing tokens. <br>
Risk: Extracted font files may have usage or redistribution restrictions. <br>
Mitigation: Confirm that you have the right to download, reuse, or redistribute any fonts found before relying on them. <br>


## Reference(s): <br>
- [MSCHF Font Interceptor](https://fontinterceptor.mschfmag.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown list of font names and TTF/OTF download links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include external download links returned by Font Interceptor.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
