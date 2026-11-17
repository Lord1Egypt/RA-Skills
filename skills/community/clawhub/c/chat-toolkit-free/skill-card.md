## Description: <br>
Chat Toolkit Free helps an agent learn explicit user communication preferences and reuse them as local Markdown memory for tone, format, and style adaptation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other agent users use this skill to capture explicit communication preferences and apply them consistently in future responses. It is best suited for personal preference management rather than team governance or content creation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests command and write authority that is broader than its stated pure-Markdown purpose. <br>
Mitigation: Install it only for explicit communication-preference tasks, deny unnecessary command execution, and review changes under ~/chat-toolkit. <br>
Risk: Local preference files can contain sensitive personal or workplace communication details. <br>
Mitigation: Avoid storing sensitive information, periodically review the files, and delete outdated or private preferences. <br>
Risk: Unrelated trigger language may cause the skill to activate outside communication-preference management. <br>
Mitigation: Use the skill only for preference capture, review, export, and reset tasks, and ignore design or visual-creation triggers. <br>
Risk: Stored preferences can become outdated or conflict with newer user intent. <br>
Mitigation: Require explicit confirmation before adoption, prefer the latest explicit instruction, and maintain rejected preferences for traceability. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/thcjp/skills/chat-toolkit-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with local file paths and occasional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, read, or update local Markdown preference files under ~/chat-toolkit when the agent follows the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
