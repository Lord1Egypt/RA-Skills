## Description: <br>
Extract valid downloadable URLs from Array[String] structures, clean and standardize them, then output directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users use this skill to extract direct download links from JSON arrays or code snippets containing string arrays. It returns only valid HTTP or HTTPS URLs, one per line, for direct reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Extracted URLs may point to untrusted or unsafe downloads. <br>
Mitigation: Review links before fetching or downloading them, and apply normal allowlist, scanning, and trust checks for downloaded content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openlark/array-url-extractor) <br>


## Skill Output: <br>
**Output Type(s):** [text] <br>
**Output Format:** [Plain text, one URL per line] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Filters for valid http:// and https:// URLs and avoids extra explanatory text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
