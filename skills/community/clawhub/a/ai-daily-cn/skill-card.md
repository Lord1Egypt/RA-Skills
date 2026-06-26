## Description: <br>
AI 日报 - 自动抓取 LLM/Agent 领域热点信息，生成结构化中文简报。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanhe](https://clawhub.ai/user/yanhe) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and AI practitioners use this skill to generate a daily Chinese Markdown briefing about LLM, agent, AI industry, KOL, and arXiv updates from configured online sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Network fetching weakens HTTPS certificate verification. <br>
Mitigation: Restore normal HTTPS certificate verification before production use and review outbound data-source URLs. <br>
Risk: The artifact includes automation paths for cron, systemd, and OpenClaw scheduled jobs. <br>
Mitigation: Review scheduled commands, working directories, logs, and service files before enabling recurring execution. <br>
Risk: The DingTalk push script can send report content to a fixed external group. <br>
Mitigation: Delete the script or replace the destination with an approved channel before using external sharing. <br>
Risk: Optional API keys are read from environment variables, including Tavily, Alibaba Cloud, and GitHub tokens. <br>
Mitigation: Use scoped credentials, avoid unnecessary tokens, and store secrets in a managed secret store or another controlled runtime location. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yanhe/ai-daily-cn) <br>
- [Tavily configuration portal](https://app.tavily.com) <br>
- [Alibaba Cloud DashScope console](https://dashscope.console.aliyun.com) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Configuration] <br>
**Output Format:** [Markdown report files with command-line status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are saved as output/AI-Daily-{date}.md and are controlled by JSON source configuration plus optional API keys.] <br>

## Skill Version(s): <br>
1.2.0 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0 and changelog lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
