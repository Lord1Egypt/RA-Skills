## Description: <br>
A comprehensive Bilibili toolkit that integrates hot trending monitoring, video downloading, video watching/playback, subtitle downloading, and video publishing capabilities into a single unified skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hollowings](https://clawhub.ai/user/hollowings) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and creators use this skill to monitor Bilibili trends, inspect video metrics, download videos or subtitles, retrieve playback information, and manage authenticated publishing workflows from a CLI or Python API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated operations require sensitive Bilibili session cookies that can affect the user's account. <br>
Mitigation: Install only if the publisher is trusted, use a test account for evaluation, and prefer environment variables or in-memory credentials over saved credential files. <br>
Risk: Upload, edit, schedule, and delete actions can change content on Bilibili. <br>
Mitigation: Require explicit user confirmation before account-changing publishing actions. <br>
Risk: Dependency versions are range-based, which can reduce reproducibility. <br>
Mitigation: Pin dependencies before deployment in controlled environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hollowings/bilibili-all-in-one-1-0-12) <br>
- [Publisher profile](https://clawhub.ai/user/hollowings) <br>
- [Project homepage](https://github.com/wscats/bilibili-all-in-one) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON-like command results, Python API results, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create downloaded video, audio, subtitle, or credential files when the user invokes those actions.] <br>

## Skill Version(s): <br>
1.0.12 (source: artifact frontmatter); release package version 1.0.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
