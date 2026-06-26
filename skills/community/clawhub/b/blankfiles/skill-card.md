## Description: <br>
Use blankfiles.com as a binary test-file gateway: discover formats, filter by type/category, and return direct download URLs from the public API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seblavoie](https://clawhub.ai/user/seblavoie) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and test engineers use this skill to find real blank binary files for upload, parser, and file-handling tests. It helps agents discover supported formats and return concise direct download links with category and testing context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes ClawHub install, login, and publish commands that are unrelated to ordinary blankfiles.com lookup use. <br>
Mitigation: Use the skill only for blankfiles.com API lookups and direct download URLs unless deliberately maintaining and publishing the skill. <br>
Risk: A stale or unsupported format request could lead to incorrect file URLs. <br>
Mitigation: Verify availability through the documented public API before presenting a format or download URL. <br>


## Reference(s): <br>
- [Blank Files](https://blankfiles.com) <br>
- [Blank Files API Reference](references/endpoints.md) <br>
- [Blank Files API Status](https://blankfiles.com/api/v1/status) <br>
- [Blank Files Catalog API](https://blankfiles.com/api/v1/files) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with direct download URLs and concise format, category, and notes fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses should verify availability through the public API and avoid fabricated formats or URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
