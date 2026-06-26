## Description: <br>
Helps an agent identify and defend against indirect prompt injection hidden in external content such as webpages, search results, email, social media, user-generated content, and documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[XvarX](https://clawhub.ai/user/XvarX) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to keep external content as information rather than instructions, detect suspicious injection patterns, and require confirmation before sensitive actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause extra pauses before sending messages, running commands, writing files, accessing sensitive files, installing software, or sending data to external services. <br>
Mitigation: Treat those pauses as intentional confirmation gates and review the proposed sensitive action before allowing it. <br>
Risk: Keyword-based prompt-injection detection can flag benign external content that contains instruction-like terms. <br>
Mitigation: Review flagged content in context and proceed only when the requested action still matches the user's explicit intent. <br>


## Reference(s): <br>
- [Attack Patterns Reference](references/attack-patterns.md) <br>
- [ClawHub skill page](https://clawhub.ai/XvarX/claw-prompt-injection-guard) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/XvarX) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Analysis] <br>
**Output Format:** [Markdown guidance and confirmation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only defensive guidance; no files, commands, or API calls are produced by the skill itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
