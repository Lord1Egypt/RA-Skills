## Description: <br>
Gemini Sub-Agent helps developers use Google Gemini as a subscription-backed sub-agent for text analysis, long-context processing, and medium-complexity coding tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tedo0626](https://clawhub.ai/user/tedo0626) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to delegate text analysis, summarization, Q&A, long-context document work, and medium-size coding tasks to Gemini through OpenClaw workflows. It is intended for tasks that do not require OpenClaw-native tools, real-time data, or full local agent context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Auto-approved Gemini coding mode can write files and run shell commands without interactive review. <br>
Mitigation: Avoid auto-approval on important repositories or sensitive systems unless working in a disposable or well-backed-up sandbox. <br>
Risk: The setup installs persistent global tooling and relies on cached Google credentials. <br>
Mitigation: Install only on trusted, single-user machines where global Google and Gemini tooling and cached credentials are acceptable. <br>
Risk: Prompts and piped content may send secrets, regulated data, or proprietary code to Gemini. <br>
Mitigation: Do not pass sensitive or restricted data to Gemini unless organizational policy permits sharing it with Google. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tedo0626/gemini-sub-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke Gemini CLI output and local file changes when used in agentic coding mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
