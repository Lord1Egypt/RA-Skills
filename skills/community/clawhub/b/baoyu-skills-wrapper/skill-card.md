## Description: <br>
Baoyu Skills Wrapper provides guidance for using Baoyu's content generation, AI backend, publishing, and utility skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongjie-oss](https://clawhub.ai/user/dongjie-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this wrapper to discover and run Baoyu skills for visual content generation, social publishing, AI-backed generation, translation, markdown conversion, and content formatting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some workflows use authenticated browser sessions to publish to real social platforms or interact with logged-in web services. <br>
Mitigation: Use test or draft flows where possible, review content before posting, and run only against accounts you are authorized to use. <br>
Risk: URL and social-content capture workflows may read pages visible in the current browser session, including private or unauthorized pages. <br>
Mitigation: Restrict capture to intended and authorized pages, and avoid processing pages that contain confidential data. <br>
Risk: AI generation workflows require API keys and provider credentials. <br>
Mitigation: Keep credentials out of repositories, scope keys to the minimum required permissions, and rotate keys if they are exposed. <br>
Risk: The release is a wrapper around external Baoyu skill behavior, so execution may depend on scripts and browser automation outside this artifact. <br>
Mitigation: Review the underlying scripts before running them and install only from sources you trust. <br>


## Reference(s): <br>
- [Baoyu Skills Wrapper on ClawHub](https://clawhub.ai/dongjie-oss/baoyu-skills-wrapper) <br>
- [baoyu-skills support repository referenced by the wrapper](https://github.com/JimLiu/baoyu-skills) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference external APIs, browser sessions, local files, and authenticated social accounts depending on the selected underlying skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
