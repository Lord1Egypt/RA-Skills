## Description: <br>
Agent Browser Automation provides headless browser automation guidance for AI agents, including page operations, data extraction, accessibility-tree snapshots, and structured results for authorized workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation teams use this skill to guide an agent through authorized browser navigation, interaction, data extraction, and result capture. It is suited to repeatable web workflows that need structured text, JSON, Markdown, screenshots, or accessibility snapshots rather than high-stakes autonomous decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants broad browser and command authority that could affect accounts, websites, local files, or external services. <br>
Mitigation: Require explicit user approval before logging in, submitting forms, uploading files, or running shell commands; run in a sandbox with least-privilege access. <br>
Risk: The artifact promotes anti-bot bypass behavior, which may conflict with website rules or access controls. <br>
Mitigation: Use the skill only for websites and workflows the user is authorized to automate, avoid access-control or anti-bot bypass, respect site rules, and apply conservative rate limits. <br>
Risk: Browser automation can expose API keys, session tokens, page content, screenshots, or extracted personal data. <br>
Mitigation: Keep secrets in environment variables, redact logs and outputs, avoid storing sensitive captures unnecessarily, and review extracted data before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/agent-browser-automation) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and structured JSON, text, or Markdown result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include browser action results, screenshots, accessibility-tree snapshots, execution logs, and retry/status metadata depending on the agent runtime.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
