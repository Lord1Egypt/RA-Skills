## Description: <br>
Prompt injection and jailbreak detection pack with 16 compiled regex patterns across three severity levels, supporting single-prompt and batch scanning modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to scan user prompts before processing, flagging prompt injection, jailbreak, role reassignment, encoded evasion, and data-exfiltration patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates tool behavior to mcp-openclaw-extensions. <br>
Mitigation: Install mcp-openclaw-extensions from a trusted source and verify the installed version meets the stated requirement. <br>
Risk: The documentation includes jailbreak and prompt-injection phrases as examples. <br>
Mitigation: Treat those phrases as detection examples only and avoid placing them into production prompts except as controlled test cases. <br>
Risk: Regex-based detection may miss novel or obfuscated prompt-injection variants. <br>
Mitigation: Use this skill as one layer in an input safety pipeline and monitor scan results for missed patterns that need policy or detector updates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/romainsantoli-web/firm-prompt-security-pack) <br>
- [Publisher profile](https://clawhub.ai/user/romainsantoli-web) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Guidance] <br>
**Output Format:** [Structured scan findings with integration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports single-prompt and batch scanning modes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
