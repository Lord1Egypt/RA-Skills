## Description: <br>
Anti-Hallucination provides an operational workflow that helps AI agents verify facts, code, file paths, and sources before delivering answers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qianmao1989](https://clawhub.ai/user/qianmao1989) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent operators use this skill to add pre-answer, in-process, and post-output verification routines for tasks involving dates, numbers, citations, code, files, and other accuracy-sensitive outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may prompt agents to browse the web, inspect local paths, run generated code, or handle dependencies with broad authority. <br>
Mitigation: Run it with network access, filesystem checks outside the task, package installation, and code execution gated by user confirmation; use sandboxed execution for code checks. <br>
Risk: Verification workflows can slow responses and still cannot eliminate hallucinations completely. <br>
Mitigation: Use strict mode for high-stakes work, require source labels for critical claims, and keep human review for financial, legal, medical, account, or critical configuration outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qianmao1989/anti-hallucination-v2) <br>
- [Publisher profile](https://clawhub.ai/user/qianmao1989) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional Python scripts and shell-command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes strict, balanced, and fast verification modes plus output-scanning and post-tool validation helpers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
