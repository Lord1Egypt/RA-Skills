## Description: <br>
Extracts captions and written copy from Douyin, Xiaohongshu, and other social-media links through AnyToCopy's browser-based workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darker314159](https://clawhub.ai/user/darker314159) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, researchers, and other external users use this skill to extract titles, scripts, body text, and optional media links from supported social-media posts when they provide a public URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted links are opened and processed by anytocopy.com, which may expose URL contents or tracking query parameters to a third-party service. <br>
Mitigation: Use only public, non-sensitive links; avoid private, authenticated, or tokenized URLs; remove unnecessary tracking or secret query parameters before extraction. <br>
Risk: The browser workflow depends on AnyToCopy's public interface and may fail if the site changes. <br>
Mitigation: Confirm extracted results before relying on them and update the workflow if AnyToCopy changes its input or extraction controls. <br>


## Reference(s): <br>
- [AnyToCopy](https://www.anytocopy.com/) <br>
- [ClawHub skill page](https://clawhub.ai/darker314159/anytocopy-extractor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown response containing extracted title, body or script text, and optional media links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output depends on AnyToCopy availability, supported-platform coverage, and accessibility of the submitted URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
