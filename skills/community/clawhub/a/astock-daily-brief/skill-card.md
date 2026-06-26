## Description: <br>
A-share Chinese stock market daily briefing that collects index data, sector rankings, capital flows, major announcements, and generates a structured daily report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bustes01](https://clawhub.ai/user/bustes01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to assemble a daily A-share market brief from public financial sources or an optional AShareHub API key. The skill is intended for informational reporting and instructs the agent to mark missing data as unavailable rather than guessing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional AShareHub workflow uses a sensitive API key. <br>
Mitigation: Keep the key in an environment variable, avoid pasting credentials into prompts or reports, and review API commands before execution. <br>
Risk: Market data may be delayed, incomplete, or unsuitable for investment decisions. <br>
Mitigation: Use cited public sources or the configured API, mark missing values as unavailable, and have a human review the brief before acting on it financially. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bustes01/astock-daily-brief) <br>
- [AShareHub](https://asharehub.com/zh/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style daily market brief with structured sections and optional inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a financial disclaimer and instructs the agent to mark unavailable data rather than fabricate values.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
