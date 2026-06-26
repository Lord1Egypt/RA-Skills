## Description: <br>
Generates structured NowCoder interview-experience reports by searching NowCoder posts for configured keywords, time windows, and tags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[champagne315](https://clawhub.ai/user/champagne315) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to gather recent NowCoder interview-experience posts and turn them into concise preparation reports. It supports keyword, time-window, tag, language, and report-style configuration for interview preparation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill disables HTTPS certificate verification during normal NowCoder searches. <br>
Mitigation: Use an isolated Python environment and remove or fix the TLS verification bypass before relying on results for private searches or important decisions. <br>
Risk: The skill saves preferences, prompts, and report data locally under the user's home directory. <br>
Mitigation: Review the files it creates and avoid storing sensitive search preferences or report content in shared environments. <br>
Risk: NowCoder search requests may expose configured search keywords and timing to an external service. <br>
Mitigation: Avoid private or sensitive search terms unless that external disclosure is acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/champagne315/follow-nowcoder) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/champagne315) <br>
- [NowCoder feed detail pages](https://www.nowcoder.com/feed/main/detail) <br>
- [NowCoder discussion pages](https://www.nowcoder.com/discuss) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with JSON metadata and CLI command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save report data, user configuration, and prompt customizations to local files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
