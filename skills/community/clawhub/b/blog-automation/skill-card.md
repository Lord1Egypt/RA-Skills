## Description: <br>
Automated WordPress blog publishing with scheduling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wespeakallday](https://clawhub.ai/user/wespeakallday) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content operators use this skill to convert generated article JSON into WordPress posts, then publish immediately or schedule publication through the WordPress REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish or schedule public WordPress posts using supplied credentials. <br>
Mitigation: Use a dedicated low-privilege WordPress application password, provide only an HTTPS WordPress URL you control, and review article content before publishing. <br>
Risk: Failed publishing attempts can save rendered article HTML locally. <br>
Mitigation: Run the skill in a workspace with appropriate file permissions and remove failed-output files that contain unpublished content when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wespeakallday/blog-automation) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, API Calls] <br>
**Output Format:** [JSON publication result with optional log file entry and fallback HTML file on failure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May publish or schedule WordPress posts using provided site credentials.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
