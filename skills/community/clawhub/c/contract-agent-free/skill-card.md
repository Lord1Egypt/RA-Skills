## Description: <br>
Contract Agent Free helps agents draft, sign, execute, and track milestone-based contract workflows with identity, signature, escrow-style, and dispute-handling guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate single-organization agent contract workflows, including identity registration, digital signing, milestone tracking, simulated escrow release, and dispute evidence handling. It is not appropriate for medical diagnosis, legal judgments, or real-money escrow reliance without independent review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The free edition describes escrow-like funds management but is not a real escrow or payment system. <br>
Mitigation: Use it only for explicit contract automation tasks, avoid real-money reliance, and require independent review before connecting any real payment workflow. <br>
Risk: The skill handles private signing keys and requests write/exec-capable tools. <br>
Mitigation: Store keys in an encrypted or managed keystore, restrict filesystem access, and review generated commands before execution. <br>
Risk: The workflow references external package installation and command-line setup. <br>
Mitigation: Verify the package source and contents before running npm install or executing contract-agent commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/contract-agent-free) <br>
- [Publisher Profile](https://clawhub.ai/user/thcjp) <br>
- [Skill Homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell, TypeScript, YAML, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include structured JSON result examples, execution logs, setup steps, contract templates, and key-storage guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
