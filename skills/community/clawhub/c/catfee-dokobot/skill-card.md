## Description: <br>
CatFee Dokobot guides an agent to use the dokobot CLI with a real Chrome session to read JavaScript-rendered web pages, extract dynamic content, and monitor changing data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[glory904649854](https://clawhub.ai/user/glory904649854) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to guide an agent through reading JavaScript-heavy, interactive, or authenticated pages via a local Chrome browser when normal fetching does not capture rendered content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a real Chrome session for logged-in pages, which may expose sensitive account context if the browser profile is too broad. <br>
Mitigation: Use a dedicated browser profile with only the accounts needed for the task, avoid sensitive sites unless explicitly intended, and disable the Dokobot extension or bridge when not in use. <br>


## Reference(s): <br>
- [CatFee Dokobot ClawHub listing](https://clawhub.ai/glory904649854/catfee-dokobot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include browser-session setup steps, timeout values, troubleshooting notes, and extracted page content summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
