## Description: <br>
AI Sting helps developers test AI Agent security by generating scenario-specific prompt-injection attacks, social-engineering probes, logic-bypass prompts, and defensive system-prompt patches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caizhongxian](https://clawhub.ai/user/caizhongxian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security engineers use this skill to assess AI agents they own or are authorized to test by receiving targeted risk analysis, copy-ready red-team prompt examples, and system-prompt hardening guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can generate copy-ready jailbreak, impersonation, and evasion prompts. <br>
Mitigation: Use only against AI agents you own or are explicitly authorized to assess, and treat generated prompts as live attack payloads. <br>
Risk: Weak authorization boundaries could lead users to test third-party or production systems without approval. <br>
Mitigation: Require authorization checks before use and avoid third-party or production targets unless approval is documented. <br>
Risk: Generated examples may be deployable attack text rather than harmless demonstrations. <br>
Mitigation: Prefer safer, non-deployable examples when broad sharing or training use is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caizhongxian/ai-sting) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with risk analysis, quoted test prompts, and defensive system-prompt rules] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces three attack prompt examples across instruction override, social engineering, and logic bypass, plus one or two hardening rules.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
