## Description: <br>
Automated code review for GitHub pull requests using Claude LLM, PR analysis, security scanning, and style checking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HiroFumiko](https://clawhub.ai/user/HiroFumiko) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to inspect GitHub pull requests, review changed files, request Claude-based analysis, and run configurable security and style checks before merging code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private pull request diffs may be sent to Anthropic during Claude-based review. <br>
Mitigation: Use the skill only when sharing target PR content with Anthropic is allowed; use --skip-llm or disable LLM review for sensitive or private code. <br>
Risk: GitHub and Anthropic credentials are required for full functionality. <br>
Mitigation: Keep .env files out of source control and use a fine-grained, read-only GitHub token scoped to only the repositories needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HiroFumiko/code-review-automation) <br>
- [Anthropic Console](https://console.anthropic.com/) <br>
- [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) <br>
- [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text, Rich tables and panels, Markdown review text, and .reviewrc configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GitHub access for repository and pull request data; Claude analysis requires an Anthropic API key unless LLM review is skipped.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
