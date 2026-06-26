## Description: <br>
The organic growth playbook behind 300K+ app downloads. Your AI becomes a growth coach trained on the exact system that drove 500M+ views and $30K+ revenue. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackfriks](https://clawhub.ai/user/jackfriks) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External founders, marketers, and app teams use this skill to plan organic short-form video growth, coach content testing, write captions and posting plans, and operate Post Bridge workflows for publishing approved mobile app marketing content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move from marketing coaching into posting automation and third-party API use. <br>
Mitigation: Require explicit confirmation before any post, schedule, or Post Bridge API action is created. <br>
Risk: The skill may process local media files and move files after posting. <br>
Mitigation: Inspect exact source and destination paths before allowing media processing or file movement. <br>
Risk: The skill may depend on accounts and API keys that can publish externally. <br>
Mitigation: Use only accounts and POST_BRIDGE_API_KEY credentials that are approved for agent-assisted publishing. <br>
Risk: Background or cron scheduling can continue actions after the interactive session. <br>
Mitigation: Avoid enabling cron or background scheduling unless the operator knows how to review and disable it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jackfriks/b2c-marketing) <br>
- [Proven Short-Form Video Formats for B2C App Marketing](references/formats.md) <br>
- [Larry Case Study](references/larry-case-study.md) <br>
- [Post Bridge API Reference](https://api.post-bridge.com/reference) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions, API calls] <br>
**Output Format:** [Markdown guidance with optional shell commands and API request details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require POST_BRIDGE_API_KEY for publishing workflows.] <br>

## Skill Version(s): <br>
2.0.6 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
