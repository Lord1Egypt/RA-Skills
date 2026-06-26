## Description: <br>
Check running Docker containers for newer image versions and generate a prioritized update report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newageinvestments25-byte](https://clawhub.ai/user/newageinvestments25-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to review running Docker containers, identify newer public Docker Hub image tags, and prioritize updates based on version changes and release notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads running Docker container names, image names, and tags and sends image metadata to Docker Hub and GitHub for update and changelog checks. <br>
Mitigation: Install and run it only in environments where sharing that metadata with those public services is acceptable. <br>
Risk: An optional GITHUB_TOKEN may be used for higher GitHub API limits. <br>
Mitigation: Use a least-privilege token for public API reads and avoid placing the token in shared logs or committed files. <br>
Risk: The skill reports update recommendations but does not apply updates. <br>
Mitigation: Review the generated report and validate changes through the normal deployment process before changing container images. <br>


## Reference(s): <br>
- [Container Update Advisor Setup Guide](references/setup-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with JSON intermediate data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The final report prioritizes container image updates and flags major, minor, unknown, or changelog-indicated breaking changes for review.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
