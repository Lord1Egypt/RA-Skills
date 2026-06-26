## Description: <br>
Chinese Sensitive Words checks Chinese copy for sensitive or prohibited terms across major Chinese social platforms, returns risk levels and categories, and suggests safer replacements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CCCpan](https://clawhub.ai/user/CCCpan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, content reviewers, and developers use this skill to screen marketing copy, product descriptions, live-stream scripts, social media posts, and ads before publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Checked text is sent to the configured online API service. <br>
Mitigation: Avoid submitting confidential, regulated, or unpublished business text unless the provider is trusted or SENSITIVE_WORDS_API_BASE points to a trusted private service. <br>
Risk: The token enables expanded service usage if exposed. <br>
Mitigation: Store SENSITIVE_WORDS_TOKEN only in trusted local configuration or environment variables and do not include it in shared prompts, logs, or repositories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CCCpan/chinese-sensitive-words) <br>
- [CCCpan publisher profile](https://clawhub.ai/user/CCCpan) <br>
- [Token acquisition issue tracker](https://github.com/CCCpan/chinese-sensitive-words/issues) <br>
- [Default API service endpoint](https://www.xdhdancer.top/api8888) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Markdown, Configuration] <br>
**Output Format:** [Terminal text and Markdown-style command output from Bash scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; accepts direct text or a file path for checks and can use SENSITIVE_WORDS_TOKEN and SENSITIVE_WORDS_API_BASE for service configuration.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
