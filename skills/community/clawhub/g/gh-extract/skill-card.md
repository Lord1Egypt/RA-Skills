## Description: <br>
Extract content from a GitHub URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoqiao](https://clawhub.ai/user/guoqiao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to fetch text from public GitHub repository, tree, or blob URLs, or to save fetched content to a temporary file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch arbitrary non-GitHub URLs and save remote content locally despite being presented as GitHub-only. <br>
Mitigation: Use only trusted public GitHub URLs; avoid private or internal URLs; review the skill before installation; prefer a version that rejects non-GitHub hosts and adds timeouts and size limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guoqiao/gh-extract) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files] <br>
**Output Format:** [Plain text content printed to stdout, or a temporary file path when saving content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv and wget; intended for public GitHub URLs.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
